from rest_framework import serializers
from .models import *

# serializers.ModelSerializer
# ModelForms와 비슷하게 하면 됨.

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'name']


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = "__all__"

class GenreMovieSerializer(serializers.ModelSerializer):
    movies = MovieSerializer(source="movie_set", many=True, read_only=True)
    class Meta:
        model = Genre
        fields = ['id', 'movies', 'name']


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['title','score','content']