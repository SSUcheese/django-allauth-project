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
        (1, "*"), # 해당 tuple 자료형에서 왼쪽 숫자는 model에 들어가는 애들이고 오른쪽은 선택지에 보여지는 값임
        (2, "**"),
        (3, "***"),
        (4, "****"),
        (5, "*****"),
    ]
    rating = models.IntegerField(choices=RATING_CHOICES, default = None)

    image1 = models.ImageField(upload_to="review_pics")
    image2 = models.ImageField(upload_to="review_pics", blank=True) # 이렇게 하면 빈 내용을 제출해도 된다.
    image3 = models.ImageField(upload_to="review_pics", blank=True) # 결국 이미지필드도 이미지의 url을 저장하는 원리기에 문자열 기반 필드에 해당한다.
    content = models.TextField()
    dt_created = models.DateTimeField(auto_now_add=True) # 생성된 시간 자동으로 field에 넣어줌
    dt_updated = models.DateTimeField(auto_now=True) # 마지막으로 저장된 시간 자동으로 field에 넣어줌

    author = models.ForeignKey(User, on_delete=models.CASCADE) 
    # foreign_key의 기능은 1:n 관계로 데이터베이스를 모델링할 때 n의 입장에서 기능할 수 있게 도와주는 도구다
    # on_delete는 만들어둔 모델에서 유저의 관한 정보가 지워질 때 그동안 그가 적어둔 내용들 어떻게 처리할 것인가를 다룬다.
    # 결국 위 코드의 최종적인 결과로 리뷰 내용들과 author을 우리는 1:n 관계로 묶어줬다.

    def __str__(self): # 리뷰의 제목 출력
        return self.title
