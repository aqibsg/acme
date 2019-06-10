from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from .models import Product

import pandas as pd
import numpy as np

def index(request):
    if request.method == 'POST':
        prod = pd.read_csv(request.FILES['csv_file'])
        actv = pd.Series(np.random.randint(0, 2, size=prod.shape[0], dtype=np.uint8).view(bool), name='active')
        prd = pd.concat([prod, actv], axis=1)
        for index,row in prd.iterrows():
            defaults={'name': row[0], 'description': row[2],'active': row[3]}
            try:
                obj = Product.objects.get(sku=row[1])
                for key, value in defaults.items():
                    setattr(obj, key, value)
                obj.save()
            except Product.DoesNotExist:
                new_values = {'sku': row[1]}
                new_values.update(defaults)
                obj = Product(**new_values)
                obj.save()

        prd_list = Product.objects.all() # limiting contacts based on current_page
        paginator = Paginator(prd_list, 100)

        page = request.GET.get('page', 1)
        prd_list = paginator.get_page(page)

        return redirect('/products/')

    return render(request, 'index.html')

def search(request):
    query = request.GET.get("query")
    if query:
        lookups = Q(name__icontains=query) | Q(sku__icontains=query)
        prd_list = Product.objects.filter(lookups).distinct()
        paginator = Paginator(prd_list, 100)

        page = request.GET.get('page', 1)
        prd_list = paginator.get_page(page)

        return render(request, 'products.html', {'products': prd_list})  

    if request.GET.get('active'):
        active_filter = request.GET.get('active')
        if active_filter=='None':
            prd_list = Product.objects.all()
        else:
            prd_list = Product.objects.filter(active=active_filter)
        
        paginator = Paginator(prd_list, 100)
        page = request.GET.get('page', 1)
        prd_list = paginator.get_page(page)
        return render(request, 'products.html', {'products': prd_list})

    prd_list = Product.objects.get_queryset().order_by('sku') # limiting contacts based on current_page
    paginator = Paginator(prd_list, 100)

    page = request.GET.get('page', 1)
    prd_list = paginator.get_page(page)
    return render(request, 'products.html', {'products': prd_list})

def delete(request):
    Product.objects.all().delete()
    return redirect('/', name='index')