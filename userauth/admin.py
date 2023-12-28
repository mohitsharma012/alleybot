from django.contrib import admin
from userauth.models import users, users_messages

# Register your models here
admin.site.register(users)
admin.site.register(users_messages)
