from pathlib import Path
import os
import json

from pollination_io.api.client import ApiClient
from pollination_io.interactors import Recipe, NewJob


api_key = os.environ['QB_POLLINATION_TOKEN']
recipe_tag = os.environ['RECIPE_TAG']
host = os.environ['HOST']

owner = 'ladybug-tools'
project = 'annual-daylight'

api_client = ApiClient(host, api_key)
recipe = Recipe(owner, project, recipe_tag, client=api_client)
recipe.add_to_project(f'{owner}/{project}')
job = NewJob(owner, project, recipe, client=api_client)

inputs_path = Path(__file__).parent.resolve().joinpath('inputs.json')
with open(inputs_path) as inputs_json:
    recipe_inputs = json.load(inputs_json)

inputs = {}
for recipe_input, value in recipe_inputs.items():
    input_path = Path(__file__).parent.resolve().joinpath(value)
    if input_path.exists():
        artifact_path = job.upload_artifact(input_path, 'sample')
        inputs[recipe_input] = artifact_path
    else:
        inputs[recipe_input] = value

arguments = []
arguments.append(inputs)
job.arguments = arguments

job.create()
