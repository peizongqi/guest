from django.contrib import admin
from sign.models import Event, Guest

# Register your models here.
#  通知admin为这些模块提供统一界面
class EventAdmin(admin.ModelAdmin):
    list_display = ['name', 'status', 'startTime', 'id']
    search_fields = ['name']              #搜索栏
    list_filter = ['status']              #过滤器

class GuestAdmin(admin.ModelAdmin):
    list_display = ['realName', 'phone', 'email', 'sign', 'createTime', 'event']
    search_fields = ['realName', 'phone']          #搜索栏
    list_filter = ['sign']                #过滤器

admin.site.register(Event, EventAdmin)
admin.site.register(Guest, GuestAdmin)
