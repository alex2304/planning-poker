import os

from flask import Flask

from api import routes as api_routes
from config import DefaultConfig
from services import room_service
from storage.in_memory import InMemoryStorage
from views import routes as views_routes


def create_app():
    app = Flask(__name__, template_folder=os.path.join(os.path.dirname(__file__), 'templates'))

    app.config.from_object(DefaultConfig)

    room_service.init_storage(InMemoryStorage(rooms_limit=app.config['IN_MEMORY_ROOMS_LIMIT']))

    app.register_blueprint(views_routes.bp)
    app.register_blueprint(api_routes.bp)

    return app
