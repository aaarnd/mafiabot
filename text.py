def get_players_text(data):
    string = ''
    for user in data:
        string += f'{user}\n'
    return string
def info_text(game):
    return 'Информация об игре.\n' f'Дата - {game["date"]}\n' f'Время - {game["time"]}\n' f'Место - {game["location"]}\n' f'Цена - {game["price"]}\n'
wrongchat_text = 'Вне ЛС бот поддерживает следующие команды: записаться, отписаться, правила, список игроков, информация'
rules_text = 'Текст с правилами'
join_text = 'Вы записались на игру'
unjoin_text = 'Вы отписались от игры'
get_players_list = 'Я пока не придумал, как его реализовать'
start_text = 'Привет. Данный бот предназначен для ведения учета игр в мафию и записи на них'
no_game_text = 'Сегодня игры нету!'
choose_text = 'Выберите действие:'
rightserror_text = 'Ошибка прав доступа'
setgame_text = 'Правильное использование команды: /set_game <date> <time> <location> <price>'
cancelgame_text = 'Уважаемые участники! Сегодняшняя игра к сожалению отменена' # здесь должна быть сборка упоминаний

