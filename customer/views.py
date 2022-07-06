from django.shortcuts import render
from django.http import JsonResponse

from typing import List

from customer.models import Customer

from . import views, scripts as F
from .models import Customer

# Create your views here.
def create_user(request):
    q = Customer(customer_name=request.GET.get("customer_name"))
    q.save()
    return JsonResponse({"customers" : F.customers_from_id([q.customer_id])})

def get_customers_info(request):
    return JsonResponse({"customers" : F.customers_from_id(list(map(int, request.GET.get("customer_ids").split(","))))})
