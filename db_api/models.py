from email.policy import default
from django.db import models


# Create your models here.
class User(models.Model):
    id = models.AutoField(primary_key=True)
    email = models.TextField(unique=True)
    password = models.TextField()
    user_type = models.TextField()

    def __str__(self):
        return self.email

    def to_object(self):
        return {
            "id": self.id,
            "email": self.email,
            "passwd": self.password,
            "user_type": self.user_type,
        }


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
    sn = models.TextField(default="48575443--------", unique=True)
    device = models.TextField(default="EG145V5")
    plan_name = models.ForeignKey(
        "Plans", on_delete=models.CASCADE, to_field="plan_name", db_column="plan_name"
    )
    spid = models.IntegerField(default=1)

    def to_object(self):
        return {
            "contract": self.contract,
            "frame": self.frame,
            "slot": self.slot,
            "port": self.port,
            "onu_id": self.onu_id,
            "olt": self.olt,
            "fsp": self.fsp,
            "fspi": self.fspi,
            "name_1": self.name_1,
            "name_2": self.name_2,
            "status": self.status,
            "state": self.state,
            "sn": self.sn,
            "device": self.device,
            "plan_name": self.plan_name,
            "spid": self.spid,
        }


class Plans(models.Model):
    plan_name = models.TextField(primary_key=True, unique=True)
    plan_idx = models.IntegerField(default=210)
    srv_profile = models.IntegerField(default=210)
    line_profile = models.IntegerField(default=3)
    gem_port = models.IntegerField(default=21)
    vlan = models.IntegerField(default=3100)
    provider = models.TextField(default="INTER")

    def to_object(self):
        return {
            "plan_name": self.plan_name,
            "plan_idx": self.plan_idx,
            "srv_profile": self.srv_profile,
            "line_profile": self.line_profile,
            "gem_port": self.gem_port,
            "vlan": self.vlan,
            "provider": self.provider,
        }


class Ports(models.Model):
    port_id = models.AutoField(primary_key=True, unique=True)
    frame = models.IntegerField(default=0)
    slot = models.IntegerField(default=1)
    port = models.IntegerField(default=0)
    olt = models.IntegerField(default=1)
    fspo = models.TextField(default="0/1/0-1", unique=True)
    is_open = models.BooleanField(default=False)
    oid = models.TextField(default="")

    def to_object(self):
        return {
            "port_id": self.port_id,
            "frame": self.frame,
            "slot": self.slot,
            "port": self.port,
            "olt": self.olt,
            "fspo": self.fspo,
            "is_open": self.is_open,
            "oid": self.oid
        }


class Alarms(models.Model):
    alarm_id = models.AutoField(primary_key=True, unique=True)
    contract = models.ForeignKey(
        "Clients", on_delete=models.CASCADE, to_field="contract", db_column="contract"
    )
    last_down_time = models.TextField(default="-")
    last_down_date = models.TextField(default="-")
    last_down_cause = models.TextField(default="-")

    def to_object(self):
        return {
            "alarm_id": self.alarm_id,
            "contract": self.contract.to_object()["contract"],
            "last_down_time": self.last_down_time,
            "last_down_date": self.last_down_date,
            "last_down_cause": self.last_down_cause,
        }


class OltPasswords(models.Model):
    cred_id = models.AutoField(primary_key=True, unique=True)
    user_name = models.TextField(default="-")
    password = models.TextField(default="-")

    def to_object(self):
        return {
            "cred_id": self.cred_id,
            "user_name": self.user_name,
            "password": self.password,
        }

class ACLRules(models.Model):
    rule_id = models.AutoField(primary_key=True, unique=True)
    name = models.TextField(default="-")
    rtr_acl_name = models.TextField(default="-")
    olt_acl_name = models.TextField(default="-")
    rtr_rule_id = models.IntegerField(default=1)
    olt_rule_id = models.IntegerField(default=1)
    ip_addr = models.TextField(default="-")
    
    def to_dict(self):
        return {
            "rule_id":self.rule_id,
            "name":self.name,
            "rtr_acl_name":self.rtr_acl_name,
            "olt_acl_name":self.olt_acl_name,
            "rtr_rule_id":self.rtr_rule_id,
            "olt_rule_id":self.olt_rule_id,
            "ip_addr":self.ip_addr,
        }
class Oids_ports(models.Model):
    oid_port = models.TextField(primary_key=True, unique=True)
    frame = models.IntegerField(default=0)
    slot = models.IntegerField(default=1)
    port = models.IntegerField(default=0)
    fsp = models.TextField(default="0/0/0")
    def to_dict(self):
        return {
            "oid_port":self.oid_port,
            "frame":self.frame,
            "slot":self.slot,
            "port":self.port,
            "fsp":self.fsp,
        }
class Oids(models.Model):
    oid = models.TextField(default="null")
    definition = models.TextField(primary_key=True, unique=True)
    def to_dict(self):
        return {
            "oid":self.oid,
            "definition":self.definition,
        }

class SnmpPasswords(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    community = models.TextField(default="-")
    password = models.TextField(default="-")

    def to_object(self):
        return {
            "id": self.cred_id,
            "community": self.community_username,
            "password": self.community_password,
        }