import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myairline.settings")

django.setup()

from airline.models import Airport, Plane 

def populate_airports():
    airports_data = [
        {"iCAO": "NZNE", "name": "Dairy Flat Airport", "location": "Dairy Flat", "country": "New Zealand"},
        {"iCAO": "YSSY", "name": "Sydney Airport", "location": "Sydney", "country": "Australia"},
        {"iCAO": "NZRO", "name": "Rotorua Airport", "location": "Rotorua", "country": "New Zealand"},
        {"iCAO": "NZCI", "name": "Tuuta Airport", "location": "Chatham Islands", "country": "New Zealand"},
        {"iCAO": "NZGB", "name": "Claris Airport", "location": "Great Barrier Island", "country": "New Zealand"},
        {"iCAO": "NZTL", "name": "Lake Tekapo Airport", "location": "Lake Tekapo", "country": "New Zealand"},
    ]

    for data in airports_data:
        airport = Airport(**data)
        airport.save()


def populate_planes():
    planes_data = [
        {"name": "SyberJet", "model": "SJ30i", "capacity": 6},
        {"name": "Cirrus SF50 1", "model": "SF50", "capacity": 4},
        {"name": "Cirrus SF50 2", "model": "SF50", "capacity": 4},
        {"name": "HondaJet Elite 1", "model": "Elite", "capacity": 5},
        {"name": "HondaJet Elite 2", "model": "Elite", "capacity": 5},
    ]

    for data in planes_data:
        plane = Plane(**data)
        plane.save()

def main():
    # run all functions to populate database with planes and airports
    populate_airports()

    populate_planes()

    print('Database populated successfully!')


if __name__=='__main__':
    main()