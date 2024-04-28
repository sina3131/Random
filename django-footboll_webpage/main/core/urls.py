from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.conf.urls.static import static
from django.conf import settings



urlpatterns = [
    path('', views.index, name="index"),
    path('offside', views.offside, name="offside"),
    path('index/<str:next>/', views.index, name='index'),
    path('register/', views.registerPage, name="register"),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutPage, name='logout'),

    path('user/', views.profilPage, name='user-page'),
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name = "password_reset.html"), name="reset_password" ),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name = "password_reset_sent.html"), name="password_reset_done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name = "password_reset_form.html"), name="password_reset_confirm"),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name = "password_reset_done.html"), name="password_reset_complete"),

    path('profil/', views.profilPage, name='profil'),
    path('coach/', views.coach, name='coach'),
    path('update_coach/<str:coach_id>/', views.update_coach, name='update_coach'),
    path('delete_coach/<int:coach_id>/',views.delete_coach, name='delete_coach'),
    path('location/',views.location, name='location'),
    path('delete_location/<int:location_id>/',views.delete_location, name='delete_location'),
    path('booking_type/', views.booking_type, name="booking_type"),
    path('update_booking_type/<int:booking_type_id>/', views.update_booking_type, name="update_booking_type"),
    path('delete_booking_type/<int:booking_type_id>/', views.delete_booking_type, name="delete_booking_type"),
    path('payment_types/', views.payment_types, name='payment_types'),
    path('update_payment_type/<int:payment_type_id>/', views.update_payment_type, name="update_payment_type"),
    path('delete_payment_type/<int:payment_type_id>/', views.delete_payment_type, name="delete_payment_type"),
    path('calender/', views.calender, name="calendar"),
    path('edit_profil/', views.edit_profil, name="edit_profil"),
    path('update_player/<int:player_id>/', views.update_player, name="update_player"),
    path('delete_player/<int:player_id>/', views.delete_player, name='delete_player'),

    path('camp/', views.camps, name="camps"),
    path('cup/', views.cups, name="cups"),

    path('prov_traning/', views.prov_traning, name="prov_traning"),
    path('pt_traning/', views.pt_traning, name="pt_traning"),
    path('group_traning/', views.group_traning, name="group_traning"),
    path('prov_traning_register/', views.prov_traning_register, name="prov_traning_register"),
    path('camp/<int:pk>/', views.camp_detail, name="camp_detail"),
    path('cups/<int:pk>/', views.cups_detail, name="cups_detail"),
    path('register_camp/', views.registerPage_camp, name="register_camp"),
    path('register_cup/', views.registerPage_cup, name="register_cup"),
    path('create_camp/', views.create_camp, name='create_camp'),
    path('create_cup/', views.create_cup, name='create_cup'),

    path('boka_pass/', views.boka_pass, name = "boka_pass"),
    path('boka_pass_register', views.boka_pass_register, name= "boka_pass_register"),
    path('chat/', views.chatbot, name = "chatbot"),


    path('new_year/', views.new_year, name="new_year"),
    path('booking/', views.booking, name="booking"),
    path('get_bookings/', views.get_bookings, name="get_bookings"),
    path('get_booking_info/<int:booking_id>/', views.get_booking_info, name="get_booking_info"),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)