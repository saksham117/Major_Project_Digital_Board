# Generated by Django 3.2.5 on 2021-11-27 06:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classRoom', '0002_auto_20211127_1142'),
    ]

    operations = [
        migrations.AlterField(
            model_name='submitassignment',
            name='comment',
            field=models.TextField(blank=True, default='No Comments'),
        ),
    ]
