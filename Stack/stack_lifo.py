# Значения для тестирования
TESTS = [
    '(((([{}]))))',
    '[([])((([[[a*b]-1]])))]{()}',
    '{{[b - (a^7) - 8]}}',
    '}{a^2}',
    '{{[(])]}}',
    '[[{(23*5))}]'
]


# Стэк по типу LIFO
class StackLIFO:

    def __init__(self):
        self.stack = []

    def push(self, item):
        self.stack.append(item)

    def pop(self):
        if len(self.stack) == 0:
            return None
        removed = self.stack.pop()
        return removed

    def is_empty(self):
        return len(self.stack) == 0

    def peek(self):
        return None if self.is_empty() else self.stack[-1]

    def size(self):
        return len(self.stack)


def verify_staples(_value: str) -> bool:
    """
    Функция верификации строки на предмет сбалансированности алфваита скобок alphabet_staples
    :param _value: входное значение
    :return: True - скобки сбалансированы, False - скобки несбалансированы
    """

    alphabet_staples = {'(', ')', '{', '}', '[', ']'}
    staples = {'(': ')', '{': '}', '[': ']'}

    stack = StackLIFO()

    for char in _value:

        if char in alphabet_staples:

            if char in staples.keys():
                stack.push(char)
            else:

                if not stack.is_empty() and staples[stack.peek()] == char:
                    stack.pop()
                else:
                    return False

    return stack.is_empty()


if __name__ == '__main__':
    for num, value in enumerate(TESTS):
        valid = 'Сбалансированно' if verify_staples(value) else 'Несбалансированно'
        print(f'Значение {num + 1}: {value} - {valid}.')
