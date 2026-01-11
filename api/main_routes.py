from flask import Blueprint
import hmac
from datetime import datetime
from .extensions import db
from .models import User, Referral, Package, UserPackage, Payment
from .paypal import create_paypal_order

bp = Blueprint('main', __name__)

# Route for /api-docs
@bp.route('/api-docs')
def api_docs():
    return render_template('api_docs.html')
# Route for /careers
@bp.route('/careers')
def careers():
    return render_template('careers.html')

# Route for /user-agreement
@bp.route('/user-agreement')
def user_agreement():
    return render_template('user_agreement.html')

# Route for /cookie-policy
@bp.route('/cookie-policy')
def cookie_policy():
    return render_template('cookie_policy.html')

# Route for /how-it-works (now correctly placed after bp definition)
@bp.route('/how-it-works')
def how_it_works():
    return render_template('how_it_works.html')

from flask import Blueprint, session, redirect, url_for, render_template, request, jsonify, current_app
import secrets
import hashlib
import requests
import os
import base64
import hmac
from datetime import datetime
from .extensions import db
from .models import User, Referral, Package, UserPackage, Payment
from paypal import create_paypal_order

bp = Blueprint('main', __name__)


# Route for /blog to render the blog page with dynamic posts
@bp.route('/blog')
def blog():
    blog_posts = [
        {
            'title': 'How Daily Payouts Empower Our Affiliates',
            'date': datetime.now().strftime('%B %d, %Y'),
            'badge': 'Featured',
            'badge_style': '',
            'content': '''At HostingPro, we believe in rewarding our affiliates quickly and fairly. Our daily payout system is designed to put your earnings in your hands as soon as possible, eliminating the long wait times that plague traditional affiliate programs. Every day, your commissions are calculated and made available for instant withdrawal, giving you the flexibility to manage your finances on your terms.<br><br>This approach not only motivates our affiliates to keep growing their networks, but also builds trust and transparency. You can see your progress in real time, track your referrals, and watch your income grow day by day. Whether you’re a seasoned marketer or just starting out, daily payouts mean you’re never left waiting for your hard-earned money.<br><br>Our system is automated and secure, ensuring that every transaction is processed accurately. With HostingPro, you’re not just earning commissions—you’re building a reliable, daily income stream that can scale as you do. Join us and experience the freedom of daily earnings!'''
        },
        {
            'title': 'The Power of Referrals: Why 3 is the Magic Number',
            'date': (datetime.now()).strftime('%B %d, %Y'),
            'badge': 'Referral Tips',
            'badge_style': 'background:linear-gradient(90deg,#e60000 70%,#ffd700 100%);',
            'content': '''Our affiliate program is built on the principle of fairness and sustainability. That’s why we require just three successful referrals before you unlock 100% of your daily earnings. This simple rule ensures that everyone contributes to the growth of the community, while also giving new affiliates a clear, achievable goal.<br><br>Once you’ve referred three new customers, you’ll enjoy full access to your daily payouts with no deductions. This system encourages teamwork and helps everyone succeed together. Plus, it’s a great way to motivate your network—help your referrals reach their first three, and you’ll both benefit!<br><br>By focusing on quality over quantity, we maintain a healthy, active user base and ensure that our rewards remain generous for all. Start sharing your unique link today and see how quickly you can reach your first three referrals!'''
        },
        {
            'title': 'Maximizing Your Earnings with HostingPro',
            'date': (datetime.now()).strftime('%B %d, %Y'),
            'badge': 'Earnings',
            'badge_style': 'background:linear-gradient(90deg,#1db954 70%,#e6f9ef 100%);',
            'content': '''HostingPro isn’t just another hosting provider—it’s a platform designed to help you earn more, every single day. Our affiliate dashboard gives you all the tools you need to track your performance, manage your referrals, and optimize your strategies. With detailed analytics, you can see which campaigns are working and where you can improve.<br><br>We also offer a range of packages to suit every customer, from beginners to enterprise users. This means you can target a wide audience and maximize your commissions. Our support team is always here to help you with tips, resources, and personalized advice.<br><br>The best part? There’s no cap on your earnings. The more you refer, the more you make. With daily payouts and a transparent system, your success is truly in your hands. Take advantage of our resources and start scaling your affiliate business today!'''
        },
        {
            'title': 'Why Choose HostingPro: Beyond Just Hosting',
            'date': (datetime.now()).strftime('%B %d, %Y'),
            'badge': 'Platform',
            'badge_style': 'background:linear-gradient(90deg,#10182b 70%,#e60000 100%);',
            'content': '''At HostingPro, we go beyond providing reliable web hosting. We empower our users with an AI-powered SEO toolkit, daily backups, and 24/7 expert support. Our platform is designed for growth, whether you’re building your first website or managing a portfolio of high-traffic sites.<br><br>Affiliates benefit from a robust referral system, instant payouts, and exclusive access to webinars and masterminds. We believe in community and continuous learning, so you’ll always have opportunities to improve your skills and increase your earnings.<br><br>Our commitment to transparency, security, and innovation sets us apart. Join HostingPro and discover a platform where your success is our priority, and your potential is unlimited.'''
        },
        {
            'title': 'Top Strategies for Affiliate Success',
            'date': (datetime.now()).strftime('%B %d, %Y'),
            'badge': 'Strategy',
            'badge_style': 'background:linear-gradient(90deg,#ffd700 70%,#1db954 100%);color:#10182b;',
            'content': '''Success in affiliate marketing comes down to consistency, authenticity, and smart strategy. At HostingPro, we recommend starting with your personal network—friends, colleagues, and online communities. Share your story and explain how HostingPro’s daily payouts and fair referral system have helped you.<br><br>Use social media to reach a wider audience, and don’t be afraid to create content—blog posts, videos, or tutorials—that showcases the benefits of our platform. Remember, helping your referrals succeed is the fastest way to grow your own earnings.<br><br>Stay active in our community, attend webinars, and keep learning. The more you know, the more value you can offer to your network. With dedication and the right approach, you can build a thriving affiliate business with HostingPro.'''
        },
        {
            'title': 'The Future of Earning: Daily Income with HostingPro',
            'date': (datetime.now()).strftime('%B %d, %Y'),
            'badge': 'Future',
            'badge_style': 'background:linear-gradient(90deg,#e60000 70%,#1db954 100%);',
            'content': '''The world of online income is changing, and HostingPro is leading the way with daily payouts and a transparent, fair affiliate system. No more waiting weeks or months for your commissions—our platform puts your earnings in your hands every day.<br><br>As we continue to innovate, we’re committed to providing even more tools and resources for our affiliates. From advanced analytics to new earning opportunities, HostingPro is your partner in building a sustainable, scalable online business.<br><br>Join us as we shape the future of affiliate marketing. With HostingPro, daily income isn’t just a dream—it’s your new reality.'''
        },
    ]
    return render_template('blog.html', blog_posts=blog_posts)

