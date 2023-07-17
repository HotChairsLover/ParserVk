from traceback import format_exc
from datetime import datetime
from json import loads

from requests import get

from servers_data import json_data


def parse_players(url):
    """
    Функция парсинга JSONa данных по серверам находящегося по передаваемой ссылке
    :param url: string ссылка на сайт
    :return: dict {
        string: {'players':int, 'peak':int, 'groupId':string},
        string: {'players':int, 'peak':int, 'groupId':string}
    }
    """
    try:
        r = get(url)  # Получение данных по URL
        parsed_data = loads(r.text)  # Парсинг полученного JSON
        parsed_projects = loads(json_data)  # Парсинг JSON с проектами и их серверами
        all_servers = {}
        projects = {}
        complete = {}
        for ip, data in parsed_data.items():  # Заполнение словаря со всеми серверами
            all_servers[ip] = data
        full_data = {  # Словарь с общим онлайном по всем серверам
            "players": 0,
            "peak": 0,
            "groupId": "121111933"
        }
        complete["RAGE Multiplayer"] = full_data
        for server in all_servers:  # Подсчет общего онлайна
            full_data['players'] += all_servers[server]['players']
            full_data['peak'] += all_servers[server]['peak']
        for project in parsed_projects['projects']:  # Заполнение словаря проектов
            projects[project['name']] = {"servers": project['servers'], "groupId": project['groupID']}
        for project in projects:  # Подсчет общего онлайна проектов и добавление в словарь
            data = {
                "players": 0,
                "peak": 0,
                "groupId": projects[project]['groupId']
            }
            for server in projects[project]['servers']:
                if server in all_servers:
                    data["players"] += all_servers[server]['players']
                    data["peak"] += all_servers[server]['peak']

            complete[project] = data
        return complete
    except Exception:
        print(format_exc())
        print(datetime.now())
