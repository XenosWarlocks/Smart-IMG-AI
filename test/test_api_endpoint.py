import requests

response = requests.post(
    "http://localhost:8000/api/analyze-image-url",
    json={
        "image_url": "https://t3.ftcdn.net/v2/jpg/01/76/69/98/1000_F_176699844_adobeanalytics.jpg",
        "api_key1": "api",
        "api_key2": "-api"
    }
)

# python test_api_endpoint.py
print(response.json())
