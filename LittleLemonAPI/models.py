from django.db import models

# Create your models here.

class carts(models.Model):
    username = models.CharField(max_length=255)
    title_quantity = models.JSONField()

    def __str__(self):
        return self.username

class Category(models.Model):
    slug = models.SlugField()
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title

class MenuItem(models.Model):
    title=models.CharField(max_length=255)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    inventory = models.SmallIntegerField()
    category = models.ForeignKey(Category,on_delete=models.PROTECT, default=1)

    def __str__(self):
        return self.title
    
class orders(models.Model):
    username = models.CharField(max_length=255)
    items_quantity=models.JSONField()
    order_status = models.SmallIntegerField(default=0)
    delivery_crew = models.CharField(max_length=255,default="")
    
