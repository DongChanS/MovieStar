from django.db import models
from django_countries.fields import CountryField
from django.contrib.auth import get_user_model

# Create your models here.
class Genre(models.Model):
    name = models.CharField(max_length=20)

class Actor(models.Model):
    name = models.CharField(max_length=40)
    age = models.IntegerField()
    tenure = models.IntegerField()  # 경력
    is_actor = models.BooleanField() # 배우인지 아닌지
    is_director = models.BooleanField() # 감독인지 아닌지
    profile_image = models.ImageField()
    nation = CountryField()

class Review(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    score = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    movie = models.ForeignKey("Movie", on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    recommend = models.IntegerField() # 추천수
    view_count = models.IntegerField() # 조회수

class Movie(models.Model):
    name = models.CharField(max_length=40)
    open_day = models.DateField() # 날짜만 기록 
    audiance = models.IntegerField()
    duration = models.IntegerField() # ex) 2시간 2분 => 122로 저장
    nation = CountryField() # https://github.com/SmileyChris/django-countries/
    watch_grade = models.IntegerField() # 15세이상관람가 => 15로 저장
    image = models.ImageField() # 포스터 이미지
    
    genres = models.ManyToManyField(Genre, related_name="movies")
    like_users = models.ManyToManyField(get_user_model(), related_name="like_movies")
    actors = models.ManyToManyField(Actor, related_name="act_movies")
