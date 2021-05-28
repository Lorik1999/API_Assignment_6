import logging

from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.exceptions import NotFound
from API_server.models import Pizza
from API_server.models import Topping
from API_server.models import Pizza_Ordered
from django.core.exceptions import ObjectDoesNotExist
from API_server.models import Order
from django.contrib import messages
import json
from datetime import datetime,timedelta, timezone
import requests
# Create your views here.
pizza_orders = {}

def home(request):
    # httpReq gets the chosen req
    # URL gets the url
    if request.method == "POST":
        httpReq = request.POST.get('httpReq')
        url = request.POST.get("URL")

        if url == "":
            messages.add_message(request, messages.INFO,
                                 'Please choose a url')
            return render(request, 'base.html')

        if httpReq != "POST" and httpReq != "GET" and httpReq != "PUT":
            messages.add_message(request, messages.INFO,
                                 'Please choose a http request')
            return render(request, 'base.html')

        if httpReq == "GET":
            r = requests.get(url)

            return render(request, 'base.html', {'data': r.text})

        if httpReq == "POST":
            jsonDataFromUser = request.POST.get("jsonData")
            r = requests.post(url, data=jsonDataFromUser)

            return render(request, 'base.html', {'data': r.text})

        if httpReq == "PUT":
            r = requests.put(url)
            return render(request, 'base.html', {'data': r.text})

    return render(request, 'base.html')



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
def get_delivery_time(request, order_id=-1):
    if request.method == 'GET':
        try:
            order = Order.objects.get(id=order_id)
            if order.cancelled:
                return Response('Order was cancelled')
            return_data = {}
            return_data['order'] = {}
            ordered_pizza_obj = order.pizzas.all()
            pizza_ids = []
            for ordered_pizza in ordered_pizza_obj:
                for i in range(ordered_pizza.number_ordered):
                    for p in ordered_pizza.pizza.all():
                        pizza_ids.append(p.pizza_id)
            return_data['order']['pizzas'] = pizza_ids
            return_data['order']['ordered_at'] = order.ordered_at
            return_data['order']['status'] = order.status
            return_data['order']['customer_id'] = order.customer_id
            current_time = datetime.now()
            delivery_time = order.delivery_time
            time_remaining = delivery_time - current_time
            sec_value = time_remaining.seconds % (24 * 3600)
            hour_value = sec_value // 3600
            sec_value %= 3600
            min_value = sec_value // 60
            sec_value %= 60


            time_remaining_formatted = "Hours: {hour}, mins: {min}".format(hour=hour_value, min=min_value)
            return_data['delivery_time'] = time_remaining_formatted

            return Response(return_data)
        except Exception as e:
            print(e)
            invalid_message = {
                'message': 'Order not found'
            }
            raise NotFound(detail=invalid_message, code=404)

    return Response("Not a GET request")

@api_view(['GET', 'POST', ])
def order_pizza(request, order_id=-1):
    if request.method=='POST':
        try:
            data = request.body.decode('utf-8')
            received_json_data = json.loads(data)

            current_time= datetime.now()
            time_diff= timedelta(hours=1)
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

            pizza_counter = {}
            for id in received_json_data['pizzas']:
                pizza_counter[id] = received_json_data['pizzas'].count(id)

            for id, num in pizza_counter.items():
                pizza_ordered_obj = Pizza_Ordered(number_ordered=int(num))
                pizza_ordered_obj.save()
                pizza_obj = Pizza.objects.get(pizza_id=int(id))
                pizza_ordered_obj.pizza.add(pizza_obj)
                pizza_ordered_obj.save()
                order.pizzas.add(pizza_ordered_obj)

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

    if request.method=='GET':
        try:
            n=int(order_id)
        except Exception as e:
            invalid_message= {
                'message':'Invalid id supplied'
            }
            raise NotFound(detail=invalid_message,code=400)
        try:
            order= Order.objects.get(id=order_id)
            if order.cancelled:
                return Response('This order has been cancelled. Please order again')
            return_data= {}
            return_data['id']= order.id
            return_data['customer_id']=order.customer_id
            return_data['status']=order.status
            return_data['ordered_at']=order.ordered_at
            return_data['note']=order.note
            return_data['takeaway']=order.takeaway
            return_data['payment_type']=order.payment_type
            return_data['delivery_address']={}
            return_data['delivery_address']['street']=order.street
            return_data['delivery_address']['city']= order.city
            return_data['delivery_address']['country']=order.country
            return_data['delivery_address']['zipcode']=order.zipcode
            pizzas= []
            pizza_ordered_objs= order.pizzas.all()
            for pizza_ordered in pizza_ordered_objs:
                for number_ordered in range(pizza_ordered.number_ordered):
                    for p in pizza_ordered.pizza.all():

                        pizza_data={}
                        pizza_data['pizza_id']=p.pizza_id
                        pizza_data['name']= p.name
                        pizza_data['vegetarian']=p.vegetarian
                        pizza_data['price']=p.price
                        pizzas.append(pizza_data)
            return_data['pizzas']=pizzas
            return Response(return_data)

        except Exception as e:
            print(e)
            errormessage= {
                'message':'Order_id not found'
            }
            raise NotFound(detail=errormessage,code=404)
    return Response('failed')


@api_view(['GET', 'POST','PUT' ])
def cancel_order(request, order_id=-1):
    if request.method=='PUT':
        try:
            order = Order.objects.get(id=order_id)
            order_time_placed = order.ordered_at
            time_now = datetime.now()
            time_diff = time_now - order_time_placed
            # if 5 mins has passed
            if time_diff.seconds > 300:
                message = {
                    '412': 'Cancellation cannot be performed because 5 minutes has elapsed from order time'
                }
                return Response(message)

            if (order.delivery_time - datetime.now()).seconds < 0 or order.cancelled:
                message = {
                    '422': 'Cancellation failed because it has already been cancelled or delivered.'
                }
                return Response(message)

            # otherwise cancel the order
            order.cancelled = True
            order.save()
            return_date = {}
            return_date['order_id'] = order_id
            return_date['status'] = 'cancelled'
            return Response(return_date)

        except Exception as e:
            print('at line 232' + str(e))
            message = {
                '404': 'Order ID not found'
            }
            raise NotFound(detail=message, code=404)










