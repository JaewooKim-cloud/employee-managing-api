from django.urls import path, include
from . import views

from rest_framework.authtoken.views import obtain_auth_token



urlpatterns = [
    path("menu-items/",views.menu_items),
    path("menu-items/<str:title>",views.signle_item),
    path('secret/',views.secret),
    path('api-token-auth/',obtain_auth_token),
    path('groups/manager/users',views.manager_edit),
    path('groups/manager/users/<int:id>',views.manager_delete),
    path('throttle-check/',views.throttle_check),
    path('throttle-check-auth/',views.throttle_check_auth),
    path('cart/',views.cart_view),
    path('groups/delivery-crew/users',views.delivery_crew_edit),
    path('groups/delivery-crew/users/<int:id>',views.delivery_crew_delete),
    path('orders/',views.orders_view),

]
