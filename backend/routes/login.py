from re import A
from backend.routes import login_bp
from backend.models import Accounts
from backend.app import db
from flask import request, jsonify
from sqlalchemy.sql import text

@login_bp.route('/create', methods=['POST'])
def create():
    """Create a new user with a hashed password"""
    data = request.json
    username = data.get('username')
    address = data.get('address')
    password = data.get('password')

    if not username or not address or not password:
        return jsonify({'error': 'Missing required fields'}), 400
    
    try:
        #check if the account already exists
        existing_account = Accounts.query.filter_by(username=username).first()
        if existing_account:
            return jsonify({'error': 'Account already exists'}), 400

        #generate a salt and hash the password using pgcrypto
        salt_query = text("SELECT gen_salt('bf') AS salt")
        salt_result = db.session.execute(salt_query).fetchone()
        salt = salt_result[0]

        hash_query = text("SELECT crypt(:password, :salt) AS passhash")
        hash_result = db.session.execute(hash_query, {'password': password, 'salt': salt}).fetchone()
        passhash = hash_result[0]

        #create a new account
        new_account = Accounts(
            username=username,
            address=address,
            passhash=passhash,
            role='I'  #default role of issuer
        )

        db.session.add(new_account)
        db.session.commit()

        return jsonify({'message': 'Account created successfully'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
    
@login_bp.route('/check', methods=['POST'])
def check():
    """Check if the user exists"""
    data = request.json
    address = data.get('address')
    password = data.get('password')


    if not address or not password:
        return jsonify({'error': 'Missing required fields'}), 400
    
    try:
        account = Accounts.query.filter_by(address=address).first()
        if not account:
            return jsonify({'error': 'Account not found'}), 404
        
        #verify the password using pgcrypto
        verify_query = text("SELECT crypt(:password, :stored_hash) = :stored_hash AS is_valid")

        verify_result = db.session.execute(verify_query, {'password': password, 'stored_hash': account.passhash}).fetchone()

        is_valid = verify_result[0]

        if is_valid:
            return jsonify({'message': 'User was found'}), 200
        else:
            return jsonify({'error': 'User was not found'}), 401
    except Exception as e:
        return jsonify({'error': str(e)}), 500