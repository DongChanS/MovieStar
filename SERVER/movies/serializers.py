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
    movies = MovieSerializer(many=True, read_only=True)
    class Meta:
        model = Genre
        fields = ['id', 'movies', 'name']


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id','title','score','content','user','movie','created_at']
        
class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = "__all__"
        
class WriteReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id','title','score','content']
        