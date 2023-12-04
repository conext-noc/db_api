from django.contrib import admin
from .models import Clients, User, Plans, OltPasswords, Ports, Alarms

# Register your models here.
admin.site.register(Clients)
admin.site.register(User)
admin.site.register(Plans)
admin.site.register(OltPasswords)
admin.site.register(Ports)
admin.site.register(Alarms)