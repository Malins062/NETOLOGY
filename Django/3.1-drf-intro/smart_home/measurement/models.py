from django.db import models


class Sensor(models.Model):
    id = models.AutoField(unique=True, primary_key=True)
    name = models.CharField(max_length=50, null=False, verbose_name='Название')
    description = models.TextField(null=True, blank=True, verbose_name='Описание')
    image = models.ImageField(null=True, blank=True, verbose_name='Фотография')

    class Meta:
        verbose_name = 'Датчик'
        verbose_name_plural = 'Датчики'
        ordering = ['id']

    def __str__(self):
        return f'Датчик ({self.id}): {self.name} ({self.description})'


class Measurement(models.Model):
    id = models.AutoField(unique=True, primary_key=True)
    temperature = models.FloatField(null=False, verbose_name='Температура')
    created_at = models.DateTimeField(null=False, auto_now=True,
                                      verbose_name='Дата и время измерения')
    sensor = models.ForeignKey(Sensor, related_name='measurements', on_delete=models.CASCADE,
                               verbose_name='Датчик')

    class Meta:
        verbose_name = 'Измерение'
        verbose_name_plural = 'Измерения'

    def __str__(self):
        return f'№{self.id}: {self.temperature}'
