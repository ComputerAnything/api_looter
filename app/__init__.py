import os
from flask import Flask, jsonify, request
from flask_limiter import Limiter
from flask_wtf.csrf import CSRFProtect
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

# Auto-generate allowed API domains from data.py for SSRF protection
def get_allowed_domains():
    """Extract allowed domains from API endpoints"""
    from urllib.parse import urlparse
    from .data import APIS

    domains = set()
    for api in APIS:
        endpoint = api.get('endpoint', '')
        if endpoint:
            try:
                parsed = urlparse(endpoint)
                if parsed.netloc:
                    domains.add(parsed.netloc)
            except Exception:
                pass
    return domains

ALLOWED_API_DOMAINS = get_allowed_domains()


def get_real_ip():
    """Get real IP address, accounting for proxies and Docker"""
    if request.environ.get('HTTP_X_FORWARDED_FOR'):
        return request.environ['HTTP_X_FORWARDED_FOR'].split(',')[0].strip()
    if request.environ.get('HTTP_X_REAL_IP'):
        return request.environ['HTTP_X_REAL_IP']
    return request.environ.get('REMOTE_ADDR', '127.0.0.1')


def is_allowed_domain(url):
    """Check if URL domain is in whitelist"""
    from urllib.parse import urlparse
    parsed = urlparse(url)
    return parsed.netloc in ALLOWED_API_DOMAINS


# Initialize rate limiter
limiter = Limiter(
    key_func=get_real_ip,
    default_limits=[],
    storage_uri=os.environ.get('REDIS_URL', 'memory://')
)

# Initialize CSRF protection
csrf = CSRFProtect()


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev')  # Default to 'dev' if not set

    # Initialize extensions
    limiter.init_app(app)
    csrf.init_app(app)

    # Configure CORS (allow requests from same origin)
    CORS(app, supports_credentials=True)

    # Rate limit error handler
    @app.errorhandler(429)
    def rate_limit_handler(e):
        """Handle rate limit exceeded"""
        # Return JSON for AJAX requests
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.is_json:
            return jsonify({
                'error': 'Rate Limited',
                'message': 'Too many requests. Please wait a moment before trying again.'
            }), 429

        # Return simple HTML response for regular requests
        return '''
        <html>
            <head><title>Rate Limited</title></head>
            <body style="font-family: Arial; text-align: center; padding: 2em;">
                <h1>⏱️ Rate Limited</h1>
                <p>Too many requests. Please wait a moment before trying again.</p>
                <a href="/">← Back to Home</a>
            </body>
        </html>
        ''', 429

    # Security headers
    @app.after_request
    def set_security_headers(response):
        """Set security headers on all responses"""
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'DENY'
        response.headers['X-XSS-Protection'] = '1; mode=block'
        response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        response.headers['Permissions-Policy'] = 'camera=(), microphone=(), geolocation=()'

        # HSTS in production only
        if not app.config.get('TESTING') and not app.debug:
            response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains; preload'

        # CSP for HTML pages (not API responses)
        if not request.path.startswith('/api'):
            response.headers['Content-Security-Policy'] = (
                "default-src 'self'; "
                "script-src 'self' 'unsafe-inline'; "  # Prism.js needs inline
                "style-src 'self' 'unsafe-inline'; "
                "img-src 'self' data: https:; "
                "font-src 'self'; "
            )

        return response

    from .routes import bp as main_bp
    app.register_blueprint(main_bp)  # Register the main blueprint

    # Exempt main routes from CSRF (API testing doesn't need CSRF protection)
    # We already have SameSite=Lax cookies for CSRF protection
    csrf.exempt(main_bp)

    return app
