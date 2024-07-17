from django.contrib import admin

from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('pk', 'phone', 'my_invite_code', 'another_invite_code', )
    list_filter = ('another_invite_code', )
    search_fields = ('phone', )
