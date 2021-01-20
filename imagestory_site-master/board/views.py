from django.shortcuts import render, redirect, get_object_or_404
from .models import Board, Comment, Commentalertcontent, Bookmark
from category.models import Category
from .forms import Boardmodform, Boardmodform_root, CommentTest
from account.models import Profile, Commentalert

import json
from django.http import HttpResponse, HttpResponseRedirect
from django.core import serializers
from django.urls import reverse
from django.db.models import Q

from django.core.paginator import Paginator

# Create your views here.
def main(request, board_name):

    # page 위치를 저장하기 위해서 설정
    if request.session.get('board_name',''):
        # 게시판 바꿧는지 확인 바뀌면 page를 초기화 시키기 위해서
        if request.session.get('board_name','') != board_name:
            request.session['board_name'] = board_name
            # 페이지 session 초기화
            if request.session.get('page',''):
                del request.session['page']
        else:
            if request.GET.get('page'):
                request.session['page'] = request.GET.get('page')
    else:
        request.session['board_name'] = board_name

    categoryname = Category.objects.get(board_name=board_name)

    #검색 기능 추가
    search = request.GET.get("search", "")

    #제목, 내용, 글쓴이 (콤보상자 이용)
    search_info = request.GET.get("search_option", "")

    #페이지 리쿼스트가 있을 경우
    #처음에 search를 하면 search가 남을 것이다 하지만 그다음 page를 누르면 페이지가 있을 것이다
    #결국 어차피 한번 search가 session값에 저장이 된다!
    #게시글 나가기 했을 때도 값이 남아 있어야 하나?? 추후에 생각
    if request.GET.get('page') or search:
        if search:
            request.session['search'] = search
            request.session['search_info'] = search_info
    else:
        if request.session.get('search',''):
            del request.session['search']
            del request.session['search_info']

    # root 게시글만 가져오기 (secure은 안보이게 가져오기 안그러면 page를 10으로 나누는데 비밀이 있을 경우 한 페이지에 아무것도 없을 수 있다)
    all_board = Board.objects.filter(post=None, category__board_name=board_name, secure='public')

    session_search = request.session.get('search','')

    if session_search:
        #글쓴이로 찾기
        if request.session.get('search_info','') == "user":
            all_board = all_board.filter(author__nickname=session_search).order_by("-created_at")
        #제목으로 찾기
        elif request.session.get('search_info','') == "title":
            all_board = all_board.filter(title__contains=session_search).order_by("-created_at")
        #내용으로 찾기
        elif request.session.get('search_info','') == "info":
            all_board = all_board.filter(information__contains=session_search).order_by("-created_at")
        #제목+내용으로 찾기
        else:
            all_board = all_board.filter(Q(title__contains=session_search) | Q(information__contains=session_search)).order_by("-created_at")
    else:
        all_board = all_board.order_by("-created_at")

    #페이지네이션 만들기
    all_board = Paginator(all_board, 10)

    if request.session.get('page',''):
        page = request.session.get('page')
    else:
        page = request.GET.get('page')

    #페이지 보이게 하는 숫자 구간
    page_numbers_range = 5

    #최대 녀석이 있을 경우 최대 까지만 보이도록 하기 위해서!
    max_index = len(all_board.page_range)

    #페이지가 0일 경우 1로 변경 current_page에 넣기
    current_page = int(page) if page else 1
    start_index = int((current_page - 1) / page_numbers_range) * page_numbers_range
    end_index = start_index + page_numbers_range

    if end_index >= max_index:
        end_index = max_index

    page_range = all_board.page_range[start_index:end_index]

    all_board = all_board.get_page(page) #페이지네이션 만들기

    return render(request, "main.html", {"page_range":page_range,"all_board":all_board, "board_name":board_name, "categoryname":categoryname, })

