from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser
from rest_framework.response import Response
from rest_framework import status

from .models import MenuItem, Cart, Order, OrderItem
from django.contrib.auth.models import User, Group
from .serializers import MenuItemSerializer, UserSerializer, GroupSerializer, CartSerializer, OrderSerializer, OrderItemSerializer

from .permissions import IsDeliveryCrew, IsManager, IsCustomer
from datetime import date
# Create your views here.


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
def menu_items(request):
    if request.method == 'GET':
        items = MenuItem.objects.all()
        serialized_items = MenuItemSerializer(items, many=True)
        return Response(serialized_items.data, status.HTTP_200_OK)

    if request.method == 'POST':
        if request.user.is_authenticated and (request.user.groups.filter(name="Manager").exists() or IsAdminUser()):
            serialized_item = MenuItemSerializer(data=request.data)
            serialized_item.is_valid(raise_exception=True)
            serialized_item.save()
            return Response(serialized_item.data, status.HTTP_201_CREATED)
        else:
            return Response({"message": "unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
@permission_classes([IsAuthenticatedOrReadOnly])
def single_menu_items(request, pk):

    item = get_object_or_404(MenuItem, pk=pk)

    if request.method == 'GET':
        serialized_items = MenuItemSerializer(item)
        return Response(serialized_items.data, status.HTTP_200_OK)
    elif request.method == 'DELETE':
        if request.user.is_authenticated and (request.user.groups.filter(name="Manager").exists() or IsAdminUser()):
            item.delete()
            return Response({"Successfully deleted"}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)
    elif request.method == 'PATCH':
        if request.user.is_authenticated and (request.user.groups.filter(name="Manager").exists() or IsAdminUser()):

            # Check if the request body is empty
            if not request.data:
                return Response({"message": "Request body cannot be empty"}, status=status.HTTP_400_BAD_REQUEST)

            serializer = MenuItemSerializer(
                item, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "Successfully udpated"}, status=status.HTTP_200_OK)
            else:
                return Response({"message": "The fields is wrong"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message": "unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)
    elif request.method == 'PUT':
        if request.user.is_authenticated and (request.user.groups.filter(name="Manager").exists() or IsAdminUser()):

            # Check if the request body is empty
            if not request.data:
                return Response({"message": "Request body cannot be empty"}, status=status.HTTP_400_BAD_REQUEST)

            serializer = MenuItemSerializer(
                item, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "Successfully udpated"}, status=status.HTTP_200_OK)
            else:
                return Response({"message": "The fields is wrong"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message": "unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)
    else:
        return Response({"message": "unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)


@ api_view(['GET', 'POST'])
@ permission_classes([IsAuthenticated, IsManager | IsAdminUser])
def manager_view(request):

    if request.method == 'GET':
        users = User.objects.filter(groups__name='Manager')
        serialized_users = UserSerializer(users, many=True)
        return Response(serialized_users.data, status=status.HTTP_200_OK)

    if request.method == 'POST':
        username = request.data.get('username')
        if not username:
            return Response({"message": "Username not provided"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        try:
            manager_group = Group.objects.get(name="Manager")
        except Group.DoesNotExist:
            return Response({"message": "manager group does not exist"}, status=status.HTTP_404_NOT_FOUND)

        user.groups.add(manager_group)
        return Response({"message": "User assigned to Manager group."}, status=status.HTTP_201_CREATED)


@ api_view(['DELETE'])
@ permission_classes([IsAuthenticated, IsManager | IsAdminUser])
def manager_delete(request, id):
    try:
        user = User.objects.get(id=id)
    except User.DoesNotExist:
        return Response({"message": "user not found"}, status=status.HTTP_404_NOT_FOUND)

    try:
        manager_group = Group.objects.get(name="Manager")
    except Group.DoesNotExist:
        return Response({"message": "manager group does not exist"}, status=status.HTTP_404_NOT_FOUND)

    # Check if the user not in manager group
    if user.groups.filter(name="Manager").exists():
        user.groups.remove(manager_group)
        return Response({"message": "Successfully removed user from Manager Group"}, status=status.HTTP_200_OK)
    else:
        return Response({"message": "User doesnot exist in Manager Group"}, status=status.HTTP_404_NOT_FOUND)


@ api_view(['GET', 'POST'])
@ permission_classes([IsAuthenticated, IsManager | IsAdminUser])
def delivery_view(request):
    if request.method == 'GET':
        users = User.objects.filter(groups__name='Delivery Crew')
        serialized_user = UserSerializer(users, many=True)
        return Response(serialized_user.data, status=status.HTTP_200_OK)
    if request.method == 'POST':
        username = request.data.get('username')
        if not username:
            return Response({"message": "Username not provided"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        try:
            delivery_group = Group.objects.get(name="Delivery Crew")
        except Group.DoesNotExist:
            return Response({"message": "delivery group doesnot exist"}, status=status.HTTP_404_NOT_FOUND)

        # Check if the user already in delivery group
        if user.groups.filter(name="Delivery Crew").exists():
            return Response({"message": "The user is already in Delivery Group"}, status=status.HTTP_400_BAD_REQUEST)

        user.groups.add(delivery_group)

        serialized_group = GroupSerializer(delivery_group)
        return Response(serialized_group.data, status=status.HTTP_201_CREATED)


@ api_view(['DELETE'])
@ permission_classes([IsAuthenticated, IsAdminUser | IsManager])
def delivery_delete(request, id):
    try:
        user = User.objects.get(id=id)
    except User.DoesNotExist:
        return Response({"message": "user not found"}, status=status.HTTP_404_NOT_FOUND)

    try:
        delivery_group = Group.objects.get(name="Delivery Crew")
    except Group.DoesNotExist:
        return Response({"message": "delivery group doesnot exist"}, status=status.HTTP_404_NOT_FOUND)

    # check if the user not in delivery group
    if user.groups.filter(name="Delivery Crew").exists():
        user.groups.remove(delivery_group)
        return Response({"message": "Successfully removed user from Manager Group"}, status=status.HTTP_200_OK)
    else:
        return Response({"message": "User doesnot exist in Manager Group"}, status=status.HTTP_404_NOT_FOUND)


@ api_view(['GET', 'POST', "DELETE"])
@permission_classes([IsAuthenticated, IsCustomer])
def items_in_cart(request):
    if request.method == 'GET':
        items = Cart.objects.all()
        serialized_items = CartSerializer(items, many=True)
        return Response(serialized_items.data, status.HTTP_200_OK)

    if request.method == 'POST':
        try:
            id = request.data['menuitem']
            quantity = request.data['quantity']
        except:
            return Response({"message": "Please provide the id of the item and quantity"}, status=status.HTTP_400_BAD_REQUEST)
        item = get_object_or_404(MenuItem, id=id)
        price = int(quantity) * item.price
        try:
            Cart.objects.create(user=request.user, quantity=quantity,
                                unit_price=item.price, price=price, menuitem_id=id)
        except:
            return Response({"message": "Item already in cart"}, status=status.HTTP_409_CONFLICT)
        return Response({"Successfully added to cart"}, status=status.HTTP_201_CREATED)

    if request.method == 'DELETE':
        try:
            id = request.data['menuitem']
        except:
            return Response({"message": "Please provide the id of the item"}, status=status.HTTP_400_BAD_REQUEST)
        item = get_object_or_404(MenuItem, id=id)
        cart = get_object_or_404(Cart, user=request.user, menuitem=item)
        cart.delete()
        return Response({"Successfully removed from cart"}, status=status.HTTP_200_OK)


@ api_view(['GET', 'POST'])
@ permission_classes([IsAuthenticated])
def orders(request):
    if request.method == 'GET':
        if request.user.groups.filter(name="Manager").exists():
            user_orders = Order.objects.all()
            serialized_order = OrderSerializer(user_orders, many=True)
            return Response(serialized_order.data, status=status.HTTP_200_OK)
        elif request.user.groups.filter(name="Delivery Crew").exists():
            user_orders = Order.objects.filter(user=request.user)
            serialized_order = OrderSerializer(user_orders, many=True)
            return Response(serialized_order.data, status=status.HTTP_200_OK)
        else:
            user_orders = Order.objects.filter(user=request.user)
            serialized_order = OrderSerializer(user_orders, many=True)
            return Response(serialized_order.data, status=status.HTTP_200_OK)
    if request.method == 'POST':
        if not request.user.groups.filter(name="Manager").exists() and not request.user.groups.filter(name="Delivery Crew").exists():
            cart = Cart.objects.filter(user=request.user)
            if not cart.exists():
                return Response({"Cart is empty"}, status=status.HTTP_400_BAD_REQUEST)

            total = sum(float(item['price']) for item in cart.values('price'))
            order = Order.objects.create(
                user=request.user, status=False, total=total, date=date.today())
            for item in cart.values():
                menuitem = get_object_or_404(MenuItem, id=item["menuitem_id"])
                orderitem = OrderItem.objects.create(
                    order=order, menuitem=menuitem, quantity=item['quantity'], unit_price=item['unit_price'], price=item['price'])
                orderitem.save()
            cart.delete()
            return Response({"message": "You order has been placed!"}, status=status.HTTP_201_CREATED)


@ api_view(['GET', "PUT", 'PATCH', 'DELETE'])
@ permission_classes([IsAuthenticated])
def order_id(request, id):
    order = get_object_or_404(Order, id=id)
    if request.method == 'GET':
        if not request.user.groups.filter(name="Manager").exists() and not request.user.groups.filter(name="Delivery Crew").exists():
            if order.user != request.user:
                return Response({"message": "You are not authorized to view this order."}, status=status.HTTP_403_FORBIDDEN)

            ItemInOrder = OrderItem.objects.filter(order=order)
            serialized_items = OrderItemSerializer(ItemInOrder, many=True)
            return Response(serialized_items.data, status=status.HTTP_200_OK)
        else:
            return Response({"message": "unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

    if request.method == 'PUT':
        if not request.user.groups.filter(name="Manager").exists() and not request.user.groups.filter(name="Delivery Crew").exists():
            if order.user != request.user:
                return Response({"message": "You are not authorized to change this order."}, status=status.HTTP_403_FORBIDDEN)
            if not request.data:
                return Response({"message": "Fill up all the fields"}, status=status.HTTP_400_BAD_REQUEST)
            serializer = OrderItemSerializer(order, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "Successfully udpated"}, status=status.HTTP_200_OK)
            else:
                return Response({"message": "The fields is wrong"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message": "unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

    if request.method == 'PATCH':
        if not request.user.groups.filter(name="Manager").exists() and not request.user.groups.filter(name="Delivery Crew").exists():
            if order.user != request.user:
                return Response({"message": "You are not authorized to change this order."}, status=status.HTTP_403_FORBIDDEN)
            if not request.data:
                return Response({"message": "Fill up all the fields"}, status=status.HTTP_400_BAD_REQUEST)
            serializer = OrderSerializer(
                order, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "Successfully udpated"}, status=status.HTTP_200_OK)
            else:
                return Response({"message": "The fields is wrong"}, status=status.HTTP_400_BAD_REQUEST)

        if request.user.groups.filter(name="Delivery Crew").exists():
            if order.delivery_crew != request.user:
                return Response({"message": "You are not authorized to change this order."}, status=status.HTTP_403_FORBIDDEN)
            if not request.data:
                return Response({"message": "Fill up all the fields"}, status=status.HTTP_400_BAD_REQUEST)

        if 'status' not in request.data or len(request.data) > 1:
            return Response({"messsage": "You can only change the status field"}, status=status.HTTP_400_BAD_REQUEST)

        status_value = request.data.get('status')
        if status_value not in [0, 1]:
            return Response({"message": "Invalid status value. It must be 0 or 1."}, status=status.HTTP_400_BAD_REQUEST)
        order.status = status_value
        order.save()
        return Response({"message": "Order status successfully updated."}, status=status.HTTP_200_OK)

    if request.method == 'DELETE':
        if request.user.groups.filter(name="Manager").exists():
            order.remove()
            return Response({"message": "Successfully deleted order"}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)
