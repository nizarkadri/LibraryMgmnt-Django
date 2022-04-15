from django.urls import path
from myapp import views
from . import views
app_name = 'myapp'
urlpatterns = [
 path(r'', views.index, name='index'),
 path(r'about', views.about, name='about'),
 path(r'<int:topic_id>', views.detail, name='detail'),
 path(r'findcourses', views.findcourses, name='findcourses'),
 path(r'placeorder', views.placeorder, name='placeorder'),
 path(r'review', views.review, name='review'),
 path(r'login', views.user_login, name='login'),
 path(r'logout', views.user_logout, name='logout'),
 path(r'myaccount', views.myaccount, name='myaccount'),
 path(r'register', views.register, name='register'),
 path(r'passowrd/password_reset', views.password_reset_request, name='password_reset')

 ]
