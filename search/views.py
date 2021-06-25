from django.shortcuts import render
from product.models import Product
from django.db.models import Q

def searchResult(request):
    products = None
    query = None
    if 'q' in request.GET:
        query = request.GET.get('q')
        products = Product.objects.all().filter(Q(name__icontains=query) | Q(description__icontains=query) | Q(category__category__iexact=query) | Q(category__slug__icontains=query) ).distinct()

    return render(request, 'sresult.html', {'query':query, 'products':products})
