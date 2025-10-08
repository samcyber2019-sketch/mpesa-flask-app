import os
from flask import Flask, request, jsonify, render_template
from stk_push import stk_push
import json

app = Flask(__name__)

# ================= Homepage =================
@app.route('/')
def home():
    """
    Render the cashier page where users can enter phone number and amount.
    """
    return render_template('cashier.html')


# ================= STK Push Request =================
@app.route('/stkpush', methods=['POST'])
def stkpush_route():
    """
    Receive phone number and amount from frontend and initiate STK push.
    """
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


# ================= Callback Endpoint =================
@app.route('/callback', methods=['POST'])
def mpesa_callback():
    """
    This route receives M-PESA transaction responses.
    """
    data = request.get_json()
    print("Callback received:", json.dumps(data, indent=4))
    return jsonify({"ResultCode": 0, "ResultDesc": "Accepted"})


# ================= Run App =================
if __name__ == "__main__":
    # Render assigns the port via environment variable
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
