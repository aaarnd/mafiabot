
import telebot
from telebot.types import Message, CallbackQuery


from keyboard import * 
from text import * 

from schedule import every, repeat
import logging 
import sqlite3
import json


from config_reader import config

logging.basicConfig(level=logging.INFO)

bot = telebot.TeleBot(token=config.bot_token.get_secret_value())






id_chats = []

# mockup
game = {'date' : 'ff',
        'time' : 'ff',
        'location' : 'ff',
        'price' : 'ff'}



admins = [339806382]


# старт
@bot.message_handler(commands=['start', 'menu'])
def cmd_start(message: Message):
    if message.chat.type == 'private':
        bot.send_message(message.chat.id, text=start_text, reply_markup= start_markup)
    else:
        bot.send_message(message.chat.id, text=wrongchat_text)

@bot.callback_query_handler(func=lambda call:True)
def callback_query(call: CallbackQuery):
    req = call.data.split('_')
    if req[0] == 'rules':
        get_rules_callback(call)
    elif req[0] == 'players':
        db_get_players_list_callback(call)
    elif req[0] == 'join':
        db_join_game_callback(call)
    elif req[0] == 'unjoin':
        db_unjoin_game_callback(call)
    elif req[0] == 'info':
        get_info_callback(call)
    else:
        back_callback(call)
    bot.answer_callback_query(call.id)
             

def db_join_game_callback(call: CallbackQuery):
    with sqlite3.connect('db.db') as conn:
        curs = conn.cursor()
        try:
            temp = curs.execute('SELECT ID FROM idnick').fetchall()
            if str(call.message.from_user.id) not in json.dumps(temp).split('"'):
                user_id = call.message.from_user.id
                next_msg = bot.send_message(chat_id=call.message.chat.id, text='Впишите свой никнейм.')
                bot.register_next_step_handler(next_msg, get_nickname)
            else:
                bot.send_message(chat_id=call.message.chat.id, text='Вы уже записаны!)')
        except:
            pass
                    
def db_get_players_list_callback(call: CallbackQuery):
    with sqlite3.connect('db.db') as conn:
        curs = conn.cursor()
        try:
            temp = curs.execute('SELECT NICKNAME_LIST FROM GAME').fetchone()   
        except:
            print('oops')    
        conn.commit()
    bot.send_message(chat_id=call.message.chat.id, text=get_players_text(json.loads(temp[0])))

def db_unjoin_game_callback(call: CallbackQuery):
    with sqlite3.connect('db.db') as conn:
        curs = conn.cursor()
        try:
            temp = curs.execute('SELECT ID FROM idnick WHERE ID = ?', (call.from_user.id, )).fetchone()
            if temp is not None:
                curs.execute('DELETE FROM idnick WHERE id = ?', (call.from_user.id,))
                bot.send_message(chat_id=call.message.chat.id, text='Успешно!')
            else:
                bot.send_message(chat_id=call.message.chat.id, text='Вас нету в таблице!')
        except:
            print('Ой!')
    db_list_update()

def get_rules_callback(call: CallbackQuery):
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text = rules_text, reply_markup= back_markup)

def get_info_callback(call: CallbackQuery):
    """Выводит информацию о текущей игре"""
    if game:
        bot.edit_message_text(chat_id= call.message.chat.id, message_id=call.message.message_id,
                                                        text=info_text(game), reply_markup= back_markup)
    else:
        bot.edit_message_text(chat_id= call.message.chat.id, message_id=call.message.message_id,
                                                        text=no_game_text, reply_markup= back_markup)
    
def back_callback(call: CallbackQuery):
    """Кнопка назад"""
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text=choose_text, reply_markup= start_markup)






@bot.message_handler(commands=['set_game'])
def cmd_set_game(message: Message):
    """Записывает актуальную информацию о предстоящей игре"""
    if message.from_user.id not in admins:
        bot.send_message(chat_id=message.chat.id, text=rightserror_text)
        return
    elif message.chat.type != 'private':
        bot.send_message(chat_id=message.chat.id, text=wrongchat_text)
        return
    
    ent = message.text.split(sep=' ')
    
    
    if len(ent) != 5: 
        bot.send_message(chat_id=message.chat.id, text=setgame_text)
        return
    
    i = iter(ent[1:])
    for key in game:
        game[key] = i.__next__()
        
    bot.send_message(chat_id=message.chat.id, text=info_text(game), reply_markup=back_markup)   