def root_write(request, board_name):
    boardform = Boardmodform_root()
    if request.user.is_authenticated:
        if request.method == 'POST':
            boardform = Boardmodform_root(request.POST, request.FILES)
            if boardform.is_valid():
                waitform = boardform.save(commit=False)
                waitform.category = Category.objects.get(board_name=board_name)
                waitform.author = Profile.objects.get(nickname=request.user.profile.nickname)
                waitform.save()
                return redirect('/board/'+board_name)
        return render(request, "root_write.html", {"board_name":board_name, "boardform":boardform,})
    else:
        return redirect('/board/'+board_name)

def root_modify(request, board_name, id):
    get_board = Board.objects.get(id=id)
    pre_image = get_board.image #이미지가 달라졌는지 확인하기 위해서 달라졌으면 그 이미지안에 있는 글들 전부 삭제

    #루트가 아닐 경우
    if get_board.post:
        boardform = Boardmodform(instance=get_board)
        root_author = get_board.post_root.author
        get_root_board = get_board.post_root
    #루트일 경우
    else:
        boardform = Boardmodform_root(instance=get_board)
        root_author = get_board.author
        get_root_board = get_board

    #권한이 없는 사람이 수정하기를 못 들어오도록 막기 (권한 : 작성자이면서 권한이 있을 경우)
    if request.user.is_authenticated:
        if (get_board.author == request.user.profile and request.user.profile in get_root_board.group.all()) or root_author == request.user.profile or request.user.is_superuser:
            pass
        else:
            return redirect('/')
    else:
        return redirect('/')

    if request.method == 'POST':
        if get_board.author == request.user.profile or root_author == request.user.profile or request.user.is_superuser:
            if get_board.post:
                boardform = Boardmodform(request.POST, request.FILES, instance=get_board)
            else:
                boardform = Boardmodform_root(request.POST, request.FILES, instance=get_board)
            if boardform.is_valid():
                if not boardform.cleaned_data.get("image") == pre_image:
                    if request.POST.get('layer_save') == None:
                        Board.objects.filter(post=get_board).delete() #만약 이미지가 변경 되거나 삭제되면 모든 그것에 관련된 레이어 게시글을 삭제하기 위해서
                boardform.save()
                return redirect('/board/detail/'+get_board.category.board_name+'/'+id)
        else:
            return redirect('/board/detail/'+get_board.category.board_name+'/'+id)

    return render(request, "root_modify.html", {"board_name":get_board.category.board_name,"boardform":boardform, "get_board":get_board,})

def root_delete(request, board_name, id):
    if request.method == 'POST':
        get_board = Board.objects.get(id=id)

        #제거 후 뒤로 돌아가도록 하기 위해서 설정
        # 루트가 아닐 경우
        if get_board.post:
            past_id = get_board.post.id
            root_author = get_board.post_root.author
            get_root_board = get_board.post_root
        else:
        # 루트일 경우
            past_id = False
            root_author = get_board.author
            get_root_board = get_board

        if (get_board.author == request.user.profile and request.user.profile in get_root_board.group.all()) or root_author == request.user.profile or request.user.is_superuser:
            get_board.delete()
            if past_id:
                return redirect('/board/detail/'+get_board.category.board_name+'/'+str(past_id))
            else:
                return redirect('/board/'+get_board.category.board_name)
        else:
            return redirect('/board/detail/'+get_board.category.board_name+'/'+id)


