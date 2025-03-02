# libraries
import http.client
import json
from typing import Union, Dict
import logging
import urllib.parse
import pandas as pd
import pickle
import os
import math
import numpy as np
import zipfile

logger = logging.getLogger(__name__)

def calculate_distance(origin: str, destination: str, api_key: str) -> Union[float, str]:
    """Calculate road distance using Google Distance Matrix API"""
    if not api_key:
        logger.error("API key is missing")
        return "Error: Google API key is not configured"

    try:
        # URL encode the parameters
        encoded_origin = urllib.parse.quote(origin)
        encoded_destination = urllib.parse.quote(destination)

        conn = http.client.HTTPSConnection("maps.googleapis.com")

        path = f"/maps/api/distancematrix/json?destinations={encoded_destination}&origins={encoded_origin}&mode=driving&units=imperial&key={api_key}"

        conn.request("GET", path)
        response = conn.getresponse()
        data = json.loads(response.read().decode("utf-8"))

        if data.get("status") != "OK":
            error_message = data.get("error_message", data.get("status", "Unknown error"))
            logger.error(f"API Error: {error_message}")
            if "REQUEST_DENIED" in str(error_message):
                return "Error: API key is invalid or not properly configured. Please ensure the Distance Matrix API is enabled and billing is set up."
            return f"API Error: {error_message}"

        if data["rows"][0]["elements"][0]["status"] != "OK":
            logger.error("Could not calculate distance between these locations")
            return "Could not calculate distance between these locations"

        # Distance in meters (convert to kilometers)
        distance_text = data["rows"][0]["elements"][0]["distance"]["text"]
        # Extract numeric value and convert to kilometers if in miles
        # Remove commas from the number and convert to float
        distance_value = float(distance_text.split()[0].replace(',', ''))
        if "mi" in distance_text:
            distance_value = distance_value * 1.60934  # Convert miles to kilometers

        return round(distance_value, 2)

    except Exception as e:
        logger.error(f"Error calculating distance: {str(e)}")
        return f"Error calculating distance: {str(e)}"
    finally:
        if 'conn' in locals():
            conn.close()

def calculate_railway_metrics(road_distance: float) -> Dict[str, float]:
    """Calculate railway metrics based on road distance"""
    # Assumptions for calculation
    estimated_cost = 996875*road_distance
    # Implement population 

    return {
        "estimated_cost": round(estimated_cost, 2),
    }

def haversine(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculate the distance between two points from lat/long into kilometers"""
    R = 6371  # Earth radius in kilometers
    
    # Convert degrees to radians
    lat1_rad, lon1_rad, lat2_rad, lon2_rad = map(math.radians, [lat1, lon1, lat2, lon2])
    
    # Differences
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad
    
    # Haversine formula
    a = math.sin(dlat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    return R * c

def longitude_distance(latitude: float) -> float:
    """Returns the distance in kilometers per degree of longitude at a given latitude"""
    return 111.32 * math.cos(math.radians(latitude))


# Unpack the cache.zip file
with zipfile.ZipFile("cache.zip", "r") as zip_ref:
    zip_ref.extract("cache.pkl")

# Load the cache.pkl into a DataFrame
global_data = pd.DataFrame(pickle.load(open("cache.pkl", "rb")), columns=['longitude', 'latitude', 'population'])
# Filter out rows with zero population
global_data = global_data[global_data['population'] != 0.0]

def calculate_population(longitude: float, latitude: float, radius: float) -> float:
    """Calculate the total population within a given radius of a point"""
    data = global_data.copy()
    
    # Calculate distance bounds
    lat_distance = radius / 111
    lon_distance = longitude_distance(latitude)
    lon_min = longitude - (radius / lon_distance)
    lon_max = longitude + (radius / lon_distance)
    lat_min = latitude - lat_distance
    lat_max = latitude + lat_distance

    # Filter based on bounding box
    data = data[(data['longitude'] >= lon_min) & (data['longitude'] <= lon_max) &
                (data['latitude'] >= lat_min) & (data['latitude'] <= lat_max)]

    # Convert degrees to radians for vectorized haversine calculation
    lat1_rad = math.radians(latitude)
    lon1_rad = math.radians(longitude)
    data['lat_rad'] = np.radians(data['latitude'])
    data['lon_rad'] = np.radians(data['longitude'])

    # Vectorized haversine distance calculation
    dlat = data['lat_rad'] - lat1_rad
    dlon = data['lon_rad'] - lon1_rad
    a = np.sin(dlat / 2)**2 + np.cos(lat1_rad) * np.cos(data['lat_rad']) * np.sin(dlon / 2)**2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
    data['distance'] = 6371 * c

    # Filter based on radius
    data = data[data['distance'] <= radius]

    # Return population
    return data['population'].sum()

def calculate_ridership(populationA: float, populationB: float, distance: float, mode_share: float = 1.0) -> float:
    """
    Calculates ridership between two cities given their population and distance (km)

    Equation derived from: https://pedestrianobservations.com/2021/04/25/sanity-checking-my-hsr-ridership-model/

    equation modified to be calibrated with US rail data
    """
    distance_modifier = 2
    base_factor = 11.67
    population_scaling = 0.8
    return mode_share * base_factor * (populationA)**population_scaling * (populationB)**population_scaling / distance**distance_modifier

def revenue(ridership: float, ticket_price: float = 80) -> float:
    """Calculate revenue based on ridership and ticket price, default price is 80 ($)"""
    return ridership * ticket_price

def travel_time(distance: float, accel_distance: float = 10, accel_time: float = 5, max_speed: float = 250) -> float:
    """Calculate travel time in minutes based on Shinkansen acceleration"""
    time = 0
    distance -= accel_distance * 2
    time += accel_time * 2
    time += distance / max_speed
    return time

def yearly_cost(distance: float, cost_per_km: float = 1_000_000) -> float:
    """Calculate yearly cost based on distance and cost per km, default is 1,000,000$/km"""
    return distance * cost_per_km

def yearly_profit(yearly_cost: float, yearly_revenue: float) -> float:
    """Calculate yearly profit based on yearly cost and revenue"""
    return yearly_revenue - yearly_cost





distance = 80
population1 = (calculate_population(-84.512016, 39.103119, 10))  # Example usage
population2 = (calculate_population(-84.191605, 39.758949, 10))  # Example usage
ridership = (calculate_ridership(population1, population2, distance))
estimated_cost = 30000000*distance
travel_time = travel_time(distance)
yearly_cost = yearly_cost(distance)
revenue = revenue(ridership)
yearly_profit = yearly_profit(yearly_cost, revenue)

print(f"Estimated Construction Cost: ${estimated_cost}")
print(f"Estimated Ridership: {ridership}")
print(f"Travel Time: {travel_time} minutes")
print(f"Yearly Cost: ${yearly_cost}")
print(f"Yearly Profit: ${yearly_profit}")
print(f"Population in radius of 10 km: {population1}")
print(f"Population in radius of 10 km: {population2}")
print(f"Years to profit: {estimated_cost/(yearly_profit)}")

print(calculate_ridership(1000000,1000000, 200))


