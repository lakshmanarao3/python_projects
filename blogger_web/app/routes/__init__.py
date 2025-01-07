from .auth_routes import auth
from .post_routes import post
from .admin_routes import admin

def register_blueprints(app):
    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(post)
    app.register_blueprint(admin, url_prefix='/admin')

