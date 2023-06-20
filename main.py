from datetime import datetime, timedelta
from time import sleep

from database import update_database, initialize_db, PeakOnline
from parser import parse_players
from vk_widget import widget_update

URL_TEMPLATE = "https://cdn.rage.mp/master/"
initialize_db()  # Создание таблиц в базе данных

while True:
    projects_online = parse_players(URL_TEMPLATE)  # Парсим онлайн по проектам

    for project in projects_online:
        update_database(project, projects_online[project])  # Вызов функции обновления базы данных
    # Удаление пиков онлайна возрастом 1+ день
    PeakOnline.delete().where(PeakOnline.date < (datetime.now() - timedelta(days=1)))
    widget_update()  # Вызов функции обновления виджета в группе ВК
    sleep(60)
