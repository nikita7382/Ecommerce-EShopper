from rest_framework.routers import DefaultRouter
from django.urls import path,include
from . import views


router=DefaultRouter()

router.register('productapi',views.ProductViewSet,basename='products')

urlpatterns=[
    path('',include(router.urls)),
    path('auth/',include('rest_framework.urls',namespace='rest_framework')),


]