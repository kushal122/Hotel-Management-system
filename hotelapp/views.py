from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import *
from .forms import *
from django.http import HttpResponse
from django.core import serializers
from django.contrib. auth import authenticate, login, logout
from .models import *
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.generic.edit import *
from .models import *
from django.db.models import Q
from hotelapp.forms import CommentForm, HotelForm


class ClientMixin(object):
    def get_context_data(self, **kwargs):
        blog = Blog.objects.filter(is_active=True)
        context = super().get_context_data(**kwargs)
        context['loginform'] = UserLoginForm
        context['latestblog'] = blog.order_by('-id')
        context['registerform'] = UserRegistrationForm
        return context


class ClientHomeView(ClientMixin, TemplateView):
    template_name = 'clienttemplates/clienthome.html'

    def get_context_data(self, **kwargs):
        blog = Blog.objects.filter(is_active=True)
        hotel = HotelInformation.objects.filter(is_active=True)
        city = Cities.objects.filter(is_active=True)
        context = super().get_context_data(**kwargs)
        context['citieslist'] = Cities.objects.filter(is_active=True)
        context['hotelslist'] = HotelInformation.objects.filter(is_active=True)
        context['userslist'] = UserProfile.objects.filter(is_active=True)
        context['blogslist'] = Blog.objects.filter(is_active=True)
        context['latestblog'] = blog.order_by('-id')
        context['popularhotel'] = hotel.order_by('-view_count')
        context['latesthotel'] = hotel.order_by('-id')
        context['popularcity'] = city.order_by('-number_of_hotels')
        return context


class ClientRegView(ClientMixin, CreateView):
    template_name = 'clienttemplates/base.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('hotelapp:clienthome')

    def form_valid(self, form):
        u_name = form.cleaned_data["username"]
        p_word = form.cleaned_data["password"]
        user = User.objects.create_user(u_name, "", p_word)
        form.instance.user = user
        return super().form_valid(form)


class ClientLoginView(FormView):
    template_name = 'clienttemplates/base.html'
    form_class = UserLoginForm
    success_url = reverse_lazy('hotelapp:clienthome')

    def form_valid(self, form):
        u_name = form.cleaned_data["username"]
        p_word = form.cleaned_data["password"]

        user = authenticate(username=u_name, password=p_word)
        self.thisuser = user

        if user is not None:
            login(self.request, user)

        else:
            return render(self.request, self.template_name,
                          {"error": "username or password didn't match",
                           "form": form})

        return super().form_valid(form)


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('/')


class ClientBlogListView(ClientMixin, ListView):
    template_name = 'clienttemplates/clientbloglist.html'
    model = Blog
    context_object_name = 'bloglist'
    paginate_by = 2

    def get_context_data(self, **kwargs):
        blog = Blog.objects.filter(is_active=True)
        context = super().get_context_data(**kwargs)
        context['popularblog'] = blog.order_by('-view_count')
        context['latestblog'] = blog.order_by('-id')
        return context


class ClientBlogDetailView(ClientMixin, DetailView):
    template_name = 'clienttemplates/clientblogdetail.html'
    model = Blog
    context_object_name = 'blogdetail'

    def get_context_data(self, **kwargs):
        blog = Blog.objects.filter(is_active=True)
        comment = Comment.objects.filter(is_active=True)
        context = super().get_context_data(**kwargs)
        blog_id = self.kwargs["pk"]
        blogdetail = Blog.objects.get(id=blog_id)
        blogdetail.view_count += 1
        blogdetail.save()
        context['popularblog'] = blog.order_by('-view_count')
        context['latestblog'] = blog.order_by('-id')
        context['commentform'] = CommentForm
        context['comments'] = Comment.objects.all().order_by('-id')
        context['commentlist'] = str(Comment.objects.all().count())

        return context


class UserDetailView(ClientMixin, DetailView):
    template_name = 'clienttemplates/booking.html'
    form_class = PersonalInfo
    model = HotelInformation
    success_url = '/'

    def get_context_data(self, **kwargs):
        user = UserProfile.objects.filter(is_active=True)
        context = super().get_context_data(**kwargs)
        context['personalinfo'] = PersonalInfo
        context['user'] = UserProfile.objects.all()
        return context


