from django.urls import path
from . import views

app_name = "category"

urlpatterns = [
    path('', views.show_category, name='show_category'),
    path('make_category', views.make_category, name='make_category'),
    path('mod_category/<id>', views.mod_category, name='mod_category'),
    path('del_category/<id>', views.del_category, name='del_category'),
]
