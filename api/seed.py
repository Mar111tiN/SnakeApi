from models.pipeline import PipelineModel
from models.samples import SampleModel

def seed_db():
    samples = [
        {'name': "sample1", "path": "/Users/mahtin/Dropbox/Icke/Sites/Python/Snakeflask/data/fastq/A.fastq", "encryption": None},
        {'name': "sample2", "path": "/Users/mahtin/Dropbox/Icke/Sites/Python/Snakeflask/data/fastq/B.fastq", "encryption": None},
        {'name': "sample3", "path": "/Users/mahtin/Dropbox/Icke/Sites/Python/Snakeflask/data/fastq/C.fastq", "encryption": None},
        {'name': "sample4", "path": "/Users/mahtin/Dropbox/Icke/Sites/Python/Snakeflask/data/fastq/D.fastq", "encryption": None},
        {'name': "sample5", "path": "/Users/mahtin/Dropbox/Icke/Sites/Python/Snakeflask/data/fastq/E.fastq", "encryption": None},
        {'name': "sample6", "path": "/Users/mahtin/Dropbox/Icke/Sites/Python/Snakeflask/data/fastq/F.fastq", "encryption": None},
    ]

    # paths are relative to the static/snakes folder
    pipelines = [
        {"name": "snake-tuto", "path": "snake-tuto/Snakefile", "config": "snake-tuto/config.yaml"},
        {"name": "hWES", "path": "hWES/Snakefile", "config": "hWES/config.yaml"}, # template config as a source for the pipeline query
        {"name": "DropSeq2", "path": "dropseq/Snakefile", "config": "dropseq/config.yaml"}
    ]

    # if db exists, do not add anything
    if SampleModel.find_all():
        return
    for sample in samples:
        new_sample = SampleModel(**sample)
        new_sample.save_to_db()

    for pp in pipelines:
        new_pipeline = PipelineModel(**pp)
        new_pipeline.save_to_db()