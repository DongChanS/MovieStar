from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from .models import *
from django.contrib.auth.decorators import login_required

# Create your views here.
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
    # GET, 영화 전체 목록
    movies = Movie.objects.all()[page_num*6 : page_num*6+6]
    serializers = MovieSerializer(movies, many=True)
    return Response(serializers.data)

@api_view(['GET'])
def detail_movie(request, movie_pk):
    # GET, 영화 상세 정보
    movie = get_object_or_404(Movie, pk=movie_pk)
    serializers = MovieSerializer(movie, many=False)
    return Response(serializers.data)


@api_view(['GET', 'POST'])
def movie_review(request, movie_pk):
    # POST, 평점 생성
    # GET, 해당하는 영화의 평점 조회
    movie = get_object_or_404(Movie, pk=movie_pk)
    if request.method == "POST":
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid() and request.user.is_authenticated:
            serializer.save(movie_id=movie.id)
            serializer.save(user_id=user.id)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        serializer = ReviewSerializer(movie.review_set.all(), many=True)
        return Response(serializer.data)


@api_view(['GET','PUT','DELETE'])
def review(request, review_pk):
    # GET : 평점 조회
    # PUT : 평점 수정
    # DELETE : 평점 삭제
    review = get_object_or_404(Review, pk=score_pk)
    if request.method == "GET":
        serializer = ReviewSerializer(review, many=False)
        return Response(serializer.data)
    elif request.method == "PUT":
        serializer = ReviewSerializer(instance=review, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message' : "수정되었습니다."})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        score.delete()
        return Response({'message':'삭제되었습니다.'})
    