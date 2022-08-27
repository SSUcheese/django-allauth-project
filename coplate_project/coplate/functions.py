from django.shortcuts import redirect
from allauth.account.utils import send_email_confirmation

# 아래 confirmation 어쩌고 함수는 raise exception에 들어갈 함수다
def confirmation_required_redirect(self, request):
    send_email_confirmation(request, request.user)
    # redirect의 url은 이메일 인증 확인을 받는 urls.py의 path name임
    return redirect("account_email_confirmation_required")
# 이후에 eamil 퐇더에 다른 파일넣어줘서 오버라이딩하면 된다.