import requests
from requests.auth import HTTPBasicAuth
from datetime import datetime
import base64

# ✅ LIVE M-PESA credentials
BUSINESS_SHORT_CODE = "3560929"   # Paybill or shortcode
PASSKEY = "451e31d5fa3ffc9b2d989ef21641df64ac8f7cdff9582b6022f6a1c35527ef0f"
CONSUMER_KEY = "eKOo4k8HfEnMqoAFrIMon7lAj9OayusAhSBkYAKxSyh0GjFH"
CONSUMER_SECRET = "GlAwDvRDHgFJyHPMp9aJ0VHq5ww9uOx0v2wUJEHo4KBL2C3pR9uLICAVBNYkvYIG"
CALLBACK_URL = "https://mpesa-flask-app.onrender.com/callback"

# ✅ Use production endpoint for live
BASE_URL = "https://api.safaricom.co.ke"

def get_access_token():
    url = f"{BASE_URL}/oauth/v1/generate?grant_type=client_credentials"
    response = requests.get(url, auth=HTTPBasicAuth(CONSUMER_KEY, CONSUMER_SECRET))
    response.raise_for_status()
    return response.json().get("access_token")

def stk_push(phone_number, amount):
    access_token = get_access_token()
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    data_to_encode = BUSINESS_SHORT_CODE + PASSKEY + timestamp
    password = base64.b64encode(data_to_encode.encode()).decode()
    
    stk_url = f"{BASE_URL}/mpesa/stkpush/v1/processrequest"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    payload = {
        "BusinessShortCode": BUSINESS_SHORT_CODE,
        "Password": password,
        "Timestamp": timestamp,
        "TransactionType": "CustomerBuyGoodsOnline",
        "Amount": amount,
        "PartyA": phone_number,             # Customer's phone
        "PartyB": "5662884",                # Your Till number
        "PhoneNumber": phone_number,
        "CallBackURL": CALLBACK_URL,
        "AccountReference": "SAM-CYBER",    # What appears on STK prompt
        "TransactionDesc": "Payment to SAMEX ICT CENTRE"
    }

    response = requests.post(stk_url, json=payload, headers=headers)
    return response.json()
