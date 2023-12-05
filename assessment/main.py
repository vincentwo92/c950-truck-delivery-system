# student id: 011319241

import csv
import datetime
import re
from Truck import Truck
from HashTable import HashTable
from Package import Package

# O(n) for time - two addictive for loops; O(n) for space - based on file size
# function to read package data from csv file and load into hash table
# W-2_ChainingHashTable_zyBooks_Key-Value_CSV_Greedy.py
def load_package_data(hash_table):
    with open("CSV/package.csv") as file:
        package_data = csv.reader(file, delimiter=",")
        for package in package_data:
            id = int(package[0])
            street = package[1]
            city = package[2]
            state = package[3]
            zipcode = package[4]
            deadline = package[5]
            weight = package[6]
            # packages start at the hub
            status = "at the hub"
            departure_time = None
            delivery_time = None

            # create package entity
            package = Package(id, street, city, state, zipcode, deadline, weight, status, departure_time, delivery_time)

            # insert new package entity into hash table
            hash_table.insert(id, package)

# O(n) for time - one for loop; O(n) for space - based on file size
# loading csv files
def load_distance_data(distance_data):
    with open(distance_data) as file:
        return list(csv.reader(file))
        
# O(n) for time - one for loop; O(n) for space - based on file size
def load_address_data(address_data):
    with open(address_data) as file:
        return list(csv.reader(file))    

# O(n) for time - function itself is constant lookup, but calls load_distance_data which runs O(n)
# O(n) for space - based on file size
# function for returning distance between two addresses
def distance_between(address1_index, address2_index):
    distances = load_distance_data("CSV/distance.csv")
    distance = distances[address1_index][address2_index]
    
    # distance[i][j] == distance[j][i]
    if distance == "":
        distance = distances[address2_index][address1_index]

    return float(distance)

# O(n*m) for time - for each element in the for loop, a call to get_address_index is performed 
# O(1) for space - using local/temporary variables is just some constant * O(1)
# function to find next package out of truck_packages with address closest to from_address
def min_distance_from(from_address, truck_packages, hash_table):
    # call helper function to get index of from_address
    from_address_index = get_address_index(from_address)

    # initialize helper variables for holding smallest distance and package with min distance from from_address 
    min_distance = float("inf")
    next_package_id = -1

    # loop through every packages on the truck and find the package closest to from_address
    for package_id in truck_packages:
        # search for package in hash table
        package = hash_table.search(package_id)
        # call helper function to get index of respective package address in truck_packages
        package_address_index = get_address_index(package.street)
        # call helper function to get distance between two addresses
        distance = distance_between(from_address_index, package_address_index)
        if distance < min_distance:
            min_distance = distance
            next_package_id = package_id
    return next_package_id

# O(n) for time - calls load_address_data which is O(n); O(n) for space based on file size
# helper function to get address index number if street exists in address csv file column 2
def get_address_index(street):
    # get data from address csv file
    addresses = load_address_data("CSV/address.csv")
    for address in addresses:
        if street in address[2]:
            return int(address[0])
        
# O(n) for time - 2 * O(n) calls to load_package_set simplified to O(n)
# O(n) for space - 3 * data structures created to accomadate truck package sets simplified
# function to prefill package sets on trucks based on notes requirement and return said trucks
def truck_load_packages(hash_table):
    # packages with same address are grouped together except 5/37/38 due to notes requirement
    # initialize first truck based on early deadlines except packages 6, 8, 25, 30 & 31 and packages that have to be delivered together
    truck1 = Truck([1, 4, 7, 13, 14, 15, 16, 19, 20, 21, 29, 34, 37, 39, 40], "4001 South 700 East", datetime.timedelta(hours=8))

    # initialize two additional package sets to be filled in by helper function
    # second truck initiliazed with packages required to be on truck 2 and package 9
    # third truck initialized with packages with late arrival time
    package_set2 = [3, 5, 9, 18, 36, 38]
    package_set3 = [6, 8, 25, 26, 28, 30, 31, 32]

    # list containing packages not yet used
    packages_not_loaded = [2, 10, 11, 12, 17, 22, 23, 24, 27, 33, 35]


    # call helper functions to finish generating package set 2 and 3; limits = 9 and 16 respectively
    load_package_set(package_set2, packages_not_loaded, 9, hash_table)
    load_package_set(package_set3, packages_not_loaded, 16, hash_table)

    # initialize second and third trucks 
    truck2 = Truck(package_set2, "4001 South 700 East", datetime.timedelta(hours=10, minutes=20))
    truck3 = Truck(package_set3, "4001 South 700 East", datetime.timedelta(hours=9, minutes=5))

    return truck1, truck2, truck3

# O(n*m) for time - one while loop which calls min_distance_from which runs at O(n) every iteration
# O(n) for space - proportional to array size of packages_not_loaded
# helper function to finish loading package sets based on minimal distance
def load_package_set(package_set, packages_not_loaded, limit, hash_table):
    starting_package = package_hash_table.search(package_set[0])
    starting_address = starting_package.street

    # loop using helper functions to find next package to be added to truck packages
    while len(package_set) < limit:
        next_package_id = min_distance_from(starting_address, packages_not_loaded, package_hash_table)
        next_package = hash_table.search(next_package_id)
        package_set.append(next_package_id)
        # updating current address and removing package from list of packages not loaded
        starting_address = next_package.street
        packages_not_loaded.remove(next_package_id)

