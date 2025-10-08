from flask import Flask, request, jsonify
from cashier import cashier_bp

app = Flask(__name__)
app.register_blueprint(cashier_bp)

@app.route("/")
def home():
    return "SAMEX ICT CENTRE - M-PESA Payment Gateway Active"

@app.route("/callback", methods=["POST"])
def callback():
    data = request.get_json()
    print("M-PESA CALLBACK:", data)
    return jsonify({"ResultCode": 0, "ResultDesc": "Callback received successfully"})

if __name__ == "__main__":
    app.run(debug=True)
