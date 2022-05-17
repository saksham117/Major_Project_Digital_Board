# Generated by Django 3.2.5 on 2022-05-17 02:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('classRoom', '0017_post_postids_reply'),
    ]

    operations = [
        migrations.CreateModel(
            name='QuizCodes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quizCode', models.CharField(max_length=10, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='CreateQuiz',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('submissionDate', models.DateField()),
                ('quizCode', models.CharField(max_length=10)),
                ('quiz', models.URLField()),
                ('pinned', models.BooleanField(blank=True, default=False)),
                ('classroom', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='classRoom.classroom')),
            ],
        ),
    ]
