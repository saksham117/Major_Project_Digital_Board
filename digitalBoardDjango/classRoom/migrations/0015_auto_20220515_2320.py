# Generated by Django 3.2.5 on 2022-05-15 17:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classRoom', '0014_rename_videofile_lectures_videofile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lectures',
            name='excelPath',
        ),
        migrations.AddField(
            model_name='lectures',
            name='excelFile',
            field=models.FileField(max_length=200, null=True, upload_to=''),
        ),
    ]