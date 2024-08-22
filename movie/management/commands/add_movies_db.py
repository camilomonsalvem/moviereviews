from django.core.management.base import BaseCommand
from movie.models import Movie
import os
import json

class Command(BaseCommand):
    help = 'Load movies from movie_descriptions.json into the Movie Model'
    
    def handle(self, *args, **kwargs):
        json_file_path = 'movie/management/commands/movies.json'
        
        with open(json_file_path, 'r') as file:
            movies = json.load(file)
        
        for i in range(100):
            movie = movies[i]
            exist = Movie.objects.filter(title = movie['Series_Title']).first()
            if not exist:
                Movie.objects.create(title = movie['Series_Title'],
                                     image = 'movie/images/default.png',
                                     genre = movie['Genre'],
                                     year = movie['Released_Year'])