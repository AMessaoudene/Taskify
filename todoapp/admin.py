from django.contrib import admin
from django.contrib.auth.models import User
from .models import todo, UserProfile, Contact

admin.site.register(todo)
admin.site.register(Contact)

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'date_of_birth', 'get_username', 'get_email')

    def get_username(self, obj):
        return obj.user.username

    get_username.short_description = 'Username'

    def get_email(self, obj):
        return obj.user.email

    get_email.short_description = 'Email'

    # def get_age(self, obj):
    #     if obj.date_of_birth:
    #         import datetime
    #         today = datetime.date.today()
    #         age = today.year - obj.date_of_birth.year - ((today.month, today.day) < (obj.date_of_birth.month, obj.date_of_birth.day))
    #         return age
    #     return None

    # get_age.short_description = 'Age'

admin.site.register(UserProfile, UserProfileAdmin)

