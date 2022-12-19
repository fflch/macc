from django.shortcuts import render

# Create your views here.


def show(request, code):
    return render(request, f'catalogue/{code}.html')
