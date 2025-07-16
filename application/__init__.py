from flask import Flask  
import os

from .modules.parser import Parser
from .modules.notion import NotionCalendar




def create_app():

    # Create Flask app
    app = Flask(__name__)

    # Load configuration
    with app.app_context():
        app.secret_key = os.environ.get('SECRET_KEY')
        app.demo_secret_key = os.environ.get('DEMO_SECRET_KEY')
        app.calendar = NotionCalendar()
        app.parser = Parser()

    from .endpoints import endpoints as endpoints_blueprint
    app.register_blueprint(endpoints_blueprint)

    return app