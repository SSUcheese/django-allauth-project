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

    RATING_CHOICES = [
        (1, 1), # 해당 tuple 자료형에서 왼쪽 숫자는 model에 들어가는 애들이고 오른쪽은 선택지에 보여지는 값임
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
    ]
    rating = models.IntegerField(choices=RATING_CHOICES)

    image1 = models.ImageField()
    image2 = models.ImageField()
    image3 = models.ImageField()
    content = models.TextField()
    dt_created = models.DateTimeField(auto_now_add=True) # 생성된 시간 자동으로 field에 넣어줌
    dt_updated = models.DateTimeField(auto_now=True) # 마지막으로 저장된 시간 자동으로 field에 넣어줌

    def __str__(self): # 리뷰의 제목 출력
        return self.title
    