class Student:
    def __init__(self, name, surname, gender):
        self.name = name
        self.surname = surname
        self.gender = gender
        self.finished_courses = []
        self.courses_in_progress = []
        self.grades = {}

    def rate_hw(self, lecturer, course, grade):
        if 0 <= grade <= 10:
            if isinstance(lecturer, Lecturer) and course in lecturer.courses_attached and\
                    course in self.courses_in_progress:
                if course in lecturer.grades:
                    lecturer.grades[course] += [grade]
                else:
                    lecturer.grades[course] = [grade]
                return f'Оценка лектору добавлена: {lecturer.surname} {lecturer.name}, ' \
                       f'курс "{course}" оценка - {grade}.'
            else:
                return f'ОШИБКА: студент {self.surname}{" " if course in self.courses_in_progress else " не "}' \
                       f'учится на данном курсе, a лектор {lecturer.surname}' \
                       f'{" " if course in lecturer.courses_attached else " не "}преподает указанный курс.'
        else:
            return f'ОШИБКА: выставляемая лектору {lecturer.surname} оценка - {grade} ' \
                   f'должна быть в пределах от 0 до 10!'

    def average_grade(self, course=''):
        """
        Функция посчета среднего значения оценок, выставленным студенту за домашние задания
        по преподаваемому курсу - course.
        Если параметр course не указан - производится подсчет по всем курсам, закрепленным за студентом
        """
        if course == '' and len(self.grades) > 0:
            sum_grades = sum(sum(self.grades.values(), []))
            count_grades = sum(len(value) for value in self.grades.values())
            res = sum_grades / count_grades
        elif course in self.grades.keys() and len(self.grades[course]) > 0:
            sum_grades = sum(self.grades[course])
            count_grades = len(self.grades[course])
            res = sum_grades / count_grades
        else:
            res = 0
        return res

    def __str__(self):
        return f'Имя, Фамилия: {self.name} {self.surname}\n' \
               f'Курсы в процессе изучения: {", ".join(self.courses_in_progress)}. ' \
               f'Общая средняя оценка за все домашние задания: {self.average_grade():.1f}\n' \
               f'Завершенные курсы: {", ".join(self.finished_courses)}'

    def __lt__(self, other):
        return self.average_grade() < other.average_grade()

    def __eq__(self, other):
        return self.average_grade() == other.average_grade()


class Mentor:
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.courses_attached = []


class Lecturer(Mentor):
    def __init__(self, name, surname):
        super().__init__(name, surname)
        self.grades = {}

    def average_grade(self, course=''):
        """
        Функция посчета среднего значения оценок, выставленными студентами за лекции по преподаваемому курсу - course
        Если параметр course не указан - производится подсчет по всем курсам, закрепленным за лектором
        """
        if course == '' and len(self.grades) > 0:
            sum_grades = sum(sum(self.grades.values(), []))
            count_grades = sum(len(value) for value in self.grades.values())
            res = sum_grades / count_grades
        elif course in self.grades.keys() and len(self.grades[course]) > 0:
            sum_grades = sum(self.grades[course])
            count_grades = len(self.grades[course])
            res = sum_grades / count_grades
        else:
            res = 0
        return res

    def __str__(self):
        return f'Имя, Фамилия: {self.name} {self.surname}\n' \
               f'Преподаваемые курсы: {", ".join(self.courses_attached)}. ' \
               f'Средняя оценка за лекции: {self.average_grade():.1f}'

    def __lt__(self, other):
        return self.average_grade() < other.average_grade()

    def __eq__(self, other):
        return self.average_grade() == other.average_grade()


class Reviewer(Mentor):
    def rate_hw(self, student, course, grade):
        if 0 < grade <= 5:
            if isinstance(student, Student) and course in self.courses_attached and \
                    course in student.courses_in_progress:
                if course in student.grades:
                    student.grades[course] += [grade]
                else:
                    student.grades[course] = [grade]
                return f'Оценка студенту добавлена: {student.surname} {student.name}, курс "{course}" оценка - {grade}.'
            else:
                return f'ОШИБКА: преподаватель {self.surname}{" " if course in self.courses_attached else " не "}' \
                       f'ведет дисциплину у студента, a студент {student.surname}' \
                       f'{" " if course in student.courses_in_progress else " не "}учится на указанном курсе.'
        else:
            return f'Ошибка: выставляемая студенту оценка ({grade}) должна быть в пределах от 1 до 5!'

    def __str__(self):
        return f'Имя, Фамилия: {self.name} {self.surname}\n' \
               f'Курируемые курсы: {", ".join(self.courses_attached)}.'


def print_records(lst: list, title=''):
    """
    Функция вывода на печать, посредством print(): заголовка title и value.__str__ из списка lst
    """
    print(title)
    for n, value in enumerate(lst):
        print(f'{n + 1}:', value)
    print()


