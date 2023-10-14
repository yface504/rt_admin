from django.contrib import admin
from django.urls import path
from work import views
from work import view_update

urlpatterns = [
    path('index/', views.index , name='index'),
    path('login/', views.login_view , name='login'),
    path('logout/', views.log_out_view , name='logout'),
    path('publisher/' ,views.publisher, name='publisher'),
    path('update/' ,view_update.update, name='update'),
    path('paper/' ,views.paper, name='paper'),
    path('admin/', admin.site.urls),
]