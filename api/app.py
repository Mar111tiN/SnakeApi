from flask import Flask
import os
from flask_restful import Api
from flask_jwt_extended import JWTManager
from db import db
from seed import seed_db
from resources.pipeline import RunPipeline
from resources.samples import SampleList, Sample


app = Flask(__name__, instance_relative_config=True)
app.config.from_mapping(
    SECRET_KEY='mahtin',
    SQLALCHEMY_DATABASE_URI=os.environ.get('DATABASE_URL', 'sqlite://'), # postgreSQL in /activate.d/env_vars.sh
    SQLALCHEMY_TRACK_MODIFICATIONS=True,
    PROPAGATE_EXEPTIONS=True,
    JWT_SECRET_KEY='mahtin'
    )

api = Api(app)
db.init_app(app)

@app.before_first_request
def create_tables():
    db.create_all()
    seed_db()


jwt = JWTManager(app)  # creates the /auth endpoints if needed


api.add_resource(RunPipeline, '/run/<string:name>') # get pipeline specs and post snakemake jobs
api.add_resource(SampleList, '/samples')  # query and post mock fastq samples
api.add_resource(Sample, '/sample/<string:name>')

if __name__ == '__main__':
    app.run(port=5050)
