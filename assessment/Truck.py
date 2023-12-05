import datetime

# Truck entity
class Truck:

    def __init__(self, packages, location, time,  size = 16, speed = 18, mileage = 0.0):
        self.packages = packages
        self.location = location
        self.depart_time = time
        self.size = size
        self.speed = speed
        self.time = time 
        self.mileage = mileage

    def __str__(self):
        return f"Truck: Size {self.size}, Speed {self.speed}, Location: {self.location}, Mileage: {self.mileage}, Time: {self.time}"
            