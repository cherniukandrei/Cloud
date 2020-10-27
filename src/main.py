from geopy.geocoders import Nominatim
# from pathlib import Path
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from datetime import datetime
from geopy.geocoders import Nominatim

# TOKEN_FILE = 'token.txt'
OWNER = '@cherniuk'

token = "732830968:AAFn8TY6hZ1y1tzVp8It1RkCOV3C75rQ-0g" #Path(TOKEN_FILE).read_text().strip()

def date_to_string(which):
	return which.strftime("%d-%b-%Y (%H:%M:%S)")

class TravelInfo:
	
	def __init__(self, loc_start, time_start):
		# geolocator = Nominatim(user_agent="main.py")
		# self.location_start = geolocator.reverse(loc_start.latitude, loc_start.longitude).address
		self.location_start = str(loc_start.latitude) + 'x' + str(loc_start.longitude)
		self.timestamp_start = time_start
		self.location_end    = None
		self.timestamp_end   = None

	def is_finished(self):
		return self.timestamp_end is not None

	def finish(self, loc_end, time_end):
		# self.location_end = geolocator.reverse(loc_end.latitude, loc_end.longitude).address
		self.location_end = str(loc_end.latitude) + 'x' + str(loc_end.longitude)
		self.timestamp_end = time_end

	def elapsed(self):
		return self.timestamp_end - self.timestamp_start
		# self.elapsed = duration.total_seconds()

	def to_string(self):
		return '{0}{1}{2}{3}'.format(
				'Час початку подорожі {}\n'.format(date_to_string(self.timestamp_start)),
				'Час кінця подорожі {}\n'.format(date_to_string(self.timestamp_end)),
				'Локейшн початку подорожі {}\n'.format(self.location_start),
				'Локейшн кінця подорожі {}\n'.format(self.location_end))

#TODO average elapsed

class Handler:

	def __init__(self):
		self.travels = []


	def start(self, bot, update):
		# user = update.message.from_user
		# print('You talk with user {} and his user ID: {} '.format(user['username'], user['id']))

	    """Command handler for command /start"""
	    print('Command /start')
	    bot.message.reply_text('Привіт, я відслідковую, скільки часу ти витрачаєш на шлях між будь-якими двома місцями.')
	    bot.message.reply_text('Просто надішли мені свій локейшн на початку і кінці подорожі.')



	def reset(self, bot, update):
	    """Command handler for command /reset"""
	    print('Command /reset')
	    self.travels.clear()
	    bot.message.reply_text('ОК. Дані про минуле місце положення і історія поїздок видалені.')



	def record_location(self, bot, update):

		if len(self.travels) == 0 or self.travels[-1].is_finished():
			tInfo = TravelInfo(bot.message.location, datetime.now())
			self.travels.append(tInfo)
			bot.message.reply_text("OK. Я записав дані про початок поїздки")
		else:
			self.travels[-1].finish(bot.message.location, datetime.now())
			bot.message.reply_text("OK. Поїздка завершилась")

		bot.message.reply_text(bot.message.location.latitude)
		bot.message.reply_text(bot.message.location.longitude)



	def print_history(self, bot, update):
		if len(self.travels) == 0:
			bot.message.reply_text("Ви не маєте жодних даних про поїздки")
			return
	
		travels_to_print = str()
		i = 1
		for travel in self.travels:
			assert isinstance(travel, TravelInfo), ("[Handler.print_history] Something wrong with travel type."
										           "Surely a programmer's bug!")
			if not travel.is_finished():
				continue


			current_idx = str(i) + '. '
			travels_to_print += current_idx + travel.to_string() + '\n'

			i+=1

		print(travels_to_print)		
		bot.message.reply_text(travels_to_print)



	def revert_last(self, bot, update):
		if len(self.travels) != 0:
			self.travels.pop()
			bot.message.reply_text("Дані про останню поїздку видалені")
		else:
			bot.message.reply_text("Ви не маєте жодних даних про поїздки")





def main():
    updater = Updater(token=token)
    dp = updater.dispatcher
    handler = Handler()

    dp.add_handler(CommandHandler('start',   handler.start))
    dp.add_handler(CommandHandler('reset',   handler.reset))
    dp.add_handler(CommandHandler('history', handler.print_history))
    dp.add_handler(CommandHandler('revert_last',  handler.revert_last))
    
    

    dp.add_handler(MessageHandler(Filters.location, handler.record_location))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()