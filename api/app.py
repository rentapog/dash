import os
from flask import Flask, render_template
from dotenv import load_dotenv
from .extensions import db

def create_app():
    load_dotenv()
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///local_seobrain.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    from main_routes import bp
    app.register_blueprint(bp)

    from flask import request

    @app.route('/')
    def index():
        paypal_client_id = os.getenv('PAYPAL_CLIENT_ID')
        ref = request.args.get('ref')
        if ref:
            # Show affiliate payment/packages page with affiliate_id
            return render_template('hosting_packages.html', affiliate_id=ref, paypal_client_id=paypal_client_id)
        return render_template('home.html', paypal_client_id=paypal_client_id)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
