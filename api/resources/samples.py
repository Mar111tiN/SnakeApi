from os import path
from flask_restful import Resource, fields, reqparse, marshal_with
from flask_jwt_extended import (
    jwt_required,
    get_jwt_claims,
    jwt_optional,
    get_jwt_identity,
    fresh_jwt_required
    )
from models.samples import SampleModel

enc_dict = {
    'fastq': None,
    'gzip': 'gzip',
    'gz': 'gzip',
    'bz2': 'bzip2',
    'bzip2': 'bzip2'
}


class Sample(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str, required=False)
    parser.add_argument('path', type=str, required=True)
    parser.add_argument('encryption', type=str, required=False)

    @staticmethod
    def format_sample(data):
        root_name, suff = path.splitext(data['path'])
        if not data['name']:
            data['name'] = root_name.replace('.fastq', '') # other options?
        if not data['encryption']:
            data['encryption'] = enc_dict[suff] # get encryption from suffix
        return data

    def get(self, name):
        sample = SampleModel.find_by_name(name)
        if sample:
            return sample.json(), 201
        return {'message': 'sample {} not found in Database'.format(name)}, 404

    def post(self, name):
        if SampleModel.find_by_name(name):
            return {'message': "Sample {} already exists in Database".format(name)}, 400
        data = format_sample(Sample.parser.parse_args())
        # get suffix and store root without suffix
        sample = SampleModel(name, **data)
        try:
            sample.save_to_db()
        except:
            return {'message': "An error occurred while trying to store sample"}, 500
        return sample.json(), 201

    def put(self, name):
        data = format_sample(Sample.parser.parse_args())
        sample = SampleModel.find_by_name(name)
        if sample:
            sample.path = data['path']
            sample.encryption = data['encryption']
        else:
            sample = SampleModel(name, **data)
        sample.save_to_db()
        return sample.json(), 201

    # add security for deletion
    def delete(self, name):
        sample = SampleModel.find_by_name(name)
        if sample:
            sample.delete_from_db()
        return {'message', "{} deleted from database".format(name)}


class SampleList(Resource):
    def get(self):
        samples = [sample.json() for sample in SampleModel.find_all()]
        return {'samples': samples}, 200
