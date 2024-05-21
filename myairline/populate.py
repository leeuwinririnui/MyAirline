import os
import django
from datetime import datetime, timedelta, time
import pytz

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myairline.settings")

django.setup()

from airline.models import Flight, Airport, Plane 

# timezones
tz_auckland = pytz.timezone('Pacific/Auckland')
tz_chatham = pytz.timezone('Pacific/Chatham')
tz_sydney = pytz.timezone('Australia/Sydney')

# get airport information
dairy_flat = Airport.objects.get(iCAO='NZNE')
sydney = Airport.objects.get(iCAO='YSSY')
rotorua = Airport.objects.get(iCAO='NZRO')
claris = Airport.objects.get(iCAO='NZGB')
tuuta = Airport.objects.get(iCAO='NZCI')
tekapo = Airport.objects.get(iCAO='NZTL')

# function to generate flight dates for the next year
def get_dates_for_the_next_year(weekday):
    current_date = datetime.now().date()
    while current_date.weekday() != weekday:
        current_date += timedelta(days=1)

    dates = []

    for _ in range(52): # 52 weeks into the future
        dates.append(current_date)
        current_date += timedelta(days=7)
    
    return dates


def dairy_flat_to_sydney():
    # get plane
    plane = Plane.objects.get(name='SyberJet')

    # define flight details
    outbound_flight_number = 'SJ01'
    inbound_flight_number = 'SJ02'
    seats = plane.capacity
    price_outbound = 495.00 
    price_inbound = 535.00 

    # calculate dates
    # Friday is weekday 4
    # Sunday is weekday 6
    outbound_dates = get_dates_for_the_next_year(4)
    inbound_dates = get_dates_for_the_next_year(6)

    # populate outbound flights
    for date in outbound_dates:
        departure_time = tz_auckland.localize(datetime.combine(date, time(10, 0))) # 10 am NZ time
        arrival_time = departure_time + timedelta(hours=3, minutes=30) # 3 and a half hour flight
        arrival_time = arrival_time.astimezone(tz_sydney) # convert to sydney timezone

        Flight.objects.create(
            flight_number=outbound_flight_number,
            outbound=dairy_flat,
            destination=sydney,
            plane=plane,
            departure_time=departure_time,
            arrival_time=arrival_time,
            seats=seats,
            price=price_outbound
        )

    # populate inbound flights
    for date in inbound_dates:
        departure_time = tz_sydney.localize(datetime.combine(date, time(15, 0))) # 3 pm Sydney time
        arrival_time = departure_time + timedelta(hours=3) # assume 3 hour flight
        arrival_time = arrival_time.astimezone(tz_auckland)

        Flight.objects.create(
            flight_number=inbound_flight_number,
            outbound=sydney,
            destination=dairy_flat,
            plane=plane,
            departure_time=departure_time,
            arrival_time=arrival_time,
            seats=seats,
            price=price_inbound
        )

    for obj in Flight.objects.all():
        # Access the date field of each object and print it
        if obj.destination == sydney:
            departure_time_local = obj.departure_time.astimezone(tz_auckland)
        else:
            departure_time_local = obj.departure_time.astimezone(tz_sydney)

        # Convert arrival time to local timezone
        arrival_time_local = obj.arrival_time.astimezone(tz_sydney if obj.destination == sydney else tz_auckland)

        print(f"{departure_time_local}   {arrival_time_local}")


