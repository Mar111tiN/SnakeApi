from db import db


class SampleModel(db.Model):
    __tablename__ = 'samples'

    sample_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    path = db.Column(db.String(100)) # relative path to the sample data/..
    encryption = db.Column(db.String(20))

    def __init__(self, name, path, encryption):
        self.name = name
        self.path = path
        self.encryption = encryption

    def json(self):
        return {
            'name': self.name,
            'path': self.path,
            'enc': self.encryption 
        }

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(sample_id=_id).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()

   # @classmethod
   # def find_list(cls, list_of_samples):
   #      return cls.query.filter_by 

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()