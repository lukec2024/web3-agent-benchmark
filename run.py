from app.config import app, DEBUG_MODE
from app.routes.main import register_all_routes
import logging

def config_debug_mode():
    if DEBUG_MODE:
        logging.basicConfig()
        logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)

def create_app():
    config_debug_mode()
    register_all_routes(app)
    return app

server = create_app()

if __name__ == '__main__':
    server.run(port=7007, debug=False)