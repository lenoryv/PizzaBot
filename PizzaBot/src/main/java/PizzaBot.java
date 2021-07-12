import org.telegram.telegrambots.bots.TelegramLongPollingBot;
import org.telegram.telegrambots.meta.api.methods.ParseMode;
import org.telegram.telegrambots.meta.api.objects.CallbackQuery;
import org.telegram.telegrambots.meta.api.objects.Message;
import org.telegram.telegrambots.meta.api.objects.Update;
import org.telegram.telegrambots.meta.api.methods.send.SendMessage;
import org.telegram.telegrambots.meta.api.objects.replykeyboard.InlineKeyboardMarkup;
import org.telegram.telegrambots.meta.api.objects.replykeyboard.buttons.InlineKeyboardButton;
import org.telegram.telegrambots.meta.exceptions.TelegramApiException;

import java.util.ArrayList;
import java.util.List;

public class PizzaBot extends TelegramLongPollingBot {

    @Override
    public String getBotUsername() {
        return "PizzaFriendsBot";
    }

    @Override
    public String getBotToken() {
        return "1791730721:AAHf0vrvnJiVekfueLP2XvAEHRv3EJKZcAQ";
    }

    @Override
    public void onUpdateReceived(Update update) {
        // We check if the update has a message and the message has text
        if (update.hasMessage()) {
            Message msg = update.getMessage();
            if (msg.hasText()) {
                String command = msg.getText();
                if (command.equals("/start")) {
                    // Create a SendMessage object with mandatory fields
                    SendMessage message = new SendMessage();
                    message.setChatId(msg.getChatId().toString());
                    message.setText("Bienvenido, " + msg.getFrom().getFirstName() + " ¿En qué puedo ayudarte? :)");

                    // InlineKeyboardButton

                    InlineKeyboardMarkup inlineKeyboardMarkup = new InlineKeyboardMarkup();
                    List<List<InlineKeyboardButton>> inlineButtons = new ArrayList<>();
                    List<InlineKeyboardButton> inlineKeyboardButtonList = new ArrayList<>();
                    InlineKeyboardButton inlineKeyboardButton1 = new InlineKeyboardButton();
                    InlineKeyboardButton inlineKeyboardButton2 = new InlineKeyboardButton();
                    inlineKeyboardButton1.setText("Ordenar Pizza");
                    inlineKeyboardButton2.setText("Salir");
                    inlineKeyboardButton1.setCallbackData("ordenar");
                    inlineKeyboardButton2.setCallbackData("salir");
                    inlineKeyboardButtonList.add(inlineKeyboardButton1);
                    inlineKeyboardButtonList.add(inlineKeyboardButton2);
                    inlineButtons.add(inlineKeyboardButtonList);
                    inlineKeyboardMarkup.setKeyboard(inlineButtons);
                    message.setReplyMarkup(inlineKeyboardMarkup);

                    try {
                        execute(message); // Call method to send the message
                    } catch (TelegramApiException e) {
                        e.printStackTrace();
                    }
                }
            }
        } else if (update.hasCallbackQuery()) {
            Message msg = update.getMessage();
            SendMessage message = new SendMessage();
            message.setParseMode(ParseMode.MARKDOWN);
            message.setChatId(msg.getChatId().toString());
            CallbackQuery callbackQuery = update.getCallbackQuery();
            String data = callbackQuery.getData();

            if (data.equals("ordenar")) {
                message.setText("¿Dónde empezamos?");
            } else if (data.equals("salir")) {
                message.setChatId(update.getMessage().getChatId().toString());
                message.setText("Hasta pronto");
            }
        }
    }
}