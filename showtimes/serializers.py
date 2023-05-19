from rest_framework import serializers

from movielist.models import Movie
from showtimes.models import Cinema


class CinemaSerializer(serializers.ModelSerializer):
    movies = serializers.SlugRelatedField(many=True, slug_field='title', queryset=Movie.objects.all())

    class Meta:
        model = Cinema
        fields = ('id', 'name', 'city', 'movies')
