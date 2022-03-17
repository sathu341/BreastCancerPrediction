from django.urls import path
from . import views

urlpatterns = [
    path('',views.index),
    path('userreg',views.userreg),
    path('login',views.login),
    path('predict',views.setData),
    path("treatM",views.treatment),
    path("treatB",views.treatment2),
    path("home",views.home),
    path("logout",views.logout)
]
