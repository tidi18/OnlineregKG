from django.urls import path
from . import views

urlpatterns = [
    path('', views.CompetitionCreateView.as_view(), name='create_competition'),

]