from django.shortcuts import render, redirect
from .models import Flight, Booking
from datetime import datetime
from django.http import JsonResponse
import pytz

# Create your views here.
def home(request):
    return render(request, 'home.html')

# function to retrieve timezone
def get_timezone(timezone):
    if timezone == 'YSSY':
        return pytz.timezone('Australia/Sydney')
    elif timezone == 'NZCI':
        return pytz.timezone('Pacific/Chatham')
    else:
        return pytz.timezone('Pacific/Auckland')

def flights(request):
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

    if is_ajax:
        if request.method =='GET':
            # get the values from the request 
            origin = request.GET.get('origin')
            destination = request.GET.get('destination')
            departure_date = request.GET.get('departure_date')

            # assign timezones based on origin and destination points
            origin_timezone = get_timezone(origin)
            destination_timezone = get_timezone(destination)

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
                                'unique_code': flight.unique_code,
                                'destination': flight.destination.name,
                                'departure_time': flight.departure_time.astimezone(origin_timezone).strftime('%Y-%m-%d %H:%M:%S'),
                                'arrival_time': flight.arrival_time.astimezone(destination_timezone).strftime('%Y-%m-%d %H:%M:%S'),
                                'seats': flight.seats,
                                'price': str(flight.price)}
                                for flight in flights if flight.seats > 0]

                return JsonResponse({'context': flight_data})
            
            # for safe measure
            return JsonResponse({'status': 'Invalid request'}, status=400)
        
    elif request.method == 'POST':
        # use unique code to book flight
        unique_code = request.POST.get('unique_code')

        # find flight based on data
        flight = Flight.objects.get(unique_code=unique_code)

        # check if there a seats available on the flight
        if flight.seats > 0:
            # decrement the available seats by one
            flight.seats -= 1
            flight.save()

            # retrieve the authenticated user
            if request.user.is_authenticated:
                user = request.user
                Booking.objects.create(user=user, flight=flight)
            
            return redirect('success')
    else:
        return render(request, 'flights.html') 

def profile(request):
    return render(request, 'profile.html')

def bookings(request):
    # fetch bookings for the current user from Booking model
    user_bookings = Booking.objects.filter(user=request.user)

    if request.method == 'POST':
        # retrieve unique code from form data
        booking_reference = request.POST.get('booking_reference')

        # filter through booking references
        booking_to_cancel = user_bookings.filter(booking_reference=booking_reference).first() # reminder that this will remove the relationship and not the flight itself

        if booking_to_cancel:
            # Increment the seats of the flight by one
            increment_flight = booking_to_cancel.flight
            increment_flight.seats += 1
            increment_flight.save()
            
            # cancel the booking
            booking_to_cancel.delete()

            # redirect to the same page and refresh bookings
            return redirect('bookings')
        
        print(booking_reference)

    return render(request, 'bookings.html', {'user_bookings': user_bookings})

def success(request):
    # fetch the most recent booking made by user
    latest_booking = Booking.objects.filter(user=request.user).order_by('-id').first()

    return render(request, 'success.html', {'latest_booking': latest_booking})

