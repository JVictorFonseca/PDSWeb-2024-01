from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return HttpResponse('DSWeb 2024.1, 20201014040012 - João Victor da Fonseca Dionisio')