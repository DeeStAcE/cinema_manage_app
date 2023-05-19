from random import sample
from faker import Faker
import pytz

from moviebase.settings import TIME_ZONE
from movielist.models import Movie
from showtimes.models import Screening, Cinema

faker = Faker("pl_PL")
TZ = pytz.timezone(TIME_ZONE)


def random_movies():
    # return 3 random movies from db
    movies = list(Movie.objects.all())
    return sample(movies, 3)


def add_screenings(cinema):
    # add 3 random movies for given cinema
    movies = random_movies()
    for movie in movies:
        Screening.objects.create(cinema=cinema, movie=movie, date=faker.date_time(tzinfo=TZ))


def fake_cinema_data():
    # generate fake data for a cinema
    return {
        'name': faker.name(),
        'city': faker.city(),
    }


def create_fake_cinema():
    # create fake cinema with 3 random screenings
    cinema = Cinema.objects.create(**fake_cinema_data())
    add_screenings(cinema)
