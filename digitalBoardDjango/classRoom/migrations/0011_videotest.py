# Generated by Django 3.2.5 on 2022-05-15 06:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classRoom', '0010_videolectures'),
    ]

    operations = [
        migrations.CreateModel(
            name='VideoTest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=500)),
                ('videofile', models.FileField(null=True, upload_to='videos/', verbose_name='')),
            ],
        ),
    ]
