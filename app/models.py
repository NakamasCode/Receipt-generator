from . import db
from datetime import datetime

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    receipt_id = db.Column(db.String(20), unique=True)  # ✅ custom receipt
    type = db.Column(db.String(10), nullable=False)
    item_name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, default=1)
    amount = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(200))
    customer_name = db.Column(db.String(100))
    phone_number = db.Column(db.String(20))
    date_created = db.Column(db.DateTime, default=db.func.now())

class BusinessInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    contact = db.Column(db.String(100))
    email = db.Column(db.String(100))
    logo_url = db.Column(db.String(300))  # online image URL (Cloudinary)