class SearchView(TemplateView):
    template_name = 'clienttemplates/searchedresult.html'
    paginate_by = 1

    def get_context_data(self, **kwargs):
        blog1 = Blog.objects.filter(is_active=True)
        context = super().get_context_data(**kwargs)
        keyword = self.request.GET.get('se')

        blog = blog1.filter(Q(title__icontains=keyword) | Q(
            content__icontains=keyword) | Q(tags__icontains=keyword))
        context['searchedblogs'] = blog
        context['popularblog'] = blog1.order_by('-view_count')
        return context


class CommentCreateView(CreateView):
    template_name = 'clienttemplates/commentcreate.html'
    form_class = CommentForm
    success_url = '/'

    def form_valid(self, form):
        blog_id = self.kwargs['pk']
        blog = Blog.objects.get(id=blog_id)
        form.instance.blog = blog
        return super().form_valid(form)

    def get_success_url(self):
        blog_id = self.kwargs['pk']
        return '/client/' + str(blog_id) + '/personal/detail/'

# class Gallery(ListView):
#     template_name = 'clienttemplates/clienthotellisting.html'
#     model = HotelInformation
#     context_object_name = 'gallerylist'

class RoomBookingCreateView(CreateView):
    template_name = 'clienttemplates/booking.html'
    form_class = PersonalInfo
    success_url = '/'

    def form_valid(self, form):
        user_id = self.kwargs['pk']
        user = UserProfile.objects.get(id=user_id)
        form.instance.user = user
        return super().form_valid(form)

    def get_success_url(self):
        user_id = self.kwargs['pk']
        return '/client/' + str(blog_id) + '/blog/detail/'


class HotelAddView(ClientMixin, CreateView):
    template_name = 'clienttemplates/clienthoteladd.html'
    form_class = HotelForm
    success_url = '/'

    def form_valid(self, form):
        hotel = HotelInformation.objects.filter(is_active=True)
        form.instance.blog = hotel
        return super().form_valid(form)

    def get_success_url(self):
        return '/client/hotellist/'


class ClientHotelListView(ClientMixin, ListView):
    template_name = 'clienttemplates/clienthotellisting.html'
    model = HotelInformation
    context_object_name = 'hotellist'
    paginate_by = 4


class ClientHotelDetailView(ClientMixin, DetailView):
    template_name = 'clienttemplates/clienthoteldetail.html'
    model = HotelInformation
    context_object_name = 'hoteldetail'

    def get_context_data(self, **kwargs):
        hotel = HotelInformation.objects.filter(is_active=True)
        context = super().get_context_data(**kwargs)
        hotel_id = self.kwargs["pk"]
        hoteldetail = HotelInformation.objects.get(id=hotel_id)
        hoteldetail.view_count += 1
        hoteldetail.save()
        context['popularhotel'] = hotel.order_by('-view_count')
        context['latesthotel'] = hotel.order_by('-id')
        return context


class HotelCreateView(ClientMixin, TemplateView):
    template_name = 'clienttemplates/hotelcreate.html'

    def get_context_data(self, **kwargs):
        hotel = HotelInformation.objects.filter(is_active=True)
        context = super().get_context_data(**kwargs)
        context['hotelform'] = HotelForm
        return context


class ClientCityListView(ClientMixin, ListView):
    template_name = 'clienttemplates/clientcitylist.html'
    model = Cities
    context_object_name = 'citylist'
    paginate_by = 4

    def get_context_data(self, **kwargs):
        hotel = HotelInformation.objects.filter(is_active=True)
        context = super().get_context_data(**kwargs)
        context['hotel1'] = str(HotelInformation.objects.all().count())
        return context


class ClientCityDetailView(ClientMixin, DetailView):
    template_name = 'clienttemplates/clientcitydetail.html'
    model = Cities
    context_object_name = 'hotlist'

    def get_context_data(self, **kwargs):
        hotel = HotelInformation.objects.filter(is_active=True)
        city = Cities.objects.filter(is_active=True)
        context = super().get_context_data(**kwargs)
        city_id = self.kwargs["pk"]
        citydetail = Cities.objects.get(id=city_id)
        citydetail.number_of_hotels += 1
        citydetail.save()
        return context
