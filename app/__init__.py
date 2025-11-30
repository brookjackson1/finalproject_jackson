from flask import Flask, g, render_template
from .app_factory import create_app
from .db_connect import close_db, get_db
import logging
import sys

app = create_app()
app.secret_key = 'your-secret'  # Replace with an environment

# Configure logging for Heroku
logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logger = logging.getLogger(__name__)

# Register Blueprints
from app.blueprints.examples import examples
from app.blueprints.clients import clients
from app.blueprints.bookings import bookings
from app.blueprints.inventory import inventory
from app.blueprints.dashboard import dashboard
from app.blueprints.portfolio import portfolio
from app.blueprints.chatbot import chatbot

app.register_blueprint(examples, url_prefix='/example')
app.register_blueprint(clients, url_prefix='/clients')
app.register_blueprint(bookings, url_prefix='/bookings')
app.register_blueprint(inventory, url_prefix='/inventory')
app.register_blueprint(dashboard, url_prefix='/dashboard')
app.register_blueprint(portfolio, url_prefix='/portfolio')
app.register_blueprint(chatbot, url_prefix='/chatbot')

from . import routes

@app.before_request
def before_request():
    from flask import abort
    g.db = get_db()
    if g.db is None:
        logger.error("Database connection failed in before_request")
        logger.error("Check if JAWSDB_URL environment variable is set correctly")
        abort(500, description="Database connection failed. Please check server configuration.")

# Setup database connection teardown
@app.teardown_appcontext
def teardown_db(exception=None):
    close_db(exception)

# Error handlers
@app.errorhandler(500)
def internal_error(error):
    logger.error(f"Internal Server Error: {error}")
    return render_template('error.html',
                         error_code=500,
                         error_message="Internal Server Error",
                         error_detail="Something went wrong. Please try again later."), 500

@app.errorhandler(404)
def not_found_error(error):
    return render_template('error.html',
                         error_code=404,
                         error_message="Page Not Found",
                         error_detail="The page you're looking for doesn't exist."), 404

@app.errorhandler(Exception)
def handle_exception(error):
    logger.error(f"Unhandled exception: {error}", exc_info=True)
    return render_template('error.html',
                         error_code=500,
                         error_message="Unexpected Error",
                         error_detail=str(error)), 500