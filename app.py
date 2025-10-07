from flask import Flask, request, jsonify, render_template
from stk_push import stk_push
import json

app = Flask(__name__)

# ✅ Homepage route
@app.route('/')
def home():
    return render_template('cashier.html')


# ✅ STK Push request route
@app.route('/stkpush', methods=['POST'])
def stkpush_route():
    data = request.get_json()
    phone = data.get("phone")
    amount = data.get("amount")

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


# ✅ This is needed for Render to run correctly
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
