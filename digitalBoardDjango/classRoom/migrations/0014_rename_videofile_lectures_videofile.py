# Generated by Django 3.2.5 on 2022-05-15 12:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('classRoom', '0013_videocodes'),
    ]

    operations = [
        migrations.RenameField(
            model_name='lectures',
            old_name='videofile',
            new_name='videoFile',
        ),
    ]
