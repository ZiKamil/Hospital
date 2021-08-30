from django import template
from registry.models import *

register = template.Library()


@register.filter
def get_doctor(shedule_id):
    for shed in Schedule.objects.filter(id=shedule_id):
        return shed.id_doctor

@register.filter
def get_room_number(shedule_id):
    for shed in Schedule.objects.filter(id=shedule_id):
        return shed.id_doctor.get_room_number()