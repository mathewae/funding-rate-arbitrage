import telebot
from telebot.types import ReplyKeyboardMarkup
from funding_rates import plot_funding_rates
import os
import time
import requests

TELEGRAM_BOT_TOKEN = 'your token'

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

def display_menu(chat_id):
    markup = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    markup.add('Funding Rates Comparison')
    bot.send_message(chat_id, "Choose an option:", reply_markup=markup)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Welcome to Insolvent Market Analytics!")
    display_menu(message.chat.id)  # Call display_menu here

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    if message.text == "Funding Rates Comparison":
        bot.reply_to(message, "Please enter the symbol and period in days (e.g., 'PIXEL 2'):")
        bot.register_next_step_handler(message, process_plot_request)
    else:
        bot.reply_to(message, "You selected: " + message.text)

def process_plot_request(message):
    try:
        symbol, period = message.text.split()
        if int(period) == 1:
            bot.reply_to(message, f"Plotting funding rates comparison for {symbol.upper()}USDT for the last 24 hours, it might take a few seconds..." \
                         + "\n" )
        else:
            bot.reply_to(message, f"Plotting funding rates comparison for {symbol.upper()}USDT for the last {period} days, it might take a few seconds..." \
                         + "\n")
        plot_file_path = plot_funding_rates(symbol.upper(), int(period))
        with open(plot_file_path, 'rb') as plot_file:
            bot.send_photo(message.chat.id, plot_file)
        os.remove(plot_file_path)
    except Exception as e:
        bot.reply_to(message, f"Error processing plot request: {e}")

bot.polling()

plot_funding_rates("zeta",30)

# url = f"https://api.hyperliquid.xyz/info"
# headers = {"accept": "application/json"}
# time1 = int(time.time() * 1000) - 1000*60*60*24*(2)
#
# data_funding = {
#     "type": "fundingHistory",
#     "coin": "ZETA",
#     "startTime": time1,
# }
#
# response = requests.post(url, json=data_funding, headers=headers)
# data_funding = (response.json())
# print(response)
