from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup

back_markup = InlineKeyboardMarkup()
back_markup.add(InlineKeyboardButton(
                    text='⬅',
                    callback_data='back'
                ))




start_markup = InlineKeyboardMarkup(row_width=2)
start_markup.add(InlineKeyboardButton(
                text='Записаться',
                callback_data='join_game'
                ),
                InlineKeyboardButton(
                text='Список игроков',
                callback_data='players_list'
                ),
                InlineKeyboardButton(
                text='Отписаться',
                callback_data='unjoin_game'
                ),
                InlineKeyboardButton(
                    text='Правила игры',
                    callback_data='rules'
                ),
                InlineKeyboardButton(
                text='Информация о текущей игре',
                callback_data='info'
                )
                )




# def back_keyboard():
#     return InlineKeyboardMarkup(
#         keyboard=[
#             [
#                 InlineKeyboardButton(
#                     text='⬅',
#                     callback_data='back'
#                 )
#             ]
#         ]
#     )


# def start_markup():
#     return InlineKeyboardMarkup(
#         keyboard=[
#             [InlineKeyboardButton(
#                 text = 'Записаться',
#                 callback_data= 'join_game'
#             ),
#             InlineKeyboardButton(
#                 text = 'Список игроков',
#                 callback_data= 'players_list'
#             )],
#             [InlineKeyboardButton(
#                 text = 'Отписаться',
#                 callback_data= 'unjoin_game'
#             ),
#             InlineKeyboardButton(
#                 text = 'Правила игры',
#                 callback_data= 'rules'
#             )],
#             [InlineKeyboardButton(
#                 text = 'Информация о текущей игре',
#                 callback_data= 'info'
#             )],
#         ],
#         row_width=2
#     )
    
    # markup = quick_markup({
    #     'Записаться': {'callback_data' : 'join_game'},
    #     'Список игроков' : {'callback_data' : 'players_list'},
    #     'Отписаться' : {'callback_data' : 'unjoin_game'},
    #     'Правила игры' : {'callback_data' : 'rules'},
    #     'Информация о текущей игре' : {'callback_data' : 'info'}
    # })