from django.conf import settings
from hotelapp.views import *
import django.contrib
from django.urls import include, path
from hotelapp import views

app_name = "hotelapp"
urlpatterns = [
    path('', ClientHomeView.as_view(), name='clienthome'),
    path('registration/', ClientRegView.as_view(), name='clientreg'),
    path('login/', ClientLoginView.as_view(), name='clientlogin'),
    path("logout/", LogoutView.as_view(), name='logout'),


    # blog url
    # blog url
    # blog url
    # blog url

    path('client/blog/',
         ClientBlogListView.as_view(), name='bloglist'),
    path('client/<int:pk>/blog/detail/',
         ClientBlogDetailView.as_view(), name='blogdetail'),

    path('client/hotellist/',
         ClientHotelListView.as_view(), name='hotellist'),
    path('search/', SearchView.as_view(), name='searched'),
    path('client/<int:pk>/hotel/detail/',
         ClientHotelDetailView.as_view(), name='hoteldetail'),
    path('commentcreate/<int:pk>/',
         CommentCreateView.as_view(), name='commentcreate'),
    path('client/hotel/add',
         HotelAddView.as_view(), name='hoteladd'),
    path('client/citylist/',
         ClientCityListView.as_view(), name='citylist'),
    path('client/<int:pk>/city/detail/',
         ClientCityDetailView.as_view(), name='citydetail'),
    path('rommbookingcreate/<int:pk>/',
         RoomBookingCreateView.as_view(), name='roombookingcreate'),
    path('client/<int:pk>/personal/detail/',
         UserDetailView.as_view(), name='userdetail'),
    path('commentcreate/<int:pk>/',
         HotelCreateView.as_view(), name='commentcreate'),

]
