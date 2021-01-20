from django.shortcuts import render, redirect, get_object_or_404
from .forms import SignupForm, LoginForm, ModifyForm
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib import messages

from .models import Profile, Commentalert
from board.models import Commentalertcontent, Board

from django.contrib.auth.decorators import login_required
from django.contrib import messages

import json
from django.http import HttpResponse, HttpResponseRedirect
from django.core import serializers

from django.urls import reverse

from django.db.models import Q

from django.core.paginator import Paginator

from django.core.mail import EmailMessage

# Create your views here.
def login(request):
    if request.method == "POST":
        next_page = request.POST.get('next','/')
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return HttpResponseRedirect(next_page)
        else:
            messages.info(request, "아이디 혹은 비밀번호에 문제가 있습니다!")
            return redirect(request.path+"?next="+next_page)
    else:
        form = LoginForm()
        return render(request, 'registration/login.html', {'form': form, })

def signup(request):
    if request.method == "POST":
        signupform = SignupForm(request.POST, request.FILES)

        next_page = request.POST.get('next','/')
        if request.POST["password1"]==request.POST["password2"]:
            if signupform.is_valid():
                # send_message_title = "ImageStory에 가입을 환영합니다!"
                # user_email = signupform.cleaned_data['email']
                # send_message_body = "ImageStory 회원가입을 진심으로 환영합니다!!✨✨🎉🎉\n이미지스토리에 모르는 것이 있으시면 https://imagestory.pythonanywhere.com/tutorial/ 에 접속해서 사용법을 확인 해보세요~!"

                # email_send = EmailMessage(send_message_title, send_message_body, to=[user_email])

                # try:
                #     email_send.send()
                # except:
                #     messages.info(request, '유효하지 않은 이메일입니다! 이메일을 확인 해주세요!')
                #     return render(request, 'registration/signup.html', {'signupform':signupform, 'next_page':next_page, 'checked':False})

                user = User.objects.create_user(
                    username=request.POST.get("username_id"),
                    password=request.POST.get("password1")
                )

                waitprofile = signupform.save(commit=False)
                waitprofile.user = user
                waitprofile.save()
                auth.login(request, user)
                return HttpResponseRedirect(next_page)
            else:
                messages.info(request, '이메일을 제대로 작성 해주세요!')
                return render(request, 'registration/signup.html', {'signupform':signupform, 'next_page':next_page, 'checked':False})
        else:
            messages.info(request, "재확인 비밀번호가 틀렸습니다! 재작성 해주세요!")
            return render(request, 'registration/signup.html', {'signupform':signupform, 'next_page':next_page, 'checked':False})
    else:
        signupform = SignupForm()
        loginform = LoginForm()
        return render(request, 'registration/signup.html', {'signupform':signupform, 'checked':True})

#비밀번호 변경
@login_required(login_url='/')
def mod_password(request):
    if request.method == "POST":
        current_password = request.POST.get("b_password")
        new_password = request.POST.get("n_password")
        try:
            user = User.objects.get(username=request.user)
            user.set_password(new_password)
            user.save()
        except:
            messages.info(request, '오류가 일어났습니다!')

        return redirect('/account/profile')


#회원삭제
@login_required(login_url='/')
def del_user(request):
    user = User.objects.get(username=request.user)
    user.delete()
    return redirect('/')

#회원정보 보기 및 수정하기
@login_required(login_url='/')
def profile(request):
    if request.session.get('page', ''):
        del request.session['page']

    profile_information = Profile.objects.get(user__username=request.user)
    #수정하기
    if request.method == "POST":
        profile_form = ModifyForm(request.POST, request.FILES, instance=profile_information)
        if profile_form.is_valid():
            profile_form.save()
            return redirect('/account/profile')
        else:
            messages.info(request, '비정상적인 수정 방법입니다!\n다시 수정해주세요!')
            return redirect('/account/profile')
    else:
        profile_form = ModifyForm(instance=profile_information)
    return render(request, "profile.html", {"profile_form":profile_form})


#중복확인하는 ajax용 함수 만들기 (닉네임, 아이디, 이메일)
def ajax(request, value, region):
    if request.is_ajax():
        if region == "username":
            check = User.objects.filter(username=value).exists()
        elif region == "nickname":
            check = Profile.objects.filter(nickname=value).exists()
        elif region == "email":
            check = Profile.objects.filter(email=value).exists()
        else:
            check = False

        return HttpResponse(json.dumps({'check':check}), 'application/json')

