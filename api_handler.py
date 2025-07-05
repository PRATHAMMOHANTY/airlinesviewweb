
import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('API_KEY')
GROQ_API_KEY = os.getenv('GROQ_API_KEY')
GROQ_URL = os.getenv('GROQ_URL')
GROQ_MODEL = os.getenv('GROQ_MODEL')
def get_flight_data(limit=20):
    url = 'http://api.aviationstack.com/v1/flights'
    params = {
        'access_key': API_KEY,
        'limit': limit
    }
    response = requests.get(url, params=params)

    if response.status_code == 200:
        return response.json()['data']
    else:
        print("Error:", response.status_code, response.text)
        return []


def get_chatgpt_summary(flights):
    if not flights:
        return "No flights found to summarize."

    flight_lines = [
        f"- {f['airline']['name']} | {f['departure']['airport']} → {f['arrival']['airport']} | {f['flight_status']} | {f['departure']['scheduled']}"
        for f in flights
        if f.get('airline') and f.get('departure') and f.get('arrival')
    ]
    data_summary = "\n".join(flight_lines)

    prompt = f"""
Analyze the following flight data and summarize the demand trends:

{data_summary}

Please summarize:
1. Most popular routes
2. Frequently appearing airlines
3. Any noticeable patterns
"""

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": GROQ_MODEL,
        "messages": [
            {"role": "system", "content": "You are a travel data analyst."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7
    }

    response = requests.post(GROQ_URL, headers=headers, json=payload)
    result = response.json()

    try:
        return result['choices'][0]['message']['content'].strip()
    except:
        return "Failed to fetch summary from GROQ API."
def ask_flight_bot(question, flights):
    if not flights:
        return "No flight data available to answer."

    flight_lines = [
        f"- {f['airline']['name']} | {f['departure']['airport']} → {f['arrival']['airport']} | {f['flight_status']} | {f['departure']['scheduled']}"
        for f in flights
        if f.get('airline') and f.get('departure') and f.get('arrival')
    ]
    data_summary = "\n".join(flight_lines)

    prompt = f"""
You are a flight data assistant. Here is the current flight data:

{data_summary}

Now answer this user question based on the above data:
{question}
"""

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": GROQ_MODEL,
        "messages": [
            {"role": "system", "content": "You are a helpful assistant that analyzes live flight data."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.5
    }

    response = requests.post(GROQ_URL, headers=headers, json=payload)
    result = response.json()

    try:
        return result['choices'][0]['message']['content'].strip()
    except:
        return "Failed to get response from chatbot."
