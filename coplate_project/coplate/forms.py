from django import forms
from .models import User

class SignupForm(forms.ModelForm):
    class Meta:
        model = User # 이거는 기본제공 내용들
        fields = ["nickname"] # 우리가 커스텀

    def signup(self, request, user):
        user.nickname = self.cleaned_data["nickname"]
        user.save()