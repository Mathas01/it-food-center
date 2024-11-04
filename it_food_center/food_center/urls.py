from django.urls import path
from food_center.views import *  

urlpatterns = [
    path('', LoadingView.as_view(), name='loading'),
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('home/', HomeView.as_view(), name='home'),
    path('home/shop/<int:restaurant_id>', ShopView.as_view(), name='shop'),
    path('home/shop/order/<int:fooditem_id>', OrderView.as_view(), name='order'),
    path('home/shop/qrcode/<int:order_id>', QRcodeView.as_view(), name='qrcode'),
    path('status/', StatusView.as_view(), name='status'),
    path('home/logout', LogoutView.as_view(), name="logout"),

    path('c_orderStatus/', c_orderStatusView.as_view(), name='c_orderStatus'),
    path('c_orderStatus/cancel/<int:order_id>',c_orderStatusCancelView.as_view(), name='c_orderCancel'),
    path('c_orderStatus/delete/<int:order_id>',c_orderStatusDeleteView.as_view(), name='c_orderDelete'),
    path('c_orderStatus/edit/<int:order_id>', c_orderStatusEditView.as_view(), name='c_orderEdit'),
    path('order/add/', OrderAddView.as_view(), name='order_add'),
    path('c_fooditem/', c_FoodItemView.as_view(), name='c_fooditem'),
    path('c_fooditem/delete/<int:fooditem_id>',c_fooditemDeleteView.as_view(), name='c_fooditemDelete'),
    path('c_fooditem/edit/<int:fooditem_id>', c_fooditemEditView.as_view(), name='c_orderEdit'),
    path('c_restaurant/', c_FoodItemView.as_view(), name='c_restaurant'),
]