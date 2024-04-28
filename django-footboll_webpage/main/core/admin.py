from django.contrib import admin
from .models import *

@admin.register(Groups)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('group',)
    readonly_fields = ('players',)

    def players(self, obj):
        return "\n".join([str(p) for p in obj.player.all()])

    players.short_description = 'Players'

    def get_form(self, request, obj=None, **kwargs):
        self.exclude = ("player",)
        return super().get_form(request, obj, **kwargs)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        self.inlines = [PlayerInline]
        return super().change_view(request, object_id, form_url=form_url, extra_context=extra_context)

class PlayerInline(admin.TabularInline):
    model = Player.group.through
    extra = 1
    
@admin.register(Player)
class PlayerAdmin (admin.ModelAdmin):
    pass
@admin.register(Booking_Type)
class Booking_TypeAdmin(admin.ModelAdmin):
    pass
@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    pass
@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    pass
@admin.register(PlayerBooking)
class PlayerBookingAdmin(admin.ModelAdmin):
    pass
@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    pass
@admin.register(Coach)
class CoachAdmin(admin.ModelAdmin):
    pass

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass

@admin.register(Camp_register)
class Camp_registerAdmin(admin.ModelAdmin):
    pass
@admin.register(Camp)
class CampAdmin(admin.ModelAdmin):
    pass
@admin.register(Cups)
class CupsAdmin(admin.ModelAdmin):
    pass
@admin.register(Cup_register)
class Cup_registerAdmin(admin.ModelAdmin):
    pass
@admin.register(Prov_traning)
class Prov_traningAdmin(admin.ModelAdmin):
    pass
@admin.register(Prov_traning_register)
class Prov_traning_registerAdmin(admin.ModelAdmin):
    pass
@admin.register(Pt_traning)
class Pt_traningAdmin(admin.ModelAdmin):
    pass
@admin.register(Group_traning)
class Group_traningAdmin(admin.ModelAdmin):
    pass