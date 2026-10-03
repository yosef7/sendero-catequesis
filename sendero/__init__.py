import os
import secrets
from pathlib import Path
from datetime import timedelta
from flask import Flask, request, session, jsonify, render_template, redirect, url_for
from .db import initialize, close_db
from .services import ValidationError
from werkzeug.exceptions import SecurityError


def private_value(path):
    if not path.exists():
        fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        with os.fdopen(fd, 'w') as f:
            f.write(secrets.token_urlsafe(24))
    return path.read_text().strip()


def create_app(config=None):
    app = Flask(__name__, instance_relative_config=True)
    Path(app.instance_path).mkdir(mode=0o700, parents=True, exist_ok=True)
    app.config.update(DATABASE=str(Path(app.instance_path) / 'sendero.sqlite'),
                      SECRET_KEY=private_value(Path(app.instance_path) / 'secret'),
                      ACCESS_CODE=private_value(Path(app.instance_path) / 'access-code'),
                      OLLAMA_MODEL=os.environ.get('OLLAMA_MODEL', 'qwen2.5-coder:3b'),
                      SESSION_COOKIE_HTTPONLY=True, SESSION_COOKIE_SAMESITE='Strict',
                      PERMANENT_SESSION_LIFETIME=timedelta(hours=8), MAX_CONTENT_LENGTH=32_768,
                      TRUSTED_HOSTS=['127.0.0.1', 'localhost'])
    if config:
        app.config.update(config)
    app.teardown_appcontext(close_db)
    with app.app_context():
        initialize()

    @app.before_request
    def protect():
        if isinstance(request.routing_exception, SecurityError):
            raise request.routing_exception
        if request.method in ('POST', 'PUT', 'PATCH', 'DELETE'):
            token = request.headers.get('X-CSRF-Token') or request.form.get('csrf', '')
            if not session.get('csrf') or not secrets.compare_digest(token, session['csrf']):
                return jsonify(error='La sesión venció. Recarga la página.'), 403
        if request.path.startswith('/api/') and not session.get('authenticated'):
            return jsonify(error='Inicia sesión para consultar las fichas.'), 401

    @app.after_request
    def headers(response):
        response.headers['Cache-Control'] = 'no-store'
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['Referrer-Policy'] = 'no-referrer'
        response.headers['Content-Security-Policy'] = "default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self' data:; connect-src 'self'; frame-ancestors 'none'; base-uri 'self'; form-action 'self'"
        return response

    @app.errorhandler(ValidationError)
    def validation(error):
        return jsonify(error=str(error)), 422

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        session.setdefault('csrf', secrets.token_urlsafe(24))
        error = None
        if request.method == 'POST':
            if secrets.compare_digest(request.form.get('code', ''), app.config['ACCESS_CODE']):
                session.clear()
                session.update(authenticated=True, csrf=secrets.token_urlsafe(24))
                session.permanent = True
                return redirect(url_for('index'))
            error = 'El código no coincide. Inténtalo de nuevo.'
        return render_template('login.html', error=error), 401 if error else 200

    @app.get('/')
    def index():
        if not session.get('authenticated'):
            return redirect(url_for('login'))
        return render_template('index.html', csrf=session['csrf'])

    from .routes import api
    app.register_blueprint(api)
    return app
