import requests
import webbrowser

def get_google_coordinate(address):
    url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {
        "address": address,
        "key": "AIzaSyB3bcu7nCbwkyJiKaNGkYTzBDRHUh67ToQ"
    }
    
    response = requests.get(url, params=params)
    data = response.json()

    if data["status"] == "OK":
        lat = data["results"][0]["geometry"]["location"]["lat"]
        lon = data["results"][0]["geometry"]["location"]["lng"]
        return lat, lon
        url = "https://www.yemeksepeti.com/restaurants/new?lat=" + str(lat) + "&lng=" + str(lon) + "&vertical=restaurants"

    else:
        return None

def get_yemeksepeti_link(address):
    
    lat, lon = get_google_coordinate(address)
    url = "https://www.yemeksepeti.com/restaurants/new?lat=" + str(lat) + "&lng=" + str(lon) + "&vertical=restaurants"
    return url
