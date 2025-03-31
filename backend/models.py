from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Issuers(db.Model):
    id = db.Column(db.String(255), primary_key=True)
    name = db.Column(db.String(255))
    signature = db.Column(db.String(300))

    def __repr__(self):
        return f"Issuer with ID {self.id} and Name {self.name}"

class Accounts(db.Model):
    address = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(255), nullable=False, unique=True)
    passhash = db.Column(db.String(255))
    role = db.Column(db.String(1))

    def __repr__(self):
        return f"Account with ID {self.id} and Email {self.email}"