import os
from flask import Flask, render_template_string, request, redirect, url_for, session
import stripe

app = Flask(__name__)
app.secret_key = "super_secret_session_encryption_key"

# Configure Stripe API keys (Use Test Keys from dashboard)
stripe.api_key = "sk_test_mock_key_replace_with_yours"

# In-Memory Database Simulation
PRODUCTS = {
    1: {"name": "Data Analytics Masterclass", "price": 4999, "desc": "Complete SQL & Python Blueprint"},
    2: {"name": "Automated OCR Toolkit", "price": 2999, "desc": "Small Business Bill Extraction Suite"}
}

# Base HTML Blueprint Layout
STORE_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>NextGen Dev Store</title>
    <style>
        body { font-family: sans-serif; background-color: #0B0C10; color: #C5C6C7; margin: 40px; }
        .container { max-width: 800px; margin: 0 auto; }
        .product-card { background: #1F2833; padding: 20px; border: 1px solid #45A29E; border-radius: 6px; margin-bottom: 20px; }
        .btn { background: #45A29E; color: #0B0C10; padding: 10px 20px; border: none; font-weight: bold; border-radius: 4px; cursor: pointer; text-decoration: none; display: inline-block; }
        .btn:hover { background: #66FCF1; }
        .cart-status { text-align: right; margin-bottom: 20px; color: #66FCF1; }
    </style>
</head>
<body>
    <div class="container">
        <div class="cart-status">🛒 Cart Items: {{ cart_count }}</div>
        <h1>🚀 Professional Development Store</h1>
        <hr style="border: 0; border-top: 1px solid #45A29E; margin-bottom: 30px;">
        
        {% for id, prod in products.items() %}
            <div class="product-card">
                <h2>{{ prod.name }}</h2>
                <p>{{ prod.desc }}</p>
                <p style="font-size: 20px; color: #66FCF1; font-weight: bold;">${{ "%.2f"|format(prod.price / 100) }}</p>
                <form action="{{ url_for('add_to_cart', product_id=id) }}" method="POST">
                    <button type="submit" class="btn">Add to Cart</button>
                </form>
            </div>
        {% endfor %}
        
        {% if cart_count > 0 %}
            <div style="text-align: center; margin-top: 40px;">
                <a href="{{ url_for('create_checkout_session') }}" class="btn" style="font-size: 18px; padding: 15px 30px;">Proceed to Secure Stripe Checkout</a>
            </div>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    if 'cart' not in session:
        session['cart'] = []
    return render_template_string(STORE_TEMPLATE, products=PRODUCTS, cart_count=len(session['cart']))

@app.route('/add-to-cart/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    if 'cart' not in session:
        session['cart'] = []
    session['cart'].append(product_id)
    session.modified = True  # Tell Flask session tracker that mutable array changed
    return redirect(url_for('home'))

@app.route('/create-checkout-session')
def create_checkout_session():
    if 'cart' not in session or len(session['cart']) == 0:
        return redirect(url_for('home'))
        
    line_items = []
    for prod_id in session['cart']:
        prod = PRODUCTS[prod_id]
        line_items.append({
            'price_data': {
                'currency': 'usd',
                'product_data': {'name': prod['name']},
                'unit_amount': prod['price'],
            },
            'quantity': 1,
        })
        
    try:
        # Hand over payment verification matrix to Stripe Hosted Forms
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=line_items,
            mode='payment',
            success_url='http://localhost:5000/success',
            cancel_url='http://localhost:5000/cancel',
        )
        return redirect(checkout_session.url, code=303)
    except Exception as e:
        return str(e)

@app.route('/success')
def success():
    session['cart'] = []  # Clear cart state upon verified capture
    return "<h1>🎉 Payment Successful! Your assets have been unlocked.</h1><a href='/'>Return to Shop</a>"

@app.route('/cancel')
def cancel():
    return "<h1>❌ Order cancelled. Your cart state is preserved.</h1><a href='/'>Return to Shop</a>"

if __name__ == '__main__':
    app.run(debug=True)
