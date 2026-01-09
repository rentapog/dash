from flask import Flask, render_template
import os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://user:password@localhost:5432/seobrain_db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy(app)

from .routes import bp  # Import the Blueprint
app.register_blueprint(bp)  # Register the Blueprint

@app.route('/')
def index():
    paypal_client_id = os.getenv('PAYPAL_CLIENT_ID')
    return render_template('packages.html', paypal_client_id=paypal_client_id)

if __name__ == '__main__':
    app.run(debug=True)
