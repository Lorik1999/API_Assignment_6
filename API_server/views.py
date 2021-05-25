from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.exceptions import NotFound
from API_server.models import Pizza
from API_server.models import Topping
from django.core.exceptions import ObjectDoesNotExist
import json

# Create your views here.
pizza_orders = {}

def home(request):
    return render(request,'homepage.html')





# class Get_Pizza(APIView):
@api_view(['GET', 'POST', ])
def get_pizza(request,pizza_id=-1):
    if pizza_id==-1:
        all_pizza={}
        pizza_list= Pizza.objects.all()

        for pizza in pizza_list:

            all_pizza[pizza.pizza_id]={}
            all_pizza[pizza.pizza_id]["pizza_id"]=pizza.pizza_id
            all_pizza[pizza.pizza_id]["name"]=pizza.name
            all_pizza[pizza.pizza_id]["vegetarian"] = pizza.vegetarian
            price=""+str(pizza.price)
            all_pizza[pizza.pizza_id]["price"] = price
            toppings=[]
            for topping in pizza.toppings.all():
                toppings.append(topping.Topping_name)
            all_pizza[pizza.pizza_id]["toppings"]= toppings


        return Response(all_pizza)

    try:
        pizza_obj= Pizza.objects.get(pizza_id=pizza_id)
        Pizza_data = {}
        Pizza_data['pizza_id']=pizza_obj.pizza_id
        Pizza_data['name'] = pizza_obj.name
        Pizza_data['vegetarian'] = pizza_obj.vegetarian
        price = "" + str(pizza_obj.price)
        Pizza_data['price'] = price
        toppings = []
        for topping in pizza_obj.toppings.all():
            toppings.append(topping.Topping_name)
        Pizza_data["toppings"] = toppings
        return Response(Pizza_data)

    except ObjectDoesNotExist:
        errormessage = {
            'message': 'Pizza id not found'
        }
        raise NotFound(detail=errormessage, code=404)

# =========================================================

# function will be used for the api to be displayed.

@api_view(['GET', 'POST', ])
# TODO: use try and accept to catch if json.loads() failes, meaning incorrect format
def order_pizza(request):
    if request.method=='POST':
        data = request.body.decode('utf-8')
        received_json_data = json.loads(data)
        print(received_json_data['pizzas'])
        return Response('Success')
    return Response('Failed')