#알람이 되는 ajax!
@login_required(login_url='/')
def notice_ajax(request):
    if request.is_ajax():
        getProfile = Profile.objects.get(user__username=request.user)
        comment_a = Commentalert.objects.get(profile=getProfile)

        #가져올 개수
        how_many_filter = comment_a.recent - getProfile.alert

        getProfile.alert = comment_a.recent
        getProfile.save()

        if(how_many_filter):
            show_alert = Commentalertcontent.objects.filter(profile_name=getProfile, view=True)[:5]
            qs_json = serializers.serialize('json', show_alert, use_natural_foreign_keys=True) #use_natural_foreigin_keys를 이용해 pk가 아닌 특정 내용을 가져오도록 설정 Commentalertcontent 테이블에 def로 설정해야됨!
            qs_json = json.loads(qs_json)
        else:
            show_alert = Commentalertcontent.objects.filter(profile_name=getProfile, view=True)[:5]
            qs_json = serializers.serialize('json', show_alert, use_natural_foreign_keys=True)
            qs_json = json.loads(qs_json)

        return HttpResponse(json.dumps({'show_alert':qs_json}), 'application/json')

@login_required(login_url='/')
def alert_board(request):
    request.session['page'] = 'alert_board'
    return render(request, "alert.html", )

#알림내용삭제
@login_required(login_url='/')
def del_alert_board(request, alert_id):
    if alert_id == "all":
        del_alert = Commentalertcontent.objects.filter(profile_name=request.user.profile)
        del_alert.delete()
    else:
        del_alert = get_object_or_404(Commentalertcontent, profile_name=request.user.profile, id=alert_id)
        del_alert.delete()

    return redirect("/account/alert_board/")

#북마크
@login_required(login_url='/')
def bookmark_board(request):
    request.session['page'] = 'bookmark'
    return render(request, "bookmark_page.html", )

#내가 쓴글
@login_required(login_url='/')
def my_board(request):

    #검색 기능 추가
    search = request.GET.get("search", "")

    #제목, 내용, 글쓴이 (콤보상자 이용)
    search_info = request.GET.get("search_option", "")

    # root 게시글만 가져오기
    myboards = request.user.profile.board_set.filter(post__isnull=True)

    if request.GET.get('page') or search:
        if search:
            request.session['search'] = search
            request.session['search_info'] = search_info
    else:
        if request.session.get('search',''):
            del request.session['search']
            del request.session['search_info']

    session_search = request.session.get('search','')

    if session_search:
        #제목으로 찾기
        if request.session.get('search_info','') == "title":
            myboards = myboards.filter(title__contains=session_search).order_by("-created_at")
        #내용으로 찾기
        elif request.session.get('search_info','') == "info":
            myboards = myboards.filter(information__contains=session_search).order_by("-created_at")
        #제목+내용으로 찾기
        else:
            myboards = myboards.filter(Q(title__contains=session_search) | Q(information__contains=session_search)).order_by("-created_at")
    else:
        myboards = myboards.order_by("-created_at")

    #페이지네이션 만들기
    myboards = Paginator(myboards, 10)
    page = request.GET.get('page')

    #페이지 보이게 하는 숫자 구간
    page_numbers_range = 5

    #최대 녀석이 있을 경우 최대 까지만 보이도록 하기 위해서!
    max_index = len(myboards.page_range)

    #페이지가 0일 경우 1로 변경 current_page에 넣기
    current_page = int(page) if page else 1
    start_index = int((current_page - 1) / page_numbers_range) * page_numbers_range
    end_index = start_index + page_numbers_range

    if end_index >= max_index:
        end_index = max_index

    page_range = myboards.page_range[start_index:end_index]

    myboards = myboards.get_page(page) #페이지네이션 만들기

    request.session['page'] = 'my_board'
    return render(request, "my_board.html", {"page_range":page_range, "myboards":myboards})


#권한 중복확인하는 ajax용 함수 만들기 (닉네임, 아이디, 이메일)
@login_required(login_url='/')
def auth_ajax(request, value, region, id):
    if request.is_ajax():
        #권한 없는자가 다른 게시글에 권한 추가 못하도록 하기
        if Board.objects.get(id=int(id)).author == request.user.profile:
            if region == "nickname":
                check = Profile.objects.filter(nickname=value).exists()
                if check:
                    add_user = Profile.objects.get(nickname=value)
                    Board.objects.get(id=int(id)).group.add(add_user)
            else:
                check = False
        else:
            check = False

        return HttpResponse(json.dumps({'check':check}), 'application/json')

#권한 제거
@login_required(login_url='/')
def auth_del_ajax(request, value, region, id):
    if request.is_ajax():
        #권한 없는자가 다른 게시글에 권한 추가 못하도록 하기
        if Board.objects.get(id=int(id)).author == request.user.profile:
            if region == "nickname":
                check = Profile.objects.filter(nickname=value).exists()
                if check:
                    check = Profile.objects.get(nickname=value) in Board.objects.get(id=int(id)).group.all()
                if check:
                    add_user = Profile.objects.get(nickname=value)
                    Board.objects.get(id=int(id)).group.remove(add_user)
            else:
                check = False
        else:
            check = False

        return HttpResponse(json.dumps({'check':check}), 'application/json')

#내가 쓴글
@login_required(login_url='/')
def auth_board(request):
    authboards = Board.objects.filter(group__in=[request.user.profile])
    request.session['page'] = 'auth_board'
    return render(request, "auth_board.html", {"authboards":authboards})