from flask_bcrypt import Bcrypt
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_cors import CORS
import os

bcrypt = Bcrypt()
limiter = Limiter(key_func=get_remote_address)

def configurar_seguranca(app):

    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config['SESSION_COOKIE_SECURE'] = True
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
    
    app.config['WTF_CSRF_ENABLED'] = True
    app.config['WTF_CSRF_TIME_LIMIT'] = 3600
    
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB
    
    bcrypt.init_app(app)
    limiter.init_app(app)
    
    CORS(app, 
         origins=('http://localhost:3000', 'http://localhost:5000'), 
         supports_credentials=True)

    @app.after_request
    def adicionar_headers_seguranca(response):
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'DENY'
        response.headers['X-XSS-Protection'] = '1; mode=block'
        
        if app.config.get('SESSION_COOKIE_SECURE'):
            response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
        
        return response

def obter_limiter():
    return limiter

def obter_bcrypt():
    return bcrypt