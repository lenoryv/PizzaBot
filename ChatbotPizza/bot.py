from os import name
from telegram.ext import *
import logging
import connection_dbpedia as dbpedia
import connection_OWL as geo
import spacyNLP as analysis
import constants as keys
import menu
import responses

# Set up the logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logging.info('Starting Bot...')

# Message error


def error(update, context):
    logging.error(f'Update {update} caused error {context.error}')

# MENUS


def menu_command(update, context):
    update.message.reply_text("Bienvenido a PizzaFriends ¿En qué puedo ayudarte?",
                              reply_markup=menu.main_menu_keyboard())


def main_menu(update, context):
    query = update.callback_query
    query.edit_message_text(text="Hola, soy Leor ¿Deseas ordenar una pizza?",
                            reply_markup=menu.main_menu_keyboard())


def first_menu(update, context):
    query = update.callback_query
    query.edit_message_text(
        text="¿Qué tipo de pizza deseas?",
        reply_markup=menu.first_menu_keyboard())


def first_submenu(update, context):
    query = update.callback_query
    query.edit_message_text(
        text="¿Está seguro que desea ordenar esta pizza?",
        reply_markup=menu.first_submenu_keyboard())


def second_menu(update, context):
    query = update.callback_query
    query.edit_message_text(
        text="Para crear una pizza primero indícame cuantas cubiertas tendrá tu pizza",
        reply_markup=menu.second_menu_keyboard())


def second_submenu(update, context):
    query = update.callback_query
    query.edit_message_text(
        text="Aún estamos trabajando en esta función, cuando este recién orneada te cuento ¿vale?",
        reply_markup=menu.second_submenu_keyboard())


def second_submenu_1(update, context):
    query = update.callback_query
    query.edit_message_text(
        text="Listo te avisare cuando esté listo")

# COMMANDS


def help_command(update, context):
    update.message.reply_text(
        "PizzaFriends permite realizar pedidos, revisar y crear pizzas según los gustos de un grupo de amigos"
        "\n\nPara interartuar con nuestro Bot utliza el comando /start"
        "\n\nNota: Nuestro Bot está aprendiendo así que puedes ayudarlo con una buena redación de tus mensajes")


def ingredients_command(update, context):
    user_says = " ".join(context.args)
    # update.message.reply_text("You said: " + user_says)
    update.message.reply_text(
        "Los ingredientes de  " + user_says + " son:\n\n"+dbpedia.get_response_dbpedia_ingredients(user_says.capitalize()))


def pizza_command(update, context):
    update.message.reply_text(
        "Puedes encontrar información de las siguientes pizzas :"
        "\n\nPizza_al_taglio"
        "\nDetroit-style_pizza"
        "\nNeapolitan_pizza"
        "\nDeep-fried_pizza"
        "\nDeep-fried_pizza"
        "\nItalian_tomato_pie"
        "\nSicilian_pizza"
        "\nChicago-style_pizza"
    )


def start_command(update, context):
    update.message.reply_text(
        'Hola, mi nombre es Leor\n\nPuedo ayudarte a crear y ordenar tu pizza.')
    update.message.reply_text(
        "A continuación algunos de los comandos con los que podemos empezar:\n"
        "\n/menu -> ordenar una pizza mediante una lista de recomendación"
        "\n/pizza -> mostrar el nombre "
        "\n/listPizzaDb -> mostrar lista de pizzas desde DBpedia"
        "\n/listPizza -> mostrar lista de pizzas desde PizzaFriends"
        "\n/ingredients \"nombre de la pizza\" -> buscar los ingredientes de una pizza. Utiliza el commando /pizza para ver la lista de pizzas y la forma correcta de escribir el nombre para la búsqueda)")


def types_command_dbpedia(update, context):
    qres = dbpedia.get_response_dbpedia_pizzas()
    for i in range(len(qres['results']['bindings'])):
        result = qres['results']['bindings'][i]
        name, comment, image_url = result['name']['value'], result['comment']['value'], result['image']['value']
        update.message.reply_text('Nombre de la pizza (DBpedia) : ' + name +
                                  "\n\nDescripción : " + comment + "\n" + image_url)


def types_command_bot(update, context):
    qres = geo.get_response_pizzas()
    for i in range(len(qres['results']['bindings'])):
        result = qres['results']['bindings'][i]
        name = result['name']['value']
        update.message.reply_text('Nombre de la pizza (PizzaFriends): ' + name)


def handle_message(update, context):
    text = str(update.message.text).lower()
    logging.info(f'User ({update.message.chat.id}) says: {text}')

    listNoun = []
    listVerb = []

    doc = analysis.spacy_info(text)
    for w in doc:
        update.message.reply_text(
            w.text + " es un " + w.pos_ + " lemma: " + w.lemma_)
        if w.pos_ == "NOUN":
            print("NOUN " + w.text)
            listNoun.append(w.text)
        if w.pos_ == "VERB":
            print("VERB " + w.text)
            listVerb.insert(0, w.lemma_)

    response = responses.get_response(listVerb[0])
    if (response):
        update.message.reply_text(
            "Tu intención es pedir:")
        for list in listNoun:
            if list == "pizza":
                update.message.reply_text(
                    " Una -  \""+list+"\" :\n"+dbpedia.get_response_dbpedia(list.capitalize()))
            else:
                temp = "Lista de Pizzas que contienen el ingrediente - " + list + " :\n"
                qres = dbpedia.get_response_dbpedia_food(list)
                for i in range(len(qres['results']['bindings'])):
                    result = qres['results']['bindings'][i]
                    label = result['label']['value']
                    temp += "\n - " + label

                update.message.reply_text(temp)

    else:
        text = "Perdón, pero no puedo entender tu mensaje\n\nUsaste las siguientes intenciones :\n"
        for w in listVerb:
            temp = " - " + w + "\n"
            text += temp
        text += "\n(Utiliza una sola acción para entender tu mensaje)"
        update.message.reply_text(text)


if __name__ == '__main__':
    updater = Updater(token=keys.API_KEY, use_context=True)

    dp = updater.dispatcher

    # Commands
    dp.add_handler(CommandHandler('start', start_command))
    dp.add_handler(CommandHandler('menu', menu_command))
    dp.add_handler(CommandHandler('listPizzaDb', types_command_dbpedia))
    dp.add_handler(CommandHandler('listPizza', types_command_bot))
    dp.add_handler(CommandHandler('pizza', pizza_command))
    dp.add_handler(CommandHandler(
        'ingredients', ingredients_command, pass_args=True))

    dp.add_handler(CallbackQueryHandler(main_menu, pattern='main'))
    dp.add_handler(CallbackQueryHandler(first_menu, pattern='m1'))
    dp.add_handler(CallbackQueryHandler(second_menu, pattern='m2'))
    dp.add_handler(CallbackQueryHandler(first_submenu, pattern='m3'))
    dp.add_handler(CallbackQueryHandler(second_submenu, pattern='m4'))
    dp.add_handler(CallbackQueryHandler(second_submenu_1, pattern='m5'))

    # Messages
    dp.add_handler(MessageHandler(Filters.text, handle_message))

    # Log all errors
    dp.add_error_handler(error)

    # Run the bot
    updater.start_polling(1.0)
    updater.idle()
