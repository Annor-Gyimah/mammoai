# Generated by Django 4.2.7 on 2024-07-28 22:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_dashboard', '0007_results_heatmap_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='results',
            name='entry_count',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
