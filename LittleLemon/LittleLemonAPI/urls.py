from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('api-token-auth/', obtain_auth_token),
    path('menu-items/', views.menu_items, name='menu_items'),
    path('menu-items/<int:pk>', views.single_menu_items, name='sing_menu_items'),
    path('groups/manager/users', views.manager_view, name='manager_view'),
    path('groups/manager/users/<int:id>',
         views.manager_delete, name='manager_delete'),
    path('groups/delivery-crew/users', views.delivery_view, name="delivery_view"),
    path('groups/delivery-crew/users/<int:id>',
         views.delivery_delete, name='delivery_delete'),
    path('cart/menu-items', views.items_in_cart, name="items_in_cart"),
    path('orders/', views.orders, name="orders"),
    path('orders/<int:id>', views.order_id, name="orders_id")
]
