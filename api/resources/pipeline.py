from flask_restful import Resource, fields, reqparse, marshal_with
from flask import request
import io, os
from contextlib import redirect_stdout
from subprocess import Popen, STDOUT, PIPE, CalledProcessError
import json
# from flask_jwt_extended import (
#     jwt_required,
#     get_jwt_claims,
#     jwt_optional,
#     get_jwt_identity,
#     fresh_jwt_required
#     )
from models.pipeline import PipelineModel
import yaml
import snakemake
from snakemake.utils import update_config

path_to_static = "/Users/mahtin/Dropbox/Icke/Sites/Python/Snakeflask/api/static/snakes"


class RunPipeline(Resource):
    def get(self, name):
        # return the dag from exemplary pipeline
        pipeline = PipelineModel.find_by_name(name)
        if pipeline:
            return pipeline.json(), 201
        return {'message': "Pipeline {} not found in Database".format(name)}

    def post(self, name):
        # get data from post 
        data = request.get_json()
        pipeline = PipelineModel.find_by_name(name)
        if not pipeline:
            return {'message': f"Pipeline {name} not found in Database"}
        # load config json into config dict
        path_to_snakefile = os.path.join(path_to_static, name, 'Snakefile')
        # load user configs if given
        config = pipeline.json()['config']
        if data:
            user_config = data['config']
            # use the function load_config from snakemake itself!!
            update_config(config, user_config)
        workdir = config['workdir']
        os.makedirs(workdir, exist_ok=True)
        path_to_config_file = os.path.join(workdir, 'config.yaml')
        path_to_dag = os.path.join(workdir, 'dag.json')
        with open(path_to_config_file, 'w+') as stream:
            yaml.dump(config, stream, default_flow_style=False)
        try:
            dagcmd = f"snakemake --snakefile {path_to_snakefile} --configfile {path_to_config_file} --d3dag > {path_to_dag}"
            # ! place dag in d3dag and return
            snakedag = Popen(dagcmd, shell=True, stdout=PIPE, stderr=STDOUT, close_fds=True)
        except CalledProcessError as er:
            print(f'Snakemake returned Error code {er.returncode}')
        snakedag.communicate()
        with open(path_to_dag, 'r') as file:
            d3dag = json.load(file)
        info = {'dag': d3dag, 'config':config}
        # run the snakemake jobs
        # try:
        #     subprocess.check_call(['snakemake', '--snakefile', path_to_snakefile, '--configfile', path_to_config_file])
        # except subprocess.CalledProcessError as er:
        #     print(f'Snakemake returned Error code {er.returncode}')
        return info
