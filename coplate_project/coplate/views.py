from django.shortcuts import render
from django.urls import reverse
from django.views.generic import ListView, DetailView
from allauth.account.views import PasswordChangeView
from .models import User, Review


# Create your views here.
class IndexView(ListView):
    model = Review # 리뷰 내용을 보여줄 예정이니 당연히 모델은 rview로 갖고 온다.
    template_name= "coplate/index.html"
    context_object_name = "reviews" # 데이터 긁어서 템플릿에 넘길 때 그 이름은 reivews로 한다.
    paginate_by = 4 
    ordering = ["-dt_created"]

class ReviewDetailListView(DetailView):
    model = Review
    template_name = "coplate/review_detail.html"
    pk_url_kwarg = "review_id"
# 참고로 detailView와 같이 object를 하나만 갖고 오는 view에선 context_object_name의 default 값이 model의 이름이 된다.

class CustomPasswordChangeView(PasswordChangeView): # 이거 기존 부모코드에서 있는 success_url 자식코드에서 오버라이딩 해서 사용하는 구조임
    def get_success_url(self): # 어떤 form이 성공적으로 처리되면 어디로 redirection 핳건지 정해주는 함수
        return reverse("index")