def dairy_flat_to_rotorua():
    # Get plane
    plane = Plane.objects.get(name='Cirrus SF50 1') 

    # Define flight details
    outbound_flight_number = 'CJ01'
    inbound_flight_number = 'CJ02'
    seats = plane.capacity
    price_outbound = 170.00  
    price_inbound = 150.00   

    # calculate dates 
    outbound_dates = []
    inbound_dates = []

    for weekday in range(0, 5): # Monday to Friday
        outbound_dates += get_dates_for_the_next_year(weekday)
        inbound_dates += get_dates_for_the_next_year(weekday)

    print(outbound_dates)
    print(inbound_dates)

    # populate outbound flights
    for date in outbound_dates:
        # create two flights for early morning and late afternoon
        for _ in range(2):
            departure_time = tz_auckland.localize(datetime.combine(date, time(6, 0))) if _ == 0 else tz_auckland.localize(datetime.combine(date, time(16, 0)))
            arrival_time = departure_time + timedelta(minutes=40)
            arrival_time = arrival_time.astimezone(tz_auckland)

            Flight.objects.create(
                flight_number=outbound_flight_number,
                outbound=dairy_flat,
                destination=rotorua,
                plane=plane,
                departure_time=departure_time,
                arrival_time=arrival_time,
                seats=seats,
                price=price_outbound
            )

    # populate inbound flights
    for date in inbound_dates:
        # create two flights for mid morning and evening
        for _ in range(2):
            departure_time = tz_auckland.localize(datetime.combine(date, time(8, 0))) if _ == 0 else tz_auckland.localize(datetime.combine(date, time(18, 0)))
            arrival_time = departure_time + timedelta(minutes=45)
            arrival_time = arrival_time.astimezone(tz_auckland)

            Flight.objects.create(
                flight_number=inbound_flight_number,
                outbound=rotorua,
                destination=dairy_flat,
                plane=plane,
                departure_time=departure_time,
                arrival_time=arrival_time,
                seats=seats,
                price=price_inbound
            )

    for obj in Flight.objects.all():
        # Access the date field of each object and print it
        departure_time_local = obj.departure_time.astimezone(tz_auckland)

        arrival_time = obj.arrival_time.astimezone(tz_auckland)

        print(f"{obj.outbound.name }    {departure_time_local}    {obj.destination.name }    {arrival_time}")

  
def dairy_flat_to_great_barrier():
    # get airports 
    dairy_flat = Airport.objects.get(iCAO='NZNE')
    claris = Airport.objects.get(iCAO='NZGB')

    plane = Plane.objects.get(name="Cirrus SF50 2")

    # Define flight details
    outbound_flight_number = 'CJ03'
    inbound_flight_number = 'CJ04'
    seats = plane.capacity
    price_outbound = 180.00  
    price_inbound = 175.00

    # calculate dates
    outbound_dates = []
    inbound_dates = []

    for weekday in range(0, 6):  # Monday to Saturday
        if weekday % 2 == 0:  # Monday, Wednesday, and Friday
            outbound_dates += get_dates_for_the_next_year(weekday)
        else:  # Tuesday, Thursday, and Saturday
            inbound_dates += get_dates_for_the_next_year(weekday)


    # populate outbound flights
    for date in outbound_dates:
        departure_time = tz_auckland.localize(datetime.combine(date, time(8, 00))) 
        arrival_time = departure_time + timedelta(minutes=30)
        arrival_time = arrival_time.astimezone(tz_auckland)

        Flight.objects.create(
            flight_number=outbound_flight_number,
            outbound=dairy_flat,
            destination=claris,
            plane=plane,
            departure_time=departure_time,
            arrival_time=arrival_time,
            seats=seats,
            price=price_inbound
        )

    # populate inbound flights
    for date in inbound_dates:
        departure_time = tz_auckland.localize(datetime.combine(date, time(7, 30))) 
        arrival_time = departure_time + timedelta(minutes=30)
        arrival_time = arrival_time.astimezone(tz_auckland)

        Flight.objects.create(
            flight_number=inbound_flight_number,
            outbound=claris,
            destination=dairy_flat,
            plane=plane,
            departure_time=departure_time,
            arrival_time=arrival_time,
            seats=seats,
            price=price_outbound
        )

    for obj in Flight.objects.all():
        # Access the date field of each object and print it
        if obj.destination == claris:
            departure_time_local = obj.departure_time.astimezone(tz_auckland)
        else:
            departure_time_local = obj.departure_time.astimezone(tz_chatham)

        # Convert arrival time to local timezone
        arrival_time_local = obj.arrival_time.astimezone(tz_chatham if obj.destination == claris else tz_auckland)

        print(f"{departure_time_local}   {arrival_time_local}")


