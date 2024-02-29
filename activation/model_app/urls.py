from django.urls import path
from .views import ModelView

urlpatterns = [
    path('post/', ModelView.as_view()),
]