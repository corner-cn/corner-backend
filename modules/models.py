from database import db, CRUDMixin
from geoalchemy2.types import Geography


class BoothInfo(db.Model, CRUDMixin):

    __tablename__ = 'corner_booth_info'
    id = db.Column(db.Integer, primary_key=True)
    # booth_id = db.Column(db.String(255))
    # Basic Info
    booth_name = db.Column(db.String(255))
    loc_text = db.Column(db.Text())
    loc_lo = db.Column(db.String(255))
    loc_la = db.Column(db.String(255))
    phone_number = db.Column(db.String(255))
    email = db.Column(db.String(255))
    open_time = db.Column(db.String(255))
    category = db.Column(db.String(255))
    # About the owner
    booth_owner = db.Column(db.String(255))
    booth_story = db.Column(db.Text())
    # Miscs
    like_count = db.Column(db.Integer)
    create_time = db.Column(db.DateTime)
    create_by = db.Column(db.String(255))
    disabled = db.Column(db.Boolean())


class BoothImages(db.Model, CRUDMixin):

    __tablename__ = 'corner_booth_images'
    id = db.Column(db.Integer, primary_key=True)
    booth_id = db.Column(db.String(255))
    image_path = db.Column(db.String(255))
    flag = db.Column(db.String(255))
    create_time = db.Column(db.DateTime)
    disabled = db.Column(db.Boolean())


class BoothAccusation(db.Model, CRUDMixin):

    __tablename__ = 'corner_booth_accusation'
    id = db.Column(db.Integer, primary_key=True)
    booth_id = db.Column(db.String(255))
    accusation = db.Column(db.Text())
    reporter = db.Column(db.String(255))
    report_time = db.Column(db.DateTime)
    status = db.Column(db.String(255))

