from django.shortcuts import render
from django.urls import reverse
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from braces.views import LoginRequiredMixin, UserPassesTestMixin
from allauth.account.models import EmailAddress
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

class ReviewCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView): 
    # 여기서 access mixin은 generic view 옆에 써줘야 한다. 코드는 왼쪽에서 오른쪽으로 진행되니까.
    # 저기서 UserPassesTestMixin은 user가 이메일 인증 통과했는지 알아보는 mixin이다.
    model = Review
    form_class = ReviewForm
    template_name = "coplate/review_form.html"

    redirect_unauthenticated_users
    raise_exeception

    def form_valid(self, form): # 데이터가 유효할 때 담아두는 obj 만들고 저장하는 여기에 author 데이터도 같이 넣어서 저장
        form.instance.author = self.request.user # 이게 기본적인 예시이고, 이런 view에서 현재 user에 접근할 떄는 request.user로 접근 앞에 self는 함수형 view와 달리 class형 view에서는 붙여줘야 한다.
        return super().form_valid(form) # 저기서 super는 ReviewCreateView의 상위 클래스인 CreateView 클래스를 뜻한다. 폼의 인스턴스에 user 정보 넣어주고 그걸 CreateView에 form_valid에 넣어줬기에 쟤도 같이 들어간다. // 결국 메소드 오버라이딩

    def get_success_url(self):
        return reverse("review-detail", kwargs={"review_id":self.object.id})

    def test_func(self, user):
        # 얘는 파라미터로 self, user을 받아 user의 view 접근가능여부를 boolean 값으로 알려준다.
        return EmailAddress.objects.filter(user=user, verified=True).exists(): 
        # 유저가 이메일 인증을 통과해는지 검증하는 코드, filter안에 내용은 user=user은 등록이 되었는지 여부 체크
            
class ReviewUpdateView(UpdateView):
    model = Review
    form_class = ReviewForm
    template_name = "coplate/review_form.html"
    pk_url_kwarg = "review_id"

    # updateView는 작성자를 건들 필요가 없어서 form_valid가 필요없다.
    def get_success_url(self):
        return reverse("review-detail", kwargs={"review_id":self.object.id})    

class ReviewDeleteView(DeleteView):
    model = Review
    tempalte_name = "coplate/review_confirm_delete.html"
    pk_url_kwarg = "review_id"
    
    def get_success_url(self):
        return reverse("index")

class CustomPasswordChangeView(PasswordChangeView): # 이거 기존 부모코드에서 있는 success_url 자식코드에서 오버라이딩 해서 사용하는 구조임
    def get_success_url(self): # 어떤 form이 성공적으로 처리되면 어디로 redirection 핳건지 정해주는 함수
        return reverse("index")
