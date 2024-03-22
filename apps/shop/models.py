from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=150, unique=True)
    slug = models.SlugField(max_length=150, unique=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    class Meta:
        unique_together = ('slug', 'parent')
        verbose_name_plural = 'categories'

    def __str__(self) -> str:
            return self.name


class Product(models.Model):
    category =  models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=150)
    description= models.TextField()
    price = models.PositiveIntegerField(default=0)
    in_stock = models.BooleanField(default=True)
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True)

    def __str__(self) -> str:
        return self.name
    

class Order(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    address = models.CharField(max_length=225)
    postal_code = models.CharField(max_length=225)
    city = models.CharField(max_length=225)
    created = models.DateField(auto_now_add=True)
    update = models.DateField(auto_now_add=True)
    paid = models.BooleanField(default=True)

    class Meta:
         ordering = ('-created',)

    def __str__(self):
         return f"Order {self.id}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name = 'items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name = 'order_items', on_delete=models.CASCADE)
    price = models.PositiveIntegerField(default=0)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)