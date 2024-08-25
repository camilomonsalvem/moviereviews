from django.shortcuts import render
from django.http import HttpResponse

from .models import Movie

import matplotlib.pyplot as plt
import matplotlib
import io
import urllib, base64

# Create your views here.

def home(request):
    #return HttpResponse('<h1>Welcome to Home Page</h1>')  # Con esta opcion cuando se hace el request se hace 'quemando' el html
    #return render(request, 'home.html') # Con esta opcion se accede al archivo HTML de la carpeta templates
    #return render(request, 'home.html', {'name':'Camilo Monsalve'})
    searchTerm = request.GET.get('searchMovie')
    if searchTerm:
        movies = Movie.objects.filter(title=searchTerm)
    else:
        movies = Movie.objects.all()
    return render(request, 'home.html', {'searchTerm': searchTerm, 'movies': movies})

def about(request):
    #return HttpResponse('<h1>Welcome to About Page</h1>')
    return render(request, 'about.html')

def signup(request):
    email = request.GET.get('email')
    return render(request, 'signup.html', {'email':email})

def statistics_view(request):
    matplotlib.use('Agg')
    
    # Obtener todas las películas
    all_movies = Movie.objects.all()
    
    # Crear diccionarios para almacenar la cantidad de películas por año y por género
    movie_counts_by_year = {}
    movie_counts_by_genre = {}
    
    # Filtrar las películas por año y contar la cantidad de películas por año y por el primer género
    for movie in all_movies:
        year = movie.year if movie.year else "None"
        genre = movie.genre.split(',')[0].strip() if movie.genre else "None"
        
        if year in movie_counts_by_year:
            movie_counts_by_year[year] += 1
        else:
            movie_counts_by_year[year] = 1
        
        if genre in movie_counts_by_genre:
            movie_counts_by_genre[genre] += 1
        else:
            movie_counts_by_genre[genre] = 1

    # Ancho de las barras
    bar_width = 0.5
    
    # Posiciones de las barras para el gráfico de películas por año
    year_bar_positions = range(len(movie_counts_by_year))
    
    # Crear la gráfica de barras para películas por año
    plt.bar(year_bar_positions, movie_counts_by_year.values(), width=bar_width, align='center')
    plt.title('Movies per year')
    plt.xlabel('Year')
    plt.ylabel('Number of movies')
    plt.xticks(year_bar_positions, movie_counts_by_year.keys(), rotation=90)
    plt.subplots_adjust(bottom=0.3)
    
    # Guardar la gráfica de películas por año en un objeto BytesIO
    buffer_year = io.BytesIO()
    plt.savefig(buffer_year, format='png')
    buffer_year.seek(0)
    plt.close()
    
    # Convertir la gráfica a base64
    image_year_png = buffer_year.getvalue()
    buffer_year.close()
    graphic_year = base64.b64encode(image_year_png).decode('utf-8')
    
    # Posiciones de las barras para el gráfico de películas por género
    genre_bar_positions = range(len(movie_counts_by_genre))
    
    # Crear la gráfica de barras para películas por género
    plt.bar(genre_bar_positions, movie_counts_by_genre.values(), width=bar_width, align='center', color='orange')
    plt.title('Movies per genre')
    plt.xlabel('Genre')
    plt.ylabel('Number of movies')
    plt.xticks(genre_bar_positions, movie_counts_by_genre.keys(), rotation=90)
    plt.subplots_adjust(bottom=0.3)
    
    # Guardar la gráfica de películas por género en un objeto BytesIO
    buffer_genre = io.BytesIO()
    plt.savefig(buffer_genre, format='png')
    buffer_genre.seek(0)
    plt.close()
    
    # Convertir la gráfica a base64
    image_genre_png = buffer_genre.getvalue()
    buffer_genre.close()
    graphic_genre = base64.b64encode(image_genre_png).decode('utf-8')
    
    # Renderizar la plantilla statistics.html con ambas gráficas
    return render(request, 'statistics.html', {'graphic_year': graphic_year,'graphic_genre': graphic_genre})

