from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from django.conf import settings
from django.conf.urls.static import static
from django.utils.module_loading import autodiscover_modules
from practice1 import views

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

urlpatterns = [
    path('city', views.CityList.as_view(), name="CityList"),
    path('restaurants', views.RestaurantList.as_view()),
    path('address', views.AddressList.as_view()),
    path('cart', views.CartView.as_view()),
    path('payment', views.PaymentView.as_view()),
    path('user', views.UserView.as_view()),
    path('order', views.PlaceOrder.as_view()),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('register', views.RegisterUser.as_view()),
    path('review', views.PostRatingsAndReview.as_view()),
    path('demo', views.DemoView.as_view())
]