def write(request, board_name, id): #작성자만 작성가능하도록 사용하겠음 일단 추후에 그룹 같은 것 만들어서 그들 끼리 할 수 있도록 설정
    if request.user.is_authenticated:
        if request.method == 'POST':
            qs = Board.objects.get(id=id)

            # 만약 쓰는 위치가 루트가 아닐 경우
            if qs.post_root:
                group_list = qs.post_root.group.all()
                # 권한이 있는 자만 작성 가능
                if request.user.profile in group_list or qs.author == request.user.profile:
                    boardform = Boardmodform(request.POST, request.FILES)
                    if boardform.is_valid():
                        waitform = boardform.save(commit=False)
                        waitform.category = Category.objects.get(board_name=qs.category.board_name)
                        waitform.post = qs
                        if qs.post_root:
                            waitform.post_root = qs.post_root
                        else:
                            waitform.post_root = qs
                        waitform.author = Profile.objects.get(nickname=request.user.profile.nickname)
                        waitform.save()
                        return redirect('/board/detail/'+qs.category.board_name+'/'+id)
                else:
                    return redirect('/board/detail/'+qs.category.board_name+'/'+id)
            # 만약 쓰는 위치가 루트 일 경우
            else:
                group_list = qs.group.all()
                # 권한이 있는 자만 작성 가능
                if request.user.profile in group_list or qs.author == request.user.profile:
                    boardform = Boardmodform(request.POST, request.FILES)
                    if boardform.is_valid():
                        waitform = boardform.save(commit=False)
                        waitform.category = Category.objects.get(board_name=board_name)
                        waitform.post = qs
                        if qs.post_root:
                            waitform.post_root = qs.post_root
                        else:
                            waitform.post_root = qs
                        waitform.author = Profile.objects.get(nickname=request.user.profile.nickname)
                        waitform.save()
                        return redirect('/board/detail/'+board_name+'/'+id)
                else:
                    return redirect('/board/detail/'+board_name+'/'+id)
    else:
        return redirect('/board/detail/'+board_name+'/'+id)

def detail(request, board_name, id):
    get_board = Board.objects.get(id=id)
    root_board = get_board.post

    #댓글 작성
    commentform = CommentTest()

    #댓글 보여주기
    detail_getComment = Comment.objects.filter(main_post=get_board, post__isnull=True)

    #root게시판이 아닐 경우
    if get_board.post_root: #search를 보여주는 조건 만약 작성자가 아닐 경우는 search로 못찾도록 만약 작성자일 경우는 전부다!!
        groups = get_board.post_root.group.all()
        root_author = get_board.post_root.author
        get_root_board = get_board.post_root
        if request.user.is_authenticated: #로그인 했을 경우! 이거 안하면 익명자에게는 profile이라는 필드강 없어서 오류가 남
            if get_board.post_root.author == request.user.profile or request.user.profile in groups: #profile이라는 것으로 작성자인지 아닌지 확인하기 위해서 작성자이면 private도 볼수 있음!
                # 작성자이면 비공개인 것을 다 볼 수 있음
                search_board = Board.objects.filter(post_root=get_board.post_root).order_by("title")
                areas = get_board.board_set.filter()
                find_input = areas.order_by('title')
            else:
                # 작성자가 아니면 공개만
                search_board = Board.objects.filter(post_root=get_board.post_root, secure='public').order_by("title")
                areas = get_board.board_set.filter(secure='public')
                find_input = areas.order_by('title')
        else:
            # 비로그인 일 경우
            search_board = Board.objects.filter(post_root=get_board.post_root, secure='public').order_by("title")
            areas = get_board.board_set.filter(secure='public')
            find_input = areas.order_by('title')
    else:
        #root게시판일 경우
        groups = get_board.group.all()
        root_author = get_board.author
        get_root_board = get_board
        if request.user.is_authenticated:
            # 작성자이면 비공개인 것을 다 볼 수 있음
            if get_board.author == request.user.profile or request.user.profile in groups:
                search_board = Board.objects.filter(post_root=get_board).order_by("title")
                areas = get_board.board_set.filter()
                find_input = areas.order_by('title')
            else:
                search_board = Board.objects.filter(post_root=get_board, secure='public').order_by("title")
                areas = get_board.board_set.filter(secure='public')
                find_input = areas.order_by('title')
        else:
            search_board = Board.objects.filter(post_root=get_board, secure='public').order_by("title")
            areas = get_board.board_set.filter(secure='public')
            find_input = areas.order_by('title')

    board_form = Boardmodform()

    if request.user.is_authenticated:
        if board_name[:7] == "alerted": # 만약 알림에서 확인했을 경우! True를 False로 바꾼다! (읽음 느낌)
            change = get_object_or_404(Commentalertcontent, id=board_name[7:], profile_name=request.user.profile)
            change.view = False
            change.save()

    if get_board.secure == "public":
        return render(request, "detail.html", {"find_input":find_input,"areas":areas,"get_board":get_board, "board_name":board_name, "board_form":board_form, "search_board":search_board, "commentform":commentform, "detail_getComment":detail_getComment,})
    elif not request.user.is_authenticated: #만약 회원가입하지 않은 일반 사람이 public이 아닌글을 읽을려고 하는 경우 바로 안보이도록 설정 위에 있는 이유는 user.profile을 익명자가 없기 때문에
        return redirect('/')
    #권한 있는 사람들은 비공개 글 볼 수 있도록! (권한 있는자 : 권한이 있는 사람, 루트 게시글 작성자, 관리자)
    elif request.user.profile in groups or root_author == request.user.profile or request.user.is_superuser:
        return render(request, "detail.html", {"find_input":find_input,"areas":areas,"get_board":get_board, "board_name":board_name, "board_form":board_form, "search_board":search_board, "commentform":commentform, "detail_getComment":detail_getComment,})
    else:
        return redirect('/')

