import json


def load_testing_data(data_filename: str) -> list:
    """
    Функция загрузки данных из файла в формате json, для дальнейшего тестирования
    :param data_filename: имя файла
    :return: данные в виде списка
    """
    test_data = []
    with open(data_filename, 'r', encoding='utf-8') as f:
        data = json.load(f)
        for data_for_test in data['test_data']:
            test_data.append(tuple(data_for_test))
    return test_data
