from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from accounts.models import User
from event.models import Event


class EventInline(admin.TabularInline):
    model = Event
    exclude = ['description']


class UserAdmin(BaseUserAdmin):
    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'first_name', 'last_name', 'date_of_birth', 'is_admin')
    list_filter = ('is_admin',)
    inlines = [EventInline]
    fieldsets = (
        ('User', {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'cell_phone', 'date_of_birth',)}),
        ('Permissions', {'fields': ('is_admin',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email',
                'password1',
                'password2',
                'first_name',
                'last_name',
                'date_of_birth',
                'cell_phone'
            )}
        ),
    )

    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()


admin.site.register(User, UserAdmin)
admin.site.unregister(Group)


