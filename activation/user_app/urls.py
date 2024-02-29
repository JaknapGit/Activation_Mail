from django.urls import path
from .views import UserView, UserAccountActivate

urlpatterns = [
    path('user/', UserView.as_view(), name='register'),
    path('activate/<uidb64>/<token>/', UserAccountActivate.as_view(), name='activate'),
]