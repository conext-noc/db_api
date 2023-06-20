# Generated by Django 3.2.18 on 2023-06-14 22:02

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("db_api", "0002_auto_20230614_2111"),
    ]

    operations = [
        migrations.AddField(
            model_name="plans",
            name="provider",
            field=models.TextField(default="INTER"),
        ),
        migrations.AddField(
            model_name="plans",
            name="vlan",
            field=models.IntegerField(default=3100),
        ),
        migrations.AlterField(
            model_name="plans",
            name="gem_port",
            field=models.IntegerField(default=21),
        ),
        migrations.AlterField(
            model_name="plans",
            name="line_profile",
            field=models.IntegerField(default=3),
        ),
        migrations.AlterField(
            model_name="plans",
            name="plan_idx",
            field=models.IntegerField(default=210),
        ),
        migrations.AlterField(
            model_name="plans",
            name="srv_profile",
            field=models.IntegerField(default=210),
        ),
    ]
