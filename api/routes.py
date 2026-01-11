from flask import Blueprint, render_template, request, jsonify
from paypal import create_paypal_order
import os

main = Blueprint('main', __name__)

API_KEY = os.getenv('AFFILIATE_API_KEY', 'changeme')  # Set this in your environment for security

@main.route('/')
def home():
    return render_template('home.html')

@main.route('/api/paypal/payout', methods=['POST'])
def paypal_payout():
    # Simple API key authentication
    auth_header = request.headers.get('Authorization', '')
    if not auth_header.startswith('Bearer '):
        return jsonify({'error': 'Missing or invalid Authorization header'}), 401
    token = auth_header.split(' ', 1)[1]
    if token != API_KEY:
        return jsonify({'error': 'Invalid API key'}), 403

    data = request.get_json(force=True)
    affiliate_id = data.get('affiliate_id')
    amount = data.get('amount')
    currency = data.get('currency', 'USD')
    description = data.get('description', 'Affiliate payout')

    if not affiliate_id or not amount:
        return jsonify({'error': 'Missing affiliate_id or amount'}), 400

    # Call your PayPal payout logic (currently only supports USD)
    try:
        result = create_paypal_order(amount, description)
        return jsonify({'status': 'success', 'paypal_result': result}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

