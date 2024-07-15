# JJJs/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Booking, Hostel, Area
from .forms import CustomUserCreationForm, BookingForm

# Admin configuration for custom User model
class UserAdmin(BaseUserAdmin):
    add_form = CustomUserCreationForm
    model = User
    list_display = ('email', 'first_name', 'last_name', 'phone_number', 'is_admin')
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'phone_number')}),
        ('Permissions', {'fields': ('is_admin',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'phone_number', 'password1', 'password2'),
        }),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()



    class BookingForm():
        add_form = BookingForm
        model = Booking



admin.site.register(User, UserAdmin)
admin.site.register(Booking)
admin.site.register(Hostel)
admin.site.register(Area)
