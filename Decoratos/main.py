from pprint import pprint
import requests
from datetime import datetime, timedelta, timezone

# Имя файла логов
LOG_FILE_NAME: str = 'results.log'
PATH_LOG: str = 'LOG/'


def function_tracer(log_file_name):
    """
    Декоратор с входными параметрами
    :param log_file_name: путь и имя лог-файла
    :return:
    """
    def _decorator(_function):
        def _tracer(*args, **kwargs):

            try:
                with open(log_file_name, 'a', encoding='utf-8') as f_write:
                    f_write.write('\n' + ('-' * 150))
                    f_write.write(f'\n{datetime.now()} - вызвана функция {_function.__name__}'
                                  f'с аргументами: {args} {kwargs}.\n')

                    result = _function(*args, **kwargs)

                    f_write.write(f'Результат выполнения функции:\n{result}\n')
                    f_write.write('-' * 150)

            except BaseException as Err:
                result = Err
                print(f'ПАРАМЕТРЫ:\n1) имя и путь лог-файла: {log_file_name}')
                print(f'2) функция {_function.__name__} с аргументами: {args} {kwargs}.\n')
                print('ОШИБКА:')
                pprint(result)

            return result

        return _tracer

    return _decorator


@function_tracer(log_file_name=PATH_LOG + LOG_FILE_NAME)
def task_3(last_days: int):
    """
    Задание 3. Вывод всех опубликованных вопросов на сайте stackoverflow за последние 'last_days' дней с тэгом Python
    :type last_days: количество дней для выборки
    :return:
    """
    print('\n--- Поиск вопросов на сайте StackOverFlow c тэгом Python ---')

    # Вычисление период за послдение два дня
    date_to = datetime.now()
    date_from = (date_to - timedelta(last_days)).strftime('%d/%m/%Y')
    date_to = date_to.strftime('%d/%m/%Y')
    print(f'Вывод информации за период с {date_from} по {date_to}:')

    # Преобразование даты в Unix формат
    date_to = round(datetime.strptime(date_to, "%d/%m/%Y").replace(tzinfo=timezone.utc).timestamp())
    date_from = round(datetime.strptime(date_from, "%d/%m/%Y").replace(tzinfo=timezone.utc).timestamp())
    tag = 'Python'
    url = f'https://api.stackexchange.com/2.3/questions?fromdate={date_from}' \
          f'&todate={date_to}&order=desc&sort=activity&tagged={tag}&site=stackoverflow'
    response = requests.get(url, timeout=15)
    if 199 < response.status_code < 300:
        result = response.json()
        pprint(result)
        return result
    else:
        try:
            response.raise_for_status()
        except Exception as Err:
            print('Ошибка при обращении к сетевому ресурсу: ' + str(Err))


if __name__ == '__main__':
    try:
        days = int(input('Введите количество дней, для анализа сетевого ресурса: '))
        # Вывов функции из давнишнего задания по курсу, используя декоратор
        task_3(days)
    except Exception as Err:
        print('Ошибка выполнения: ' + str(Err))