# O(n*m^2) for time - one for loop + one while loop calling distance_between and distance_between; O(n) + (O(n) * (O(n*m) + O(n)) 
# O(n) for space - proportional to size of not_delivered
# algorithm/function to deliver packages
def truck_deliver_packages(truck, hash_table):
    # initialize empty list to hold all undelivered packages on the truck
    not_delivered = []
    # looping through the packages on the truck and appending them to not delivered list
    for id in truck.packages:
        package = hash_table.search(id)
        # update package departure time
        package.departure_time = truck.time
        not_delivered.append(id)

    # clearing truck packages to ensure clean state for nearest neighbor algorithm
    truck.packages.clear()

    # loop through the undelivered packages for the next package to be delivered
    while len(not_delivered) > 0:
        next_package_id = min_distance_from(truck.location, not_delivered, hash_table)
        next_package = package_hash_table.search(next_package_id)
        # get distance from truck current location to next address 
        distance = distance_between(get_address_index(truck.location), get_address_index(next_package.street))

        # repopulate truck packages in order of next closest package
        truck.packages.append(next_package_id)
        # remove package from not delivered 
        not_delivered.remove(next_package_id)
        # update truck mileage based on travel distance from point A to point B
        truck.mileage += distance
        # update truck location
        truck.location = next_package.street
        # update the time based on truck traveling at 18 mph
        truck.time += datetime.timedelta(hours = distance / 18.0)
        # update package delivery time
        next_package.delivery_time = truck.time
        # change package status to delivered
        next_package.status = f"delivered at {truck.time}"
    
# O(n) for time - calls distance_between which runs at O(n); O(1) for space
# helper function for calcuting truck final mileage and time after returning to hub
def return_to_hub(truck):
    hub = "4001 South 700 East"
    distance = distance_between(get_address_index(truck.location), get_address_index(hub))
    truck.mileage += distance
    truck.time += datetime.timedelta(hours = distance / 18.0)

# O(1) for time and space
# helper functin to print menu
def print_menu():
    print()
    print("Possible Menu Options:")
    print("***************************************")
    print("1. Print All Package Status and Total Mileage")
    print("2. Get a Single Package Status with a Time")
    print("3. Get All Package Status with a Time ")
    print("4. Exit the Program  ")
    print("***************************************")

# O(1) for time - one for loop with constant size; O(1) for space
# function for displaying menu option 1
def print_all_package_status_and_total_mileage(hash_table, truck1, truck2, truck3):
    for i in range(1, 41):
        print(hash_table.search(i))
    print(f"Total mileage for the three trucks are {truck1.mileage + truck2.mileage + truck3.mileage}")

# O(n) for time - while loop dependent on user inputs; O(1) for space
# function for displaying one package based on time
def get_single_package_status_with_time(hash_table):
    user_time = convert_user_time()

    # keep looping until valid input provided
    while True:
        try:
            package_id = int(input("Enter package ID number (#1-40): "))
            package = hash_table.search(int(package_id))
            package.update_status(user_time)
            break
        except ValueError:
            print("Invalid input. Please try again.")

# O(1) for time - one for loop with constant size; O(1) for space
# function for displaying all packages based on time
def get_all_package_status_with_time(hash_table):
    user_time = convert_user_time()

    for i in range(1, 41):
        package = hash_table.search(i)
        package.update_status(user_time)

# O(n) for time - while loop dependent on user inputs; O(1) for space
# helper function to get and convert user time
def convert_user_time():
    # using regex for correct time format    
    pattern = r"([01][0-9]|2[0-3]):[0-5][0-9]:([0-5][0-9]){1}$" 
    user_time = input("Enter time in the following format: HH:MM:SS - ")

    # keep looping until user provide time in correct format
    while True:
        if re.match(pattern, user_time):
            (hours, minutes, seconds) = user_time.split(":")
            convert_timedelta = datetime.timedelta(hours=int(hours), minutes=int(minutes), seconds=int(seconds))
            return convert_timedelta
        else:
            user_time = input("Invalid time. Enter time in the following format: HH:MM:SS - ")


"""
Overall program calls multiple helper functions and has one while loop, but since functions are called separately, the time
complexities are simply added together. The helper function truck_deliver_packages have the worse time complexity of O(n*2m) and
will determine the program time complexity. 
O(n*m^2) for time and O(n) for space due to space allocated for size of hash table and package sets in trucks.
"""
# initialize hash table
package_hash_table = HashTable()
# call function to load hash table
load_package_data(package_hash_table)
# initialize trucks
truck1, truck2, truck3 = truck_load_packages(package_hash_table)

# truck 1 start delivering packages at 8AM and truck 3 at 9:05AM after receiving delayed packages
truck_deliver_packages(truck1, package_hash_table)
truck_deliver_packages(truck3, package_hash_table)

# returning trucks 1 and 3 to hub
return_to_hub(truck1)
return_to_hub(truck3)

# update package 9 address to 410 S. State St, Salt Lake City, UT 84111 at 10:20AM
if truck2.time == datetime.timedelta(hours=10, minutes=20):
    package9 = package_hash_table.search(9)
    package9.street = "410 S State St"

# truck 2 will start delivering at 10:20AM after receiving update to package 9 address
truck_deliver_packages(truck2, package_hash_table)

# returning truck 2 to hub
return_to_hub(truck2)


print("Welcome to WGUPS Routing Program.")

# ui to interact with user with four differnt options
while True:
    print_menu()
    user_input = input("What would you like to do? ")
    match user_input:
        # print all status update and total mileage
        case "1":
            print_all_package_status_and_total_mileage(package_hash_table, truck1, truck2, truck3)
        # print information on one package based on time provided
        case "2":
            get_single_package_status_with_time(package_hash_table)
        # print all packages based on time provided
        case "3":
            get_all_package_status_with_time(package_hash_table)
        case "4":
            print("Bye bye!")
            break
