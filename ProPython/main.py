from application import salary as slr
from db import people as ppl
from db.data import CATEGORY_EMPLOYEES, USER_NAMES
from datetime import datetime as dt


def print_hi(name):
    print(f'Привет, {name}! \n')


def print_datetime_now():
    print(f'{dt.now():%d.%m.%Y %H-%M-%S}:')


if __name__ == '__main__':
    print_datetime_now()
    print_hi(USER_NAMES[1])

    print_datetime_now()
    ppl.get_employees(CATEGORY_EMPLOYEES[0])

    print_datetime_now()
    slr.calculate_salary(CATEGORY_EMPLOYEES[0])

