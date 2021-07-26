from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import connection_OWL as geo


def main_menu_keyboard():
    keyboard = [[InlineKeyboardButton(
                    'Recomendar Pizza', callback_data='m1')],
                [InlineKeyboardButton('Crear una pizza', callback_data='m2')]]
    return InlineKeyboardMarkup(keyboard)


def first_menu_keyboard():
    keyboard = [[InlineKeyboardButton('Menú Principal', callback_data='main')]]

    qres = geo.get_response_pizzas()

    for i in range(len(qres['results']['bindings'])):
        result = qres['results']['bindings'][i]
        name = result['name']['value']
        keyboard.insert(0, [InlineKeyboardButton(
            name, callback_data='m3')])

    return InlineKeyboardMarkup(keyboard)


def first_submenu_keyboard():
    keyboard = [[InlineKeyboardButton('Si, Realizar pago mediante PayPal',
                                      url='https://paypal.me/leor0104?locale.x=es_XC')],
                [InlineKeyboardButton('No, Volver a menú principal', callback_data='main')]]
    return InlineKeyboardMarkup(keyboard)


def second_menu_keyboard():
    keyboard = [[InlineKeyboardButton('Pizza Pequeña', callback_data='m4')],
                [InlineKeyboardButton('Pizza Mediana', callback_data='m4')],
                [InlineKeyboardButton('Pizza Grande', callback_data='m4')],
                [InlineKeyboardButton('Menu Principal', callback_data='main')]]
    return InlineKeyboardMarkup(keyboard)


def second_submenu_keyboard():
    keyboard = [[InlineKeyboardButton('Listo, muy bien', callback_data='m5')],
                [InlineKeyboardButton('Menú Principal', callback_data='main')]]
    return InlineKeyboardMarkup(keyboard)
