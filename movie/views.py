from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def home(request):
    #return HttpResponse('<h1>Welcome to Home Page</h1>')  # Con esta opcion cuando se hace el request se hace 'quemando' el html
    #return render(request, 'home.html') # Con esta opcion se accede al archivo HTML de la carpeta templates
    return render(request, 'home.html', {'name':'Camilo Monsalve'})

def about(request):
    return HttpResponse('<h1>Welcome to About Page</h1>')