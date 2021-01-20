from django.urls import path
from . import views

app_name = "tutorial"

urlpatterns = [
    path('', views.tutorial_list, name='tutorial_list'),
    path('board_info', views.board_info, name='board_info'),
    path('board_write', views.board_write, name='board_write'),
    path('board_modify', views.board_modify, name='board_modify'),
    path('board_delete', views.board_delete, name='board_delete'),
    path('area_write', views.area_write, name='area_write'),
    path('area_layer', views.area_layer, name='area_layer'),
    path('area_modify', views.area_modify, name='area_modify'),
    path('area_delete', views.area_delete, name='area_delete'),
    path('alert_info', views.alert_info, name='alert_info'),
    path('mypage', views.mypage, name='mypage'),
    path('auth_info', views.auth_info, name='auth_info'),
]
