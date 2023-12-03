from db_api.models import ACLRules
from db_api.ms_health_status import get_ms_ips


# CREATE
def add_rules(rules):
    for rule in rules:
        rule_db = ACLRules(**rule)
        rule_db.save()
    return {"message": "Success!", "error": False}


# READ (ALL)
def get_rules():
    rules = get_ms_ips()["data"]
    update_rules_ip(rules)
    alarms_db = ACLRules.objects.all()
    alarms = [alarm.to_dict() for alarm in alarms_db]
    return {"message": "Success!", "error": False, "data": alarms}


# READ (SINGLE)
def get_rule(name):
    rule = ACLRules.objects.filter(name=name)[0]
    return {"message": "Success!", "error": False, "data": rule.to_dict()}


# UPDATE
def update_rules_ip(rules):
    print(rules)
    for rule in rules:
        rule_db = ACLRules.objects.filter(name=rule['name'])[0]
        print(rule_db.to_dict())
        rule_db.ip_addr = rule['new_ip_addr']
        rule_db.save()
    return {"message": "Success!", "error": False}
