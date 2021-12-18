import requests
from bs4 import BeautifulSoup
from progress.bar import IncrementalBar
import pandas as pd

# Определяем список ключевых слов
KEYWORDS = {'дизайн', 'фото', 'web', 'python', 'занимательные задачки'}
# Наименование колонок для вывода списка статей
TITLES = ["Дата и время публикации", "Заголовок", "Ссылка", "Слова"]


def response_error(response) -> bool:
    """
    Функция проверки ответа от сервера и вывода сообщения в случае ошибки
    :param response: response.requests.get()
    :return: True - ошибка, False ответ - OK
    """
    try:
        response.raise_for_status()
        return False
    except Exception as Ex:
        print(f'Ошибка при обращении к странице: {Ex}')
        return True


class HabrScrapping:
    def __init__(self, url, keywords):
        # ссылка ресурса
        self.url = url

        # ссыдка для извлечения отдельной статьи через API
        self.url_article = 'https://habr.com/kek/v2/articles/'

        # ссылкка для извлечения свежих статей
        self.url_articles_list = self.url + '/ru/all/'

        # ключевые слова
        self.keywords = keywords

        # найденные статьи
        self.articles = {}

        self.params = {
            'fl': 'ru',
            'hl': 'ru'
        }

    def get_artilces_list(self):
        """
        Извлечение свежих статей в переменную экземлпяра self.articles, обработка отдельных колонок:
        дата и время публикации, название статьи, ссылка, тэги
        :return: количество считанных статей
        """
        headers = {
            'Cookie': '_ym_uid=1639148487334283574; _ym_d=1639149414; _ga=GA1.2.528119004.1639149415; _gid=GA1.2.512914915.1639149415; habr_web_home=ARTICLES_LIST_ALL; hl=ru; fl=ru; _ym_isad=2; __gads=ID=87f529752d2e0de1-221b467103cd00b7:T=1639149409:S=ALNI_MYKvHcaV4SWfZmCb3_wXDx2olu6kw',
            'Accept-Language': 'ru-RU,ru;q=0.9',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1',
            'Cache-Control': 'max-age=0',
            'If-None-Match': 'W/"37433-+qZyNZhUgblOQJvD5vdmtE4BN6w"',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36',
            'sec-ch-ua-mobile': '?0'
            }

        # Запрос
        response = requests.get(self.url_articles_list, headers=headers)

        # Проверка ответа сервера и вывод ошибки в случае неверного ответа
        if response_error(response):
            return False

        # Обработка ответа
        soup = BeautifulSoup(response.text, 'html.parser')

        self.articles = {}

        # Извлекаем превью статей
        articles = soup.find_all('article', class_='tm-articles-list__item')

        for article_ in articles:
            data_article = {}

            # Извлекаем ID статьи
            article_id = article_.attrs.get('id')
            # Если идентификатор статьи не найден, это что-то странное, пропускаем
            if not article_id:
                continue

            # Извлекаем дату статьи
            published = article_.find('span', class_='tm-article-snippet__datetime-published').find('time')
            data_article['published'] = published.attrs.get('title', None)

            # Извлекаем ссылку статьи
            header_article = article_.find('a', class_='tm-article-snippet__title-link')
            data_article['url'] = self.url + header_article.attrs.get('href', None)

            # Извлекаем заголовок статьи
            data_article['title'] = header_article.find('span').text

            # Извлекаем хеш-теги статьи
            hubs = article_.find_all('a', class_='tm-article-snippet__hubs-item-link')
            tags = set(hub.find('span').text.lower() for hub in hubs)

            data_article['keywords'] = tags & KEYWORDS

            self.articles[article_id] = data_article

        return len(self.articles)

    def checking_article(self, id_article):
        """
        Обоработка отдельно статьи, через запрос API и добавления искомых слов, если они найдены в тексте статьи
        :param id_article: идентификатор статьи
        :return: количество найденных слов
        """
        checking_article = self.get_article(id_article)
        for keyword in self.keywords:
            if checking_article['textHtml'].lower().find(keyword) > -1:
                self.articles[id_article]['keywords'].add(keyword)
        return len(self.articles[id_article]['keywords'])

    def get_article(self, id_article):
        """
        Получение всех значений по идентификатору статьи через запрос по API
        :param id_article: идентификатор статьм
        :return: словарь json статьи или ошибка
        """
        # Запрос
        response = requests.get(self.url_article + id_article + '/', self.params)
        # Проверка ответа сервера и вывод ошибки в случае неверного ответа
        if response_error(response):
            return False
        else:
            try:
                return response.json()
            except Exception as Ex:
                return Ex

    def articles_with_keywords(self):
        """
        Вывод списка статей в которой присутствуют в колонке keywords пристутствуют слова self.keywrods
        :return: список статей
        """
        return [
            self.articles[article_]
            for article_ in self.articles
            if self.articles[article_]['keywords'] & self.keywords
        ]


def listing_articles(dict_, titles):
    """
    Функция вывода списка в виде таблицы Pandas
    :param titles: наименовение заголовков таблицы
    :param dict_: слоаврь со значениями заголовков titles
    :return: frame - таблица
    """
    frame = pd.DataFrame([value.values() for value in dict_], columns=titles)
    frame.index = frame.index + 1
    frame.columns.name = '№'
    return f'{frame}'


if __name__ == '__main__':

    # СОздание экземпляра ХАБРа
    habr = HabrScrapping('https://habr.com', KEYWORDS)

    # Извлечение свежих статей в переменную habr.articles и получение их количества
    count_articles = habr.get_artilces_list()

    print(f'Количество найденных свежих статей ресурса: {habr.url} - {count_articles}.\n')

    if count_articles > 0:
        print(f'Обработка отдельно каждой статьи...')
        suffix = '%(percent)d%%.'
        bar = IncrementalBar('Процесс - ', color='green', suffix=suffix, max=count_articles + 2)
        bar.next()

        # Проверка кажды статьи на присутствие в ней ключевыъ слов
        for num, article in enumerate(habr.articles):
            bar.suffix = '{sfx} обработка статьи id{id}: {num} из {count}'.\
                format(id=article, num=num+1, count=count_articles, sfx=suffix)

            # Проверка ключевых слов в верхних тэгах
            if not habr.articles[article]['keywords']:
                # Если в тэгах нет, то отдельно поиск в тексте статьи через запрос API
                habr.checking_article(article)

            bar.next()

        bar.suffix = '{sfx} Анализ контента завершен.'.format(sfx=suffix)
        bar.next()
        bar.finish()

        print(f'\nИТОГОВЫЙ РЕЗУЛЬТАТ\nНайденные статьи по ключевым словам: {habr.keywords}\n')
        print(f'{listing_articles(habr.articles_with_keywords(), TITLES)}\n')
