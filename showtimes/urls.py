from django.urls import path
from showtimes.views import *

urlpatterns = [
    path('cinemas/', CinemaListView.as_view(), name='cinemas-list'),
    path('cinemas/<int:pk>', CinemaView.as_view(), name='cinema-detail'),
    path('screenings/', ScreeningListView.as_view(), name='screening-list'),
    path('screenings/<int:pk>', ScreeningView.as_view(), name='screening-detail'),
]
