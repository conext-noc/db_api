# Generated by Django 3.2.18 on 2023-08-02 18:24

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("db_api", "0006_ports"),
    ]

    operations = [
        migrations.CreateModel(
            name="OltPasswords",
            fields=[
                (
                    "cred_id",
                    models.AutoField(primary_key=True, serialize=False, unique=True),
                ),
                ("user_name", models.TextField(default="-")),
                ("password", models.TextField(default="-")),
            ],
        ),
    ]