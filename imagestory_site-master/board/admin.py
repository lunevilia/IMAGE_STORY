from django.contrib import admin
from .models import *

class BoardAdmin(admin.ModelAdmin):
    list_display = ('title', 'author')

admin.site.register(Board, BoardAdmin)
admin.site.register(Commentalertcontent)
admin.site.register(Comment)

