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
