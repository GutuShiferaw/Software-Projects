# Generated by Django 4.1.7 on 2023-03-22 22:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GridOverview', '0003_windspeed'),
    ]

    operations = [
        migrations.CreateModel(
            name='totalPower',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('power', models.IntegerField()),
            ],
        ),
    ]
