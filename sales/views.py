from django.shortcuts import render
from .models import Sale

def sales_home(request):
    sales = Sale.objects.all().order_by('-date')
    return render(request, 'sales/home.html', {'sales': sales})
