from django.contrib import admin
from registry.models import *

admin.site.register(User)
admin.site.register(Patients)
admin.site.register(Doctor)
admin.site.register(Schedule)
admin.site.register(Reception)

