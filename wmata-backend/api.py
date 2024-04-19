import os

from dotenv import load_dotenv, find_dotenv
import requests

from utils import logger


# load env vars
load_dotenv(find_dotenv())

API_URL = os.environ.get('WMATA_API_URL')
MISC_API_URL = os.environ.get('WMATA_MISC_API_URL')
HEADERS = {'api_key': os.environ.get('WMATA_PRIMARY_KEY')}


@logger
def get_stop_schedule(stop_id: int):
    """API wrapper for stop info + routes served at a stop"""
    r = requests.get(f'{API_URL}/jStopSchedule',
                     params={'StopID': stop_id}, headers=HEADERS)
    try:
        return r.json()
    except:
        return {}


@logger
def get_stop_predictions(stop_id: int):
    """API wrapper for route timings for a stop"""
    r = requests.get(f'{MISC_API_URL}/jPredictions',
                     params={'StopID': stop_id}, headers=HEADERS)
    try:
        return r.json()
    except:
        return {}


@logger
def get_waypoints(route_id: str):
    """API wrapper for route path"""
    r = requests.get(f'{API_URL}/jRouteDetails',
                     params={'RouteID': route_id}, headers=HEADERS)
    try:
        return r.json()
    except:
        return {}


@logger
def get_bus_positions(route_id: str, route_dir_text: str, stop_lon: float, stop_lat: float):
    """API wrapper for live bus positions for a given route, within specified radius from a point"""
    r = requests.get(f'{API_URL}/jBusPositions',
                     params={'RouteID': route_id, 'DirectionText': route_dir_text,
                             'Lon': stop_lon, 'Lat': stop_lat, 'Radius': 10000},
                     headers=HEADERS)
    try:
        return r.json()
    except:
        return {}


@logger
def get_routes():
    r = requests.get(f'{API_URL}/jRoutes', headers=HEADERS)
    try:
        return r.json()
    except:
        return {}
