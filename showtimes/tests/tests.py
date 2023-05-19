import pytest
import pytz
from faker import Faker
from django.urls import reverse

from movielist.models import Movie
from movielist.tests.conftest import client
from moviebase.settings import TIME_ZONE
from showtimes.models import Cinema, Screening
from showtimes.tests.utils import random_movies, fake_cinema_data

faker = Faker("pl_PL")
TZ = pytz.timezone(TIME_ZONE)


@pytest.mark.django_db
def test_post_cinema(client, set_up):
    cinemas_before = Cinema.objects.count()
    new_cinema = fake_cinema_data()
    url = reverse('cinemas-list')
    response = client.post(url, new_cinema, format='json')
    assert response.status_code == 201
    assert Cinema.objects.count() == cinemas_before + 1
    for key, value in new_cinema.items():
        assert key in response.data
        assert response.data[key] == value


@pytest.mark.django_db
def test_get_cinema_list(client, set_up):
    url = reverse('cinemas-list')
    response = client.get(url, {}, format='json')

    assert response.status_code == 200
    assert Cinema.objects.count() == len(response.data)


@pytest.mark.django_db
def test_get_cinema_detail(client, set_up):
    cinema = Cinema.objects.first()
    url = reverse('cinema-detail', kwargs={'pk': cinema.pk})
    response = client.get(url, {}, format='json')

    assert response.status_code == 200
    for field in ('name', 'city', 'movies'):
        assert field in response.data


@pytest.mark.django_db
def test_delete_cinema(client, set_up):
    cinema = Cinema.objects.first()
    url = reverse('cinema-detail', kwargs={'pk': cinema.pk})
    response = client.delete(url, {}, format='json')
    assert response.status_code == 204
    cinema_ids = [cinema.pk for cinema in Cinema.objects.all()]
    assert cinema.pk not in cinema_ids


@pytest.mark.django_db
def test_update_cinema(client, set_up):
    cinema = Cinema.objects.first()
    url = reverse('cinema-detail', kwargs={'pk': cinema.pk})
    response = client.get(url, {}, format='json')
    cinema_data = response.data
    new_name = 'helios'
    cinema_data['name'] = new_name
    new_city = 'warsaw'
    cinema_data['city'] = new_city
    new_movies = [movie.title for movie in random_movies()]
    cinema_data['movies'] = new_movies
    response = client.patch(url, cinema_data, format='json')
    assert response.status_code == 200
    updated_cinema = Cinema.objects.get(pk=cinema.pk)
    assert updated_cinema.name == new_name
    assert updated_cinema.city == new_city
    updated_cinema_movie_titles = [movie.title for movie in updated_cinema.movies.all()]
    assert len(updated_cinema_movie_titles) == len(new_movies)


@pytest.mark.django_db
def test_post_screening(client, set_up):
    screenings_before = Screening.objects.count()
    new_screening_data = {
        "movie": Movie.objects.first().title,
        "cinema": Cinema.objects.first().name,
        "date": faker.date_time(tzinfo=TZ).isoformat()
    }
    url = reverse('screening-list')
    response = client.post(url, new_screening_data, format='json')
    assert response.status_code == 201
    assert Screening.objects.count() == screenings_before + 1

    new_screening_data["date"] = new_screening_data["date"].replace('+00:00', 'Z')
    for key, value in new_screening_data.items():
        assert key in response.data
        assert response.data[key] == value


@pytest.mark.django_db
def test_get_screening_list(client, set_up):
    url = reverse('screening-list')
    response = client.get(url, {}, format='json')

    assert response.status_code == 200
    assert Screening.objects.count() == len(response.data)


@pytest.mark.django_db
def test_get_screening_detail(client, set_up):
    screening = Screening.objects.first()
    url = reverse('screening-detail', kwargs={'pk': screening.pk})
    response = client.get(url, {}, format='json')

    assert response.status_code == 200
    for field in ('movie', 'cinema', 'date'):
        assert field in response.data


@pytest.mark.django_db
def test_delete_screening(client, set_up):
    screening = Screening.objects.first()
    url = reverse('screening-detail', kwargs={'pk': screening.pk})
    response = client.delete(url, {}, format='json')
    assert response.status_code == 204
    screening_ids = [screening.pk for screening in Screening.objects.all()]
    assert screening.pk not in screening_ids


@pytest.mark.django_db
def test_update_screening(client, set_up):
    screening = Screening.objects.first()
    url = reverse('screening-detail', kwargs={'pk': screening.pk})
    response = client.get(url, {}, format='json')
    screening_data = response.data
    new_cinema = Cinema.objects.last()
    screening_data['cinema'] = new_cinema.name
    new_movie = Movie.objects.last()
    screening_data['movie'] = new_movie.title
    response = client.patch(url, screening_data, format='json')
    assert response.status_code == 200
    updated_screening = Screening.objects.get(pk=screening.pk)
    assert updated_screening.cinema == new_cinema
    assert updated_screening.movie == new_movie
