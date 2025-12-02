import requests

from config import GOOGLE_PLACES_API_KEY

BASE_URL = "https://places.googleapis.com/v1/"

def search_places(query: str):
    url = BASE_URL + "places:searchText"

    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": GOOGLE_PLACES_API_KEY,
        "X-Goog-FieldMask": (
            "places.id,places.displayName,places.formattedAddress,"
            "places.rating,places.googleMapsUri,places.photos"
        ),
    }

    payload = {
        "textQuery": query,
        "languageCode": "uk"
    }

    response = requests.post(url, headers=headers, json=payload).json()
    return response.get("places", [])

def get_photo_url(photo_name: str, max_width=800):
    return (
        f"{BASE_URL}{photo_name}/media"
        f"?maxWidthPx={max_width}&key={GOOGLE_PLACES_API_KEY}"
    )