def dairy_flat_to_tuuta():
    # get airports
    dairy_flat = Airport.objects.get(iCAO='NZNE')
    tuuta = Airport.objects.get(iCAO='NZCI')

    # get plane
    plane = Plane.objects.get(name="HondaJet Elite 1")

    # define flight details
    outbound_flight_number = 'HE01'
    inbound_flight_number = 'HE02'
    seats = plane.capacity
    price_outbound = 220.00  
    price_inbound = 195.00

    # calculate dates
    outbound_dates = []
    inbound_dates = []

    # calculate outbound dates
    outbound_dates += get_dates_for_the_next_year(1) # tuesday
    outbound_dates += get_dates_for_the_next_year(4) # friday

    # calculate inbound dates
    inbound_dates += get_dates_for_the_next_year(2) # wednesday
    inbound_dates += get_dates_for_the_next_year(5) # saturday

    # populate outbound flights
    for date in outbound_dates:
        departure_time = tz_auckland.localize(datetime.combine(date, time(9, 15))) 
        arrival_time = departure_time + timedelta(hours=2, minutes=15)
        arrival_time = arrival_time.astimezone(tz_chatham)

        Flight.objects.create(
            flight_number=outbound_flight_number,
            outbound=dairy_flat,
            destination=tuuta,
            plane=plane,
            departure_time=departure_time,
            arrival_time=arrival_time,
            seats=seats,
            price=price_outbound
        )

    # populate inbound flights
    for date in inbound_dates:
        departure_time = tz_chatham.localize(datetime.combine(date, time(10, 0))) 
        arrival_time = departure_time + timedelta(hours=2, minutes=25)
        arrival_time = arrival_time.astimezone(tz_auckland)

        Flight.objects.create(
            flight_number=inbound_flight_number,
            outbound=tuuta,
            destination=dairy_flat,
            plane=plane,
            departure_time=departure_time,
            arrival_time=arrival_time,
            seats=seats,
            price=price_inbound
        )

    for obj in Flight.objects.all():
        # Access the date field of each object and print it
        departure_time_local = obj.departure_time.astimezone(tz_auckland)

        arrival_time = obj.arrival_time.astimezone(tz_auckland)

        print(f"{obj.outbound.name }    {departure_time_local}    {obj.destination.name }    {arrival_time}")

def dairy_flat_to_tekapo():
    # get plane
    plane = Plane.objects.get(name="HondaJet Elite 2")

    # define flight details
    outbound_flight_number = 'HE03'
    inbound_flight_number = 'HE04'
    seats = plane.capacity
    price_outbound = 120.00  
    price_inbound = 130.00
    
    outbound_date = []
    inbound_date = []

    # calculate dates
    outbound_date += get_dates_for_the_next_year(0) # monday
    inbound_date += get_dates_for_the_next_year(1) # tuesday

    # outbound flight
    for date in outbound_date:
        departure_time = tz_auckland.localize(datetime.combine(date, time(9, 30))) 
        arrival_time = departure_time + timedelta(hours=1, minutes=25)
        arrival_time = arrival_time.astimezone(tz_auckland)

        Flight.objects.create(
                flight_number=outbound_flight_number,
                outbound=dairy_flat,
                destination=tekapo,
                plane=plane,
                departure_time=departure_time,
                arrival_time=arrival_time,
                seats=seats,
                price=price_outbound
            )
        
    # inbound flight
    for date in inbound_date:
        # inbound flight
        departure_time = tz_auckland.localize(datetime.combine(date, time(10, 0))) 
        arrival_time = departure_time + timedelta(hours=1, minutes=25)
        arrival_time = arrival_time.astimezone(tz_auckland)

        Flight.objects.create(
                flight_number=inbound_flight_number,
                outbound=tekapo,
                destination=dairy_flat,
                plane=plane,
                departure_time=departure_time,
                arrival_time=arrival_time,
                seats=seats,
                price=price_inbound
        )
    
    for obj in Flight.objects.all():
        # Access the date field of each object and print it
        departure_time_local = obj.departure_time.astimezone(tz_auckland)

        arrival_time = obj.arrival_time.astimezone(tz_auckland)

        print(f"{obj.outbound.name }    {departure_time_local}    {obj.destination.name }    {arrival_time}")


def main():
    # run all functions to populate database with flights
    dairy_flat_to_sydney()

    dairy_flat_to_rotorua()

    dairy_flat_to_great_barrier()

    dairy_flat_to_tuuta()

    dairy_flat_to_tekapo()

    print('Database populated successfully!')


if __name__=='__main__':
    main()
