# WebNLG⁺⁺

## Overview

**WebNLG⁺⁺** is a harmonized, timely, and internally consistent version of the **WebNLG⁺ test set**.  
It was developed to reflect ontology and entity changes in the latest version of **DBpedia**(September 2025), thereby improving alignment between benchmark data and the current world knowledge embedded in large language models (LLMs).

The dataset contains **1,779 texts** and **5,639 triples**, each carefully reviewed through a **manual validation process supported by an LLM**.  
This combination of automated assistance and human oversight ensures both scalability and accuracy in updating entity URIs and ontology predicates.

To validate the usefulness of the new benchmark, **three LLMs** and **three pretrained transformer-based encoder-only models** were evaluated on the updated dataset.  
Results show that LLMs outperform encoder-only models, even under **zero-shot prompting**, while the LLM scores on the updated dataset are improved compared to the original WebNLG⁺ test set.  
This highlights the importance of keeping benchmarks synchronized with evolving knowledge bases to ensure **fair and realistic model comparisons**.

By improving the alignment between dataset content and current language modeling capabilities, **WebNLG⁺⁺** offers the research community a more **reliable and relevant benchmark** for the evaluation and comparison of LLM-based approaches in knowledge extraction and generation.

---

## Motivation

Over time, DBpedia entities, predicates, and URIs evolve — new ones are added, old ones are renamed, and factual relations may change.
Such changes affect benchmarks like WebNLG⁺, which rely on static knowledge snapshots.

To address this, WebNLG⁺⁺ incorporates updates to ensure:

* Consistency with current DBpedia URIs and ontology.
* Relevance for evaluating modern LLMs.
* Traceability of all changes made to triples.

---

## Types of Changes

We identify three main cases of modifications applied to the original WebNLG⁺ triples:

1. **Predicate Change (Ontology Update):**
   The predicate label changes while meaning remains equivalent.
   Example: `city → locationCity`

2. **URI Change (Same Entity):**
   The subject or object URI changes to a new identifier, but the entity remains the same.
   Example: `Otkrytiye_Arena → Otkritie_Arena`

3. **URI Change (Different Entity):**
   The subject or object URI changes because the underlying fact has changed.
   Example:
   `Agremiação_Sportiva_Arapiraquense | league | Campeonato_Brasileiro_Série_C` →
   `Agremiação_Sportiva_Arapiraquense | league | Campeonato_Brasileiro_Série_D`

---

## Dataset Files

Three JSON files are provided, each corresponding to a different use case (UC):

| File                                     | Description                                                                                           |
| ---------------------------------------- | ----------------------------------------------------------------------------------------------------- |
| `webnlg_plus_mod_ground_truth.json`      | Contains original references and targets from WebNLG⁺ but updated ground-truth triples from WebNLG⁺⁺. |
| `webnlg_plus_mod_pred_ground_truth.json` | Contains original references and targets from WebNLG⁺, with only updated predicates.                  |
| `webnlg_plus_plus_ground_truth.json`     | Contains updated references, targets, and triples — all fully aligned with WebNLG⁺⁺.                  |

---

## Use Cases

### UC1 — Benchmark Relevance for LLMs
Uses **original references and targets** from WebNLG⁺, but updated ground-truth triples according to all three change types (predicate, URI-same, and URI-different).  
By aligning entities and predicates with the latest DBpedia version, benchmark outputs better match modern LLMs’ internal knowledge, reducing outdated references.  
**File:** `webnlg_plus_mod_ground_truth.json`

### UC2 — URIs and Ontology Evolution
Uses **original references and targets**; only predicate (ontology) updates are applied.  
This enables testing model robustness to ontology-level changes while keeping entity mentions constant.  
**File:** `webnlg_plus_mod_pred_ground_truth.json`

### UC3 — Temporal Facts Evaluation
Uses **modified references, targets, and triples** to reflect temporal evolution in DBpedia facts (e.g., team changes leagues).  
Supports evaluation of model adaptability to real-world factual changes over time.  
**File:** `webnlg_plus_plus_ground_truth.json`

---

## JSON File Structure

Each JSON file follows the same structure:

- **`references`**: The original or updated natural-language reference texts.
- **`target`**: The sentence from which the triples are extracted.
- **`output`**: The list of ground-truth triples for the given entry.

