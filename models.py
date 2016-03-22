from database import db
from geoalchemy2.types import Geography

class BoothInfo(db.Model):

    __tablename__ = ''
    identifier = db.Column(db.String(255), primary_key=True)
    owner_id = db.Column(db.String(255))
    name = db.Column(db.String(255))
    location_txt = db.Column(db.Text())
    location_geo = db.Column(Geography(geometry_type='POINT'))
    phone_number = db.Column(db.String(255))
    email = db.Column(db.String(255))
    open_time = db.Column(db.String(255))
    category = db.Column(db.String(255))
    description = db.Column(db.Text())
    create_time = db.Column(db.DateTime)
    disabled = db.Column(db.Boolean())


class BoothOwner(db.Model):

    __tablename__ = ''
    identifier = db.Column(db.String(255), primary_key=True)
    name = db.Column(db.String(255))
    phone_number = db.Column(db.String(255))
    description = db.Column(db.Text())
    create_time = db.Column(db.DateTime)
    create_by = db.Column(db.String(255))
    disabled = db.Column(db.Boolean())

