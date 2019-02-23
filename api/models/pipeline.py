import yaml
import os
from db import db

path_to_static = "/Users/mahtin/Dropbox/Icke/Sites/Python/Snakeflask/api/static/snakes"


class PipelineModel(db.Model):
    __tablename__ = 'pipelines'

    pipe_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    path = db.Column(db.String(350))
    config = db.Column(db.String(350))                  # relative path to the config file

    def __init__(self, name, path, config):
        self.name = name
        self.path = path
        self.config = config

    # reads config.yaml@config_path into dict
    @staticmethod
    def yaml_to_dict(config_path):
        path = os.path.join(path_to_static, config_path)  #
        with open(path, 'r') as stream:
            try:
                config_object = yaml.load(stream)
            except yaml.YAMLError as exc:
                print(exc)
        return config_object

    # returns json representation of pipeline entry
    # ?? should I include paths as well or keep output dry?
    def json(self):
        return {
            'pipeline': self.name,
            'config': PipelineModel.yaml_to_dict(self.config)
        }

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(pipe_id=_id).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
