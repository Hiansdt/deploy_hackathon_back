# Generated by Django 4.2.3 on 2023-07-21 14:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_coment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='coment',
            name='livro',
        ),
        migrations.AddField(
            model_name='coment',
            name='stars',
            field=models.IntegerField(default=0),
        ),
    ]
