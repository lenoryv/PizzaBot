# PizzaBot
App Pizza Friends Chatbot

Utilizando el servicio de creación de chatbots de Telegram mediante el chatbot BotFather, nos permite crear un bot mediante comandos en este caso /newbot, ingresamos el nombre e identificativo de nuestro bot y nos devolverá el token para poder conectarlo.

La programación del bot se realiza mediante el lenguaje de programación Python y para la interpretación de mensajes se utiliza SpaCy para los procesos de tokenización, lematización y reconocimiento de entidad nombrada (NER), lo que nos permite interpretar los mensajes enviados por los clientes para reconocer la intención dentro de su mensaje.
```python
import spacy

nlp = spacy.load("es_core_news_sm")


def spacy_info(text):
    doc = nlp(text)
    print([(w.text, w.pos_) for w in doc])
    return doc

```
Conexión con la ontologia utilizando Apache Jena Fuseki, un servicio que permite realizar consultas y obtener la información de la ontología.

```python
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

```
Conexión con DBpedia para obtener lista de Pizzas
```python
import requests
from rdflib import Graph
from SPARQLWrapper import SPARQLWrapper, JSON, N3
from pprint import pprint

sparql = SPARQLWrapper('https://dbpedia.org/sparql')
sparql.setQuery('''
    SELECT ?object
    WHERE { dbr:Barack_Obama rdfs:label ?object .}
    # WHERE { dbr:Barack_Obama dbo:abstract ?object .}
''')
sparql.setReturnFormat(JSON)
qres = sparql.query().convert()

# pprint(qres)
for result in qres['results']['bindings']:
    # print(result['object'])

    lang, value = result['object']['xml:lang'], result['object']['value']
    print(f'Lang: {lang}\tValue: {value}')
    # if lang == 'en':
    # print(value)

sparql = SPARQLWrapper("http://dbpedia.org/sparql")
sparql.setQuery('''
CONSTRUCT { dbc:Machine_learning skos:broader ?parent .
            dbc:Machine_learning skos:narrower ?child .} 
WHERE {
    { dbc:Machine_learning skos:broader ?parent . }
UNION
    { ?child skos:broader dbc:Machine_learning . }
}''')

sparql.setReturnFormat(N3)
qres = sparql.query().convert()

g = Graph()
g.parse(data=qres, format='n3')
print(g.serialize(format='ttl').decode('u8'))


sparql = SPARQLWrapper('https://dbpedia.org/sparql')

instruments = ['Nadaswaram', 'Trombone', 'Air_horn', 'Kazoo', 'Mandolin',
               'Clavichord', 'Kaval', 'Electronic_keyboard', 'Choghur', 'Zill']

for instrument in instruments:
    print('###########################################')
    sparql.setQuery(f'''
    SELECT ?name ?comment ?image
    WHERE {{ dbr:{instrument} rdfs:label ?name.
             dbr:{instrument} rdfs:comment ?comment.
             dbr:{instrument} dbo:thumbnail ?image.
    
        FILTER (lang(?name) = 'en')
        FILTER (lang(?comment) = 'en')
    }}''')

    sparql.setReturnFormat(JSON)
    qres = sparql.query().convert()

    result = qres['results']['bindings'][0]
    name, comment, image_url = result['name']['value'], result['comment']['value'], result['image']['value']

    print(name)
    print(image_url)
    response = requests.get(image_url)
    # display(Image.open(BytesIO(response.content)))
    print(f'{comment}...')
```
