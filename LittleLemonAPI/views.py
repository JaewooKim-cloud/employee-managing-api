from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import MenuItem,carts, orders
from .serializers import MenuItemSerializer, CartSerializer,MenuItemUpdateSerializer, OrdersSerializer
from rest_framework import status

from django.shortcuts import get_object_or_404

from django.core.paginator import Paginator, EmptyPage

from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes

from rest_framework.throttling import AnonRateThrottle
from rest_framework.throttling import UserRateThrottle
from rest_framework.decorators import throttle_classes
from .throttles import TenCallsPerMinute

from django.http import HttpResponse
from django.contrib.auth.models import User,Group

from rest_framework import viewsets

from .serializers import CurrentUserSerializer

# Create your views here.

@api_view(["GET","POST"])
def menu_items(request):
    if request.method=="GET":
        items=MenuItem.objects.select_related('category').all()
        category_name = request.query_params.get('category')
        to_price = request.query_params.get('to_price')
        search = request.query_params.get('search')
        ordering = request.query_params.get('ordering')

        #perpage = request.query_params.get('perpage',default=2)
        #page = request.query_params.get('page',default=1)

        if category_name:
            items = items.filter(category__title=category_name)
        if to_price:
            items = items.filter(price__lte=to_price) #lte is conditional operator(less  than or equal to)
            #items = items.filter(price=to_price)

        if search:
            items = items.filter(title__istartswith=search) #lte is conditional operator(less  than or equal to)
        
        if ordering:
            #items = items.order_by(ordering)
            ordering_fields = ordering.split(",")
            items = items.order_by(*ordering_fields)

        #paginator = Paginator(items,per_page=perpage)
        #try:
        #    items = paginator.page(number=page)
        #except EmptyPage:
        #    items = []




        serialized_item = MenuItemSerializer(items,many=True)
        return Response(serialized_item.data)
    elif not request.user.groups.filter(name='Manager').exists():
        return Response({"message":"You are not authorized."}, status.HTTP_403_FORBIDDEN)
        
    elif request.method=="POST":
        serialized_item=MenuItemSerializer(data=request.data)
        serialized_item.is_valid(raise_exception=True)
        serialized_item.save()
        return Response(serialized_item.data, status.HTTP_201_CREATED)

@api_view(["GET","PUT","PATCH","DELETE"])
def signle_item(request,title):
    #item=MenuItem.objects.get(pk=id)
    if request.method=="GET":
        item = get_object_or_404(MenuItem,title=title)
        serialized_item = MenuItemSerializer(item)
        return Response(serialized_item.data)
    elif not request.user.groups.filter(name='Manager').exists():
        return Response({"message":"You are not authorized."}, status.HTTP_403_FORBIDDEN)
    elif request.method=="PUT" or request.method=="PATCH":
        #temp=MenuItemSerializer.objects.filter(title=request.data['title'])
        temp = get_object_or_404(MenuItem,title=title)
        temp.delete()
        serialized_item=MenuItemSerializer(data=request.data)
        serialized_item.is_valid(raise_exception=True)
        serialized_item.save()
        return Response(serialized_item.data, status.HTTP_200_OK)
    elif request.method=="DELETE":
        temp = get_object_or_404(MenuItem,title=title)
        temp.delete()
        return HttpResponse('deleted')



@api_view()
@permission_classes([IsAuthenticated])
def secret(request):
    return Response({"message" : "Some secret message"})


    
@api_view()
@throttle_classes([AnonRateThrottle])
def throttle_check(request):
    return Response({"message":"successful"})

@api_view()
@permission_classes([IsAuthenticated])
#@throttle_classes([UserRateThrottle])
@throttle_classes([TenCallsPerMinute])
def throttle_check_auth(request):
    return Response({"message":"message for the logged in users only"})



