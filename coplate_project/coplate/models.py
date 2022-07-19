from django.db import models
from django.contrib.auth.models import AbstractUser
from .validators import validate_no_special_characters
# Create your models here.
class User(AbstractUser): # User모델의 user 인스턴스를 출력하는데 사용되는 str메소드에는 자동으로 username이 사용되기에 이를 email을 쓰도록 해야한다.
    nickname = models.CharField(
        max_length=15, 
        unique=True, 
        null=True,
        validators=[validate_no_special_characters],
        error_messages={'unique': "이미 사용중인 닉네임입니다."}, # unique라는 error code가 발생하면 띄운다
    )

    def __str__(self):
        return self.email # 홈페이지 안녕하세요 ㅡㅡ 님 이 부분에 메일이 나올거임
    

class Review(models.Model):
    title = models.CharField(max_length=30)
    restaurant_name = models.CharField(max_length=20)
    restaurant_link = models.URLField()