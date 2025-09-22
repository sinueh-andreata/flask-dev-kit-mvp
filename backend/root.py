from flask import jsonify, request, session, render_template, redirect, url_for
from config import app, db, bcrypt
from models import Root
from backend.auth.usuarios_login import root_required

