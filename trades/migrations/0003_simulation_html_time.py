# Generated by Django 5.1.2 on 2024-10-28 02:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trades', '0002_simulation_delete_simulationresult'),
    ]

    operations = [
        migrations.AddField(
            model_name='simulation',
            name='html_time',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
