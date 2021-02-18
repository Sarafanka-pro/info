from uuid import uuid4

import requests

# Имя пользователя, обладающего доступом к необходимым API
USERNAME = ''
# Пароль пользователя
PASSWORD = ''

# URL адрес API сервера
API_URL = 'https://api.sarafanka.space/'  # TEST ENV
# API_URL = 'https://api.sarafanka.store/'  # PRODUCTION ENV

# API URN для авторизации по токену (POST)
LOGIN_TOKEN = 'api/user/login/token/'
# API URN для создания чека (POST) и получения списка чеков (GET)
CHECK = 'api1c/check_cyrillic/list/'
# API URN для отмены чека (PATCH)
CANCEL_CHECK = 'api1c/check/cyrillic/canceled/{}/'


################################
# Получение токена авторизации #
################################

# Объект с авторизационными данными
token_data = {
    'username': USERNAME,
    'password': PASSWORD
}

# Отправка запроса
r = requests.post(API_URL + LOGIN_TOKEN, json=token_data)
result = r.json()
assert r.status_code == 200, result
TOKEN = result['token']

# Заголовок с токеном авторизации
headers = {
    'Authorization': f'Token {TOKEN}'
}


########################################################
# Создание нового чека с двумя товарами одним запросом #
########################################################

# Создаем список объектов продуктов
products = [
    {
        'Ууид': uuid4().hex,  # Уникальный набор из 32 символов
        'Номенклатура': '1200 25 Поплавок для дальн. заброса упрощенный (h40/d20) 25г',  # Строка 512 символов
        'Количество': 20,  # float число
        'Цена': 25,  # float число
        'Сумма': 450,  # float число
        'Штрихкод': '123'  # Строка 128 символов
    },
    {
        'Ууид': uuid4().hex,  # Уникальный набор из 32 символов
        'Номенклатура': 'Леска',  # Строка 512 символов
        'Количество': 10,  # float число
        'Цена': 10,  # float число
        'Сумма': 100,  # float число
        'Штрихкод': '456'  # Строка 128 символов
    },
]

# Создаем объект чека для создания
check_data = {
    'Ууид': uuid4().hex,  # Уникальный набор из 32 символов
    'ФормаОплаты': 'Наличная',  # Варианты: Наличная, Карта, Бонусами
    'КассаККМ': 'Тайга',  # Строка 256 символов
    'Кассир': 'Админ',  # Строка 256 символов
    'Организация': 'ИП Егерь И.Г.',  # Строка 256 символов
    'СуммаДокумента': sum(product['Сумма'] for product in products),  # float число
    'ПромоКод': 'ghtysh32hef',  # Для идентификации консультанта, который обеспечил продажу
    'МагазинУуид': 'YqHfrUn4vsyYplwxvu2WSMAuOklXCNwx',  # Для идентификации магазина, в котором произошла продажа
    'Товар': products  # Список объектов продуктов
}

# Отправка запроса
r = requests.post(API_URL + CHECK, json=check_data, headers=headers)
result = r.json()
assert r.status_code == 201, result


####################################
# Получение списка созданных чеков #
####################################

# Отправка запроса
r = requests.get(API_URL + CHECK, headers=headers)
list_result = r.json()
assert r.status_code == 200, list_result


################################
# Отмена ранее созданного чека #
################################
cancel_data = {
    'ВозвратОтменаЧека': True,
}
cancel_uri = API_URL + CANCEL_CHECK.format(list_result['results'][0]['Ууид'])
r = requests.put(cancel_uri, headers=headers, json=cancel_data)
cancel_result = r.json()
assert r.status_code == 200, cancel_result
