import requests
import datetime
import base64
from requests.auth import HTTPBasicAuth

# === LIVE SAFARICOM M-PESA CREDENTIALS ===
CONSUMER_KEY = "eKOo4k8HfEnMqoAFrIMon7lAj9OayusAhSBkYAKxSyh0GjFH"
CONSUMER_SECRET = "GlAwDvRDHgFJyHPMp9aJ0VHq5ww9uOx0v2wUJEHo4KBL2C3pR9uLICAVBNYkvYIG"

BUSINESS_SHORT_CODE = "3560929"      # HOr
PASSKEY = "451e31d5fa3ffc9b2d989ef21641df64ac8f7cdff9582b6022f6a1c35527ef0f"
TILL_NUMBER = "5662884"              # PartyB
CALLBACK_URL = "https://mpesa-flask-app.onrender.com/callback"

def get_access_token():
    url = "https://api.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
    response = requests.get(url, auth=HTTPBasicAuth(CONSUMER_KEY, CONSUMER_SECRET))
    response.raise_for_status()
    return response.json()["access_token"]

def stk_push(phone, amount):
    access_token = get_access_token()
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    password = base64.b64encode((BUSINESS_SHORT_CODE + PASSKEY + timestamp).encode()).decode()

    url = "https://api.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
    payload = {
        "BusinessShortCode": BUSINESS_SHORT_CODE,
        "Password": password,
        "Timestamp": timestamp,
        "TransactionType": "CustomerBuyGoodsOnline",
        "Amount": amount,
        "PartyA": phone,
        "PartyB": TILL_NUMBER,
        "PhoneNumber": phone,
        "CallBackURL": CALLBACK_URL,
        "AccountReference": "SAM-CYBER",
        "TransactionDesc": "Payment to SAMEX ICT CENTRE - SAM-CYBER"
    }
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)
    return response.json()
