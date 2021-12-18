from application import *
from db import *
from datetime import *


def print_hi(name):
    print(f'Привет, {name}! \n')


def print_datetime_now():
    print(f'{datetime.now():%d.%m.%Y %H-%M-%S}:')


if __name__ == '__main__':
    print_datetime_now()
    print_hi(data.USER_NAMES[1])

    print_datetime_now()
    people.get_employees(data.CATEGORY_EMPLOYEES[0])

    print_datetime_now()
    salary.calculate_salary(data.CATEGORY_EMPLOYEES[0])

