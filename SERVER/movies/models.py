from django.db import models
from django_countries.fields import CountryField
from django.contrib.auth import get_user_model

# Create your models here.
class Genre(models.Model):
    name = models.CharField(max_length=20)
    
    def __str__(self):
        return self.name

class Actor(models.Model):
    name = models.CharField(max_length=40)
    filmography = models.TextField()
    profile_image = models.ImageField(blank=True)

class Review(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    score = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    recommend = models.IntegerField(default=0) # 추천수
    view_count = models.IntegerField(default=0) # 조회수
    
    movie = models.ForeignKey("Movie", on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    

class Movie(models.Model):
    name = models.CharField(max_length=40)
    open_day = models.CharField(max_length=40) # 날짜만 기록 
    audiance = models.IntegerField()
    duration = models.IntegerField() # ex) 2시간 2분 => 122로 저장
    watch_grade = models.IntegerField() # 15세이상관람가 => 15로 저장
    image = models.ImageField(blank=True) # 포스터 이미지
    
    genres = models.ManyToManyField(Genre, related_name="movies")
    like_users = models.ManyToManyField(get_user_model(), related_name="like_movies")
    actors = models.ManyToManyField(Actor, related_name="act_movies")
    
    def __str__(self):
        return self.name + "이미지 : " + str(self.image)
