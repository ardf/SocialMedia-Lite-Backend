from django.contrib import admin
from .models import User
# Register your models here.
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'name', 'id')
    readonly_fields = ('id',)

# admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
