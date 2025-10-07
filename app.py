from flask import Flask, request, jsonify, render_template
import requests
from requests.auth import HTTPBasicAuth
import base64
from datetime import datetime

app = Flask(__name__)

# Credentials and details
consumer_key = "eKOo4k8HfEnMqoAFrIMon7lAj9OayusAhSBkYAKxSyh0GjFH"
consumer_secret = "GlAwDvRDHgFJyHPMp9aJ0VHq5ww9uOx0v2wUJEHo4KBL2C3pR9uLICAVBNYkvYIG"
business_short_code = "3560929"
passkey = "451e31d5fa3ffc9b2d989ef21641df64ac8f7cdff9582b6022f6a1c35527ef0f"
callback_url = "https://5320980d6a60.ngrok-free.app/callback"  # Your current ngrok URL

def get_access_token():
    api_url = "https://api.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
    response = requests.get(api_url, auth=HTTPBasicAuth(consumer_key, consumer_secret))
    return response.json()["access_token"]

@app.route('/cashier')
def cashier():
    return render_template('cashier.html')

@app.route('/stkpush', methods=['POST'])
def stkpush():
    data = request.get_json()
    phone = data['phone']
    amount = data['amount']

    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    password_str = business_short_code + passkey + timestamp
    password = base64.b64encode(password_str.encode()).decode()

    access_token = get_access_token()
    api_url = "https://api.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
    headers = {"Authorization": f"Bearer {access_token}"}
    payload = {
        "BusinessShortCode": business_short_code,
        "Password": password,
        "Timestamp": timestamp,
        "TransactionType": "CustomerBuyGoodsOnline",
        "Amount": amount,
        "PartyA": phone,
        "PartyB": "5662884",  # Your till number
        "PhoneNumber": phone,
        "CallBackURL": callback_url,
        "AccountReference": "TestPayment",
        "TransactionDesc": "Payment for goods"
    }
    response = requests.post(api_url, json=payload, headers=headers)
    return jsonify(response.json())

@app.route('/callback', methods=['POST'])
def callback():
    data = request.get_json()
    print("Callback received:", data)
    return jsonify({"ResultCode": 0, "ResultDesc": "Accepted"})

if __name__ == '__main__':
    app.run(debug=True)
