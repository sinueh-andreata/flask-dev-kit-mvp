from flask import jsonify, request, session, render_template, redirect, url_for
from core.config import app, db, bcrypt
from models.models import Root
from auth.usuarios_login import root_required

