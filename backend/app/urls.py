from django.urls import path

from . import views
from .api import partner

urlpatterns = [
    path('', views.home, name='home'),
    path('partner', partner.RxFillView.as_view()),
]
