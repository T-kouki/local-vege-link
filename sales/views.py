from django.shortcuts import render
from django.db.models import Sum
from .models import Order

def sales_home(request):
    return render(request, 'sales/home.html')

def sales_report(request):
    farmer_orders = Order.objects.filter(farmer=request.user)
    total_sales = farmer_orders.aggregate(Sum('total_price'))['total_price__sum'] or 0
    return render(request, 'sales/report.html', {
        'orders': farmer_orders,
        'total_sales': total_sales
    })