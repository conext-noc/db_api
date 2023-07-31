# Generated by Django 3.2.18 on 2023-07-31 16:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("db_api", "0003_auto_20230614_2202"),
    ]

    operations = [
        migrations.AlterField(
            model_name="clients",
            name="sn",
            field=models.TextField(default="48575443--------", unique=True),
        ),
        migrations.CreateModel(
            name="Alarms",
            fields=[
                ("alarm_id", models.AutoField(primary_key=True, serialize=False)),
                ("last_down_time", models.TextField(default="-")),
                ("last_down_date", models.TextField(default="-")),
                ("last_down_cause", models.TextField(default="-")),
                (
                    "contract",
                    models.ForeignKey(
                        db_column="contract",
                        on_delete=django.db.models.deletion.CASCADE,
                        to="db_api.clients",
                    ),
                ),
            ],
        ),
    ]
