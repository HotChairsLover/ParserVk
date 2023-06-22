from traceback import format_exc
from datetime import datetime

from peewee import Model, MySQLDatabase, AutoField, CharField, IntegerField, ForeignKeyField, DateTimeField

from settings import host, user, password, port, database

connection = MySQLDatabase(host=host, user=user, password=password, port=port, database=database)  # Подключение к БД


class BaseModel(Model):
    """
    Базовая модель
    """

    class Meta:
        database = connection


class Projects(BaseModel):
    """
    Модель онлайна проектов
    """
    id = AutoField(column_name="id")
    name = CharField(column_name="name", null=False, unique=True, max_length=100)
    players = IntegerField(column_name="players", null=False)
    peak = IntegerField(column_name="peak", null=False)
    record = IntegerField(column_name="record", null=False)
    percent = CharField(column_name="percent", null=False, max_length=10)
    logo = CharField(column_name="logo", null=False, max_length=20)

    class Meta:
        table_name = 'projects'


class PeakOnline(BaseModel):
    """
    Модель пикового онлайна проектов
    """
    id = AutoField(column_name="id")
    name = ForeignKeyField(Projects, to_field="name", column_name="name", null=False)
    peak = IntegerField(column_name="peak", null=False)
    date = DateTimeField(column_name="date", default=datetime.now, null=False)

    class Meta:
        table_name = 'peak_online'


def initialize_db():
    """
    Функция создающая в базе данных таблицы
    :return: None
    """
    try:
        connection.connect()
        connection.create_tables([Projects, PeakOnline], safe=True)
        connection.close()
    except Exception:
        print(format_exc())
        print(datetime.now())


def update_database(project, project_data):
    """
    Функция обновления онлайна проектов в базе
    :param project: string название проекта
    :param project_data: dict {'players':int, 'peak':int, 'groupId':string}
    :return:
    """
    try:
        if not Projects.select().where(Projects.name == project).exists():  # Проекта в базе нет
            proj = Projects()  # Добавляем новый проект
            proj.name = project
            proj.players = project_data['players']
            proj.peak = project_data['peak']
            proj.record = project_data['peak']
            proj.percent = "0"
            proj.logo = project_data['groupId']
            proj.save()

            online = PeakOnline()  # Добавляем пиковый онлайн
            online.name = project
            online.peak = proj.peak
            online.save()
        else:  # Проект в базе есть
            proj = Projects.get(Projects.name == project)  # Получение проекта по имени и обновление онлайна
            proj.players = project_data['players']
            proj.peak = project_data['peak']
            yesterday_peak = PeakOnline.select().where(PeakOnline.name == project).order_by(PeakOnline.date.asc()) \
                .limit(1).get()  # Получение самого старого пика онлайна у проекта
            if proj.record < project_data['peak']:  # Обновелнение рекорда онлайна
                proj.record = project_data['peak']
            online = PeakOnline()  # Добавляем новый пиковый онлайн
            online.name = project
            online.peak = proj.peak
            online.save()
            if yesterday_peak.peak < project_data['peak']:  # Подсчет разницы между пиками онлайна
                percent = ((project_data['peak'] - yesterday_peak.peak) / yesterday_peak.peak) * 100
                percent = round(percent, 2)
                proj.percent = f"+{percent}%"
            else:
                percent = ((yesterday_peak.peak - project_data['peak']) / project_data['peak']) * 100
                percent = round(percent, 2)
                proj.percent = f"-{percent}%"

            proj.save()
    except Exception:
        print(format_exc())
        print(datetime.now())
