# Generated by Django 3.2.22 on 2025-02-05 19:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20250127_2233'),
    ]

    operations = [
        migrations.CreateModel(
            name='dictionary',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
    ]