def mod_detail(request, board_name, id):
    get_board = Board.objects.get(id=id)
    # pre_image = get_board.image #이미지가 달라졌는지 확인하기 위해서 달라졌으면 그 이미지안에 있는 글들 전부 삭제
    boardform = Boardmodform(instance=get_board)
    root_board = get_board.post

    if root_board:
        root_author = get_board.post_root.author
        get_root_board = get_board.post_root
    #루트일 경우
    else:
        root_author = get_board.author
        get_root_board = get_board

    #권한이 없는 사람이 수정하기를 못 들어오도록 막기 (권한의 기준 : 게시글을 작성한 사람 혹은 영역을 작성한 사람이고 권한을 가지고 있는 사람)
    if request.user.is_authenticated:
        if (get_board.author == request.user.profile and request.user.profile in get_root_board.group.all()) or root_author == request.user.profile:
            pass
        else:
            # 권한이 없을 경우 detail로 원래 위치로 돌아가기
            return HttpResponseRedirect(reverse('board:detail', args=[get_board.post.category.board_name, get_board.post.id]))
    else:
        return HttpResponseRedirect(reverse('board:detail', args=[get_board.post.category.board_name, get_board.post.id]))

    if request.method == 'POST':
        if (get_board.author == request.user.profile and request.user.profile in get_root_board.group.all()) or root_author == request.user.profile:
            boardform = Boardmodform(request.POST, instance=get_board)
            if boardform.is_valid():
                boardform.save()
                return redirect('/board/detail/'+get_board.post.category.board_name+'/'+str(root_board.id))
            else:
                return redirect('/board/detail/'+get_board.post.category.board_name+'/'+str(root_board.id))
        else:
            return redirect('/board/'+get_board.post.category.board_name+'/'+str(root_board.id))

    return render(request, "modify.html", {"root_board":root_board, "boardform":boardform, "get_board":get_board,})

# def del_detail(request, board_name, id):
#     if request.method == 'POST':
#         get_board = Board.objects.get(id=id)
#         root_board = get_board.post
#         if get_board.author == request.user.profile:
#             get_board.delete()
#             return redirect('/board/detail/'+get_board.category.board_name+'/'+str(root_board.id))
#         else:
#             return redirect('/board/'+get_board.category.board_name+'/'+str(root_board.id))

