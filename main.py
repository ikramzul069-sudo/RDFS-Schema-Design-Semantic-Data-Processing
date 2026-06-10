import csv
import os
from rdflib import Dataset, Namespace, Literal, URIRef, XSD, RDF, Graph
import owlrl

ex = Namespace("http://example.org/comp318/onto#")
res = Namespace("http://example.org/comp318/res/")
graph_iri = URIRef("http://example.org/comp318/graph/data")

def clean_date(date_str):
    if not date_str or "/" not in date_str:
        return None
    parts = date_str.split('/')
    return f"{parts[2]}-{parts[1]}-{parts[0]}" if len(parts) == 3 else None

def run_assignment():
    ds = Dataset()
    g = ds.graph(graph_iri)
    
    if not os.path.exists('outputs'):
        os.makedirs('outputs')

    with open('placements.csv', mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter=';')
        for row in reader:
            assignment_uri = res[f"assignment/{row['AssignmentID']}"]
            person_uri = res[f"person/{row['PersonID']}"]
            project_uri = res[f"project/{row['Project Code']}"]
            organisation_uri = res[f"org/{row['Org Identifier']}"]

            g.add((assignment_uri, RDF.type, ex.Placement))
            g.add((assignment_uri, ex.hasAssignee, person_uri))
            g.add((assignment_uri, ex.atOrganisation, organisation_uri))
            g.add((assignment_uri, ex.onProject, project_uri))
            
            g.add((project_uri, ex.projectCode, Literal(row['Project Code'], datatype=XSD.string)))
            g.add((organisation_uri, ex.orgCityLabel, Literal(row['Org City'], datatype=XSD.string)))
            g.add((organisation_uri, ex.orgCountryLabel, Literal(row['Org Country'], datatype=XSD.string)))
            g.add((assignment_uri, ex.workMode, Literal(row['Work Mode'], datatype=XSD.string)))
            
            start_date_val = clean_date(row['Start Date'])
            if start_date_val:
                g.add((assignment_uri, ex.startDate, Literal(start_date_val, datatype=XSD.date)))
            
            end_date_val = clean_date(row['End Date'])
            if end_date_val:
                g.add((assignment_uri, ex.endDate, Literal(end_date_val, datatype=XSD.date)))

    g.serialize(destination="outputs/data.ttl", format="turtle")

    g.parse("schema.ttl", format="turtle")
    engine = owlrl.RDFSClosure.RDFS_Semantics(g, False, False, False)
    engine.closure()

    results_entailment = {}
    
    e1_passed = False
    for assignment_res, person_res in g.subject_objects(ex.hasAssignee):
        if (assignment_res, RDF.type, ex.Assignment) in g:
            e1_passed = True
            break
    results_entailment[1] = "PASS" if e1_passed else "FAIL"

    e2_passed = False
    for assignment_res, person_res in g.subject_objects(ex.hasAssignee):
        if (person_res, RDF.type, ex.Person) in g:
            e2_passed = True
            break
    results_entailment[2] = "PASS" if e2_passed else "FAIL"

    e3_passed = False
    for assignment_res, project_res in g.subject_objects(ex.onProject):
        if (project_res, RDF.type, ex.Project) in g:
            e3_passed = True
            break
    results_entailment[3] = "PASS" if e3_passed else "FAIL"

    e4_passed = False
    for placement_res in g.subjects(RDF.type, ex.Placement):
        if (placement_res, RDF.type, ex.Assignment) in g:
            e4_passed = True
            break
    results_entailment[4] = "PASS" if e4_passed else "FAIL"

    with open("outputs/entailment_report.txt", "w") as f:
        for i in range(1, 5):
            f.write(f"ENTAILMENT {i}: {results_entailment[i]}\n")

    print(len(ds.graph(graph_iri)))

    query_1 = """PREFIX ex: <http://example.org/comp318/onto#>
    SELECT ?assignmentId ?personId ?projectCode WHERE {
        GRAPH <http://example.org/comp318/graph/data> {
            ?assignment a ex:Assignment ;
                        ex:hasAssignee ?person ;
                        ex:onProject ?project .
            ?project ex:projectCode ?projectCode .
            FILTER NOT EXISTS { ?assignment ex:endDate ?endDate }
            BIND(REPLACE(STR(?assignment), "^.*assignment/", "") AS ?assignmentId)
            BIND(REPLACE(STR(?person), "^.*person/", "") AS ?personId)
        }
    }"""

    query_2 = """PREFIX ex: <http://example.org/comp318/onto#>
    SELECT ?projectCode (COUNT(?assignment) AS ?nAssignments) (COUNT(DISTINCT ?person) AS ?nPeople) WHERE {
        GRAPH <http://example.org/comp318/graph/data> {
            ?assignment a ex:Assignment ;
                        ex:onProject ?project ;
                        ex:hasAssignee ?person .
            ?project ex:projectCode ?projectCode .
        }
    } GROUP BY ?projectCode"""

    query_3 = """PREFIX ex: <http://example.org/comp318/onto#>
    SELECT ?city (COUNT(DISTINCT ?country) AS ?nCountries) (GROUP_CONCAT(DISTINCT ?country; separator=", ") AS ?countries) WHERE {
        GRAPH <http://example.org/comp318/graph/data> {
            ?organisation ex:orgCityLabel ?city ;
                          ex:orgCountryLabel ?country .
        }
    } GROUP BY ?city HAVING (COUNT(DISTINCT ?country) > 1)"""

    query_4 = """PREFIX ex: <http://example.org/comp318/onto#>
    SELECT ?assignmentId ?status WHERE {
        GRAPH <http://example.org/comp318/graph/data> {
            { 
                ?assignment ex:endDate ?anyDate . 
                BIND("finished" AS ?status) 
            }
            UNION
            { 
                ?assignment a ex:Assignment . 
                FILTER NOT EXISTS { ?assignment ex:endDate ?anyDate } 
                BIND("ongoing" AS ?status) 
            }
            BIND(REPLACE(STR(?assignment), "^.*assignment/", "") AS ?assignmentId)
        }
    }"""

    with open("outputs/answers.txt", "w") as f:
        for i, query_string in enumerate([query_1, query_2, query_3, query_4], 1):
            f.write(f"Q{i}:\n")
            query_results = ds.query(query_string)
            for row in query_results:
                values = list(row)
                if i == 3:
                    sorted_countries = sorted([c.strip() for c in str(values[2]).split(',')])
                    values[2] = ", ".join(sorted_countries)
                f.write("\t".join(str(v) for v in values).strip() + "\n")

if __name__ == "__main__":
    run_assignment()