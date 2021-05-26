from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.exceptions import NotFound
from API_server.models import Pizza
from API_server.models import Topping
from django.core.exceptions import ObjectDoesNotExist
from API_server.models import Order
import json
from datetime import datetime,timedelta
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
        try:
            data = request.body.decode('utf-8')
            received_json_data = json.loads(data)
            print(received_json_data['pizzas'])
            current_time= datetime.now()
            time_diff= timedelta(days=0,hours=1,minutes=0)
            delivery_time= current_time+time_diff
            order=Order(takeaway=received_json_data['takeaway'],
                        payment_type=received_json_data['payment_type'],
                        customer_id=received_json_data['customer_id'],
                        note=received_json_data['note'],
                        street=received_json_data['delivery_address']['street'],
                        city=received_json_data['delivery_address']['street'],
                        country=received_json_data['delivery_address']['country'],
                        zipcode=received_json_data['delivery_address']['zipcode'],
                        ordered_at=datetime.now(),
                        status='in progress',
                        delivery_time=delivery_time
                        )
            order.save()
            for id in received_json_data['pizzas']:
                pizza_obj= Pizza.objects.get(pizza_id=id)
                order.pizzas.add(pizza_obj)
            order.save()


            return_data= {}
            return_data['order']={}
            return_data['order']['order_id']=order.id
            return_data['order']['ordered_at'] = order.ordered_at
            return_data['order']['status']=order.status
            return_data['delivery_time']= order.delivery_time

            return Response(return_data)
        except Exception as e:
            print(e)
            errormessage= {
                'message':'The format of the object is invalid'
            }
            raise NotFound(detail=errormessage,code=400)
    return Response('Failed')







