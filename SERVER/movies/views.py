from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect

# Create your views here.
@api_view(["POST","GET"])
def movie_review(request, movie_pk):
    # POST, 평점 생성
    # GET, 해당하는 영화의 평점 조회
    movie = get_object_or_404(Movie, pk=movie_pk)
    if request.method == "POST":
        serializer = WriteReviewSerializer(data=request.data)
        if serializer.is_valid() and request.user.is_authenticated:
            serializer.save(movie=movie, user=request.user)
            return Response(serializer.data)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
    else:
        serializer = ReviewSerializer(movie.review_set.all(), many=True)
        return Response(serializer.data)


@api_view(['GET'])
def genre_list(request):
    # GET, 장르의 목록
    genres = Genre.objects.all()
    serializers = GenreSerializer(genres, many=True)
    return Response(serializers.data)
    
@api_view(['GET'])
def genre_movies(request, genre_pk):
    # GET, 장르에 대한 영화목록
    genre = get_object_or_404(Genre, pk=genre_pk)
    serializers = GenreMovieSerializer(genre, many=False)
    return Response(serializers.data)
    

@api_view(['GET'])
def movie_list(request):
    # GET, 영화 전체 목록
    movies = Movie.objects.all()
    serializers = MovieSerializer(movies, many=True)
    return Response(serializers.data)
    
    
@api_view(['GET'])
def movie_page(request,page_num):
    movies = Movie.objects.all()[page_num*6 : page_num*6+6]
    serializers = MovieSerializer(movies, many=True)
    return Response(serializers.data)

@api_view(['GET'])
def detail_movie(request, movie_pk):
    # GET, 영화 상세 정보
    movie = get_object_or_404(Movie, pk=movie_pk)
    serializers = MovieSerializer(movie, many=False)
    return Response(serializers.data)

@api_view(['GET','PUT','DELETE'])
def review(request, review_pk):
    # GET : 평점 조회
    # PUT : 평점 수정
    # DELETE : 평점 삭제
    review = get_object_or_404(Review, pk=review_pk)
    if request.method == "GET":
        serializer = ReviewSerializer(review, many=False)
        serializer.data['user_name'] = review.user.username
        return Response(serializer.data)
    elif request.method == "PUT":
        serializer = WriteReviewSerializer(instance=review, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message' : "수정되었습니다."})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        review.delete()
        return Response({'message':'삭제되었습니다.'})

@api_view(['GET'])
def review_users(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    reviews = movie.review_set.all()
    names = [review.user.username for review in reviews]
    
    return JsonResponse({'names' : names})


@api_view(['GET'])
def actor_page(request, page_num):
    actors = Actor.objects.all()[page_num*6 : page_num*6+6]
    serializers = ActorSerializer(actors, many=True)
    return Response(serializers.data)

@api_view(['GET'])
def actor_movies(request, actor_pk):
    actor = get_object_or_404(Actor, pk=actor_pk)
    serializers = MovieSerializer(actor.act_movies, many=True)
    return Response(serializers.data)

@api_view(['GET'])
def actor_list(request):
    actors = Actor.objects.all()
    serializers = ActorSerializer(actors, many=True)
    return Response(serializers.data)

@api_view(['GET'])
def recommend(request,genre_pk,actor_name):
    
    actor = get_object_or_404(Actor, name=actor_name)
    movies = actor.act_movies.all()
    user = request.user
    
    if len(movies) == 0:
        genre = get_object_or_404(Genre, pk=genre_pk)
        movies = genre.movies.all()
        if len(movies) == 0:
            movie = Movie.objects.first()
            serializer = MovieSerializer(movie, many=False)
            return Response(serializer.data)
        else:
            serializer = MovieSerializer(movies[0], many=False)
            return Response(serializer.data)
            

    # 일치하는 장르가 있으면 반환
    genre_movies = []
    for movie in movies:
        for genre in movie.genres.all():
            if genre.id == genre_pk:
                genre_movies.append(movie)
                break
    if len(genre_movies) == 1:
        serializer = MovieSerializer(genre_movies[0], many=False)
        return Response(serializer.data)
    elif len(genre_movies) == 0:
        # genre_movies를 기준으로 평점, 트롤스코어를 통해 거르기
        genre_movies = movies
    # 그렇지 않은 경우는 전체 영화를 기준으로 평점, 트롤스코어를 통해 거르기
    
    max_score = 0
    max_movies = []
    reviews = user.review_set.all()
    for movie in genre_movies:
        for review in reviews:
            if review.movie == movie:
                if max_score < review.score:
                    max_score = review.score
                    max_movies = [movie]
                elif max_score == review.score:
                    max_movies.append(movie)
    
    if len(max_movies) == 1:
        serializer = MovieSerializer(max_movies[0], many=False)
        return Response(serializer.data)
    elif len(max_movies) == 0:
        max_movies = genre_movies
        
    # 애초에 Troll score기준으로 정렬되어있기 때문에!
    movie = max_movies[0]
    serializer = MovieSerializer(movie, many=False)
    return Response(serializer.data)

@api_view(['GET'])
def like_actors(request, user_id):
    user = get_object_or_404(get_user_model(), pk=user_id)
    actors = user.like_actors.all()
    
    serializers = ActorSerializer(actors, many=True)
    return Response(serializers.data)
    