from django.contrib import admin

# Register your models here
from Main.models import *


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ["user","bio","gender","picture"]

@admin.register(Meeting)
class MeetingAdmin(admin.ModelAdmin):
    list_display = ["teacher", "capacity", "start", "end", "date"]

