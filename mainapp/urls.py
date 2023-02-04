from django.urls import path
from .views import *
from rest_framework_simplejwt.views import (TokenRefreshView,TokenVerifyView,)

urlpatterns = [

    path('api/v1/register', RegistrationView.as_view()),
    path('api/v1/login', AuthorizateView.as_view()),
    path('api/v1/nameResidentialComplex/get', GetJk.as_view()),
    path('api/v1/profile/get',ProfileView.as_view()),
    path('api/v1/login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/v1/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    path('api/v1/electron/post',ElectronView.as_view()),
    

  

]
