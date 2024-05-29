from django.db import models
from django.contrib.auth.models import AbstractUser
import hashlib
import random

# function to generate unique reference between 100 and 999
def generate_unique_reference():
    # used for booking reference
    return str(random.randint(100, 999))

# extend Djangos built in User model
class CustomUser(AbstractUser):
    # title
    title = models.CharField(max_length=4, blank=False);
    # gender
    gender = models.CharField(max_length=1, blank=False);
    # username 
    username = models.CharField(max_length=64, unique=True);
    # email
    email = models.EmailField(unique=True, blank=False)
    # users first name
    first_name = models.CharField(max_length=64, blank=False)
    # users last name
    last_name = models.CharField(max_length=64, blank=False)

    # define the required fields when creating a new user
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']
    # override username field with email as primary key
    USERNAME_FIELD = 'username'

# model for various flights
class Airport(models.Model):
    # 4 letter ICAO code - unique identifier
    iCAO = models.CharField(max_length=4, primary_key=True)
    # name
    name = models.CharField(max_length=64)
    # airport location
    location = models.CharField(max_length=64)
    # airport location
    country = models.CharField(max_length=128)

    def __str__(self):
        return f"{self.name} ({self.iCAO})"
    
    # getter functions
    def get_icao(self):
        return self.iCAO
    
    def get_name(self):
        return self.name
    
    def get_location(self):
        return self.location
    
    def get_timezone(self):
        return self.timezone
    
    def get_country(self):
        return self.country

# model for various flights
class Flight(models.Model):
    # flight number - 4 character code
    flight_number = models.CharField(max_length=4)
    # outbound point
    outbound = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name='outbound_flight') 
    # destination point
    destination = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name='destination_flight')
    # foreign key for plane
    plane = models.ForeignKey('Plane', on_delete=models.CASCADE, related_name='plane_flight', null=True)
    # departure time
    departure_time = models.DateTimeField()
    # arrival time
    arrival_time = models.DateTimeField()
    # amount of available seats 
    seats = models.IntegerField()
    # price of flight
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    # Unique code field
    unique_code = models.CharField(max_length=128, blank=True, null=True, unique=True)

    def save(self, *args, **kwargs):
        # generate the unique code before saving
        if not self.unique_code:
            self.unique_code = self.generate_unique_code()
        super().save(*args, **kwargs)

    # function to generate unique code
    def generate_unique_code(self):
            # concantenate flight details to create a unique string
            details_str = f"{self.flight_number}-{self.outbound.iCAO}-{self.destination.iCAO}-{self.departure_time}-{self.arrival_time}"

            # Hash the concatenated string to generate a unique code
            unique_code = hashlib.sha256(details_str.encode()).hexdigest()

            return unique_code
            
    # order flights by date
    class Meta:
        ordering = ['departure_time']

    def __str__(self):
        return f"{self.outbound} to {self.destination} on {self.departure_time.date()}"
    
# model for various planes
class Plane(models.Model):
    # name of plane model - primary key
    name = models.CharField(max_length=64, primary_key=True)
    # model of plane
    model = models.CharField(max_length=64)
    # capacity of plane (passengers)
    capacity = models.IntegerField()

    def __str__(self):
        return f"{self.name} ({self.model})"
    
    def get_name(self):
        return self.name
    
    def get_model(self):
        return self.model
    
    def get_capacity(self):
        return self.capacity
    
# model for unique booking reference assigned to each user when flight has been booked
class Booking(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='bookings')
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE, related_name='bookings')
    booking_reference = models.CharField(max_length=12, unique=True)

    def save(self, *args, **kwargs):
        # check if booking reference exists
        if not self.booking_reference:
            # generate a unique reference number
            while True:
                flight_number = self.flight.flight_number
                unique_reference = generate_unique_reference()
                booking_reference = f"{flight_number}-{unique_reference}"
                # check if generated reference is unique
                if not Booking.objects.filter(booking_reference=booking_reference).exists():
                    self.booking_reference = booking_reference
                    break
        # save unique booking reference
        super().save(*args, **kwargs)
    

    