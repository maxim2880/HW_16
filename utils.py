import json


def load_data_from_json(PATH):
    """Функция для распарсивания json файла"""

    f_data = open(PATH, encoding='utf-8')
    data = f_data.readline()
    return json.loads(data.replace("'", '"'))
