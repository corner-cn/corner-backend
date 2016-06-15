from extensions import db
from sqlalchemy.exc import IntegrityError


class CRUDMixin(object):
    """
    Mixin that adds convenience methods for CRUD (create, read, update, delete)
    operations.
    """
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)

    @classmethod
    def find_or_create_by(cls, **kw):
        """
        Find or create by attributes
        """
        instance = cls.where(cls, **kw).first()
        if instance:
            return instance
        else:
            return cls(**kw).save()

    @classmethod
    def where(cls, **kw):
        return db.session.query(cls).filter_by(**kw)

    @classmethod
    def exist(cls, **kw):
        return cls.count(**kw) != 0

    @classmethod
    def first(cls, **kw):
        return cls.where(**kw).first()

    @classmethod
    def count(cls, **kw):
        return cls.where(**kw).count()

    @classmethod
    def all(cls, **kw):
        return cls.where(**kw).all()

    @classmethod
    def get_by_id(cls, id):
        if any(
                (isinstance(id, basestring) and id.isdigit(),
                 isinstance(id, (int, float))),
        ):
            return cls.query.get(int(id))
        return None

    @classmethod
    def create(cls, **kwargs):
        """
        Create a new record and save it the database.
        """
        instance = cls(**kwargs)
        return instance.save()

    def reload(self):
        db.session.refresh(self)
        return self

    def update(self, commit=True, **kwargs):
        """
        Update specific fields of a record.
        """
        for attr, value in kwargs.iteritems():
            setattr(self, attr, value)
        return commit and self.save() or self

    def save(self, commit=True):
        db.session.add(self)
        if commit:
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()
        return self

    def delete(self, commit=True):
        """
        Remove the record from the database.
        """
        db.session.delete(self)
        return commit and db.session.commit()