# Route for /how-it-works
@bp.route('/how-it-works')
def how_it_works():
    return render_template('how_it_works.html')
from flask import Blueprint, session, redirect, url_for, render_template, request, jsonify, current_app
import secrets
import hashlib
import requests
import os
import base64
import hmac
from datetime import datetime
from .extensions import db
from .models import User, Referral, Package, UserPackage, Payment
from paypal import create_paypal_order

bp = Blueprint('main', __name__)

# Route for /blog to render the blog page
@bp.route('/blog')
def blog():
    return render_template('blog.html')

# Route for /how-it-works
@bp.route('/how-it-works')
def how_it_works():
    return render_template('how_it_works.html')
# Route for /affiliate-program to render the affiliate program page
@bp.route('/affiliate-program')
def affiliate_program():
    return render_template('affiliate_program.html')

# Affiliate-only hosting packages page with live payment links
@bp.route('/aff/<affiliate_id>/hosting')
def affiliate_hosting(affiliate_id):
    paypal_client_id = os.getenv('PAYPAL_CLIENT_ID')
    # Pass affiliate_id and PayPal client ID to the template for live payment links
    return render_template('home.html', affiliate_id=affiliate_id, paypal_client_id=paypal_client_id)

# Route for /payment to render the payment page
@bp.route('/payment')
def payment():
    return render_template('payment.html')

# Route for /privacy-policy
@bp.route('/privacy-policy')
def privacy_policy():
    return render_template('privacy_policy.html')


# Route for /terms
@bp.route('/terms')
def terms():
    return render_template('terms.html')

# Route for /packages to render the main packages page
@bp.route('/packages')
def packages():
    return render_template('hosting_packages.html')
