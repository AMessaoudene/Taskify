# Generated by Django 4.2.6 on 2023-12-01 16:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todoapp', '0009_todo_priority'),
    ]

    operations = [
        migrations.AlterField(
            model_name='todo',
            name='priority',
            field=models.CharField(choices=[('high', 'High Priority'), ('medium', 'Medium Priority'), ('low', 'Low Priority')], max_length=15),
        ),
    ]
