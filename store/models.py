from secrets import choice
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Customer(models.Model):
  STATE_CHOICES=[
      ('Banke','Banke'),
      ('Bagmati','Bagmati'), 
      ('Bheri','Bheri'), 
      ('Dhawalagiri','Dhawalagiri'),
      ('Gandaki ','Gandaki'),
      ('Janakpur ','Janakpur '),
      ('Karnali','Karnali'),
      ('koshi','koshi') ,
      ('Lumbini','Lumbini'),
      ('Mahakali','Mahakali'), 
      ('Mechi','Mechi'),
      ('Narayani','Narayani'),
      ('Rapti','Rapti'),
      ('Sagarmatha','Sagarmatha'),
      ('seti','seti')
    ]
  method=[
    ('Cash on delivery','Cash on deleivery'),
    ('khalti','khalti'),
    ('esewa','esewa'),
  ]
  user=models.ForeignKey(User,on_delete=models.CASCADE)
  name=models.CharField(max_length=200)
  payement_method=models.CharField(choices=method,max_length=20,default='Cash on Delivery')
  locality=models.CharField(max_length=200)
  city=models.CharField(max_length=200)
  zipcode=models.IntegerField()
  state=models.CharField(choices=STATE_CHOICES,max_length=50)


  def __str__(self):
    return str(self.id)

class Product(models.Model):
  category=[
    ('TW','Top Wear'),
    ('BW','Bottom Wear'),
    ('Shoes','Shoes'),
    ('mobile','mobile'),
    ('Laptop','Laptop')
  ]
  title=models.CharField(max_length=100)
  selling_price=models.FloatField()
  discounted_price=models.FloatField()
  description=models.TextField()
  brand=models.CharField(max_length=100)
  Category=models.CharField(choices=category,max_length=10)
  product_image=models.ImageField(upload_to='productimg')
   
  def __str__(self):
    return str(self.id)

class Cart(models.Model):
  user=models.ForeignKey(User,on_delete=models.CASCADE)
  product=models.ForeignKey(Product,on_delete=models.CASCADE)
  quantity=models.PositiveIntegerField(default=1)

  def __str__(self):
    return str(self.id)

class OrderPlaced(models.Model):
  status=[
        ('Pending','Pending'),
        ('Cancel','Cancel',),
        ('Delivered',('Delivered'))
    ]
  user=models.ForeignKey(User,on_delete=models.CASCADE)
  customer=models.ForeignKey(Customer,on_delete=models.CASCADE)
  product=models.ForeignKey(Product,on_delete=models.CASCADE)
  quantity=models.PositiveIntegerField(default=1)
  ordered_date=models.DateTimeField(auto_now_add=True)
  status=models.CharField(max_length=50,choices=status,default='Pending')
  payment_completed = models.BooleanField(default=False, null=True, blank=True)

  def __str__(self):
    return str(self.id)

  @property
  def total_cost(self):
    return self.quantity * self.product.discounted_price





