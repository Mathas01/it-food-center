import datetime
from typing import Any
from .models import *
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
import re

class OrderForm(forms.Form):
    size = forms.ChoiceField(choices=[
        ('ธรรมดา', 'ธรรมดา เพิ่ม ฿ 0'),
        ('พิเศษ', 'พิเศษ เพิ่ม ฿ 10'),
    ], widget=forms.RadioSelect)
    
    quantity = forms.IntegerField(min_value=1, initial=1)
    description = forms.CharField(widget=forms.Textarea, required=False)

class OrderAddForm(forms.Form):
    food_item = forms.ModelChoiceField(queryset=FoodItem.objects.all(), label="เลือกเมนู")
    size = forms.ChoiceField(choices=[
        ('ธรรมดา', 'ธรรมดา เพิ่ม ฿ 0'),
        ('พิเศษ', 'พิเศษ เพิ่ม ฿ 10'),
    ], widget=forms.RadioSelect)
    quantity = forms.IntegerField(min_value=1, initial=1, label="จำนวน")
    description = forms.CharField(widget=forms.Textarea, required=False, label="คำอธิบาย")
    student = forms.ModelChoiceField(queryset=Student.objects.all(), label="นักเรียน")

class OrderEditForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['FoodItem', 'description', 'order_status','price']

class FoodItemEditForm(forms.ModelForm):
    class Meta:
        model = FoodItem
        fields = ['name', 'description','quantity','price'] 

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=150, required=True)
    last_name = forms.CharField(max_length=150, required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2',)

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError("ชื่อผู้ใช้นี้ถูกใช้งานแล้ว")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("อีเมลนี้ถูกใช้งานแล้ว")
        if not email.endswith('@kmitl.ac.th'):
            raise ValidationError("อีเมลต้องลงท้ายด้วย @kmitl.ac.th")
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise ValidationError("รหัสผ่านไม่ตรงกัน")

        if not self.is_password_strong(password1):
            raise ValidationError("รหัสผ่านควรมีตัวอักษรใหญ่ ตัวอักษรเล็ก ตัวเลข และสัญลักษณ์พิเศษอย่างน้อย 5 ตัว")

        return password2

    def is_password_strong(self, password):
        return (
            len(password) >= 5 and
            re.search(r'[A-Z]', password) and
            re.search(r'[a-z]', password) and
            re.search(r'[0-9]', password)
        )
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user