@app.route('/stkpush', methods=['POST'])
def stkpush():
    phone = request.form.get("phone")
    amount = request.form.get("amount")

    # If no data came from form, try JSON (for API testing tools)
    if not phone or not amount:
        try:
            data = request.get_json(force=True)
            phone = data.get("phone")
            amount = data.get("amount")
        except:
            return jsonify({"error": "No valid data received"}), 400

    access_token = get_access_token()
    api_url = f"{base_url}/mpesa/stkpush/v1/processrequest"

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    password = base64.b64encode((shortcode + passkey + timestamp).encode()).decode()

    headers = {"Authorization": f"Bearer {access_token}"}
    payload = {
        "BusinessShortCode": shortcode,
        "Password": password,
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": amount,
        "PartyA": phone,
        "PartyB": shortcode,
        "PhoneNumber": phone,
        "CallBackURL": "https://mydomain.com/callback",
        "AccountReference": "Test",
        "TransactionDesc": "Payment"
    }

    response = requests.post(api_url, json=payload, headers=headers)
    return jsonify(response.json())
