from django.db.models import query
from django.utils import datastructures
from rest_framework import serializers
from rest_framework.response import Response
from practice1.models import *
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from rest_framework.views import APIView
from practice1.models import City
from practice1.serializers import *
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import models
from rest_framework.permissions import IsAuthenticated
from random import randint

class RegisterUser(APIView):
    
    def post(self, request):
        print("I am here")
        data = request.data
        # username = data.get('name')
        # password = data.get('password')
        name = request.data['name']
        mobile = request.data['mobile']
        email = request.data['email']
        password = request.data['password']

        # djangoUser = models.User(username=mobile)
        # djangoUser.set_password(password)
        # djangoUser.save()

        try:
            queryset = User.objects.get(phone_number__exact=mobile)
            return Response({"status": "User not created", "msg": "User already exist with this mobile number"})
        except BaseException:
            user = User(name=name, email=email, phone_number=mobile)
            djangoUser = models.User(username=mobile)
            djangoUser.set_password(password)

            refresh = RefreshToken.for_user(user)
            
            user.save()
            djangoUser.save()
            return Response({
                "status": "Success",
                "user_id": user.id,
                "refresh": str(refresh),
                "access": str(refresh.access_token)
            })

class DemoView(APIView):
    permission_classes = [IsAuthenticated]

    def get(selft, request):
        print("Printing user = ", request.user)
        mobile = request.data['mobile']
        try:
            queryset = User.objects.get(phone_number=mobile)
        except BaseException:
            pass
        print(queryset)
        serializer = UserSerializer(queryset, many=False)
        return Response({"status": serializer.data})

