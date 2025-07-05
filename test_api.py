
import requests
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv('API_KEY')

def test_api_call():
    url = 'http://api.aviationstack.com/v1/flights'
    params = {
        'access_key': API_KEY,
        'limit': 5  # just fetch 5 for now
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        flights = response.json()['data']
        for f in flights:
            airline = f['airline']['name']
            dep = f['departure']['airport']
            arr = f['arrival']['airport']
            date = f['departure']['scheduled'][:10] if f['departure']['scheduled'] else 'N/A'

            print(f"{airline} | {dep} -> {arr} | Date: {date}")
    else:
        print("❌ API call failed!")
        print("Status Code:", response.status_code)
        print("Response:", response.text)

# Run the test
test_api_call()
