from django.db import models
# import uuid
from django.contrib.auth.models import User

# class Category(models.Model):
#     part_name = models.CharField(max_length=50)
#
#     def __str__(self):
#         return self.part_name
#
# class Product(models.Model):
#     product_id = models.UUIDField(default=uuid.uuid4, help_text='unique id for this product')
#     product_name = models.CharField(max_length=50)
#     main_image = models.ImageField(upload_to='images')
#     image_1 = models.ImageField(upload_to='images', blank=True)
#     image_2 = models.ImageField(upload_to='images', blank=True)
#     image_3 = models.ImageField(upload_to='images', blank=True)
#     price = models.FloatField()
#     discount_price = models.FloatField(blank=True, null=True)
#     description = models.TextField()
#     compatibility = models.TextField()
#     category = models.ForeignKey(Category, on_delete=models.DO_NOTHING)
#     qunatity = models.IntegerField(default=1)
#     list_date = models.DateTimeField(auto_now_add=True)
#     slug = models.SlugField()
#
#     def __str__(self):
#         return self.product_name


########################################
class Customer(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.name}-{self.email}"


class Product(models.Model):
    # product_id = models.UUIDField(default=uuid.uuid4, help_text='unique id for this product')
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    # discount_price = models.FloatField(blank=True, null=True)
    main_image = models.ImageField(upload_to='images', null=True, blank=True)
    image_1 = models.ImageField(upload_to='images', null=True, blank=True)
    image_2 = models.ImageField(upload_to='images', null=True, blank=True)
    image_3 = models.ImageField(upload_to='images', null=True, blank=True)
    compatibility = models.TextField()
    description = models.TextField()
    digital = models.BooleanField(default=False, null=True, blank=True)

    def __str__(self):
        return self.name


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True, blank=True)
    transaction_id = models.CharField(max_length=100, null=True)

    def __str__(self):
        return f"{self.customer} {self.id}"

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total

    @property
    def shipping(self):
        shipping = False
        orderItems = self.orderitem_set.all()
        for i in orderItems:
            if i.product.digital == False:
                shipping = True
        return shipping


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product.name

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total


class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    city = models.CharField(max_length=200, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
