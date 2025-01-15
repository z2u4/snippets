import requests


API_URL = "http://localhost:3303"

def api_get(url: str, params: dict = None) -> list[dict]:
    return requests.get(f"{API_URL}/{url}", params=params).json()

def api_post(url: str, data: dict = None, params: dict = None) -> dict:
    return requests.post(f"{API_URL}/{url}", json=data, params=params).json()

def api_put(url: str, data: dict = None, params: dict = None) -> dict:
    return requests.put(f"{API_URL}/{url}", json=data, params=params).json()

def api_patch(url: str, data: dict = None, params: dict = None) -> dict:
    return requests.patch(f"{API_URL}/{url}", json=data, params=params).json()

def api_delete(url: str, params: dict = None) -> dict:
    return requests.delete(f"{API_URL}/{url}", params=params).json()

