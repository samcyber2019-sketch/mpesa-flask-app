from flask import Flask, request, jsonify, render_template
from stk_push import stk_push
import os
import json

app = Flask(__name__)

# =======================
# Homepage route
# =======================
@app.route('/')
def home():
    return render_template('cashier.html')

# =======================
# STK Push route
# =======================
@app.route('/stkpush', methods=['POST'])
def stkpush_route():
    data = request.get_json()
    phone = data.get("phone")
    amount = data.get("amount")

    if not phone or not amount:
        return jsonify({"error": "Phone number and amount are required"}), 400

    try:
        response = stk_push(phone, amount)
        return jsonify(response)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# =======================
# Callback route (M-PESA response)
# =======================
@app.route('/callback', methods=['POST'])
def mpesa_callback():
    data = request.get_json()
    print("Callback received:", json.dumps(data, indent=4))  # Logs in Render
    return jsonify({"ResultCode": 0, "ResultDesc": "Accepted"})

# =======================
# Render requires this
# =======================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
