from . import views
from django.conf.urls import url, include
from django.urls import path,include

urlpatterns = [
    path('participants', views.all_users, name='all_users'),
    path('user/count', views.get_user_count, name='get_user_count'),
    path('user/average/contribution', views.get_average_contrbution, name='get_average_contrbution'),
    path('user/most&least/contribution', views.most_and_least_contribution, name='most_and_least_contribution'),
    
]

