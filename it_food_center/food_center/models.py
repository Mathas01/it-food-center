from django.db import models
from django.contrib.auth.models import User

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    gmail = models.EmailField(max_length=200)  # เปลี่ยนเป็น EmailField สำหรับความถูกต้อง

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Cook(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=200, null=False)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class ResturantCategory(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name


class Restaurant(models.Model):  
     
    class StatusChoice(models.TextChoices):
        OPEN = "O", "เปิด"
        CLOSED = "C", "ปิด"

    name = models.CharField(max_length=150)
    description = models.CharField(max_length=150)
    cook = models.ForeignKey(Cook, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=StatusChoice.choices, default=StatusChoice.OPEN)
    category = models.ManyToManyField(ResturantCategory) 

    def __str__(self):
        return self.name

class FoodItem(models.Model):
    name = models.CharField(max_length=150)
    description = models.CharField(max_length=150)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)  # แก้ชื่อเป็น restaurant

    def __str__(self):
        return self.name

class Order(models.Model):

    class StatusChoice(models.TextChoices):
        WAITING = "W", "รอการยืนยัน"
        IN_KITCHEN = "C", "อยู่ในครัว"
        ALREADY_COOKED = "AC", "ทำเสร็จแล้ว"
        FINISHED = "F", "เสร็จสิ้น"
        REJECT = "R", "ยกเลิก"
    


    FoodItem = models.ForeignKey(FoodItem, on_delete=models.CASCADE)
    description = models.CharField(max_length=250)
    order_status = models.CharField(max_length=10, choices=StatusChoice.choices, default=StatusChoice.WAITING)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    order_datetime = models.DateTimeField(auto_now_add=True)
    price=models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Order {self.id} by {self.student}"
