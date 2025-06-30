from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
    name = models.CharField(max_length=100, null=True)
    price = models.IntegerField(null=True)
    stock = models.IntegerField(null=True)
    product_image = models.ImageField(upload_to='media/', null=True)
    categ = models.ForeignKey('Category', on_delete=models.CASCADE, null=True, related_name='products')
    description = models.TextField(null=True, blank=True)
    def __str__(self):
        return self.name

class User_details(models.Model):
    username = models.CharField(max_length=30, null=True)
    email = models.EmailField(max_length=50, null=True)
    phone_number = models.IntegerField(null=True)
    password = models.CharField(max_length=40, null=True)
    password2 = models.CharField(max_length=40, null=True)
    def __str__(self):
        return self.username

class Category(models.Model):
    name = models.CharField(max_length=100, null=True)
    description = models.TextField(null=True, blank=True)
    def __str__(self):
        return self.name

class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    @property
    def subtotal(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='Pending')
    total = models.DecimalField(max_digits=10, decimal_places=2)
    # Add more fields as needed

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"


class Orders_detail(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.TextField()
    payment_method = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='pending')




class employee(models.Model):
    name = models.CharField(max_length=100, null=True)
    def __str__(self):
        return self.name
class task(models.Model):
    taskname = models.CharField(max_length=30, null=True)
    emp = models.ForeignKey(employee, on_delete=models.CASCADE, null=True,blank=True, related_name='task')
    def __str__(self):
        return self.taskname
    
class book(models.Model):
    bookname = models.CharField(max_length=30, null=True)
    author = models.CharField(max_length=30, null=True)
    price = models.IntegerField(null=True)
    def __str__(self):
        return self.bookname
    
class publisher(models.Model):
    name = models.CharField(max_length=30, null=True)
    book = models.ForeignKey(book, on_delete=models.CASCADE, null=True,blank=True, related_name='publisher')
    def __str__(self):
        return self.name
