from random import choices
from django.db import models
class Maincategory(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=150)
    def __str__(self):
        return self.name
class Subcategory(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=150)
    def __str__(self):
        return self.name
class Student(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    username = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    phone = models.CharField(max_length=15)
    addressline1 = models.CharField(max_length=100,default=None,null=True,blank=True)
    addressline2 = models.CharField(max_length=100,default=None,null=True,blank=True)
    addressline3 = models.CharField(max_length=100,default=None,null=True,blank=True)
    pin = models.CharField(max_length=50,default=None,null=True,blank=True)
    city = models.CharField(max_length=50,default=None,null=True,blank=True)
    state = models.CharField(max_length=50,default=None,null=True,blank=True)
    pic = models.ImageField(upload_to="images",default="noimage.jpg",null=True,blank=True)
    def __str__(self):
        return self.username
class Admin(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    username = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    phone = models.CharField(max_length=15)
    addressline1 = models.CharField(max_length=100,default=None,null=True,blank=True)
    addressline2 = models.CharField(max_length=100,default=None,null=True,blank=True)
    addressline3 = models.CharField(max_length=100,default=None,null=True,blank=True)
    pin = models.CharField(max_length=50,default=None,null=True,blank=True)
    city = models.CharField(max_length=50,default=None,null=True,blank=True)
    state = models.CharField(max_length=50,default=None,null=True,blank=True)
    pic = models.ImageField(upload_to="images",default="noimage.jpg",null=True,blank=True)
    def __str__(self):
        return self.username
class Videos(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=500)
    maincategory = models.ForeignKey(Maincategory,on_delete=models.CASCADE)
    subcategory = models.ForeignKey(Subcategory,on_delete=models.CASCADE)
    admin = models.ForeignKey(Admin,on_delete=models.CASCADE)
    description = models.TextField()
    video = models.FileField(upload_to="video",default="noimagep.jpg",null=True,blank=True)
    def __str__(self):
        return self.name
class Newslater(models.Model):
    id = models.AutoField(primary_key=True)
    email = models.EmailField(max_length=50,unique=True)
contactstatuschoice =((1,'Active'),(2,'Done'))
class Contact(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=50)
    phone = models.CharField(max_length=15)
    subject = models.TextField()
    message = models.TextField()
    status = models.IntegerField(choices=contactstatuschoice,default=1)