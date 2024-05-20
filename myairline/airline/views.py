from django.shortcuts import render
from .models import Flight
from datetime import datetime
from django.http import JsonResponse
import json
# Create your views here.
def home(request):
    return render(request, 'home.html')

def flights(request):
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

    if is_ajax:
        if request.method =='GET':
            # get the values from the request 
            origin = request.GET.get('origin')
            destination = request.GET.get('destination')
            departure_date = request.GET.get('departure_date')

            print(origin)
            print(destination)
            print(departure_date)

            # if origin and destiantion have been selected
            if origin and destination:
                # query the database for flights based on provided parameters
                flights = Flight.objects.filter(outbound__iCAO__iexact=origin, destination__iCAO__iexact=destination)

                # optionally, filter flights by departure time if provided
                if departure_date:
                    # convert departure_date string to a datetime object
                    departure_date = datetime.strptime(departure_date, '%Y-%m-%d')

                    # filter flights by departure_date
                    flights = flights.filter(departure_time__date=departure_date)

                # serialize filght data into a list of dictionaries
                flight_data = [{'origin': flight.outbound.name,
                                'destination': flight.destination.name,
                                'departure_time': flight.departure_time.strftime('%Y-%m-%d %H:%M:%S'),
                                'arrival_time': flight.arrival_time.strftime('%Y-%m-%d %H:%M:%S'),
                                'seats': flight.seats,
                                'price': str(flight.price)}
                                for flight in flights]
                            
            
                print(flight_data)

                return JsonResponse({'context': flight_data})
            return JsonResponse({'status': 'Invalid request'}, status=400)
    else:
        return render(request, 'flights.html') 
        

def profile(request):
    return render(request, 'profile.html')

def bookings(request):
    return render(request, 'bookings.html')

