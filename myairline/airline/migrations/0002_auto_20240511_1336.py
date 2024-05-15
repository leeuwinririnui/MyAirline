# Generated by Django 3.2.15 on 2024-05-11 01:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('airline', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='flight',
            old_name='number',
            new_name='flight_number',
        ),
        migrations.AddField(
            model_name='flight',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='airport',
            name='location',
            field=models.CharField(max_length=64),
        ),
        migrations.AlterField(
            model_name='airport',
            name='name',
            field=models.CharField(default='Default Airport Name', max_length=64),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='first_name',
            field=models.CharField(max_length=64),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='last_name',
            field=models.CharField(max_length=64),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='username',
            field=models.CharField(default='default_username', max_length=64, unique=True),
        ),
        migrations.RemoveField(
            model_name='flight',
            name='plane',
        ),
        migrations.AddField(
            model_name='flight',
            name='plane',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='plane_flight', to='airline.plane'),
        ),
        migrations.AlterField(
            model_name='plane',
            name='model',
            field=models.CharField(max_length=64),
        ),
        migrations.AlterField(
            model_name='plane',
            name='name',
            field=models.CharField(max_length=64, primary_key=True, serialize=False),
        ),
    ]
