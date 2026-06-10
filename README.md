# Semantic Web & RDF Graph Processing (rdflib)

<div align="center">
  <img src="https://img.shields.io/badge/Language-Python-blue.svg" alt="Python">
  <img src="https://img.shields.io/badge/Library-rdflib-green.svg" alt="rdflib">
  <img src="https://img.shields.io/badge/Library-owlrl-orange.svg" alt="owlrl">
</div>

---

## 1. About This Project & File Structure

### Project Description
This project implements a Semantic Web data pipeline using Python, `rdflib`, and `owlrl` to parse tabular data into a structured knowledge graph. 

The primary objective of this project is to build and analyze an RDF graph by determining the optimal strategy for:
* **Data Transformation:** Converting raw CSV data (`placements.csv`) regarding personnel assignments, projects, and organizations into formalized RDF triples using custom namespaces.
* **Ontology & Reasoning:** Applying RDFS semantics and reasoning (entailment) via `owlrl` using a predefined schema (`schema.ttl`) to infer new relationships and validate data integrity.
* **Data Extraction (SPARQL):** Formulating and executing complex SPARQL queries to extract insights, such as calculating project assignment statistics, filtering by date constraints, and identifying multi-country organizational operations.

This project covers essential Semantic Web and Knowledge Graph concepts, including URI generation, RDF serialization (Turtle format), graph querying, and logic-based entailment testing.

### File Structure & Functionality
Here is a breakdown of the key files involved in this repository:
* **`main.py`**: The core Python script containing the complete pipeline. It handles CSV reading, RDF graph construction, entailment checking, and SPARQL query execution.
* **`placements.csv`** *(Input)*: The raw dataset containing assignment details, person IDs, project codes, and organization locations.
* **`schema.ttl`** *(Input)*: The Turtle file containing the RDFS ontology rules used to infer new knowledge during the entailment phase.
* **`outputs/`** *(Generated)*: A directory created automatically upon execution. It houses:
  * `data.ttl`: The serialized RDF graph in Turtle format.
  * `entailment_report.txt`: The PASS/FAIL results of the automated RDFS entailment tests.
  * `answers.txt`: The formatted results returned by the 4 SPARQL queries.

---

## 2. Set-Up
Before running this project, ensure your local environment has the following dependencies installed:

1. **Python:** Python 3.x installed on your system.
2. **Input Files:** Ensure `placements.csv` and `schema.ttl` are placed in the same root directory as the script.
3. **Python Libraries:** Install the required Semantic Web packages using `pip`:
```bash
pip install rdflib owlrl
```

3. Compilation
Since this project is written in standard Python, traditional compilation (like make or gcc) is not required. Instead, you utilize the Python interpreter to execute the script directly from your terminal.

Open your terminal in the project directory where main.py is located to prepare for execution.

4. Execution
Unlike interactive Jupyter Notebooks, you run this pipeline as a single command-line execution.

Running the Script:
Open your terminal and run the following command:

Bash
python main.py
Expected Results:
Once the script finishes executing, you should see the following outputs:

Console Output: The script will print a single integer to the terminal, representing the total number of triples successfully loaded and inferred within the RDF graph.

Generated Outputs Directory: A new folder named outputs will appear in your project directory containing:

data.ttl: The complete graph data mapped from your CSV.

entailment_report.txt: A text log detailing whether Entailments 1 through 4 resulted in a "PASS" or "FAIL".

answers.txt: A text file documenting the structured results of the 4 SPARQL queries (e.g., ongoing assignment statuses, project counts, and grouped city/country data).
