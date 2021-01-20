from django.urls import path
from . import views


app_name = "board"

urlpatterns = [
    path('<board_name>', views.main, name='main'),
    path('root_write/<board_name>', views.root_write, name='root_write'),
    path('cur_modify/<board_name>/<id>', views.root_modify, name='root_modify'),
    path('root_delete/<board_name>/<id>', views.root_delete, name='root_delete'),
    path('write/<board_name>/<id>', views.write, name='write'),
    path('detail/<board_name>/<id>', views.detail, name='detail'),
    path('mod_detail/<board_name>/<id>', views.mod_detail, name='mod_detail'),
    # path('del_detail/<board_name>/<id>/', views.del_detail, name='del_detail'),
    #댓글 생성
    path('comment/<board_name>/<int:id>', views.comment_write, name='comment_write'),
    path('recomment/<board_name>/<int:id>/<int:comment_id>', views.recomment_write, name='recomment_write'),
    #댓글 삭제
    path('comment_del/<board_name>/<int:id>/<int:comment_id>', views.comment_del, name='comment_del'),

    #북마크
    path('ajax_board_bookmark/<int:id>', views.ajax_board_bookmark, name='ajax_board_bookmark'),
]
