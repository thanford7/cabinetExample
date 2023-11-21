from django.http import HttpResponse
from django.shortcuts import render


def home(request):
    return HttpResponse('All is well with this app')
