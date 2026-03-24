from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
import cloudinary

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")

    cloudinary.config(
        cloud_name=os.environ.get("CLOUDINARY_CLOUD_NAME"),
        api_key=os.environ.get("CLOUDINARY_API_KEY"),
        api_secret=os.environ.get("CLOUDINARY_API_SECRET"),
        secure=True
    )
    
    db.init_app(app)
    
    with app.app_context():
        from . import routes
        db.create_all()
        
    return app


