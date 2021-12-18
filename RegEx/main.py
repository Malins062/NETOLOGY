import re
import pandas as pd
import csv


class ContactsBook:
    """
    Общий класс книги контактов
    """

    def __init__(self):
        self.contacts_list = []
        self.contacts_headers = []

    def __str__(self):
        frame = pd.DataFrame(self.contacts_list, columns=['ФАМИЛИЯ', 'ИМЯ', 'ОТЧЕСТВО',
                                                          'ОРГАНИЗАЦИЯ', 'ДОЛЖНОСТЬ', 'ТЕЛЕФОН',
                                                          'E-MAIL'])
        frame.index = frame.index + 1
        frame.columns.name = '№'
        return f'{frame}'

    def read_book(self, book_file_name):
        try:
            # Чтение csv файла
            with open(book_file_name, encoding='utf-8') as file:
                rows = csv.reader(file, delimiter=",")
                self.contacts_list = list(rows)

                # Сохранение заголовков списка
                self.contacts_headers = self.contacts_list[0]

                # Уаделение заголовков списка
                self.contacts_list.pop(0)
                return True
        except Exception as Ex:
            print(Ex)
            return False

    def write_book(self, book_file_name):
        try:
            # Добавление заголовков к списку
            self.contacts_list.insert(0, self.contacts_headers)

            # Запись в файл
            with open(book_file_name, 'w', newline='', encoding='utf-8') as file:
                data_writer = csv.writer(file, delimiter=',')
                data_writer.writerows(self.contacts_list)
                return True
        except Exception as Ex:
            print(Ex)
            return False

    def correct_book(self):
        """
        Фукнция приведения поля телефонного номера из списка конактнов contact_list,
        к единому стандарту +7(999)999-99-99 доб.999, а также разбивка ФИО на соответствующие поля
        """
        try:
            # Регулярное выражение телефонных номеров
            phone_pattern = re.compile(r'(\+*)([7|8]*)([\s-]*)(\(?)([\s-]*)(\d{3})([\s-]*)(\)?)([\s-]*)'
                                       r'(\d{3})([\s-]*)(\d{2})([\s-]*)(\d{2})'
                                       r'(\s?)([\s|(]*)(доб.)*(\s*)(\d*)([\s|)]*)')
            phone_pattern_replace = r'+7(\6)\10-\12-\14\15\17\19'

            for record in self.contacts_list:
                # Форматирование телефонного номера
                record[5] = phone_pattern.sub(phone_pattern_replace, record[5])

                # Разбивка Ф + И + О
                fio = record[0] + ' ' + record[1] + ' ' + record[2]
                for index, value in enumerate(fio.split()):
                    record[index] = value
            return True
        except Exception as Ex:
            print(Ex)
            return False

    def set_unique_FI_book(self):
        """
        Метод объединения двойных записей в контактном листе contact_list
        """
        try:
            names_contact = {}
            for record in self.contacts_list:
                # Ключ-идентификатор по которому будут объединяться записи
                _id = record[0] + record[1]

                new_record = names_contact.get(_id, False)
                if not new_record:
                    names_contact[_id] = record
                else:
                    for index, value in enumerate(record[2:], 2):
                        if len(value) > 0 and value != new_record[index]:
                            names_contact[_id][index] += value

            self.contacts_list = [record for record in names_contact.values()]
            return True
        except Exception as Ex:
            print(Ex)
            return False


if __name__ == '__main__':
    NEW_BOOK_FILE_NAME = 'phonebook.csv'
    BOOK_FILE_NAME = 'phonebook_raw.csv'

    book = ContactsBook()

    if book.read_book(BOOK_FILE_NAME):
        print(f'ИСХОДНЫЕ ДАННЫЕ:\n{book}\n')

        if book.correct_book() and book.set_unique_FI_book():
            print(f'СКОРРЕКТИРОВАННЫЕ ДАННЫЕ:\n{book}\n')
            if book.write_book(NEW_BOOK_FILE_NAME):
                print(f'Новая книга контактов сохранена в файл: {NEW_BOOK_FILE_NAME}')
