from app.config import app, DEBUG_MODE
from app.routes.main import register_all_routes
import logging

def config_debug_mode():
    if DEBUG_MODE:
        logging.basicConfig()
        logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)

if __name__ == '__main__':
    config_debug_mode()
    register_all_routes(app)
    app.run(port=7007, debug=False)