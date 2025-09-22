from core.config import app
from flask import jsonify, render_template

@app.errorhandler(429)
def ratelimit_handler(e):
    return render_template('too_much.html'), 429
