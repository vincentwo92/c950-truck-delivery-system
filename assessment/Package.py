# Package entity 
class Package:

    def __init__(self, id, street, city, state, zipcode, deadline, weight, status, departure_time, delivery_time):
        self.id = id
        self.street = street
        self.city = city
        self.state = state
        self.zipcode = zipcode
        self.deadline = deadline
        self.weight = weight
        self.status = status
        self.departure_time = departure_time
        self.delivery_time = delivery_time

    def __str__(self):
        return f"Delivery ID: {self.id}, Address: {self.street}, Deadline: {self.deadline}, City: {self.city}, Zipcode: {self.zipcode}, Weight: {self.weight} lbs, Status: {self.status}"
    
    # O(1) for time and space
    # function to update status based on time provided
    def update_status(self, convert_timedelta):
        if self.delivery_time < convert_timedelta:
            print(f"Delivery ID: {self.id}, Address: {self.street}, Deadline: {self.deadline}, City: {self.city}, Zipcode: {self.zipcode}, Weight: {self.weight} lbs, Status: {self.status}")
        elif self.departure_time > convert_timedelta:
            print(f"Delivery ID: {self.id}, Address: {self.street}, Deadline: {self.deadline}, City: {self.city}, Zipcode: {self.zipcode}, Weight: {self.weight} lbs, Status: at the Hub")
        else:
            print(f"Delivery ID: {self.id}, Address: {self.street}, Deadline: {self.deadline}, City: {self.city}, Zipcode: {self.zipcode}, Weight: {self.weight} lbs, Status: en route")
