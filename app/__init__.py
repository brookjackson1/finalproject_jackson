from flask import Flask, g
from .app_factory import create_app
from .db_connect import close_db, get_db

app = create_app()
app.secret_key = 'your-secret'  # Replace with an environment

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
    g.db = get_db()
    if g.db is None:
        print("Warning: Database connection unavailable. Some features may not work.")

# Setup database connection teardown
@app.teardown_appcontext
def teardown_db(exception=None):
    close_db(exception)