from django.contrib import admin
from .models import *

admin.site.register([UserProfile, HotelInformation,
                     Cities, Admin, Blog, Comment, Room, Photo,Amenity])
