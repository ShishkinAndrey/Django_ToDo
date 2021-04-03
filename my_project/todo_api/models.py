import datetime

from django.contrib.auth.models import User
from django.db import models


class Note(models.Model):
    STATE = (
        (0, 'Отложено'),
        (1, 'Активно'),
        (2, 'Выполнено')
    )
    next_day = datetime.datetime.now() + datetime.timedelta(days=1)
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    content = models.TextField(default='', verbose_name='Содержание', blank=True)
    state = models.IntegerField(default='0', choices=STATE, verbose_name='Статус состояния')
    author = models.ForeignKey(User, related_name='author', on_delete=models.PROTECT, blank=True)
    importance = models.BooleanField(default=False, verbose_name='Важно')
    public = models.BooleanField(default=False, verbose_name='Публичная')
    pubdate = models.DateTimeField(default=next_day, verbose_name='Дата')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Блог'
        verbose_name_plural = 'Блог'