@bot.message_handler(commands=['cancel_game'])
def cmd_cancel_game(message: Message):
    """Отменяет текущую игру и присылает всем уведомления."""
    if message.from_user.id not in admins:
        bot.send_message(chat_id=message.chat.id, text=rightserror_text)
    elif message.chat.type != 'private':
        bot.send_message(chat_id=message.chat.id, text=wrongchat_text)
        return
    
    for chat_id in id_chats: 
        bot.send_message(chat_id= chat_id, text=cancelgame_text)       
    
@repeat(every().wednesday.at('09:00', 'Europe/Moscow'))
@repeat(every().friday.at('09:00', 'Europe/Moscow'))
def send_game_notification():
    """Отправляет уведомления в ЛC насчет новой игры."""
    if game:
        for chat_id in id_chats:
            bot.send_message(chat_id= chat_id, text='Доброе утро! Информация по текущей игре')
            bot.send_message(chat_id= chat_id, text=info_text(game))

def db_list_update():
    with sqlite3.connect('db.db') as conn:
        try:
            curs = conn.cursor()
            ids = curs.execute('SELECT ID FROM idnick').fetchall()
            nicks = curs.execute('SELECT NICKNAME FROM idnick').fetchall()
            temp = []
            for row in ids:
                temp.append(row[0])
            curs.execute('UPDATE GAME SET ID_LIST = ?', (json.dumps(temp),))
            temp = []
            for row in nicks:
                temp.append(row[0])
            curs.execute('UPDATE GAME SET NICKNAME_LIST = ?', (json.dumps(temp),))
        except:
            print('хуйня')
        conn.commit()
    

    
        
def get_nickname(message: Message):
    with sqlite3.connect('db.db') as conn:
        curs = conn.cursor()
        try:
            data = (int(message.from_user.id), str(message.text),)
            curs.execute('INSERT INTO idnick VALUES(?,?)', data)
            bot.send_message(chat_id=message.chat.id, text=f'Ваш никнейм: {message.text}')
        except:
            print('Ой!')
        conn.commit()
    db_list_update()

def db_join_update(message: Message):
    with sqlite3.connect('db.db') as conn:
        curs = conn.cursor()
        try:
            temp = curs.execute('SELECT ID FROM idnick').fetchall()
            if str(message.from_user.id) not in json.dumps(temp).split('"'):
                user_id = message.from_user.id
                next_msg = bot.send_message(chat_id=message.chat.id, text='Впишите свой никнейм.')
                bot.register_next_step_handler(next_msg, get_nickname)
            else:
                bot.send_message(chat_id=message.chat.id, text='Вы уже записаны!)')
        except:
            pass
        

def db_unjoin_update(message: Message):
    with sqlite3.connect('db.db') as conn:
        curs = conn.cursor()
        try:
            temp = curs.execute('SELECT ID FROM idnick WHERE ID = ?', (message.from_user.id, )).fetchone()
            if temp is not None:
                curs.execute('DELETE FROM idnick WHERE id = ?', (message.from_user.id,))
                bot.send_message(chat_id=message.chat.id, text='Успешно!')
            else:
                bot.send_message(chat_id=message.chat.id, text='Вас нету в таблице!')
        except:
            print('Ой!')
    db_list_update()
            

def db_get_players_list(message: Message):
    with sqlite3.connect('db.db') as conn:
        curs = conn.cursor()
        try:
            temp = curs.execute('SELECT NICKNAME_LIST FROM GAME').fetchone()   
        except:
            print('oops')    
        conn.commit()
    bot.send_message(chat_id=message.chat.id, text=get_players_text(json.loads(temp[0])))

@bot.message_handler(content_types=['text'])
def get_text_messages(message: Message):
    if 'записаться' in message.text.lower():
        db_join_update(message)
    elif message.text.lower() == 'правила':
        bot.send_message(chat_id=message.chat.id, text=rules_text)
    elif message.text.lower() == 'список игроков':
        db_get_players_list(message)
    elif message.text.lower() == 'отписаться':
        db_unjoin_update(message)
    elif message.text.lower() == 'информация':
        bot.send_message(chat_id=message.chat.id, text=info_text(game))
    else:
        if message.chat.id not in id_chats:
            id_chats.append(message.chat.id)
        


# def infinity_loop_start():
#     try:
#         bot.infinity_polling()
#     except:
#         bot.infinity_polling()
        
# try:
#     infinity_loop_start()
# except:
#     infinity_loop_start()

bot.infinity_polling()
