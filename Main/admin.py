from django.contrib import admin

# Register your models here
from Main.models import Person


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ["user","bio","gender","picture"]