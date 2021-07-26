from SPARQLWrapper import SPARQLWrapper, JSON

sparql = SPARQLWrapper(
    'http://localhost:3030/App/sparql')


def get_response_pizzas():
    sparql.setQuery('''
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX pzf: <http://www.pizzafriends.com/ontologies/pizza.owl#>
        SELECT DISTINCT ?name 
        WHERE { 
            ?s rdfs:subClassOf pzf:NamedPizza .
            ?s rdfs:label ?name
            FILTER (lang(?name) = 'es')
        }
    ''')
    sparql.setReturnFormat(JSON)
    qres = sparql.query().convert()
    return qres
