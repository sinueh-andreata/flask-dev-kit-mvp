from core.config import app
from flask import jsonify

@app.errorhandler(429)
def ratelimit_handler(e):
    return jsonify({'success': False, 'message': 'Muitas tentativas de login. Tente novamente em instantes.'}), 429
