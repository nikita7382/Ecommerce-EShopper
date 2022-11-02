from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .forms import PasswordChangeCustomForm

urlpatterns=[
    path('',views.home.as_view(),name='home'),
    path('productdetail/<int:pk>/',views.ProuctDetailView.as_view(),name='productdetail' ),
    path('searchproduct/<slug:data>/',views.searchproduct,name='searchproduct'),
    path('searchbar/',views.searchbar,name='searchbar'),
    path('passwordchange/',auth_views.PasswordChangeView.as_view(template_name='store/passwordchange.html',form_class=PasswordChangeCustomForm),name='passwordchange'),
    path('passwordchangedone/',auth_views.PasswordChangeDoneView.as_view(template_name='store/passwordchangedone.html'),name='password_change_done'),
    path('register/',views.register,name='register'),
    path('login/',views.loginUser,name='login'),
    path('logout/',views.logoutUser,name="logout"),
    path('add-to-cart/',views.addtocart,name='addtocart'),
    path('cart/',views.showcart,name='cart'),
    path('removecart/',views.remove_cart),
    path('orders/',views.orders,name='orders'),
     path('pluscart/',views.plus_cart),
    path('ShippingAdd/',views.ShippingAddress,name="ShippingAdd"),
    path('khaltirequest/',views.KhaltirequestView.as_view(),name='khaltirequest'),
    path('khaltiverify/',views.KhaltiVerifyView.as_view(),name='khaltiverify'),
     path('password_reset/',auth_views.PasswordResetView.as_view(template_name='store/password_reset.html'),name='reset_password'),
    path('password_reset_sent/',auth_views.PasswordResetDoneView.as_view(template_name='store/password_reset_sent.html'),name='password_reset_done'),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='store/password_reset_form.html'),name='password_reset_confirm'),
    path('password_reset_complete/',auth_views.PasswordResetCompleteView.as_view(template_name='store/password_reset_done.html'),name='password_reset_complete'),
]



