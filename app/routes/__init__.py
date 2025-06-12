# routes/__init__.py

from .users import user_bp
from .images import image_bp
from .questions import question_bp
from .choices import choice_bp
from .answers import answer_bp
from .stats_routes import stats_bp

def register_routes(app):
    app.register_blueprint(user_bp)
    app.register_blueprint(image_bp)
    app.register_blueprint(question_bp)
    app.register_blueprint(choice_bp)
    app.register_blueprint(answer_bp)
    app.register_blueprint(stats_bp)
