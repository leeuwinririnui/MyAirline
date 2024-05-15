from django.shortcuts import render
from .models import Flight

# Create your views here.
def home(request):
    return render(request, 'home.html')

def flights(request):
    return render(request, 'flights.html', {'flights': Flight.objects.all()})

def profile(request):
    return render(request, 'profile.html')

def bookings(request):
    return render(request, 'bookings.html')

