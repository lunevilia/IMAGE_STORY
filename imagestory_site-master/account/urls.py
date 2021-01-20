from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = "account"

urlpatterns = [
    path('login', views.login, name='login'),
    path('logout', auth_views.LogoutView.as_view(), name='logout'),
    path('signup', views.signup, name='signup'),

    #비밀번호 변경
    path('mod_password', views.mod_password, name='mod_password'),

    #아이디삭제
    path('del_user', views.del_user, name='del_user'),

    #회원정보 수정 requried login 추가
    path('profile', views.profile, name='profile'),

    #중복확인
    path('ajax/<value>/<region>', views.ajax, name='ajax'),

    #알람 글 보이기
    path('notice_ajax', views.notice_ajax, name='notice_ajax'),

    #알림확인
    path('alert_board', views.alert_board, name='alert_board'),
    
    #알림삭제
    path('del_alert_board/<alert_id>', views.del_alert_board, name='del_alert_board'),

    #북마크
    path('bookmark_board', views.bookmark_board, name='bookmark_board'),

    #내가 쓴글 보기
    path('my_board', views.my_board, name='my_board'),

    #권한 추가
    path('auth_ajax/<value>/<region>/<id>', views.auth_ajax, name='auth_ajax'),

    #권한 제거
    path('auth_del_ajax/<value>/<region>/<id>', views.auth_del_ajax, name='auth_del_ajax'),

    #권한 게시글
    path('auth_board', views.auth_board, name='auth_board'),

    
]
