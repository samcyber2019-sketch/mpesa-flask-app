@app.route('/stkpush', methods=['POST'])
def stkpush_route():
    data = request.get_json()
    phone = data.get("phone")
    amount = data.get("amount")

    # ✅ Automatically fix phone format
    if phone.startswith("07"):
        phone = "254" + phone[1:]

    if not phone or not amount:
        return jsonify({"error": "Phone number and amount are required"}), 400

    response = stk_push(phone, amount)
    return jsonify(response)

# ✅ Callback route (for M-PESA response)
@app.route('/callback', methods=['POST'])
def mpesa_callback():
    data = request.get_json()
    print("Callback received:", json.dumps(data, indent=4))
    return jsonify({"ResultCode": 0, "ResultDesc": "Accepted"})

# ✅ For Render hosting
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)
