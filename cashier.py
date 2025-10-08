from flask import Blueprint, render_template, request, jsonify
from stk_push import stk_push

cashier_bp = Blueprint("cashier", __name__)

@cashier_bp.route("/cashier")
def cashier_page():
    return render_template("cashier.html")

@cashier_bp.route("/pay", methods=["POST"])
def pay():
    data = request.get_json()
    phone = data.get("phone")
    amount = data.get("amount")

    if not phone or not amount:
        return jsonify({"error": "Phone and amount required"}), 400

    response = stk_push(phone, amount)
    return jsonify(response)
