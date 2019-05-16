from django.urls import path
from . import views
from rest_framework_swagger.views import get_swagger_view

urlpatterns = [
    path('genres/', views.genre_list, name="genre_list"),
    path('genres/<int:genre_pk>/', views.genre_movies, name="genre_movies"),
    
    path('movies/', views.movie_list, name="movie_list"),
    path('movies/page/<int:page_num>/', views.movie_page, name="movie_page"),
    path('movies/<int:movie_pk>/', views.detail_movie, name="detail_movie"),
    path('movies/<int:movie_pk>/reviews/', views.movie_review, name="movie_review"),
    path('movies/<int:movie_pk>/users/', views.review_users, name="review_users"),
    
    path('reviews/<int:review_pk>/', views.review, name="review"),
    
    path('actor/page/<int:page_num>/', views.actor_page, name="actor_page"),
    path('actor/', views.actor_list, name="actor_list"),
    path('actor/<int:actor_pk>/', views.actor_movies, name="actor_movies"),
    
    path('recommend/<int:genre_pk>/<str:actor_name>/', views.recommend, name="recommend"),
    path('docs/', get_swagger_view(title="API문서")),
]