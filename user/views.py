from django.contrib.auth import get_user_model, login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import render

from .forms import LoginForm, RegisterForm

User = get_user_model()

# 로그인한 유저이름 출력
def index(request):
    # user = User.objects.filter(username="admin").first()     # 유저네임이 "admin"인 첫 번째 유저 가져오기
    # user = User.objects.get(username="admin/")               # 위와 같은 코드 
    # email = user.email if user else "Anonymous USER!"
    # print(email)
    # print(request.user.is_authenticated)
    # if request.user.is_authentificated is False:
    #     users = "Anonymous User!"
    # print("user", user)
    form = LoginForm(request.POST)
    return render(request, "index.html", {"form": form} )


def register_view(request):
    print("회원가입 시작")
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            print("회원가입 완료")
            return HttpResponseRedirect("/login")
    else:
        logout(request)
        form = RegisterForm()
    return render(request, "register.html", {"form": form})


def login_view(request):
    form = LoginForm()
    if request.method == "POST":
        #print("# TODO: 1. /login로 접근하면 로그인 페이지를 통해 로그인이 되게 해주세요")
        #print("# TODO: 2. login 할 때 form을 활용해주세요")
        form = LoginForm(request.POST)
        print("로그인 시작")
        if form.is_valid():
            print("로그인폼 유효")
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=raw_password)
            # print(">> username:", username, "raw_password", raw_password)
            if user:
                login(request, user)
                print(user, '로그인 성공!\n')
                return HttpResponseRedirect("/", {"form": form})
    else:
        form = LoginForm()
    print("로그인 되어 Index로 이동????")
    return render(request, "login.html", {"form": form})


def logout_view(request):
    # TODO: 3. /logout url을 입력하면 로그아웃 후 / 경로로 이동시켜주세요

    if request.method == "GET":
        logout(request)
        print("로그아웃 성공!!!!")
        return HttpResponseRedirect("/")
    return HttpResponseRedirect("/login")


# TODO: 8. user 목록은 로그인 유저만 접근 가능하게 해주세요
@login_required
def user_list_view(request):
    # TODO: 7. /users 에 user 목록을 출력해주세요
    # TODO: 9. user 목록은 pagination이 되게 해주세요
    print("userlist 보기")
    page = int(request.GET.get("page", 1))
    users = User.objects.all().order_by("-id")     # 모든 유저정보 가져오기(내림차순)
    paginator = Paginator(users, 5)               # 10개씩 보여주기
    users = paginator.get_page(page)

    return render(request, "users.html", {"users": users})
