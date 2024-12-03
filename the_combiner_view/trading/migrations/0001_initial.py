# Generated by Django 5.1.3 on 2024-12-03 14:31

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AutomationRule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('exchanges', models.JSONField()),
                ('market_type', models.CharField(choices=[('spot', 'Spot'), ('future', 'Future'), ('both', 'Both')], max_length=10)),
                ('account', models.CharField(max_length=255)),
                ('amount_usdt', models.FloatField()),
                ('status', models.CharField(choices=[('enabled', 'Enabled'), ('disabled', 'Disabled')], default='enabled', max_length=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
