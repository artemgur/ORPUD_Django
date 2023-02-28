from django.contrib.auth import get_user_model
from django.db import models

User: type = get_user_model()


class Tag(models.Model):
    text = models.TextField(verbose_name='Текст')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.text


class Note(models.Model):
    title = models.TextField(verbose_name='Название')
    text = models.TextField(verbose_name='Текст')
    time_created = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    time_edited = models.DateTimeField(auto_now=True, verbose_name='Время изменения')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, verbose_name='Теги')


class PageVisitCount(models.Model):
    url = models.TextField(verbose_name='URL')
    visit_count = models.IntegerField(verbose_name='Количество посещений')
