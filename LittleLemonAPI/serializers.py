from rest_framework import serializers
from .models import MenuItem, carts, orders
from decimal import Decimal
from .models import Category
from django.contrib.auth import models as usermd

from rest_framework.validators import UniqueValidator
from rest_framework.validators import UniqueTogetherValidator

import bleach

from django.contrib.auth.models import User

# class MenuItemSerializer(serializers.Serializer):
#     id = serializers.IntegerField()
#     title = serializers.CharField(max_length=255)
#     price = serializers.DecimalField(max_digits=6, decimal_places=2)
#     inventory = serializers.IntegerField()

class CategorySerializer (serializers.ModelSerializer):
    class Meta:
        model = Category
        fields=["id","slug","title"]

class MenuItemSerializer(serializers.ModelSerializer):
    stock = serializers.IntegerField(source="inventory")
    price_after_tax = serializers.SerializerMethodField(method_name='calculate_tax')
    category = CategorySerializer(read_only=True)#category = CategorySerializer()#serializers.StringRelatedField()
    category_id = serializers.IntegerField(write_only=True)

    #price = serializers.DecimalField(max_digits=6, decimal_places=2, min_value=2)
    title = serializers.CharField(
             max_length=255,
            validators=[UniqueValidator(queryset=MenuItem.objects.all())]
        )
    def validate_title(self, value):
        return bleach.clean(value)
    class Meta:
        model = MenuItem
        fields= ["id","title","price",'stock','price_after_tax','category','category_id']
        extra_kwargs = {'price': {'min_value': 2},'stock':{'source':'inventory', 'min_value': 0}, 
                     'title': {
                        'validators': [
                            UniqueValidator(
                                queryset=MenuItem.objects.all()
                            )
                        ]
            }
        }  
                        


    def calculate_tax(self, product:MenuItem):
        return product.price * Decimal(1.1)
    

class CartSerializer(serializers.ModelSerializer):
    
    #price = serializers.DecimalField(max_digits=6, decimal_places=2, min_value=2)
    username = serializers.CharField(
             max_length=255,
            #validators=[UniqueValidator(queryset=carts.objects.all())]
        )
    
    class Meta:
        model = carts
        fields= ["id","username","title_quantity"]
"""         extra_kwargs = { 
                     'username': {
                        'validators': [
                            UniqueValidator(
                                queryset=carts.objects.all()
                            )
                        ]
            }
        }   """
                        


class MenuItemUpdateSerializer(serializers.ModelSerializer):
    stock = serializers.IntegerField(source="inventory")
    price_after_tax = serializers.SerializerMethodField(method_name='calculate_tax')
    category = CategorySerializer(read_only=True)#category = CategorySerializer()#serializers.StringRelatedField()
    category_id = serializers.IntegerField(write_only=True)

    #price = serializers.DecimalField(max_digits=6, decimal_places=2, min_value=2)
    title = serializers.CharField(
             max_length=255,
            
        )
    def validate_title(self, value):
        return bleach.clean(value)
    class Meta:
        model = MenuItem
        fields= ["id","title","price",'stock','price_after_tax','category','category_id']
        extra_kwargs = {'price': {'min_value': 2},'stock':{'source':'inventory', 'min_value': 0}, 
                     'title': {
                        'validators': [
                            UniqueValidator(
                                queryset=MenuItem.objects.all()
                            )
                        ]
            }
        }  
                        


    def calculate_tax(self, product:MenuItem):
        return product.price * Decimal(1.1)
    

class CurrentUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'id')

class OrdersSerializer(serializers.ModelSerializer):
    class Meta:
        model = orders
        fields= ["username","items_quantity"]
