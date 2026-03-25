"""Geospatial utility using geopy for accurate geodesic distance."""
from geopy.distance import geodesic


def get_distance_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Return geodesic distance in kilometres between two coordinates."""
    return geodesic((lat1, lon1), (lat2, lon2)).km