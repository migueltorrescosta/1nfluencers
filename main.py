import requests
import numpy
import pprint
import json
from flask import Flask, request
import data_filters

app = Flask(__name__)
@app.route('/demographics/<name>')
def get_data(name):

    # ids = request.args.get('kpi_ids')

    if name != "data":
        return {},404

    url = 'https://python-exerc.herokuapp.com/data'
    response = requests.get(url=url, timeout=0.1)
    
    if response.status_code != 200:
        return {}, 500
    
    tree = response.json()
    ids = [299]
    pruned_tree = data_filters.get_subtree_by_id(ids,tree)
    return json.dumps(pruned_tree), 200

app.run
