# Generated by Django 4.1.1 on 2024-04-22 16:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_consejo_titulo'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='consejo',
            options={'verbose_name': 'consejo'},
        ),
        migrations.AlterField(
            model_name='consejo',
            name='texto',
            field=models.TextField(max_length=150),
        ),
        migrations.AlterField(
            model_name='consejo',
            name='titulo',
            field=models.TextField(default='Sin titulo', max_length=50),
        ),
    ]
