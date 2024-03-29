# Generated by Django 4.1.7 on 2023-02-28 17:50

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('web', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PageVisitCount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.TextField(verbose_name='URL')),
                ('visit_count', models.IntegerField(verbose_name='Количество посещений')),
            ],
        ),
        migrations.AlterField(
            model_name='note',
            name='tags',
            field=models.ManyToManyField(to='web.tag', verbose_name='Теги'),
        ),
        migrations.AlterField(
            model_name='note',
            name='text',
            field=models.TextField(verbose_name='Текст'),
        ),
        migrations.AlterField(
            model_name='note',
            name='time_created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Время создания'),
        ),
        migrations.AlterField(
            model_name='note',
            name='time_edited',
            field=models.DateTimeField(auto_now=True, verbose_name='Время изменения'),
        ),
        migrations.AlterField(
            model_name='note',
            name='title',
            field=models.TextField(verbose_name='Название'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='text',
            field=models.TextField(verbose_name='Текст'),
        ),
    ]
