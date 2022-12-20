from django.contrib import admin
from app1 import models

class Site_User_Admin(admin.ModelAdmin):
    list_display = ['name']

class Orders_Admin(admin.ModelAdmin):
    list_display = ['name']

admin.site.register(models.Orders)
admin.site.register(models.Feedback)
admin.site.register(models.PermanentOrders)
#admin.site.register(models.Temp_Food)
admin.site.register(models.Site_User,Site_User_Admin)


admin.site.site_header = 'My administration'
admin.site.site_index = 'My index'

