from django.db import models

class Site_User(models.Model):
    name = models.CharField(max_length=100,default="")
    email = models.EmailField(default="", max_length=254) 
    dob = models.DateField(auto_now=False,null=True,blank=True)
    m_no = models.PositiveIntegerField(default=0)
    password = models.CharField(max_length=100,default="")
    def __str__(self):
        return self.name
    
class Temp_Food(models.Model):
    meal_name = models.CharField(max_length=100)
    meal_qty = models.PositiveIntegerField(default=1)
    meal_price = models.PositiveIntegerField(default=1)
    def __str__(self):
        return self.meal_name
    
class Orders(models.Model):
    user_name = models.ForeignKey(Site_User, on_delete=models.CASCADE)
    meal_name = models.CharField(max_length=100,default="")
    meal_qty = models.PositiveIntegerField(default=1)
    meal_price = models.PositiveIntegerField(default=0)
    qrimage = models.ImageField(upload_to='qrimage',blank=True,null=True)    
    def __unicode__(self):
        return self.meal_name
    
class PermanentOrders(models.Model):
    user_name = models.ForeignKey(Site_User, on_delete=models.CASCADE)
    meal_name = models.CharField(max_length=100,default="")
    meal_qty = models.PositiveIntegerField(default=1)
    meal_price = models.PositiveIntegerField(default=0)
    def __unicode__(self):
        return self.meal_name
    
class Feedback(models.Model):
    name=models.CharField(max_length=20)
    phone=models.DecimalField(decimal_places=0,max_digits=10)
    email=models.EmailField()
    message=models.TextField()
    def __str__(self):
        return self.name


