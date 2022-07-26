from django.shortcuts import render
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView
from allauth.account.views import PasswordChangeView
from .models import User, Review
from .forms import ReviewForm


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

class ReviewCreateView(CreateView):
    model = Review
    form_class = ReviewForm
    template_name = "coplate/review_form.html"

    def form_valid(self, form): # 데이터가 유효할 때 담아두는 obj 만들고 저장하는 여기에 author 데이터도 같이 넣어서 저장
        form.instance.author = self.request.user # 이게 기본적인 예시이고, 이런 view에서 현재 user에 접근할 떄는 request.user로 접근 앞에 self는 함수형 view와 달리 class형 view에서는 붙여줘야 한다.
        return super().form_valid(form) # 저기서 super는 ReviewCreateView의 상위 클래스인 CreateView 클래스를 뜻한다. 폼의 인스턴스에 user 정보 넣어주고 그걸 CreateView에 form_valid에 넣어줬기에 쟤도 같이 들어간다. // 결국 메소드 오버라이딩

    def get_success_url(self):
        return reverse("review-detail", kwargs={"review_id":self.object.id})

class CustomPasswordChangeView(PasswordChangeView): # 이거 기존 부모코드에서 있는 success_url 자식코드에서 오버라이딩 해서 사용하는 구조임
    def get_success_url(self): # 어떤 form이 성공적으로 처리되면 어디로 redirection 핳건지 정해주는 함수
        return reverse("index")
