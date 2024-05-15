# Generated by Django 3.2.15 on 2024-05-13 00:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('airline', '0007_airport_country'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='flights',
            field=models.ManyToManyField(blank=True, related_name='passengers', to='airline.Flight'),
        ),
    ]
