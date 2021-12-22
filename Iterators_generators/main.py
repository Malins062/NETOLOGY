# nested_list = []

nested_list = [
    1,
    ['a', 'b', 'c', [89, [100]]],
    ['d', 'e', 'f', 'h', False],
    [1, 2, None],
    'КОНЕЦ'
]


class FlatIterator:

    def __init__(self, list_: list):
        # Распаковка списка, использование ниженаписанного генератора вывода списка
        self.list = [item for item in flat_itarator(list_)]
        # Длина обрабатываемого списка
        self.end = len(self.list)

    def __iter__(self):
        self.start = -1
        return self

    def __next__(self):
        self.start += 1
        if self.start == self.end:
            raise StopIteration
        else:
            return self.list[self.start]


def flat_itarator(list_: list):
    cursor = 0
    while cursor != len(list_):
        value = list_[cursor]
        if isinstance(value, list):
            yield from flat_itarator(value)
        else:
            yield value
        cursor += 1


if __name__ == '__main__':

    # Итераторы
    print(f'{"-" * 10} ИТЕРАТОРЫ {"-" * 10}')
    flat_list = [item for item in FlatIterator(nested_list)]
    print(flat_list)

    for item in FlatIterator(nested_list):
        print(item)

    # Генераторы
    print(f'\n{"-"*10} ГЕНЕРАТОРЫ {"-"*10}')
    flat_list = [item for item in flat_itarator(nested_list)]
    print(flat_list)

    for item in flat_itarator(nested_list):
        print(item)
