# 🧩 WebNLG⁺⁺ (`webnlg_improved`)

## Overview

**WebNLG⁺ Improved (WebNLG⁺ᴵ)** is a harmonized, timely, and internally consistent version of the **WebNLG⁺ test set**.
It was developed to reflect ontology and entity changes in the latest version of **DBpedia**, thereby improving alignment between benchmark data and the **current world knowledge** embedded in large language models (LLMs).

This dataset enables researchers to evaluate LLMs and triple extraction systems under realistic, temporally aware, and ontology-evolving conditions.

---

## ✳️ Motivation

Over time, DBpedia entities, predicates, and URIs evolve — new ones are added, old ones are renamed, and factual relations may change.
Such changes affect benchmarks like WebNLG⁺, which rely on static knowledge snapshots.

To address this, WebNLG⁺ Improved incorporates updates to ensure:

* **Consistency** with current DBpedia URIs and ontology.
* **Relevance** for evaluating modern LLMs.
* **Traceability** of all changes made to triples.

---

## ⚙️ Types of Changes

We identify **three main cases of modifications** applied to the original WebNLG⁺ triples:

1. **Predicate Change (Ontology Update):**
   The predicate label changes while meaning remains equivalent.
   *Example:* `city → locationCity`

2. **URI Change (Same Entity):**
   The subject or object URI changes to a new identifier, but the entity remains the same.
   *Example:* `Otkrytiye_Arena → Otkritie_Arena`

3. **URI Change (Different Entity):**
   The subject or object URI changes because the underlying fact has changed.
   *Example:*
   `Agremiação_Sportiva_Arapiraquense | league | Campeonato_Brasileiro_Série_C` →
   `Agremiação_Sportiva_Arapiraquense | league | Campeonato_Brasileiro_Série_D`

---

## 📦 Dataset Files

Three JSON files are provided, each corresponding to a different use case (UC):

| File                                         | Description                                                                                           | Change Cases Considered |
| -------------------------------------------- | ----------------------------------------------------------------------------------------------------- | ----------------------- |
| **`webnlg_plus_mod_ground_truth.json`**      | Contains original references and targets from WebNLG⁺ but updated ground-truth triples from WebNLG⁺ᴵ. | (i), (ii), (iii)        |
| **`webnlg_plus_mod_pred_ground_truth.json`** | Contains original references and targets from WebNLG⁺, with only updated predicates.                  | (i)                     |
| **`webnlg_plus_plus_ground_truth.json`**     | Contains updated references, targets, and triples — all fully aligned with WebNLG⁺ᴵ.                  | (i), (ii), (iii)        |

---

## 🧠 Use Cases

### **UC1 — Benchmark Relevance for LLMs**

By aligning entities and predicates with the latest DBpedia version, benchmark outputs better match modern LLMs’ internal knowledge, reducing outdated references.

**File:** `webnlg_plus_mod_ground_truth.json`

---

### **UC2 — URIs and Ontology Evolution**

Enables studying model robustness to unseen predicates and ontology shifts caused by DBpedia updates.

**File:** `webnlg_plus_mod_pred_ground_truth.json`

---

### **UC3 — Temporal Facts Evaluation**

Supports analysis of how models handle factual updates over time, helping evaluate temporal reasoning capabilities.

**File:** `webnlg_plus_plus_ground_truth.json`

---

## 🔍 Examples of Changes

### 1. No Changes

```
"initial":  "Estádio_Municipal_Coaracy_da_Mata_Fonseca | location | Arapiraca",
"modified": "Estádio_Municipal_Coaracy_da_Mata_Fonseca | location | Arapiraca"
```

### 2. Predicate Modification

```
"initial":  "MotorSport_Vision | city | Fawkham",
"modified": "MotorSport_Vision | locationCity | Fawkham"
```

### 3. URI Modification (Same Entity)

```
"initial":  "FC_Spartak_Moscow | ground | Otkrytiye_Arena",
"modified": "FC_Spartak_Moscow | ground | Otkritie_Arena"
```

### 4. URI & Predicate Modification

```
"initial":  "Adolfo_Suárez_Madrid–Barajas_Airport | operatingOrganisation | ENAIRE",
"modified": "Adolfo_Suárez_Madrid–Barajas_Airport | operator | Aena"
```

### 5. Fact Modification (Changed Entity)

```
"initial":  "Agremiação_Sportiva_Arapiraquense | league | Campeonato_Brasileiro_Série_C",
"modified": "Agremiação_Sportiva_Arapiraquense | league | Campeonato_Brasileiro_Série_D"
```

---

## 📁 Structure

```
webnlg_improved/
│
├── webnlg_plus_mod_ground_truth.json
├── webnlg_plus_mod_pred_ground_truth.json
├── webnlg_plus_plus_ground_truth.json
├── examples/
│   ├── predicates_changes.json
│   ├── uri_changes.json
│   └── fact_changes.json
└── README.md
```

---

## 📈 Potential Applications

* **Benchmarking** LLM-based triple extraction systems.
* **Studying** ontology and URI evolution in knowledge graphs.
* **Evaluating** temporal fact consistency and reasoning in LLMs.

---

## ⚖️ License & Citation

This dataset is distributed under the **CC BY-SA 4.0 License**.
When using it, please cite:

```bibtex
@dataset{webnlg_improved_2025,
  title     = {WebNLG⁺ Improved: A Timely, Consistent Benchmark for LLM and Knowledge Graph Evaluation},
  author    = {Your Name and Co-Authors},
  year      = {2025},
  publisher = {DBpedia / WebNLG Community},
  url       = {https://github.com/yourrepo/webnlg_improved}
}
```

---

## 🧩 Acknowledgments

This dataset builds upon the **WebNLG⁺** benchmark and integrates updates from the **DBpedia** ontology and entity set.
We thank the WebNLG organizers and DBpedia maintainers for their foundational contributions.

---

## 📬 Contact

For questions, comments, or contributions:
📧 **[your.email@example.com](mailto:your.email@example.com)**
