from django.db import models


# Create your models here.
class User(models.Model):
    id = models.AutoField(primary_key=True)
    email = models.TextField(unique=True)
    password = models.TextField()
    user_type = models.TextField()

    def __str__(self):
        return self.email


class Clients(models.Model):
    contract = models.TextField(primary_key=True, unique=True)
    frame = models.IntegerField(default=0)
    slot = models.IntegerField(default=1)
    port = models.IntegerField(default=0)
    onu_id = models.IntegerField(default=0)
    olt = models.IntegerField(default=1)
    fsp = models.TextField(default="0/1/0")
    fspi = models.TextField(default="0/1/0/0")
    name_1 = models.TextField()
    name_2 = models.TextField()
    status = models.TextField(default="online")
    state = models.TextField(default="active")
    sn = models.TextField(default="48575443--------")
    device = models.TextField(default="EG145V5")
    plan_name = models.ForeignKey(
        "Plans", on_delete=models.CASCADE, to_field="plan_name", db_column="plan_name"
    )
    spid = models.IntegerField(default=1)


class Plans(models.Model):
    plan_name = models.TextField(primary_key=True, unique=True)
    plan_idx = models.IntegerField(default=210)
    srv_profile = models.IntegerField(default=210)
    line_profile = models.IntegerField(default=3)
    gem_port = models.IntegerField(default=21)
    vlan = models.IntegerField(default=3100)
    provider = models.TextField(default="INTER")
