from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name="index"),
    path('Meals/<str:choise>',views.Mealview,name="meal"),
    path('Vag-Meals/<str:choise>',views.VageMealview,name="vage_meal"),
    path('Non-Vag-Meals/<str:choise>',views.NonVageMealview,name="non_vage_meal"),
    path('view/<int:id>', views.Meal_single, name='meal_view'),
    path('about/',views.about,name="about"),
    path('contact/',views.contact,name="contact"),
    path('signup/',views.RegisterView,name="register"),
    path('login/',views.LoginView,name='login'),
    path('Orders/',views.orders,name='order'),
    path('OrderList/',views.OrderList,name='OrderList'),
    path('EmailCall/',views.EmailCall,name='emailcall'),
    path('Place_order/<int:id>',views.palce_order,name='palce_order'),
    path('logout/',views.LogoutView,name="logout"),
    path('remove/<int:id>/',views.cart_remove, name='cart_remove'),
    path("checkavailability/",views.Checkavailability, name="checkavailability"),
    path('verify/',views.verify,name='verify'),
    path('change/',views.change_pass,name='change_pass'),
    path('tablebooking/<str:Table_No>/',views.tablebooking,name='tablebooking'),
    path('allshow/',views.alltablebook,name='allshow'),
    path('edit/<int:id>/',views.edit,name='edit'),
    path('account_status/', views.Account_status, name='Account_status'),
    path('approve/<int:id>/', views.Approve_acc, name='approve'),
    path('login_admin/', views.login_admin, name='login_admin'),
    path('signup_admin/', views.signup_admin, name='signup_admin'),
    path('logout_admin/', views.logout_admin, name="logout_admin"),
    path('alltable/',views.show_all,name='alltable'),
    path('historydta/',views.historydta,name='historydta'),
    
    path('allorders/',views.allOrders,name='allOrders'),
    path('pay/',views.payment,name='PAYMENT'),


]