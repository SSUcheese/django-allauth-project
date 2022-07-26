from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Review


# Register your models here.
admin.site.register(User, UserAdmin)
UserAdmin.fieldsets += (("Custom fields", {"fields" : ("nickname","profile_pic","intro")}),)
# 유저모델에 대한 추가필드는 기본적으로 어드민 페이지에 나타나지 않기에 이렇게 따로 추가해주는 것임.

admin.site.register(Review)