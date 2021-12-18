from pprint import pprint
import requests
from ya_disk import YaUpLoader
from datetime import datetime, timedelta, timezone


def task_1():
    """
    Задание 1: Кто самый умный супергерой?
    :return: Список супер героев, отсортированный по их интеллекту в порядке убывания
    """
    token = "2619421814940190"
    heroes = ['Hulk', 'Captain America', 'Thanos', 'Magic']

    def search_intelligence(token: str, name_hero: str):
        """
        Функция поиска на сетевом ресурсе "https://superheroapi.com/api" интелекутального уровня, героя
        :param token: token for API
        :param name_hero: имя героя для поиска его интеллекта
        :return: интеллект героя, если ошибка то выдает отрицательное число (код ошибки)
        """
        url = f"https://superheroapi.com/api/{token}/search/{name_hero}"
        response = requests.get(url, timeout=5)
        if 199 < response.status_code < 300:
            answer = response.json().get('results', -1)
            if answer != -1:
                for value in answer:
                    if value['name'] == name_hero:
                        return int(value['powerstats']['intelligence'])
                else:
                    return -2
            else:
                return -1
        else:
            return response.status_code * (-1)

    heroes_intelligence = []
    for name in heroes:
        heroes_intelligence.append([name, search_intelligence(token, name)])
    heroes_intelligence = sorted(heroes_intelligence, key=lambda x: x[1], reverse=True)
    return heroes_intelligence


def task_2():
    """
    Задание 2. Передача файла на Яндекс диск
    :return:
    """
    filename = 'test.txt'
    path_disk = 'NETOLOGY'
    token = ''
    uploader = YaUpLoader(token)
    uploader.upload_file_to_disk(path_disk+'/'+filename, filename)


def task_3():
    """
    Задание 3. Вывод всех опубликованных вопросов на сайте stackoverflow за определенный период с тэгом Python
    :return:
    """
    # Вычисление период за послдение два дня
    date_to = datetime.now()
    date_from = (date_to - timedelta(1)).strftime('%d/%m/%Y')
    date_to = date_to.strftime('%d/%m/%Y')
    print(f'Вывод информации за период с {date_from} по {date_to}:')

    # Преобразование даты в Unix формат
    date_to = round(datetime.strptime(date_to, "%d/%m/%Y").replace(tzinfo=timezone.utc).timestamp())
    date_from = round(datetime.strptime(date_from, "%d/%m/%Y").replace(tzinfo=timezone.utc).timestamp())
    tag = 'Python'
    url = f'https://api.stackexchange.com/2.3/questions?fromdate={date_from}&todate={date_to}&order=desc&sort=activity&tagged={tag}&site=stackoverflow'
    response = requests.get(url, timeout=15)
    if 199 < response.status_code < 300:
        r = response.json()
        pprint(response.json())
    else:
        try:
            response.raise_for_status()
        except Exception as e:
            print('Ошибка при обращении к сетевому ресурсу: ' + str(e))


if __name__ == '__main__':
    # Задание 1
    print('Список интеллекта для представленных героев (первый герой, самый умный): ')
    pprint(task_1())

    # Задание 2
    print('\nПередача файла на Yandex Disk: ')
    task_2()

    # Задание 3
    print('\n--- Поиск вопросов на сайте StackOverFlow c тэгом Python ---')
    task_3()
