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
from coplate.functions import confirmation_required_redirect


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

class ReviewCreateView(LoginRequiredMixin, UserPassesTestMixin,CreateView): 
    # 여기서 access mixin은 generic view 옆에 써줘야 한다. 코드는 왼쪽에서 오른쪽으로 진행되니까.
    # 저기서 UserPassesTestMixin은 user가 이메일 인증 통과했는지 알아보는 mixin이다.
    model = Review
    form_class = ReviewForm
    template_name = "coplate/review_form.html"


    # 아래 두 로직은 위에 적어둔 로그인 믹스인이랑 유저 패스 믹스인에서 걸러지면 실행된다. 로그인을 시키거나 메일 인증을 시키거나
    # 로그인이 되어 있는 유저랑 아닌 유저에 대한 처리를 다르게 할 것인지에 관한 코드.
    # 저거 true로 하면 로그인 안 한 유저는 로그인 페이지로, 로그인 한 유저는 raise_exception에 따라서 처리 방식이 정해진다.
    # 당연히 False로 하면 로그인 여부와 관계 없이 일괄적으로 처리한다.
    redirect_unauthenticated_users = True
    raise_exception = confirmation_required_redirect    # 이메일 인증을 안내하는 페이지로 리디렉트
    # raise exception 부분은 우리가 만든 함수로 넣는다.
    
    def form_valid(self, form): # 데이터가 유효할 때 담아두는 obj 만들고 저장하는 여기에 author 데이터도 같이 넣어서 저장
        form.instance.author = self.request.user # 이게 기본적인 예시이고, 이런 view에서 현재 user에 접근할 떄는 request.user로 접근 앞에 self는 함수형 view와 달리 class형 view에서는 붙여줘야 한다.
        return super().form_valid(form) # 저기서 super는 ReviewCreateView의 상위 클래스인 CreateView 클래스를 뜻한다. 폼의 인스턴스에 user 정보 넣어주고 그걸 CreateView에 form_valid에 넣어줬기에 쟤도 같이 들어간다. // 결국 메소드 오버라이딩

    def get_success_url(self):
        return reverse("review-detail", kwargs={"review_id":self.object.id})

    def test_func(self, user):
        # 위에 UserPassesTestMixin의 testfunc 메소드를 구현하는 과정임
        # 얘는 파라미터로 self, user을 받아 user의 view 접근가능여부를 boolean 값으로 알려준다. 따라서 if문으로 구분할 필요 없이 그냥 return에 달아서 써도 된다.
        return EmailAddress.objects.filter(user=user, verified=True).exists()
        # allauth는 다양한 이메일을 받아서 관리하는데, 그 이메일들이 eamiladress 저기에 모여있다
        # 유저가 이메일 인증을 통과해는지 검증하는 코드, filter안에 내용은 user=user은 등록이 되었는지 여부 체크
            
            
class ReviewUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Review
    form_class = ReviewForm
    template_name = "coplate/review_form.html"
    pk_url_kwarg = "review_id"
    
    raise_exception = True # 페이지 접근권한이 없으면 403 exception 돌려준다
    redirect_unauthenticated_users = False # 로그인 여부와 상관없이 403 보낼거임. 사실 이거는 default가 false라서 없어도 ㄱㅊ

    # updateView는 작성자를 건들 필요가 없어서 form_valid가 필요없다.
    def get_success_url(self):
        return reverse("review-detail", kwargs={"review_id":self.object.id}) 
    
    def test_func(self, user):
        review = self.get_object()
        return review.author == user

class ReviewDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Review
    tempalte_name = "coplate/review_confirm_delete.html"
    pk_url_kwarg = "review_id"
    
    raise_exception = True
    
    def get_success_url(self):
        return reverse("index")
    
    def test_func(self, user):
        review = self.get_object()
        return review.author == user

class CustomPasswordChangeView(PasswordChangeView): # 이거 기존 부모코드에서 있는 success_url 자식코드에서 오버라이딩 해서 사용하는 구조임
    def get_success_url(self): # 어떤 form이 성공적으로 처리되면 어디로 redirection 핳건지 정해주는 함수
        return reverse("index")
