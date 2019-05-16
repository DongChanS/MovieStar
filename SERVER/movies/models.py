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
    filmography = models.TextField(blank=True)
    profile_image = models.ImageField(blank=True)
    search_image = models.ImageField(blank=True)
    movies_cnt = models.IntegerField(blank=True)
    like_users = models.ManyToManyField(get_user_model(), related_name="like_actors")
    
    def __str__(self):
        return self.name
    
class Movie(models.Model):
    actor_list = models.CharField(max_length=500)
    audiance = models.IntegerField()
    director_list = models.CharField(max_length=100)
    duration = models.IntegerField() # ex) 2시간 2분 => 122로 저장
    name = models.CharField(max_length=40)
    open_day = models.CharField(max_length=40) #날짜만 기록 
    story_header = models.CharField(max_length=200)
    watch_grade = models.CharField(max_length=40)
    troll = models.IntegerField()
    image = models.ImageField(blank=True) # 포스터 이미지
    
    genres = models.ManyToManyField(Genre, related_name="movies")
    actors = models.ManyToManyField(Actor, related_name="act_movies")
    like_users = models.ManyToManyField(get_user_model(), related_name="like_movies")
    
    
    def __str__(self):
        return self.name

class Review(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    score = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # recommend = models.IntegerField(default=0) # 추천수
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    
    def __str__(self):
        return f"작성자 : {self.user} // 영화 : {self.movie.name} // 내용 : {self.content}"