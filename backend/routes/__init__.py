from flask import Blueprint

# Create blueprints for each entity
admin_bp = Blueprint('admin', __name__, url_prefix='/api/admin')
issuer_bp = Blueprint('issuer', __name__, url_prefix='/api/issuer')
verifier_bp = Blueprint('verifier', __name__, url_prefix='/api/verifier')
holder_bp = Blueprint('holder', __name__, url_prefix='/api/holder')
login_bp = Blueprint('login', __name__, url_prefix='/api/login')
common_bp = Blueprint('common', __name__, url_prefix='/api')

# Import routes (use relative imports since we're in the routes package)
from .admin import *
from .issuer import *
from .verifier import *
from .holder import *
from .login import *
from .common import *

# List of all blueprints to register
blueprints = [admin_bp, issuer_bp, verifier_bp, holder_bp, login_bp, common_bp]
