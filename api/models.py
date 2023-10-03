from api import database, mongo_db
from datetime import datetime

class ParkingRecord(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    plate = database.Column(database.String(10), nullable=False)
    time = database.Column(database.String(50), nullable=False)
    paid = database.Column(database.Boolean, default=False)
    date = database.Column(database.DateTime,nullable=False, default=datetime.utcnow())
    
class ParkingRecord(mongo_db.Model):
    id = mongo_db.Column(mongo_db.Integer, primary_key=True)
    plate = mongo_db.Column(mongo_db.String(10), nullable=False)
    time = mongo_db.Column(mongo_db.String(50), nullable=False)
    paid = mongo_db.Column(mongo_db.Boolean, default=False)
    date = mongo_db.Column(mongo_db.DateTime,nullable=False, default=datetime.utcnow())