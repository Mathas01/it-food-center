from django.views import View
from django.shortcuts import render, get_object_or_404
from django.shortcuts import render, redirect
from food_center.models import *
from .forms import *
from django.contrib.auth import logout, login
from .models import *
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import Group

class LoadingView(View):
    def get(self, request):
        return render(request, 'loading.html')

class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('login')

class RegisterView(View):
    def get(self, request):
        form = RegistrationForm()
        return render(request, 'register.html', {'form': form})

    def post(self, request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()  
            Student.objects.create(
                user=user,
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                gmail=user.email 
            )
            student_group = Group.objects.get(name='student')
            user.groups.add(student_group)
            return redirect('login')
        return render(request, 'register.html', {'form': form})

class LoginView(View):

    def get(self, request):
        return render(request, 'login.html', {"form": AuthenticationForm()})
    
    def post(self, request):
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user() 
            login(request, user)

            if user.username == "it65070191":
                return redirect('../../admin/')
            elif hasattr(user, 'cook'):
                return redirect('c_orderStatus')
            else:
                return redirect('home')
        
        return render(request, 'login.html', {"form": form})

class HomeView(LoginRequiredMixin,PermissionRequiredMixin, View):
    login_url = '/login/'
    permission_required = ["food_center.change_student"]

    def get(self, request):
        thai = Restaurant.objects.filter(category__name="ร้านอาหารไทย")
        japan = Restaurant.objects.filter(category__name="ร้านอาหารญี่ปุ่น")
        student = Student.objects.get(user__username=request.user.username)

        context = {
            "thai": thai,
            "japan": japan,
            "student": student,
        }
        return render(request, 'home.html', context)

class OrderView(LoginRequiredMixin,PermissionRequiredMixin, View):
    login_url = '/login/'
    permission_required = ["food_center.change_student"]

    def get(self, request, fooditem_id):
        food_item = FoodItem.objects.get(id=fooditem_id)
        form = OrderForm()
        context = {
            "food_item": food_item,
            "form": form
        }
        return render(request, 'order.html', context)

    def post(self, request, fooditem_id):
        form = OrderForm(request.POST)
        if form.is_valid():
            food_item = FoodItem.objects.get(id=fooditem_id)
            quantity = form.cleaned_data['quantity']
            size = form.cleaned_data['size']
            description = form.cleaned_data['description']
            student = Student.objects.get(user__username=request.user.username)

            if size == "พิเศษ":
                price = (food_item.price + 10) * quantity
            else:
                price = food_item.price * quantity
            
            order = Order.objects.create(
                FoodItem=food_item,
                description=f"จำนวน : {quantity} ขนาด : {size} เพิ่มเติม: {description}",
                student=student,
                price=price
            )
            return redirect('qrcode', order_id=order.id)
        else:
            food_item = FoodItem.objects.get(id=fooditem_id)
            context = {
                "food_item": food_item,
                "form": form
            }
            return render(request, 'order.html', context)

class QRcodeView(LoginRequiredMixin,PermissionRequiredMixin, View):
    login_url = '/login/'
    permission_required = ["food_center.change_student"]

    def get(self, request, order_id):
        order = Order.objects.get(id=order_id)
        context = {
            "order_id": order_id,
            "order": order
        }
        return render(request, 'qrcode.html', context)

class ShopView(LoginRequiredMixin,PermissionRequiredMixin, View):
    login_url = '/login/'
    permission_required = ["food_center.change_student"]

    def get(self, request, restaurant_id):
        restaurant = Restaurant.objects.get(id=restaurant_id)
        fooditems = FoodItem.objects.filter(restaurant=restaurant)
        student = Student.objects.get(user__username=request.user.username)
        context = {
            "restaurant_id": restaurant_id,
            "restaurants": restaurant,
            "foodItems": fooditems,
            "student":student
        }
        return render(request, 'shop.html', context)

class StatusView(LoginRequiredMixin,PermissionRequiredMixin, View):
    login_url = '/login/'
    login_url = '/login/'
    permission_required = ["food_center.change_student"]

    def get(self, request):
        student = Student.objects.get(user__username=request.user.username)
        orders = Order.objects.filter(student=student)
        return render(request, 'status.html', {"orders": orders})
    
# แม่ค้า---------------------------------------------------------------------------------------------------------------------

class c_orderStatusView(LoginRequiredMixin,PermissionRequiredMixin, View):
    login_url = '/login/'
    permission_required = ["food_center.change_cook"]

    def get(self, request):
        cook = Cook.objects.get(user__username=request.user.username)
        restaurant = Restaurant.objects.get(cook=cook.id)
        order = Order.objects.filter(FoodItem__restaurant=restaurant)

        context = {
            "cook": cook,
            "restaurant":restaurant,
            "orders":order
        }
        return render(request, 'c_orderStatus.html', context)

class c_orderStatusDeleteView(LoginRequiredMixin, View):
    login_url = '/login/'
    permission_required = ["food_center.change_cook"]
    def get(self, request,order_id):
        order = Order.objects.get(id = order_id)
        order.delete()
        return redirect('c_orderStatus')
    
class c_orderStatusCancelView(LoginRequiredMixin, View):
    login_url = '/login/'
    permission_required = ["food_center.change_cook"]
    def get(self, request,order_id):
        order = Order.objects.get(id = order_id)
        print(order)
        order.order_status="R"
        order.save()
        return redirect('c_orderStatus')

class c_orderStatusEditView(LoginRequiredMixin,PermissionRequiredMixin, View):
    login_url = '/login/'
    permission_required = ["food_center.change_cook"]
    def get(self, request, order_id):
        order = Order.objects.get(id=order_id)  # ใช้พารามิเตอร์ที่ถูกต้อง
        food_item = order.FoodItem
        form = OrderEditForm(instance=order)
        # ถ้าต้องการส่งฟอร์มไปยัง template
        return render(request, 'c_orderEdit.html', {'form': form, 'order': order ,'food_item':food_item})

    def post(self, request, order_id):
        order = Order.objects.get(id=order_id)
        food_item = order.FoodItem
        form = OrderEditForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('c_orderStatus') 
        return render(request, 'c_orderEdit.html', {'form': form, 'order': order ,'food_item':food_item})
    
class OrderAddView(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/login/'
    permission_required = ['food_center.add_order']

    def get(self, request):
        cook = Cook.objects.get(user=request.user)
        restaurant = Restaurant.objects.get(cook=cook)
        form = OrderAddForm()
        form.fields['food_item'].queryset = FoodItem.objects.filter(restaurant=restaurant)
        context = {
            'form': form,
            'restaurant': restaurant
        }
        return render(request, 'c_orderAdd.html', context)

    def post(self, request):
        cook = Cook.objects.get(user=request.user)
        restaurant = Restaurant.objects.get(cook=cook)
        form = OrderAddForm(request.POST)
        form.fields['food_item'].queryset = FoodItem.objects.filter(restaurant=restaurant)
        
        if form.is_valid():
            food_item = form.cleaned_data['food_item']
            quantity = form.cleaned_data['quantity']
            size = form.cleaned_data['size']
            description = form.cleaned_data['description']
            student = form.cleaned_data['student']

            if size == "พิเศษ":
                price = (food_item.price + 10) * quantity
            else:
                price = food_item.price * quantity

            order = Order.objects.create(
                FoodItem=food_item,
                description=f"จำนวน : {quantity} ขนาด : {size} เพิ่มเติม: {description}",
                student=student,
                price=price
            )
            return redirect('c_orderStatus')
        print(form.errors) 
        context = {
            'form': form,
            'restaurant': restaurant
        }
        return render(request, 'c_orderAdd.html', context)

class c_FoodItemView(LoginRequiredMixin, PermissionRequiredMixin,View):
    login_url = '/login/'
    permission_required = ["food_center.change_cook"]
    login_url = '/login/'

    def get(self, request):
        cook = Cook.objects.get(user__username=request.user.username)
        restaurant = Restaurant.objects.get(cook=cook.id)
        foooditem = FoodItem.objects.filter(restaurant=restaurant)

        context = {
            "cook": cook,
            "restaurant":restaurant,
            "food_items":foooditem
        }
        return render(request, 'c_fooditem.html', context)

class c_fooditemDeleteView(LoginRequiredMixin,PermissionRequiredMixin, View):
    login_url = '/login/'
    permission_required = ["food_center.change_cook"]
    login_url = '/login/'
    permission_required = ["food_center.change_cook"]
    login_url = '/login/'
    def get(self, request,fooditem_id):
        fooditem = FoodItem.objects.get(id = fooditem_id)
        fooditem.delete()
        return redirect('c_fooditem')

class c_fooditemEditView(LoginRequiredMixin,PermissionRequiredMixin, View):
    login_url = '/login/'
    permission_required = ["food_center.change_cook"]
    login_url = '/login/'
    def get(self, request, fooditem_id):
        food_item = FoodItem.objects.get(id=fooditem_id)  # ใช้พารามิเตอร์ที่ถูกต้อง
        form = FoodItemEditForm(instance=food_item)
        return render(request, 'c_fooditemEdit.html', {'form': form,'food_item':food_item})

    def post(self, request, fooditem_id):
        food_item = FoodItem.objects.get(id=fooditem_id)
        form = FoodItemEditForm(request.POST, instance=food_item)
        if form.is_valid():
            print('valid')
            form.save()
            return redirect('c_fooditem') 
        return render(request, 'c_fooditemEdit.html', {'form': form ,'food_item':food_item})
    
    





