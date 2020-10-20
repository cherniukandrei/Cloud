from pathlib import Path
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

from urllib.request import Request, urlopen
import json

# TOKEN_FILE = 'token.txt'
OWNER = '@cherniuk'
EXCHANGE_RATE_UTL = 'http://resources.finance.ua/ru/public/currency-cash.json'

token = "732830968:AAH4HNcsqOfmBXpddDA7jg4kq46W-ATFe6I" #Path(TOKEN_FILE).read_text().strip()

def start(bot, update):
    """Command handler for command /start"""
    print('Command /start')
    bot.message.reply_text(f'Привет, я персональний бот, мой шеф {OWNER}')
    bot.message.reply_text('Доступные команды: Купить доллары')


def buy_usd(bot, update):
    req = Request(EXCHANGE_RATE_UTL, headers={'User-Agent': 'Mozilla/5.0'})
    text = urlopen(req).read()
    data = json.loads(text)
    sellers = [o for o in data['organizations'] if 'USD' in o['currencies']]
    sellers.sort(key = lambda o: float(o['currencies']['USD']['ask']))
    best_seller = sellers[0]['currencies']['USD']['ask']
    address_of_best_seller = sellers[0]["address"]
    msg.bot.message.reply_text(f'Лучший курс: {best_seller}\nАдрес продажи: {address_of_best_seller}')

def main():

    updater = Updater(token=token)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(MessageHandler(Filters.regex('Купить доллары'), buy_usd))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()