from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from abc import ABC, abstractmethod


class Connector:
    #общий класс подключения с экспоненциальнй задержкой
    def connect_retry(self, func_connect, max_attempts=None, initial_wait=1, max_wait=60):
        """
        Подключение к БД ClickHouse с использованием метода экспоненциальной задержки и 
        последующей повторной попыткой подключения.

        max_attempts: Задается количество попыток подключения
        initial_wait: Начальная задержка, которая увеличивается экспоненцивльно
        max_wait: Максимальное время ожидания между попытками подкючения
        """
        attempt = 0
        while True:
            try:
                client = func_connect()
                print(f'Успешное подключение к БД на попытке {attempt + 1}')
                return client
            except Exception as e:
                print(f'Ошибка подключения к БД: {e}')
                attempt +=1
                if max_attempts and attempt >= max_attempts:
                    print(f'Превышено количество попыток подключения к БД: {attempt}')
                    raise e
                
                wait_time = min(initial_wait * (2 ** (attempt - 1)), max_wait)
                print(f'Ошибка подключения к БД: {e}. Попытка {attempt}, повторная попытка через {wait_time} секунд.')
                print(wait_time)


class ElasticBase:
    def __init__(self):
        self.host = os.getenv('ELASTICSEARCH_HOST')
        self.port = int(os.getenv('ELASTICSEARCH_PORT'))
        self.login = None
        self.password = None
        self.con = Elasticsearch([{'host': self.host, 'port': self.port, 'scheme': 'http'}])


# Класс для управления индексами в Elasticsearch
class ElasticsearchIndexManager(ElasticBase):
    def index_correct_logs_period(self, list_index:list):
        """
        Проверка наличия индекса и его создания в случае отсутвия
        """

        mapping = {
    "mappings": {
        "properties": {
            "time": {
                "type": "date",  
                "format": "yyyy-MM-dd'T'HH:mm:ssZ"   
            },
            "log_level": {
                "type": "keyword"  
            },
            "content": {
                "type": "text"  
            },
            "service": {
                "type": "keyword"  
            }
        }
    }
}

        for index in list_index:
            if not self.con.indices.exists(index=index):
                self.con.indices.create(index=index, body=mapping)


class ElasticConnector(ElasticBase, Connector):
    def connect(self):
        con = Elasticsearch([{'host': self.host, 'port': self.port, 'scheme': 'http'}])
        #TODO тут проверка на коннект (?)
        pass
        

class ElasticSearchInsertLogs(ElasticBase):
    def insert_logs(self, logs:list):
        try:
            success, failed = bulk(self.con, logs)
        except Exception as err:
            #TODO добавить обработку/повторную попытку записи
            print(err)
