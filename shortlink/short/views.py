from django.contrib.auth import logout
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView
from .forms import *
import pyshorteners


# Create your views here.


class Home(ListView):
    model = Links
    template_name = 'short/index.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'home_page'
        return context


class ShortenedLinks(DetailView):
    model = User
    slug_field = 'slug'
    slug_url_kwarg = 'username'
    template_name = 'short/shortened_links.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'shortened_links'
        context['links'] = Links.objects.filter(user_name=context['object'])
        return context


class ShorteningLink(SuccessMessageMixin, CreateView):
    model = Links
    form_class = AddLink
    template_name = 'short/shortening_link.html'
    success_url = reverse_lazy('shortening_link')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'shortening_link'
        return context

    def post(self, request, *args, **kwargs):
        form = AddLink(request.POST)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        old_link = self.request.POST.get('your_link')
        s = pyshorteners.Shortener()
        new_link = s.tinyurl.short(old_link)
        self.object = form.save(commit=False)
        self.object.user_name = User.objects.all().filter(username=self.request.user)[0]
        self.object.new_link = new_link
        self.object.save()
        self.success_message = new_link
        return super().form_valid(form)


class SignUp(CreateView):
    form_class = RegisterUserForm
    template_name = 'short/sign_up.html'
    success_url = reverse_lazy('sign_in')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'sign_up'
        return context


class SignIn(LoginView):
    form_class = AuthenticationForm
    template_name = 'short/sign_in.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'sign_in'
        return context

    def get_success_url(self):
        return reverse_lazy('shortening_link')


def logout_user(request):
    logout(request)
    return redirect('sign_in')
