from tkinter import Widget
from django import forms
from .models import User, Review

# class SignupForm(forms.ModelForm):
#     class Meta:
#         model = User # 이거는 기본제공 내용들
#         fields = ["nickname"] # 우리가 커스텀

#     def signup(self, request, user):
#         user.nickname = self.cleaned_data["nickname"]
#         user.save()

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = [
            "title",
            "restaurant_name",
            "restaurant_link",
            "rating",
            "image1",
            "image2",
            "image3",
            "content",
        ]
        # widegts = {
        #     "rating": forms.RadioSelect, # 펼처서 구하는거 말고 바로 구하게 해주는 코드
        # }
        widgets = {
            "rating": forms.RadioSelect,
        }
        
class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            "nickname",
            "profile_pic",
            "intro"
        ]
        widget = {
            "intro": forms.Textarea
        }