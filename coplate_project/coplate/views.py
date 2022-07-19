from django.shortcuts import render
from django.urls import reverse
from allauth.account.views import PasswordChangeView


# Create your views here.

def index(request):
    print(request.user.is_authenticated)
    return render(request, "coplate/index.html")

class CustomPasswordChangeView(PasswordChangeView): # 이거 기존 부모코드에서 있는 success_url 자식코드에서 오버라이딩 해서 사용하는 구조임
    def get_success_url(self): # 어떤 form이 성공적으로 처리되면 어디로 redirection 핳건지 정해주는 함수
        return reverse("index")