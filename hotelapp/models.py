from django.db import models
from django.contrib.auth.models import User, Group


class TimeStamp(models.Model):
    ordered_at = models.DateTimeField(auto_now_add=True)
    check_in_at = models.DateTimeField(auto_now=True, auto_now_add=False)
    check_out_active = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True


class Cities(TimeStamp):
    name = models.CharField(max_length=500)
    about = models.TextField(blank=True, null=True)
    number_of_hotels = models.BigIntegerField(default=0)
    image = models.ImageField(models.ImageField(
        upload_to='team/cities/', blank=True, null=True))

    def __str__(self):
        return self.name


class HotelInformation(TimeStamp):
    user = models.OneToOneField(User, on_delete=models.CASCADE,blank=True, null=True)
    name = models.CharField(max_length=500)
    address = models.CharField(max_length=500)
    contact_no = models.CharField(max_length=500)
    city = models.ForeignKey(
        Cities, on_delete=models.CASCADE, null=True, blank=True)
    alt_contact_no = models.CharField(max_length=500, null=True, blank=True)
    map_location = models.CharField(max_length=500)
    email = models.EmailField(null=True, blank=True)
    about_us = models.TextField()
    view_count = models.BigIntegerField(default=0)
    number_of_rooms = models.BigIntegerField(default=0)
    privacy_policy = models.TextField(null=True, blank=True)
    facebook = models.CharField(max_length=500, null=True, blank=True)
    instagram = models.CharField(max_length=500, null=True, blank=True)
    twitter = models.CharField(max_length=500, null=True, blank=True)
    youtube = models.CharField(max_length=500, null=True, blank=True)
    linkedin = models.CharField(max_length=500, null=True, blank=True)
    featured_photo = models.ImageField(upload_to="organization")
    featured_video_link = models.CharField(max_length=500)
    messenger_script = models.TextField(null=True, blank=True)
    google_analytics_script = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class Photo(TimeStamp):

    path = models.FileField()
    hotel = models.ForeignKey(HotelInformation, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.hotel.name


class Admin(TimeStamp):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=500)
    contact_no = models.CharField(max_length=500)
    address = models.CharField(max_length=500)
    email = models.EmailField(null=True, blank=True)
    image = models.ImageField(
        upload_to='team/admin/', blank=True, null=True)
    about = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        group, group_created = Group.objects.get_or_create(name="Admin")
        self.user.groups.add(group)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.full_name


class FoodCategory(TimeStamp):
    title = models.CharField(max_length=500)
    slug = models.SlugField(unique=True, null=True, blank=True)
    image = models.ImageField(
        upload_to="foods/main_category", null=True, blank=True)
    icon_character = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return self.title


class FoodSubcategory(TimeStamp):
    title = models.CharField(max_length=500)
    slug = models.SlugField(unique=True, null=True, blank=True)
    image = models.ImageField(
        upload_to="foods/sub_category", null=True, blank=True)
    icon_character = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return self.title


class Food(models.Model):
    name = models.CharField(max_length=500)
    image = models.ImageField(
        upload_to='team/foods/', blank=True, null=True)
    description = models.TextField()
    cost = models.CharField(max_length=500)
    category = models.ForeignKey(
        FoodCategory, on_delete=models.CASCADE, null=True, blank=True)
    sub_category = models.ForeignKey(
        FoodSubcategory, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name


class FoodOrdering(TimeStamp):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    food = models.ForeignKey(
        Food, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.CharField(max_length=500)

    def __str__(self):
        return self.food


class Table(TimeStamp):
    table_number = models.CharField(max_length=500)
    table_position = models.CharField(max_length=500)
    table_occupancy_number = models.CharField(max_length=500)

    def __str__(self):
        return self.table_number


class TableBooking(TimeStamp):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    table = models.ForeignKey(
        Table, on_delete=models.CharField, null=True, blank=True)
    number_of_tables = models.CharField(max_length=500)

    def __str__(self):
        return self.user


class Room(models.Model):
    hotel = models.ForeignKey(HotelInformation, on_delete=models.CASCADE)
    room_type = models.CharField(max_length=500)
    size = models.CharField(max_length=500)
    image = models.ImageField(
        upload_to='team/foods/', blank=True, null=True)
    video = models.URLField(max_length=500, null=True, blank=True)
    description = models.TextField()
    cost = models.CharField(max_length=500)

    def __str__(self):
        return self.room_type


class RoomBooking(TimeStamp):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    hotel = models.ForeignKey(HotelInformation, on_delete=models.CASCADE)
    number_of_adult = models.CharField(max_length=500)
    number_of_childern = models.CharField(max_length=500)
    check_in = models.DateField()
    check_out = models.DateField()
    totalprice = models.IntegerField(default=0)

    def __str__(self):
        return self.user


class Amenity(TimeStamp):
    hotel = models.ForeignKey(HotelInformation, on_delete=models.CASCADE)
    icon = models.ImageField(
        upload_to="team/room", null=True, blank=True)
    facility_name = models.CharField(max_length=500)

    def __str__(self):
        return self.hotel.name


class Blog(TimeStamp):
    title = models.CharField(max_length=500)
    tags = models.CharField(max_length=500)
    content = models.TextField()
    image = models.ImageField(upload_to="", null=True, blank=True)
    video_link = models.URLField(max_length=500, null=True, blank=True)
    view_count = models.BigIntegerField(default=0)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.title


class Events(TimeStamp):
    title = models.CharField(max_length=500)
    main_category = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    image = models.ImageField(upload_to="eventsimage", null=True, blank=True)
    video_link = models.URLField(max_length=500, null=True, blank=True)
    view_count = models.BigIntegerField(default=0)
    is_verified = models.BooleanField(default=False)
    expiry_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.title


class Shop(TimeStamp):
    item = models.ForeignKey(Food, on_delete=models.CASCADE)
    number_of_item = models.BigIntegerField(default=0)
    ordered_by = models.ForeignKey(User, on_delete=models.CASCADE)


class Billig(TimeStamp):
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    totalprice = models.DecimalField(max_digits=10, decimal_places=10)
    cashier = models.CharField(max_length=300)
    paidby = models.ForeignKey(User, on_delete=models.CASCADE)


class Comment(TimeStamp):
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    commenter = models.CharField(max_length=500)
    email = models.EmailField()
    comment = models.TextField()

    def __str__(self):
        return self.commenter


class AdvertizementPosition(TimeStamp):
    position = models.CharField(max_length=500)
    total_number = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.position


class Advertizement(TimeStamp):
    position = models.ForeignKey(
        AdvertizementPosition, on_delete=models.CASCADE)
    hotel = models.CharField(max_length=500)
    image = models.ImageField(upload_to="advertizements")
    link = models.URLField(max_length=500)
    expiry_date = models.DateTimeField(null=True, blank=True)
    view_count = models.BigIntegerField(default=1)
    clicks = models.BigIntegerField(default=1)

    def __str__(self):
        return self.organization


class UserProfile(TimeStamp):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    fname = models.CharField(max_length=500)
    lname = models.CharField(max_length=500)
    email = models.EmailField()
    phone = models.CharField(max_length=10, null=True, blank=True)
    address = models.CharField(max_length=400, null=True, blank=True)
    image = models.ImageField(upload_to='userprofile', blank=True, null=True)
    about = models.TextField(blank=True, null=True)
    facebook = models.CharField(max_length=500, null=True, blank=True)
    instagram = models.CharField(max_length=500, null=True, blank=True)
    twitter = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return self.email