#댓글 생성
def comment_write(request, board_name, id):
    if request.method == 'POST':
        main_post = Board.objects.get(id=id)
        # if comment_id:
        #     post = Comment.objects.get(id=comment_id)
        #답글을 클릭하면 option request.post로 option id번호 주기
        commentform = CommentTest(request.POST)
        if commentform.is_valid():
            getProfile = Profile.objects.get(user__username=request.user) #안됬는데 보니깐 슈퍼유저는 Profile이 안만들어져서 찾지를 못하는 것이였음
            a = commentform.save(commit=False)
            a.author = getProfile
            a.main_post = main_post
            a.save()

            #알람 차단한 사람은 알려주지 않고, 알람 차단하지 않은 사람은 알려주기
            #내가 내 글에 댓글을 작성했을 경우!
            if not (main_post.author.user.username == request.user.username): #and not (Donotalert.objects.filter(profile=main_post.author, board=main_post).exists()):
                comment_a = Commentalert.objects.get(profile=main_post.author)
                comment_a.recent = comment_a.recent+1
                comment_a.save()

                #body = commentform.cleaned_data['body']
                #내용과 id를 저장하기
                Commentalertcontent.objects.create(board=main_post, sender_name=getProfile.nickname, profile_name=main_post.author, content=a)

            return redirect('/board/detail/'+str(main_post.category.board_name)+'/'+str(id))
        else:
            return redirect('/board/detail/'+str(main_post.category.board_name)+'/'+str(id))

#댓글 삭제
def comment_del(request, board_name, id, comment_id):
    comment = Comment.objects.get(id=comment_id)
    if comment.author.user.username == request.user.username:
        comment.delete()
    return redirect('/board/detail/'+str(board_name)+"/"+str(id))

#대댓글 생성
def recomment_write(request, board_name, id, comment_id):
    if request.method == 'POST':
        main_post = Board.objects.get(id=id)
        post = Comment.objects.get(id=comment_id)
        #답글을 클릭하면 option request.post로 option id번호 주기
        commentform = CommentTest(request.POST)
        if commentform.is_valid():
            getProfile = Profile.objects.get(user__username=request.user) #안됬는데 보니깐 슈퍼유저는 Profile이 안만들어져서 찾지를 못하는 것이였음
            a = commentform.save(commit=False)
            a.author = getProfile
            a.main_post = main_post
            a.post = post
            a.save()

            #알람 차단한 사람은 알려주지 않고, 알람 차단하지 않은 사람은 알려주기
            if not (post.author.user.username == request.user.username):# and not (Donotalert.objects.filter(profile=post.author, board=main_post).exists()):
                comment_a = Commentalert.objects.get(profile=post.author)
                comment_a.recent = comment_a.recent+1
                comment_a.save()

                body = commentform.cleaned_data['body']
                #내용과 id를 저장하기
                Commentalertcontent.objects.create(board=main_post, sender_name=getProfile.nickname, profile_name=post.author, content=a)

            return redirect('/board/detail/'+str(board_name)+'/'+str(id))
        else:
            return redirect('/board/detail/'+str(board_name)+'/'+str(id))


#게시글 북마크
def ajax_board_bookmark(request, id):
    if request.is_ajax():
        board = Board.objects.get(id=id)
        getProfile = Profile.objects.get(user__username=request.user) #안됬는데 보니깐 슈퍼유저는 Profile이 안만들어져서 찾지를 못하는 것이였음

        #있을 경우 삭제
        try:
            a = Bookmark.objects.get(post=board, author=getProfile)
            a.delete()
            like_state = True #없어졌으니깐 좋아요를 누를 수 있음
        #없을 경우 생성
        except:
            Bookmark.objects.create(post=board, author=getProfile)
            like_state = False #생기니깐 좋아요 취소 누를 수 있음

        board_bookmark = Bookmark.objects.filter(post=board).count()
        return HttpResponse(json.dumps({'board_bookmark':str(board_bookmark), 'like_state':like_state,}), 'application/json')