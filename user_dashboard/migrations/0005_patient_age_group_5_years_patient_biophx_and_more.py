# Generated by Django 4.2.7 on 2024-07-28 15:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_dashboard', '0004_remove_patient_breast_health_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='patient',
            name='age_group_5_years',
            field=models.PositiveIntegerField(blank=True, choices=[(1, 'Age 18-29'), (2, 'Age 30-34'), (3, 'Age 35-39'), (4, 'Age 40-44'), (5, 'Age 45-49'), (6, 'Age 50-54'), (7, 'Age 55-59'), (8, 'Age 60-64'), (9, 'Age 65-69'), (10, 'Age 70-74'), (11, 'Age 75-79'), (12, 'Age 80-84'), (13, 'Age >85')], null=True),
        ),
        migrations.AddField(
            model_name='patient',
            name='biophx',
            field=models.PositiveIntegerField(blank=True, choices=[(0, 'No'), (1, 'Yes'), (9, 'Unknown')], null=True),
        ),
        migrations.AddField(
            model_name='patient',
            name='bmi_group',
            field=models.PositiveIntegerField(blank=True, choices=[(1, '10-24.99'), (2, '25-29.99'), (3, '30-34.99'), (4, '35 or more'), (9, 'Unknown')], null=True),
        ),
        migrations.AddField(
            model_name='patient',
            name='menopaus',
            field=models.PositiveIntegerField(blank=True, choices=[(1, 'Pre- or peri-menopausal'), (2, 'Post-menopausal'), (3, 'Surgical menopause'), (9, 'Unknown')], null=True),
        ),
    ]
