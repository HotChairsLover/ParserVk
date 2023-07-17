from traceback import format_exc
from datetime import datetime

from vk_api import VkApi

from database import Projects
from settings import group_token, start_play


def widget_update():
    """
    Функция обновления виджета в группе ВК с помощью vk_api
    :return: None
    """
    try:
        projects = []
        db_projects = Projects.select().order_by(Projects.players.desc())
        for project in db_projects:
            # Создание списка словарей с данными проектов
            proj_data = {
                'проект': project.name,
                'онлайн': project.players,
                'пик': project.peak,
                'рекорд': project.record,
                'за_сутки': project.percent,
                'лого': project.logo
            }
            projects.append(proj_data)

        vk_session = VkApi(token=group_token)  # Получение сессии по токену
        widget = {  # JSON виджета
            "title": "Мониторинг проектов",
            "more": "Начать играть",
            "more_url": start_play,
            "head": [
                {"text": "Проект"},
                {"text": "Онлайн",
                 "align": "center"},
                {"text": "Пик",
                 "align": "center"},
                {"text": "Рекорд онлайна",
                 "align": "center"},
                {"text": "За сутки",
                 "align": "center"}
            ], "body": []
        }
        for data in projects:  # Добавление проектов в тело виджета
            item = [{'text': data['проект'],
                     "icon_id": f"club{data['лого']}"},
                    {'text': str(data['онлайн']),
                     "align": "center"},
                    {'text': str(data['пик']),
                     "align": "center"},
                    {'text': str(data['рекорд']),
                     "align": "center"},
                    {'text': data['за_сутки'],
                     "align": "center"}
                    ]
            widget["body"].append(item)
        code = f"return {widget};"  # Окончательный вид JSONa
        vk_session.method('appWidgets.update',
                          {"code": code, "type": 'table'})  # Запрос к vk api для обновления виджета
    except Exception:
        print(format_exc())
        print(datetime.now())
