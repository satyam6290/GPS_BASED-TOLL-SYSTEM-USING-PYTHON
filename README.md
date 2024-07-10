# GPS Toll-Based System Simulation

## Overview

This project simulates a GPS toll-based system using Python. The simulation covers vehicle movements, toll calculations, and payments within a predefined geographical area, using geospatial coordinates to define road networks and toll zones. The system includes dynamic pricing based on congestion and time slots, speed limit checks, emergency contingencies, and support for multiple payment vendors.

## Features

- **Vehicle Movement Simulation**: Simulates vehicles moving along predefined routes using GPS coordinates.
- **Toll Zone Definition**: Defines toll zones or points using GPS coordinates.
- **Distance Calculation**: Calculates the distance traveled by each vehicle within toll zones.
- **Toll Calculation**: Computes toll charges based on the distance traveled or zones passed.
- **Payment Simulation**: Simulates the process of deducting toll charges from user accounts.
- **Dynamic Pricing**: Implements congestion-based and time-slot based pricing.
- **Speed Limit Checks**: Ensures vehicles adhere to speed limits, with varying limits for different sections of the toll road.
- **Emergency Contingencies**: Handles scenarios where a vehicle is stationary for a period.
- **Visualization**: Visualizes vehicle movements and toll zones on a map.
- **Analytics and Reporting**: Generates reports on vehicle movements, toll collections, and system performance.

## Installation

### Prerequisites

- Python 3.x
- PyCharm IDE

### Required Python Packages

- simpy
- geopy
- geopandas
- shapely
- folium
- pandas

### Setup

1. Clone the repository:

```bash
git clone https://github.com/yourusername/gps-toll-based-system.git
cd gps-toll-based-system

## Create and activate a virtual environment

python -m venv venv
Windows use `venv\Scripts\activate`

Install the required packages:

pip install -r requirements.txt

Open the project in PyCharm.

Run the simulation script:

python toll_simulation.py

This will start the simulation, showing the movements of vehicles, toll calculations, and deductions from user accounts.

### View the generated reports and map visualization:
A CSV report will be generated (toll_report.csv) detailing vehicle movements, total distances traveled, tolls paid, and payment vendors used.
A map visualization (vehicle_movements_area.html) will be saved, showing vehicle movements and toll zones.



Example Simulation Workflow
Setup Environment:
Define road network and toll zones using geospatial coordinates.
Initialize vehicles with starting locations and destinations.
Simulate Vehicle Movement:
Use SimPy to simulate vehicle movement along the network, updating GPS coordinates over time.
Detect Toll Zone Crossings:
Check if a vehicle's path intersects with a toll zone using Shapely and GeoPandas.
Calculate Toll Charges:
Calculate tolls based on the type of crossing (distance within zone or fixed fee for zone crossing) using predefined rates.
Simulate Payments:
Deduct toll charges from the simulated user account balances.
Analytics and Reporting:
Generate reports on vehicle movements, toll collections, and system performance.
Future Enhancements
Integration with real-time traffic data for more accurate congestion-based pricing.
Implementation of a web-based dashboard for real-time monitoring and reporting.
Support for more complex road networks and multiple toll zones.
License
This project is licensed under the MIT License. See the LICENSE file for details.

Acknowledgements
Inspired by real-world toll systems and geospatial simulation techniques.
Developed as a demonstration of combining simulation, geospatial analysis, and dynamic pricing in Python.
Contact
For any queries or issues, please contact your-email@example.com.


