from django.urls import path
from .import views 

urlpatterns=[ 
    path('',views.index,name='index'),
    path('register',views.register,name='reg'),
    path('login',views.login,name='login'),
    path('about',views.about,name='about'),
    path('data',views.data,name='data'),
    path('logout',views.logout,name='logout')
]