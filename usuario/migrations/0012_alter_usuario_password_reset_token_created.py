# Generated by Django 4.2.4 on 2023-08-18 14:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuario', '0011_alter_usuario_password_reset_token_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='password_reset_token_created',
            field=models.DateTimeField(blank=True, default=None, null=True),
        ),
    ]
