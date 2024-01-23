from django.contrib import admin
from unfold.admin import ModelAdmin
from api.models.client import Client
from api.interface.guard_admin import GuardAdmin

@admin.register(Client)
class ClientAdmin(ModelAdmin, GuardAdmin):
    list_display = ['name', 'siren', 'phone_number', 'email'] 

