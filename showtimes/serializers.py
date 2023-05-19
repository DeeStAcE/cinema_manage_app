from rest_framework import serializers

from movielist.models import Movie
from showtimes.models import Cinema, Screening


class CinemaSerializer(serializers.ModelSerializer):
    # movies = serializers.SlugRelatedField(slug_field='title', many=True, queryset=Movie.objects.all())
    movies = serializers.HyperlinkedRelatedField(many=True, view_name='movies-detail', read_only=True)

    class Meta:
        model = Cinema
        fields = ('name', 'city', 'movies')


class ScreeningSerializer(serializers.ModelSerializer):
    movie = serializers.SlugRelatedField(slug_field='title', queryset=Movie.objects.all())
    cinema = serializers.SlugRelatedField(slug_field='name', queryset=Cinema.objects.all())

    class Meta:
        model = Screening
        fields = ('movie', 'cinema', 'date')