class CityList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        querySet = City.objects.all()
        serializer = CitySerializer(querySet, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = request.data
        city_name = data['city_name']
        cityObj = City(name=city_name)
        cityObj.save()
        return Response({"status": "Successfully saved"})
    
    def put(self, request):
        data = request.data
        city_id = data['city_id']
        city_name = data['city_name']
        cityObj = City.objects.get(pk=city_id)
        cityObj.name = city_name
        cityObj.save()
        return Response({"status": "Successfully updated the name"})
    
    def delete(self, request):
        data = request.data
        city_id = data['city_id']
        cityObj = get_object_or_404(City, pk=city_id)
        cityObj.delete()
        return Response({"status": "Successfully deleted"})

class RestaurantList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        city = self.request.query_params.get('city_id')
        restaurant = self.request.query_params.get('res_id')
        if city:
            querySet = Restaurant.objects.filter(city__id=city)
            serializer = RestaurantByCitySerializer(querySet, many=True)
        elif restaurant:
            # querySet = Food_Item.objects.filter(restaurant__id=restaurant)
            # serializer = FoodItemSerializer(querySet, many=True)
            # return Response(serializer.data)
            querySet1 = Restaurant.objects.get(pk=restaurant)
            querySet2 = Food_Item.objects.filter(restaurant__id=restaurant)
            serializer1 = RestaurantSerializer(querySet1, many=False)
            serializer2 = FoodItemSerializer(querySet2, many=True)
            return Response({'restaurant': serializer1.data, 'food' : serializer2.data})
        return Response(serializer.data)

class AddressList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # user = self.request.query_params.get('user')
        user = self.request.user
        if user is not None:
            queryset = Address.objects.filter(user__phone_number=user)
            serializer = AddressSerializer(queryset, many=True)
            return Response(serializer.data)
        return Response("User Id required")

    def post(self, request):
        user_phone_number = self.request.user
        data = request.data
        raw_address = data.get('raw_address')
        lat = data.get('lat')
        lng = data.get('lng')

        try:
            user = User.objects.get(phone_number=user_phone_number)
            addressObj = Address(user=user, raw_address=raw_address, lat=lat, lng=lng)
            addressObj.save()
            return Response({"status": "Address saved"})
        except BaseException:
            return Response({"status": "Address not save", "msg": "No such user exist"})

    def put(self, request):
        user_phone_number = self.request.user
        data = request.data
        address_id = data.get('address_id')
        raw_address = data.get('raw_address')
        lat = data.get('lat')
        lng = data.get('lng')

        try:
            addressObj = Address.objects.get(pk=address_id)
            if addressObj.user.phone_number == str(user_phone_number):
                addressObj.raw_address = raw_address
                addressObj.lat = lat
                addressObj.lng = lng
                addressObj.save()
                return Response({"status": "Address updated"})
            else:
                return Response({"status": "Address not updated", "msg": "You can update your addresses only"})
        except BaseException:
            return Response({"status": "Address not updated", "msg": "No such address exist"})

    def delete(self, request):
        user_phone_number = self.request.user
        data = request.data
        address_id = data.get('address_id')

        try:
            addressObj = Address.objects.get(pk=address_id)
            if addressObj.user.phone_number == str(user_phone_number):
                addressObj.delete()
                return Response({"status": "Address deleted successfully"})
            else:
                return Response({"status": "Address not deleted", "msg": "User can not delete other user's addresses"})
        except BaseException:
            return Response({"status": "Address not deleted", "msg": "No such address exist"})
    

class CartView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # user = self.request.query_params.get('user')
        user = self.request.user
        if user:
            queryset = Cart.objects.filter(user__phone_number=user)
            foodItemObjects = Food_Item.objects.all()
            total_price = 0
            for q in queryset:
                total_price += (q.quantity*q.food_item.price)
                print(q.food_item, " ", str(q.quantity), " ", str(q.food_item.price))
            print(total_price)
            serializer = CartSerializer(queryset, many=True)
            return Response({"data": serializer.data, "total_price": total_price})
        return Response("User Id required")

    def post(self, request):
        print("I was here")
        data = request.data
        # user_id = data.get('user')
        user_phone_number = self.request.user
        res_id = data.get('res_id')
        food_item_id = data.get('food_item_id')
        quantity = data.get('quantity')


        user = User.objects.get(phone_number=user_phone_number)
        restaurant = Restaurant.objects.get(pk=res_id)
        food_item = Food_Item.objects.get(pk=food_item_id)

        res_id_of_current_food_item = food_item.restaurant.id

        if res_id_of_current_food_item == res_id:
            try:
                alreadyAddedItemsInCart = Cart.objects.filter(user__phone_number=user_phone_number)
                if alreadyAddedItemsInCart[0].restaurant.id == res_id:
                    cartObject = Cart(user = user, restaurant = restaurant, food_item = food_item, quantity = quantity)
                    cartObject.save()
                    return Response({"status": "Cart saved"})
                else:
                    return Response({"status": "Cart not saved", "msg": "You have food items from other restaurant"})
            except BaseException:
                cartObject = Cart(user = user, restaurant = restaurant, food_item = food_item, quantity = quantity)
                cartObject.save()
                return Response({"status": "Cart saved"})
        else:
            return Response({"status": "Cart not saved", "msg": "Select food items from same restaurant"})

    def put(self, request):
        data = request.data
        # user_id = data.get('user')
        user_phone_number = self.request.user
        res_id = data.get('res_id')
        food_item_id = data.get('food_item_id')
        quantity = data.get('quantity')

        print(user_phone_number, " ", res_id, " ", food_item_id, " ", quantity)

        user = User.objects.get(phone_number=user_phone_number)
        restaurant = Restaurant.objects.get(pk=res_id)
        food_item = Food_Item.objects.get(pk=food_item_id)

        res_id_of_current_food_item = food_item.restaurant.id

        if res_id_of_current_food_item == res_id:
            try:
                print("hello amit")
                # alreadyAddedItemInCart = Cart.objects.filter(user__phone_number=user_phone_number, restaurant__id=res_id, food_item__id=food_item_id)
                alreadyAddedItemInCart = Cart.objects.get(user=user, restaurant=restaurant, food_item=food_item)
                print("hello amit - ", alreadyAddedItemInCart.quantity)
                prevQuantity = alreadyAddedItemInCart.quantity
                newQuantity = prevQuantity + int(quantity)
                print("new quantity = ", newQuantity)
                
                alreadyAddedItemInCart.quantity = newQuantity
                alreadyAddedItemInCart.save()
                # cartObject = Cart(user = user, restaurant = restaurant, food_item = food_item, quantity = newQuantity)
                # cartObject.save()
                return Response({"status": "Cart item updated"})
            except BaseException:
                return Response({"status": "Cart not updated", "msg": "No such item is there in your cart"})
        else:
            return Response({"status": "Cart not updated", "msg": "You can update food items from same restaurant"})

    def delete(self, request):
        print("In delete")
        data = request.data
        # user_id = data.get('user')
        user_phone_number = self.request.user
        res_id = data.get('res_id')
        food_item_id = data.get('food_item_id')
        
        cartObjects = Cart.objects.filter(user__phone_number=user_phone_number, restaurant__id=res_id, food_item__id=food_item_id)
        if len(cartObjects) == 0:
            return Response({"status": "No cart item deleted", "msg": "You have no such item in cart"})
        cartObjects.delete()
        return Response({"status": "Cart item deleted"})

class PaymentView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_phone_number = self.request.user
        payment_id = request.data.get('payment_id')

        try:
            paymentObj = Payment.objects.get(pk=payment_id)
            serializer = PaymentSerializer(paymentObj, many=False)
            return Response({"data": serializer.data})
        except BaseException:
            return Response({"msg": "No payment exist with the given id"})

    def post(self, request):
        user_phone_number = self.request.user
        data = request.data
        transaction_id = randint(1000000000, 9999999999)
        payment_mode = data.get('payment_mode')
        payment_status = data.get('payment_status')
        res_id = data.get('res_id')

        try:
            user = User.objects.get(phone_number=user_phone_number)
            try:
                restaurant = Restaurant.objects.get(pk=res_id)
                paymentObj = Payment(transaction_id=transaction_id, payment_mode=payment_mode, payment_status=payment_status, user=user, restaurant=restaurant)
                paymentObj.save()
                return Response({"status": "Payment added successfully", "payment_id": paymentObj.id})
            except BaseException:
                return Response({"status": "Payment not added", "msg": "No such restaurant exist"})
        except BaseException:
            return Response({"status": "Payment not added", "msg": "No such user exist"})

    def put(self, request):
        user_phone_number = self.request.user
        data = request.data
        payment_id = data.get('payment_id')
        order_id = data.get('order_id')
        paymentObj = Payment.objects.get(pk=payment_id)
        paymentObj.order_id = order_id
        paymentObj.save()
        return Response({"status": "Successfully added order id"})

    def delete(self, request):
        pass

class PlaceOrder(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_phone_number = self.request.user
        data = request.data

        try:
            if 'all_active_orders' in data and data['all_active_orders']:
                orderObjQuerySet = Order.objects.filter(user__phone_number=user_phone_number, order_status=False)
            elif 'all_past_orders' in data and data['all_past_orders']:
                orderObjQuerySet = Order.objects.filter(user__phone_number=user_phone_number, order_status=True)
            elif 'all_orders' in data and data['all_orders']:
                orderObjQuerySet = Order.objects.filter(user__phone_number=user_phone_number)
            else:
                order_id = data['order_id']
                orderObjQuerySet = Order.objects.filter(id=order_id)
        except BaseException:
            return Response({"msg": "No order exist with the give id"})
    
        result = {}

        for index, orderObj in enumerate(orderObjQuerySet):
            temp_result = {}
            temp_result['id'] = orderObj.id
            temp_result['user_id'] = orderObj.user.id
            temp_result['restaurant_id'] = orderObj.restaurant.id
            temp_result['payment_id'] = orderObj.payment.id
            temp_result['total_price'] = orderObj.total_price
            temp_result['order_status'] = orderObj.order_status
            temp_result['address'] = orderObj.address
            temp_result['lat'] = orderObj.lat
            temp_result['lng'] = orderObj.lng
            result[index] = temp_result
            result[index]['order_items'] = []

            current_order_id = orderObj.id
            current_order_data_items = Order_Data.objects.filter(order__id=current_order_id)
            for current_order_data_item in current_order_data_items:
                temp_result = {}
                temp_result['id'] = current_order_data_item.id
                temp_result['name'] = current_order_data_item.name
                temp_result['quantity'] = current_order_data_item.quantity
                temp_result['price'] = current_order_data_item.price
                result[index]['order_items'].append(temp_result)
            
            # current_order_id = orderObj.id
            # current_order_data_items = Order_Data.objects.filter(order__id=current_order_id)
            
            # temp_result = {}
            # for index2, current_order_data_item in enumerate(current_order_data_items):
            # temp_result[index] = OrderDataSerializer(current_order_data_items, many=True)
            # result[index]['order_items'] = temp_result

        # print(temp_result)
        return Response(result)
        # serializer1 = OrderSerializer(orderObjQuerySet, many=False)
        # serializer2 = OrderDataSerializer(orderItemsQuerySet, many=True)

        # print("amit ", type(serializer1.data))

        # return Response({"order": serializer1.data, "order_items": serializer2.data})

    def post(self, request):
        data = request.data
        # user_id = data.get('user')
        user_phone_number = self.request.user
        payment_id = data.get('payment_id')
        address_id = data.get('address_id')

        user = User.objects.get(phone_number=user_phone_number)
        try:
            cartItems = Cart.objects.filter(user__phone_number=user_phone_number)
            payment = Payment.objects.get(pk=payment_id)
            address = Address.objects.get(pk=address_id)
        except BaseException:
            return Response({"msg": "First add something to cart"})
        
        total_price = 0
        for cartItem in cartItems:
            print("a")
            restaurant = cartItem.restaurant
            total_price += (cartItem.quantity*cartItem.food_item.price)
        
        raw_address = address.raw_address
        lat = address.lat
        lng = address.lng
        
        orderObject = Order(user=user, restaurant=restaurant, payment=payment, total_price=total_price, order_status=False, address=raw_address, lat=lat, lng=lng)
        orderObject.save()

        for cartItem in cartItems:
            name = cartItem.food_item.name
            quantity = cartItem.quantity
            price = cartItem.food_item.price*cartItem.quantity
            orderItemObject = Order_Data(order=orderObject, name=name, quantity=quantity, price=price)
            orderItemObject.save()

        #we can now delete all the items of cart
        cartItems.delete()

        #we can also update the order id in payment section
        payment.order_id = orderObject.id
        payment.save()

        return Response({"status": "Order placed"})

    def put(self, request):
        data = request.data
        order_id = data.get('order')
        try:
            orderObj = Order.objects.get(pk=order_id)
            orderObj.order_status = True
            orderObj.save()
            return Response({"status": "Order marked completed"})
        except BaseException:
            return Response({"msg": "No result exist to your query"})

    def delete(self, request):
        pass

class UserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # user = self.request.query_params.get('user')
        user_phone_number = self.request.user
        if user_phone_number is not None:
            try:
                queryset = User.objects.get(phone_number=user_phone_number)
                serializer = UserSerializer(queryset, many=False)
                return Response(serializer.data)
            except BaseException:
                return Response({"msg": "No such user exist"})
        return Response("User Id required")

class PostRatingsAndReview(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        data = self.request.data
        res_id = data.get('res_id')
        user_id = data.get('user_id')
        order_id = data.get('order_id')
        review_id = data.get('review_id')

        #either all reviews of a restaurant will be fetched
        if res_id is not None:
            queryset = RatingsAndReview.objects.filter(restaurant__id=res_id)

        #either all reviews by a user will be fetched
        if user_id is not None:
            queryset = RatingsAndReview.objects.filter(user__id=user_id)

        #either review of a particular order will be fetched
        if order_id is not None:
            queryset = RatingsAndReview.objects.filter(order__id=order_id)

        #either a particular review will be fetched
        if review_id is not None:
            queryset = RatingsAndReview.objects.filter(pk=review_id)
        
        serializer = RatingsAndReviewSerializer(queryset, many=True)
        return Response({"data": serializer.data})

    def post(self, request):
        data = self.request.data
        res_id = data.get('res_id')
        # user_id = data.get('user_id')
        user_phone_number = self.request.user
        order_id = data.get('order_id')
        delivery_rating = data.get('delivery_rating')
        food_rating = data.get('food_rating')
        delivery_review = data.get('delivery_review')
        food_review = data.get('food_review')

        user = User.objects.get(phone_number=user_phone_number)
        restaurant = Restaurant.objects.get(res_id)
        order = Order.objects.get(pk=order_id)

        if order.restaurant.id != res_id:
            return Response({"status": "Review not submitted", "msg": "Order should be from same restaurant"})
        
        if order.user.phone_number != str(user_phone_number):
            return Response({"status": "Review not submitted", "msg": "Same user can rate the order"})

        ratingsAndReviewObj = RatingsAndReview(user=user, restaurant=restaurant, order=order, delivery_rating=delivery_rating, food_rating=food_rating, delivery_review=delivery_review, food_review=food_review)
        ratingsAndReviewObj.save()

        return Response({"status": "Review submitted successfully"})

    def put(self, request):
        #User is not allowed to change any review
        pass

    def delete(self, request):
        #User is not allowed to delete any review
        pass