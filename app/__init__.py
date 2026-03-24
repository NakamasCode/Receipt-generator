from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import cloudinary

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")
    
    db.init_app(app)
    
    with app.app_context():
        from . import routes
        db.create_all()
        
    return app


cloudinary.config(
    cloud_name = "dv4tulgpd",
    api_key = "636788582287618",
    api_secret = "PBTwBRSJMo6g4RqoCF_jQFCDIqM"
)