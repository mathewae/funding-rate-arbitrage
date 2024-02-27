import asyncio
import json
import tkinter as tk
from tkinter import messagebox
import requests
from telebot import types
import telebot
import pandas as pd
from check import futures_balance
from update import get_all_positions, get_all
from telegram import Bot

# Замените 'YOUR_BOT_TOKEN' на токен вашего Telegram бота
TELEGRAM_BOT_TOKEN = '6731812244:AAEBqsIDPuoh-3H2lT0sbaE3WxBj2jrzlZI'

# Замените 'YOUR_CHAT_ID' на ID чата, в который вы хотите отправлять уведомления
TELEGRAM_CHAT_ID = 'https://t.me/positions_tracker_username_bot'

ALLOWED_USERS = ["354065369"]
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)


def is_allowed_user(user_id):
    return str(user_id) in ALLOWED_USERS


@bot.message_handler(commands=['start'])
def send_welcome(message):
    if is_allowed_user(message.from_user.id):
        bot.reply_to(message, "Welcome to Tracker Bot!")
    else:
        bot.reply_to(message, "Sorry, you are not allowed to use this bot.")


@bot.message_handler(commands=['analytics'])
def show_menu(message):
    if is_allowed_user(message.from_user.id):
        # create keyboard with menu options as buttons
        markup = types.ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True)
        account_1 = types.KeyboardButton('wallet1')
        account_2 = types.KeyboardButton('wallet2')
        account_3 = types.KeyboardButton('wallet3')
        account_4 = types.KeyboardButton('wallet4')
        _all = types.KeyboardButton('all')
        binance = types.KeyboardButton('Binance Futures')
        markup.add(account_1, account_2, account_3, account_4, _all, binance)

        # ask user for menu option
        msg = bot.reply_to(message, "Choose option:", reply_markup=markup)
        # bot.register_next_step_handler(msg, process_menu)
    else:
        bot.reply_to(message, "Sorry, you are not allowed to use this bot.")

last_result = None
@ bot.message_handler(func=lambda message: True)

def handle_message(message):
    global last_result
    if is_allowed_user(message.from_user.id):
        if message.text.startswith('0x'):
            selected_account = message.text
            result = get_all_positions(selected_account)

            result_json = result.to_json(orient='records')
            df = pd.read_json(result_json)
            result_csv = df.to_csv(index=False)
            bot.reply_to(message, result_csv)
        if message.text.startswith('Bi'):
            result = futures_balance()
            result_json = result.to_json(orient='records')
            df = pd.read_json(result_json)
            result_csv = df.to_csv(index=False)
            bot.reply_to(message, result_csv)
        elif message.text.startswith('all'):
            all_accounts = ['wallet1', 'wallet2',
                            'wallet3', 'wallet4']
            new_result = get_all(all_accounts)
            new_result_json = new_result.to_json(orient='records')
            if last_result:
                last_df = pd.read_json(last_result.to_json(orient='records'))
                new_df = pd.read_json(new_result_json)
                diff = new_df['cumFunding'] - last_df['cumFunding']
                last_result = new_result

                df = pd.DataFrame({'coin': new_df['coin'], 'difference': diff})
                result_csv = df.to_csv(index=False)
                bot.reply_to(message, result_csv)
            else:
                last_result = new_result
                df = pd.read_json(new_result_json)
                result_csv = df.to_csv(index=False)
                bot.reply_to(message, result_csv)

    else:
        bot.reply_to(message, "Sorry, you are not allowed to use this bot.")


@bot.message_handler(commands=['account'])
def get_all_positions_command(message):
    if is_allowed_user(message.from_user.id) and message.text.startswith('0x'):
        url = f"https://api.hyperliquid.xyz/info"
        headers = {"accept": "application/json"}
        data = {
            "type": "clearinghouseState",
            "user": message,
        }

        response = requests.post(url, json=data, headers=headers)
        data = (response.json())

        bot.reply_to(message, data)


# start bot
bot.polling()