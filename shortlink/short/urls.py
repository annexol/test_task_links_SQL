from django.urls import path
from .views import *

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('sign_in/', SignIn.as_view(), name='sign_in'),
    path('logout/', logout_user, name='logout'),
    path('sign_up/', SignUp.as_view(), name='sign_up'),
    path('shortening_link/', ShorteningLink.as_view(), name='shortening_link'),
    path('shortened_links/<slug:username>/', ShortenedLinks.as_view(), name='shortened_links'),

]
