from django.contrib import admin
from .models import*
@admin.register(Maincategory)
class MaincategoryAdmin(admin.ModelAdmin):
    list_display = ['id','name']
@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ['id','name']
@admin.register(Videos)
class VideoAdmin(admin.ModelAdmin):
    list_display = ['id','name','maincategory','subcategory','admin','description','video']
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['id','name','username','email','phone','addressline1','addressline2','addressline3','pin','city','state','pic']
@admin.register(Admin)
class AdminAdmin(admin.ModelAdmin):
    list_display = ['id','name','username','email','phone','addressline1','addressline2','addressline3','pin','city','state','pic']
@admin.register(Newslater)
class NewslaterAdmin(admin.ModelAdmin):
    list_display = ['id','email']
@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['id','name','email','phone','subject','message','status']