~~~json
[
  {
    "row_idx": 0,
    "row": {
      "webnlg_id": "test/SportsTeam/1/Id1",
      "output": [
        "Estádio_Municipal_Coaracy_da_Mata_Fonseca | location | Arapiraca",
        "Agremiação_Sportiva_Arapiraquense | league | Campeonato_Brasileiro_Série_D",
        "Campeonato_Brasileiro_Série_C | country | Brazil",
        "Agremiação_Sportiva_Arapiraquense | nickname | \"''Alvinegro\"",
        "Agremiação_Sportiva_Arapiraquense | ground | Estádio_Municipal_Coaracy_da_Mata_Fonseca"
      ],
      "references": [
        "Estádio Municipal Coaracy da Mata Fonseca is the name of the ground of Agremiação Sportiva Arapiraquense in Arapiraca. Agremiação Sportiva Arapiraquense, nicknamed \"Alvinegro\", lay in the Campeonato Brasileiro Série D league from Brazil.",
        "Estádio Municipal Coaracy da Mata Fonseca is the name of the ground of Agremiação Sportiva Arapiraquense in Arapiraca. Alvinegro, the nickname of Agremiação Sportiva Arapiraquense, play in the Campeonato Brasileiro Série D league from Brazil."
      ],
      "target": "Estádio Municipal Coaracy da Mata Fonseca is the name of the ground of Agremiação Sportiva Arapiraquense in Arapiraca. Agremiação Sportiva Arapiraquense, nicknamed \"Alvinegro\", lay in the Campeonato Brasileiro Série D league from Brazil."
    }
  }
]
~~~

---

## Examples of Changes

### 1. No Changes

```
"initial":  "Estádio_Municipal_Coaracy_da_Mata_Fonseca | location | Arapiraca",
"modified": "Estádio_Municipal_Coaracy_da_Mata_Fonseca | location | Arapiraca"
```

### 2. Predicate Modifications Only (Use Case 2)

```
"initial":  "MotorSport_Vision | city | Fawkham",
"modified": "MotorSport_Vision | locationCity | Fawkham"
```

### 3. URI Modifications (Use Case 1, Use Case 2)

```
"initial":  "FC_Spartak_Moscow | ground | Otkrytiye_Arena",
"modified": "FC_Spartak_Moscow | ground | Otkritie_Arena"
```

### 4. Both URI and Predicate Modifications (Use Case 1, Use Case 3)

```
"initial":  "Adolfo_Suárez_Madrid–Barajas_Airport | operatingOrganisation | ENAIRE",
"modified": "Adolfo_Suárez_Madrid–Barajas_Airport | operator | Aena"
```

### 5. Fact Modifications of Texts (UC3)

```
"initial": "Estádio Municipal Coaracy da Mata Fonseca
is the name of the ground of Agremiação Sportiva Arapiraquense
in Arapiraca. Agremiação Sportiva Arapiraquense, nicknamed
\"Alvinegro\", lay in the Campeonato Brasileiro Série C league
from Brazil."
"modified": "Estádio Municipal Coaracy da Mata Fonseca
is the name of the ground of Agremiação Sportiva Arapiraquense
in Arapiraca. Agremiação Sportiva Arapiraquense, nicknamed
\"Alvinegro\", lay in the Campeonato Brasileiro Série D league
from Brazil."
```

---

## Dataset Statistics

A detailed summary of changes, entity counts, and predicate distributions is provided in  
**`webnlg_plus_plus_statistics.xlsx`**.

For instance, this file includes:
* Number of triples affected by each change type (predicate, URI, or fact).
* Summary statistics for all three ground-truth variants.

---

## Folder Structure

```
webnlg_improved/
│
├── webnlg_plus_mod_ground_truth.json
├── webnlg_plus_mod_pred_ground_truth.json
├── webnlg_plus_plus_ground_truth.json
├── webnlg_plus_plus_statistics.xlsx
└── README.md
```

---

## Potential Applications

* Benchmarking LLM-based triple extraction systems.
* Studying ontology and URI evolution in knowledge graphs.
* Evaluating temporal fact consistency and reasoning in LLMs.

---

## License and Citation

This dataset is distributed under the **CC BY-SA 4.0 License**.

---

## Zenodo

The dataset is also publicly available on Zenodo: https://zenodo.org/records/17695689

---

## Acknowledgments

This dataset builds upon the **WebNLG⁺** benchmark and integrates updates from the **DBpedia** ontology and entity set.

---

## Contact

For questions, comments, or contributions:
**[baniotis@ics.forth.gr](mailto:baniotis@ics.forth.gr)**
