from django.db import models


# Create your models here.
class User(models.Model):
    id = models.AutoField(primary_key=True)
    email = models.TextField(unique=True)
    password = models.TextField()
    user_type = models.TextField()

    def __str__(self):
        return self.email


class Client(models.Model):
    contract = models.TextField(primary_key=True, unique=True)
    frame = models.SmallIntegerField()
    slot = models.SmallIntegerField()
    port = models.SmallIntegerField()
    onu_id = models.SmallIntegerField()
    fsp = models.TextField(default="0/1/0")
    name_1 = models.TextField()
    name_2 = models.TextField()
    status = models.TextField(default="online")
    state = models.TextField(default="active")
    last_down_cause = models.TextField(default="dying-gasp")
    last_down_time = models.TextField(default="-")
    last_down_date = models.TextField(default="-")
    sn = models.TextField(default="-")
    device = models.TextField(default="EG145V5")
    plan = models.TextField(default="-")
    vlan = models.TextField(default="-")
