# Generated by Django 4.1.1 on 2024-03-28 19:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0005_alter_alerta_id_historial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Consejos',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('categoria', models.CharField(max_length=100)),
                ('consejo', models.TextField()),
            ],
        ),
    ]