from django.db import models


class Student(models.Model):
    id = models.AutoField(unique=True, primary_key=True)
    name = models.CharField(max_length=30, verbose_name='Имя')
    group = models.CharField(max_length=10, verbose_name='Класс')

    class Meta:
        verbose_name = 'Ученик'
        verbose_name_plural = 'Ученики'

    def __str__(self):
        return self.name


class Teacher(models.Model):
    id = models.AutoField(unique=True, primary_key=True)
    name = models.CharField(max_length=30, verbose_name='Имя')
    subject = models.CharField(max_length=10, verbose_name='Предмет')
    students = models.ManyToManyField(Student, verbose_name='Ученики', related_name='teachers')

    class Meta:
        verbose_name = 'Учитель'
        verbose_name_plural = 'Учителя'

    def __str__(self):
        return self.name
