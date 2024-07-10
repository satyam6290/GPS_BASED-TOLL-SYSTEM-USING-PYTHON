import simpy
import random
from geopy.distance import geodesic
import geopandas as gpd
from shapely.geometry import Point, Polygon
import folium
import pandas as pd
import time

# Define constants
TOLL_RATE_PER_KM = 4.00  # INR per kilometer
FIXED_TOLL_FEE = 15.00  # INR
DYNAMIC_PRICING_RATE = 1.50  # INR per kilometer
CONGESTION_THRESHOLD = 1.0  # kilometers
SPEED_LIMIT_SECTIONS = {
    'section_1': 60,
    'section_2': 80,
    'section_3': 100
}
TIME_SLOT_PRICING = {
    'peak': 0.1,
    'off_peak': -0.05
}
PEAK_HOURS = [(7, 9), (17, 19)]

# Define Vehicle class
class Vehicle:
    def __init__(self, env, vehicle_id, start, end, account, toll_zones, payment_vendors):
        self.env = env
        self.vehicle_id = vehicle_id
        self.start = start
        self.end = end
        self.position = start
        self.account = account
        self.toll_zones = toll_zones
        self.payment_vendors = payment_vendors
        self.route = self.generate_route(start, end)
        self.process = env.process(self.run())
        self.stationary_time = 0

    def generate_route(self, start, end):
        # Generates intermediate points between start and end for simplicity
        return [(start[0] + i * (end[0] - start[0]) / 10, start[1] + i * (end[1] - start[1]) / 10) for i in range(11)]

    def run(self):
        for position in self.route:
            if self.stationary_time >= 5:
                print(f'Emergency contingency: {self.vehicle_id} has been stationary for 5 time units.')
                break

            self.position = position
            self.check_toll_zone()
            self.check_speed_limit()
            yield self.env.timeout(1)
            if random.random() < 0.1:  # Randomly generate congestion
                yield self.env.timeout(1)

            # Check if vehicle is stationary
            if self.position == self.route[-1]:
                self.stationary_time += 1
            else:
                self.stationary_time = 0

    def check_toll_zone(self):
        for toll_zone in self.toll_zones:
            if toll_zone.contains(Point(self.position)):
                distance = calculate_distance(self.start, self.position)
                toll = calculate_toll(distance, self.env.now)
                self.account.deduct_toll(toll, random.choice(self.payment_vendors))
                print(f'{self.vehicle_id} crossed toll zone. Toll: {toll:.2f} INR, Remaining balance: {self.account.balance:.2f} INR')

    def check_speed_limit(self):
        for section, limit in SPEED_LIMIT_SECTIONS.items():
            if calculate_distance(self.start, self.position) > limit:
                print(f'{self.vehicle_id} exceeded speed limit in {section}. Speed limit: {limit} km/h')

# Define UserAccount class
class UserAccount:
    def __init__(self, balance):
        self.balance = balance
        self.payments = []

    def deduct_toll(self, amount, vendor):
        self.balance -= amount
        self.payments.append((amount, vendor))
        return self.balance

# Calculate distance between two points
def calculate_distance(start, end):
    return geodesic(start, end).kilometers

# Calculate toll based on distance and dynamic pricing
def calculate_toll(distance, current_time):
    toll = distance * TOLL_RATE_PER_KM + FIXED_TOLL_FEE
    if distance > CONGESTION_THRESHOLD:
        toll += distance * DYNAMIC_PRICING_RATE
    
    # Apply time-slot based pricing
    current_hour = current_time % 24
    for start, end in PEAK_HOURS:
        if start <= current_hour < end:
            toll += toll * TIME_SLOT_PRICING['peak']
            break
    else:
        toll += toll * TIME_SLOT_PRICING['off_peak']
    
    return toll

# Setup the simulation environment
def setup_environment(env, vehicles):
    for vehicle in vehicles:
        env.process(vehicle.run())

# Visualize vehicle movements and toll zones on a map
def visualize_movements(vehicles, toll_zones):
    m = folium.Map(location=[13.0827, 80.2707], zoom_start=12)  # Center map on Chennai
    
    for vehicle in vehicles:
        folium.Marker(location=vehicle.position, popup=vehicle.vehicle_id).add_to(m)
    
    for toll_zone in toll_zones:
        folium.GeoJson(toll_zone).add_to(m)
    
    return m

# Generate analytics report
def generate_report(vehicles):
    report = {
        "Vehicle ID": [],
        "Total Distance Traveled (km)": [],
        "Total Toll Paid (INR)": [],
        "Payment Vendor": []
    }
    for vehicle in vehicles:
        total_distance = calculate_distance(vehicle.start, vehicle.end)
        total_toll = sum(payment[0] for payment in vehicle.account.payments)
        report["Vehicle ID"].append(vehicle.vehicle_id)
        report["Total Distance Traveled (km)"].append(total_distance)
        report["Total Toll Paid (INR)"].append(total_toll)
        report["Payment Vendor"].append([payment[1] for payment in vehicle.account.payments])
    
    df = pd.DataFrame(report)
    df.to_csv("toll_report.csv", index=False)
    print("Report generated: toll_report.csv")

# Define the main function
def main():
    env = simpy.Environment()
    user_account = UserAccount(1000)  # Initial balance in INR
    
    # Define vehicle routes within a 100km by 100km area (approximate coordinates)
    routes = [
        [(13.0827, 80.2707), (13.1420, 80.2800)],
        [(13.0827, 80.2707), (13.1020, 80.2600)],
        [(13.0827, 80.2707), (13.1300, 80.2700)],
        [(13.0827, 80.2707), (13.1200, 80.2750)],
        [(13.0827, 80.2707), (13.1350, 80.2650)],
        [(13.0827, 80.2707), (13.1400, 80.2850)],
        [(13.0827, 80.2707), (13.1250, 80.2950)]
    ]
    
    # Define a toll zone within the area (approximate coordinates)
    toll_zone_coords = [
        (13.05, 80.25), (13.05, 80.35),
        (13.10, 80.25), (13.10, 80.35),
        (13.20, 80.25), (13.20, 80.35), 
        (13.15, 80.35), (13.15, 80.25)
    ]
    toll_zones = [Polygon(toll_zone_coords)]
    
    payment_vendors = ['Vendor_A', 'Vendor_B', 'Vendor_C']
    
    vehicles = [Vehicle(env, f'Vehicle_{i}', route[0], route[1], user_account, toll_zones, payment_vendors) for i, route in enumerate(routes)]

    setup_environment(env, vehicles)
    env.run(until=100)

    m = visualize_movements(vehicles, toll_zones)
    m.save("vehicle_movements_area.html")
    
    generate_report(vehicles)

if __name__ == "__main__":
    main()
