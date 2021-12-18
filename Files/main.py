import os
from pprint import pprint


def read_file_cook_book(f_name: str, encoding='utf-8') -> dict:
    """
    Функция считывания структурированных данных из файла и записи их в словарь
    :param encoding: тип кодировки файла, если не указан то 'utf-8'
    :param f_name: имя файла
    :return: считанные данные из файла в виде словаря
    """
    output_data = {}
    try:
        with open(f_name, encoding=encoding) as f:
            for line in f:
                # Строка наименования ключа верхнего уровня
                key = line.rstrip()
                if not key:
                    continue
                # Строка количества наименований нижнего уровня
                cnt = int(f.readline().rstrip())
                # Создания списка словаря нижнего уровня
                temp_list = []
                for _ in range(cnt):
                    name, count, units = f.readline().strip().rstrip().split('|')
                    temp_list.append(
                        {'Наименование': name.strip(), 'Количество': int(count.strip()), 'Ед.изм.': units.strip()}
                    )
                output_data[key] = temp_list
    except BaseException as Err:
        output_data['Error'] = Err
    print(id(output_data))
    return output_data


def get_shop_list_by_dishes(book: dict, dishes: list, person_count=1) -> dict:
    """
    Функция расчета и вывода списка необходимого количества ингридиентов для приготовления списка блюд dishes,
    для person_count персон.
    :param book: список блюд в меню, и рецептов
    :param dishes: список блюд
    :param person_count: количество персон для общего расчета суммы всех необходимых ингридентов,
    если параметр не задан, расчет будет производиться для одной персоны
    :return: список необходимых ингрдиентов и их сумму
    """
    output_data = {}
    for plate in dishes:
        for ingredient in book.get(plate):
            name = ingredient['Наименование']
            if output_data.get(name):
                output_data[name] = {'measure': ingredient['Ед.изм.'],
                                     'quantity': ingredient['Количество'] * person_count + output_data[name]['quantity']
                                     }
            else:
                output_data[name] = {'measure': ingredient['Ед.изм.'],
                                     'quantity': ingredient['Количество'] * person_count}
    return output_data


def files_to_file(files_: list, file_: str, encoding='utf-8') -> str:
    """
    Функция объединения списка файлов  files_ в один файл file_
    :param encoding: тип кодировки файлов, если не указан то 'utf-8'
    :param files_: список файлов для объединения
    :param file_: результирующий файл
    :return: имя результирующего файла в случае успешного объединения, иначе наименование ошибки
    """
    res = file_
    try:
        with open(file_, 'w', encoding=encoding) as f_write:
            for value in files_:
                # Запись наименование обрабатываеомго файла
                f_write.write(value[0]+'\n')
                # Запись колчиества строк в обрабатываем файле
                f_write.write(str(value[1])+'\n')
                # Запись содержимого, обрабатываемого файла
                with open(value[0], encoding=encoding) as f_read:
                    f_write.writelines(f_read.readlines())
                    f_write.write('\n')
    except BaseException as Err:
        res = Err
    return res


def len_files(files: list, encoding='utf-8') -> list:
    """
    Функция подсчета количества строк в представленном списке файлов - files
    :param files: Список файлов
    :param encoding: тип кодировки файлов, если не указана то 'utf-8'
    :return: Список в виде кортежей, отсортированный по второвму значению: (Имя файла : количество строк)
    """
    output_data = {}
    for file_ in files:
        try:
            with open(file_, encoding=encoding) as f:
                count = sum(1 for _ in f)
            output_data[file_] = count
        except BaseException as Err:
            output_data['Error'] = Err
        output_data[file_] = count
    return sorted(output_data.items(), key=lambda x: x[1])


if __name__ == '__main__':
    # Данные файла для считывания информации
    file_name = 'data\\recipes.txt'
    full_file_name = os.getcwd() + '\\' + file_name

    # --- ЗАДАНИЕ №1 ---
    # Считывание словаря рецептов
    cook_book = read_file_cook_book(full_file_name)
    # Вывод книги рецептов на экран
    print('--- КНИГА РЕЦЕПТОВ ---')
    pprint(cook_book)

    # --- ЗАДАНИЕ №2 ---
    # Расчет количество необходимых ингрдиентов для нужных блюд и количества персон
    ingredients_order = get_shop_list_by_dishes(cook_book, ['Запеченный картофель', 'Омлет'], 2)
    # Вывод расчета на экран
    print('\n--- ПЕРЕЧЕНЬ ИНГРДИЕНТОВ ДЛЯ ЗАКАЗА ---')
    pprint(ingredients_order)

    # --- ЗАДАНИЕ №3 ---
    dir_to_read = 'data'
    full_path = os.getcwd() + '\\' + dir_to_read
    files_to_read = [full_path + '\\' + name for name in os.listdir(full_path)]

    # Вывод на экран списка обрабатываемых файлов
    print('\n--- СПИСОК ОБРАБАТЫВАЕМЫХ ФАЙЛОВ ---')
    pprint(files_to_read)

    # Подсчёт количества строк в файлах
    files_dict = len_files(files_to_read)
    # Вывод на экран количества строк в файлах
    print('\n--- КОЛИЧЕСТВО СТРОК В ФАЙЛАХ ---')
    pprint(files_dict)

    # Вывод на экран результата объединения файлов
    print('\n--- ОБЪЕДИНЕНИЕ ФАЙЛОВ ---')
    pprint(f'Результат объедения файлов: {files_to_file(files_dict, "result.txt")}.')