def average_grade(lst: list, course=''):
    """
    Функция подсчета среднего значения оценок в списке lst по отдельному курсу (направлению) course
    """
    sum_average_grades = 0
    count_persons = 0
    res = 0
    for cls in lst:
        if (isinstance(cls, Student) and course in cls.courses_in_progress) or \
                (isinstance(cls, Lecturer) and course in cls.courses_attached):
            sum_average_grades += cls.average_grade(course)
            count_persons += 1
    if count_persons > 0:
        res = sum_average_grades / count_persons
    return res


# Ввод исходных данных студентов
students = [Student('Alexei', 'Malinovskiy', 'Male'),
            Student('Dmitriy', 'Ivanov', 'Male'),
            Student('Kulikova', 'Olga', 'Female')]
students[0].courses_in_progress += ['Python']
students[0].finished_courses += ['GitHub']
students[1].courses_in_progress += ['GitHub']
students[2].courses_in_progress += ['GitHub', 'Python']
students[2].finished_courses += ['English', 'Flask']
# Исходные данные лекторов
lecturers = [Lecturer('Oleg', 'Bulygin'), Lecturer('Alena', 'Batitskaya')]
lecturers[0].courses_attached += ['Python', 'GitHub']
lecturers[1].courses_attached += ['GitHub']
# Исходные данные проверяющих
reviewers = [Reviewer('Alexander', 'Bardin'), Reviewer('Mike', 'Okatiev')]
reviewers[0].courses_attached += ['Python', 'GitHub']
reviewers[1].courses_attached += ['English', 'GitHub']

# Вывод первоначальных данных
print('--- ИСХОДНЫЕ ДАННЫЕ ---')
print_records(students, 'СТУДЕНТЫ:')
print_records(lecturers, 'ЛЕКТОРЫ:')
print_records(reviewers, 'ПРОВЕРЯЮЩИЕ:')

print('\n--- ВЫСТАВЛЕНИЕ ОЦЕНОК ---')
# Выставление оценок студентам
print('ОЦЕНКИ СТУДЕНТАМ ЗА ДОМАШНИЕ ЗАДАНИЯ:')
print(reviewers[0].rate_hw(students[0], 'Python', 5))
print(reviewers[0].rate_hw(students[0], 'Python', 4))
print(reviewers[0].rate_hw(students[0], 'Python', 3))
print(reviewers[1].rate_hw(students[1], 'GitHub', 8))
print(reviewers[1].rate_hw(students[1], 'GitHub', 3))
print(reviewers[1].rate_hw(students[1], 'GitHub', 2))
print(reviewers[0].rate_hw(students[2], 'GitHub', 4))
print(reviewers[0].rate_hw(students[2], 'Python', 3))
print(reviewers[1].rate_hw(students[2], 'GitHub', 5))

# Выставление оценок лекторам
print('\nОЦЕНКИ ЛЕКТОРАМ СТУДЕНТАМИ:')
print(students[0].rate_hw(lecturers[0], 'Python', 9))
print(students[1].rate_hw(lecturers[0], 'Python', 10))
print(students[2].rate_hw(lecturers[0], 'Python', 10))
print(students[2].rate_hw(lecturers[1], 'GitHub', 7))
print(students[2].rate_hw(lecturers[0], 'GitHub', 10))
print(students[1].rate_hw(lecturers[1], 'GitHub', 20))

# Вывод изменнных данных, после выставления оценок
print('\n--- ИЗМЕНЕННЫЕ ДАННЫЕ ---')
print_records(students, 'СТУДЕНТЫ:')
print_records(lecturers, 'ЛЕКТОРЫ:')

# Проверка работоспособности операторов < >
print('\n --- ПРОВЕРКА ОПЕРАТОРОВ СРАВНЕНИЯ С ОПИСАННЫМИ КЛАССАМИ ---')
print(students[0] > students[1])
print(lecturers[0] < lecturers[1])

print('\n --- РЕЗУЛЬТАТЫ СРЕДНИХ ОЦЕНОК СТУДЕНТОВ ПО КУРСАМ ---')
courses = []
for person in students:
    courses.extend(person.courses_in_progress)
for i in set(courses):
    print(f'Курс - {i}. Средняя оценка {average_grade(students, i):.1f}')

print('\n --- РЕЗУЛЬТАТЫ СРЕДНИХ ОЦЕНОК СТУДЕНТОВ ЛЕКТОРАМ ---')
courses = []
for person in lecturers:
    courses.extend(person.courses_attached)
for i in set(courses):
    print(f'Курс - {i}. Средняя оценка - {average_grade(lecturers, i):.1f}')
