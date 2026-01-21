import json
import requests
import re
import time

def clean_string(s):
    """Removes extra quotes and whitespace from a string."""
    s = s.strip()
    if s.startswith('"') and s.endswith('"'):
        s = s[1:-1]
    s = re.sub(r"^''|''$", '', s)
    return s.replace('_', ' ')

def format_resource(s):
    """Formats a string as a DBpedia resource URI."""
    return f"<http://dbpedia.org/resource/{s.replace(' ', '_')}>"

def format_literal(s):
    """Formats a string as a string literal with an English language tag."""
    return f'"{s.replace("\"", "\\\"")}"@en'

def format_plain_literal(s):
    """Formats a string as a plain, simple literal without a language tag."""
    return f'"{s.replace("\"", "\\\"")}"'

def format_xsd_string_literal(s):
    """Formats a string as a literal explicitly typed as xsd:string."""
    return f'"{s.replace("\"", "\\\"")}"^^<http://www.w3.org/2001/XMLSchema#string>'


def check_triple_exists(subject, predicate, obj):
    """
    Checks if a triple exists by first checking for special data types and then
    performing sequential checks for ambiguous types like 4-digit numbers and other formats.
    """
    sparql_endpoint = "https://dbpedia.org/sparql"
    
    s_formatted = format_resource(clean_string(subject))
    p_cleaned = clean_string(predicate)
    obj_cleaned = clean_string(obj)

    def run_ask_query(object_formatted):
        """A helper function to run a single SPARQL ASK query."""
        query = f"""
        PREFIX dbo: <http://dbpedia.org/ontology/>
        PREFIX dbp: <http://dbpedia.org/property/>

        ASK WHERE {{
          {{ {s_formatted} dbo:{p_cleaned} {object_formatted} . }}
          UNION
          {{ {s_formatted} dbp:{p_cleaned} {object_formatted} . }}
        }}
        """
        headers = {"Accept": "application/sparql-results+json"}
        params = {"query": query, "format": "json"}
        try:
            response = requests.get(sparql_endpoint, params=params, headers=headers, timeout=30)
            response.raise_for_status()
            return response.json().get('boolean', False), query
        except Exception as e:
            print(f"A query failed for query {query}: {e}")
            return False, query

    # --- Step 1: Check for unambiguous special data types first ---
    
    if re.fullmatch(r'\d{4}-\d{2}-\d{2}', obj_cleaned):
        o_as_date = f'"{obj_cleaned}"^^<http://www.w3.org/2001/XMLSchema#date>'
        return run_ask_query(o_as_date)

    height_match = re.match(r'(\d+\.?\d*)\s*\(centimetres\)', obj_cleaned)
    if height_match:
        cm = float(height_match.group(1))
        meters = cm / 100.0
        o_as_double = f'"{meters}"^^<http://www.w3.org/2001/XMLSchema#double>'
        return run_ask_query(o_as_double)

    # --- Step 2: Handle ambiguous 4-digit numbers (gYear or integer) ---
    if re.fullmatch(r'\d{4}', obj_cleaned):
        # First, try as gYear
        o_as_gYear = f'"{obj_cleaned}"^^<http://www.w3.org/2001/XMLSchema#gYear>'
        exists, query = run_ask_query(o_as_gYear)
        if exists:
            return True, query
        
        # If not found as gYear, try as Integer. Return this result.
        o_as_integer = f'"{int(obj_cleaned)}"^^<http://www.w3.org/2001/XMLSchema#integer>'
        return run_ask_query(o_as_integer)

    # --- Step 3: Check for any other kind of number ---
    try:
        if len(obj_cleaned) > 1 and obj_cleaned.startswith('0') and obj_cleaned.isdigit():
            raise ValueError("Leading zero indicates a string, not a number.")

        if '.' in obj_cleaned:
            num = float(obj_cleaned)
            o_as_double = f'"{num}"^^<http://www.w3.org/2001/XMLSchema#double>'
            return run_ask_query(o_as_double)
        else:
            num = int(obj_cleaned)
            o_as_integer = f'"{num}"^^<http://www.w3.org/2001/XMLSchema#integer>'
            return run_ask_query(o_as_integer)
    except ValueError:
        pass

    # --- Step 4: If not a special type, perform the sequential check for other formats ---

    o_as_resource = format_resource(obj_cleaned)
    exists, query = run_ask_query(o_as_resource)
    if exists: return True, query

    o_as_literal_en = format_literal(obj_cleaned)
    exists, query = run_ask_query(o_as_literal_en)
    if exists: return True, query
    
    o_as_plain_literal = format_plain_literal(obj_cleaned)
    exists, query = run_ask_query(o_as_plain_literal)
    if exists: return True, query

    o_as_xsd_string = format_xsd_string_literal(obj_cleaned)
    exists, query = run_ask_query(o_as_xsd_string)
    
    return exists, query


def main():
    """Main function to read triples, verify them, and save the results."""
    input_filename = 'YOUR_INPUT_FILE_NAME.json'
    output_filename = 'YOUR_OUTPUT_FILE_NAME.json'

    try:
        with open(input_filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Error: '{input_filename}' not found.")
        return
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from '{input_filename}'.")
        return

    results = []
    total_triples = sum(len(item.get("output", [])) for item in data)
    processed_count = 0

    for item in data:
        webnlg_id = item.get("title")
        input_triples = item.get("output", [])

        for triple_str in input_triples:
            processed_count += 1
            
            if not isinstance(triple_str, str):
                print(f"Skipping invalid data for id {webnlg_id}: Item is not a string.")
                continue

            parts = triple_str.split(' | ')
            if len(parts) != 3:
                print(f"Skipping malformed triple for id {webnlg_id}: {triple_str}")
                continue

            subject, predicate, obj = parts
            time.sleep(0.2) # throttle requests to avoid DBpedia SPARQL rate limits

            exists, final_query = check_triple_exists(subject, predicate, obj)

            result_item = {
                "webnlg_id": webnlg_id,
                "triple": [subject, predicate, obj],
                "generated_query": final_query,
                "exists_in_dbpedia": exists
            }
            results.append(result_item)
            
            status = 'exists' if exists else 'does not exist'
            print(f"Processed {processed_count}/{total_triples}: Triple for '{webnlg_id}' {status}.")

    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    existing_count = sum(1 for r in results if r['exists_in_dbpedia'])
    print("\n--- Verification Summary ---")
    print(f"Total triples processed: {processed_count}")
    print(f"Triples found in DBpedia: {existing_count}")
    print(f"Triples not found: {processed_count - existing_count}")
    print(f"Results saved to '{output_filename}'")


if __name__ == "__main__":
    main()