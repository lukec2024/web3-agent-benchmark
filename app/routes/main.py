from flask import Flask
from app.routes.round import round_bp
from app.routes.rpc import rpc_bp

def register_all_routes(app: Flask):
    app.register_blueprint(round_bp, url_prefix=f'/{round_bp.name}')
    app.register_blueprint(rpc_bp, url_prefix=f'/{rpc_bp.name}')