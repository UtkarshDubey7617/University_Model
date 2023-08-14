from django.contrib import admin
from django.urls import path
admin.site.site_header='NNU University'
from django.conf import settings
from django.conf.urls.static import static
from mainApp import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home),
    path('signup/', views.signup),
    path('About/', views.About),
    path('event/', views.event),
    path('blog/', views.blog),
    path('teachers/', views.teachers),
    path('exam/', views.exam),
    path('login/', views.login),
    path('addvideo/', views.addvideo),
    path('courses/<int:num>/', views.courses),
    path('editvideo/<int:num>/', views.editvideo),
    path('deletevideo/<int:num>/', views.deletevideo),
    path('singlevideo/<int:num>/', views.singlevideo),
    path('logout/', views.logout),
    path('updateprofile/', views.updateprofile),
    path('profile/', views.profilePage),
    path('contact/', views.contact),
    path('forgetusername/', views.forgetusername),
    path('forgetotp/', views.forgetotp),
    path('forgetpassword/', views.forgetpassword),

]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
