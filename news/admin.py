from django.contrib import admin
from .models import NewsPost, Press

# Register your models here.
admin.site.register(NewsPost)

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name', )}

admin.site.register(Press, CategoryAdmin)
