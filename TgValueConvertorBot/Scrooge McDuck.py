from telebot import TeleBot
from ValueConverter import *

bot = TeleBot(token)

@bot.message_handler(commands=["start", "help"])
def instruction(message):
    text = ("Доброго времени суток\nЯ могу конвертировать сумму из одной валюты в другую"
            "\nДля этого передайте команду в следующем формате:"
            "\n<валюта, которую переводим> <валюту, в которую переводить> <цена переводимой валюты>\n"
            "Например: перевод 100 рублей в доллары выглядить будет так: рубль доллар 100\n"
            "Список доступных валют можно вывести командой /values")
    bot.reply_to(message, text=text)

@bot.message_handler(commands=["values"])
def get_values(message):
    text = "Доступные валюты:"
    for i in allow_values:
        text = "\n".join((text, i))
    bot.reply_to(message, text=text)

@bot.message_handler(content_types=["text"])
def convertation(message):
    try:
        if len(message.text.split(" ")) > 3:
            raise APIException("неверный ввод данных, передано больше 3 аргументов")
        elif len(message.text.split(" ")) < 3:
            raise APIException(f"неверный ввод данных, передано {len(message.text.split(" "))} вместо 3")

        base, quote, amount = message.text.lower().split(" ")
        amount = float(amount)

        if base not in allow_values:
            raise APIException(f"неудалось обработать валюту: {base}")
        elif quote not in allow_values:
            raise APIException(f"неудалось обработать валюту: {quote}")

        if base == quote:
            raise APIException("нельзя конвертировать одиннаковые валюты")

    except APIException as e:
        bot.send_message(message.chat.id, f"Пользовательская ошибка: {e}\nЕсли нужна помощь воспользуйтесь командой /help")

    except ValueError:
        bot.send_message(message.chat.id, f"Пользовательская ошибка: неудалось обработать число {amount}")

    except:
        bot.send_message(message.chat.id, f"Серверная ошибка: неудалось обработать команду")

    converter = ConvertValue()

    text = f"{base} {amount} в {quote} будет {converter.get_price(base, quote, amount)}"
    bot.send_message(message.chat.id, text)

bot.infinity_polling()