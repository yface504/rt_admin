from django.contrib import admin
from django.urls import path
from work import views

urlpatterns = [
    path('index/', views.index , name='index'),
    path('login/', views.login_view , name='login'),
    path('logout/', views.log_out_view , name='logout'),
    path('publisher/' ,views.publisher, name='publisher'),
    path('admin/', admin.site.urls),
]
