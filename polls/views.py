from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def menu(request):
     return render(request, 'registration/menu.html')
def cart(request):
    return render(request,'registration/cart.html') 