@api_view(["GET","POST","DELETE"])
@permission_classes([IsAuthenticated])
def cart_view(request):
    if request.user.groups.filter(name='Manager').exists():
        return Response({"message":"You Are Not Authorized!"})
    elif request.user.groups.filter(name='Delivery crew').exists():
        return Response({"message":"You Are Not Authorized!"})
    else:
        if request.method=="GET": #username=request.user.username
            items=carts.objects.filter(username=request.user.username)
            serialized_item = CartSerializer(items,many=True)
            return Response(serialized_item.data)
      




        if request.method == "POST":
            temp=carts.objects.filter(username=request.user.username)
            temp.delete()

            request.data.update({"username": request.user.username})
            serialized_item=CartSerializer(data=request.data)
            serialized_item.is_valid(raise_exception=True)
            serialized_item.save()
            return Response(serialized_item.data, status.HTTP_201_CREATED)
        
        if request.method == "DELETE":
            temp=carts.objects.filter(username=request.user.username)
            temp.delete()
            return HttpResponse('deleted')
        
@api_view(["GET","POST"])
@permission_classes([IsAuthenticated])
def manager_edit(request):
    if request.user.groups.filter(name='Manager').exists():
        if request.method=="GET":
            users = User.objects.filter(groups__name='Manager')
            values=users.values()

            return Response(values)
        if request.method == "POST":
            new_manager_username=request.data['username']
            new_manager = User.objects.get(username=new_manager_username)
            
            group = Group.objects.get(name="Manager")
            group.user_set.add(new_manager)
            
            return Response(status.HTTP_200_OK)
           


    else:
        return Response({"message":"You Are Not Authorized!"},status.HTTP_403_FORBIDDEN)
    

@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def manager_delete(request,id):
    if request.user.groups.filter(name='Manager').exists():
            new_manager = User.objects.get(id=id)
            
            group = Group.objects.get(name="Manager")
            group.user_set.remove(new_manager)
            
            return Response(status.HTTP_200_OK)



    else:
        return Response({"message":"You Are Not Authorized!"},status.HTTP_403_FORBIDDEN)
    



@api_view(["GET","POST"])
@permission_classes([IsAuthenticated])
def delivery_crew_edit(request):
    if request.user.groups.filter(name='Manager').exists():
        if request.method=="GET":
            users = User.objects.filter(groups__name='Delivery crew')
            values=users.values()

            return Response(values)
        if request.method == "POST":
            new_crew_username=request.data['username']
            new_crew = User.objects.get(username=new_crew_username)
            
            group = Group.objects.get(name="Delivery crew")
            group.user_set.add(new_crew)
            
            return Response(status.HTTP_200_OK)
           


    else:
        return Response({"message":"You Are Not Authorized!"},status.HTTP_403_FORBIDDEN)
    

@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delivery_crew_delete(request,id):
    if request.user.groups.filter(name='Manager').exists():
            new_crew = User.objects.get(id=id)
            
            group = Group.objects.get(name="Delivery crew")
            group.user_set.remove(new_crew)
            
            return Response(status.HTTP_200_OK)



    else:
        return Response({"message":"You Are Not Authorized!"},status.HTTP_403_FORBIDDEN)
    
@api_view(["GET","POST"])
@permission_classes([IsAuthenticated])
def orders_view(request):
    if request.user.groups.filter(name='Manager').exists():
            all_orders=orders.objects.all()
            serialized_item = OrdersSerializer(all_orders,many=True)


            return Response(serialized_item.data,status.HTTP_200_OK)



    elif request.user.groups.filter(name='Delivery crew').exists():
        return Response({"message":"You Are Not Authorized!"},status.HTTP_403_FORBIDDEN)

    else:
        if request.method=="POST":
            request.data.update({"username": request.user.username})
            serialized_item=OrdersSerializer(data=request.data)
            serialized_item.is_valid(raise_exception=True)
            serialized_item.save()
            return Response(serialized_item.data, status.HTTP_201_CREATED)

        if request.method=="GET":
            items=orders.objects.filter(username=request.user.username)
            serialized_item = OrdersSerializer(items,many=True)


            return Response(serialized_item.data,status.HTTP_200_OK)