from django.urls import path
from . import views
from rest_framework_swagger.views import get_swagger_view

urlpatterns = [
    path('genres/', views.genre_list, name="genre_list"),
    path('genres/<int:genre_pk>/', views.genre_movies, name="genre_movies"),
    path('movies/', views.movie_list, name="movie_list"),
    path('movies/<int:movie_pk>/', views.detail_movie, name="detail_movie"),
    path('movies/<int:movie_pk>/reviews/', views.movie_review, name="movie_review"),
    path('reviews/<int:review_pk>/', views.review, name="review"),
    path('docs/', get_swagger_view(title="API문서")),
]