import requests
import numpy
import pprint
import json
from flask import Flask, request
import data_filters

app = Flask(__name__)
@app.route('/demographics/<name>')
def get_data(name):

    ids = [int(request.args.get('kpi_id'))]

    if name != "data":
        return "The endpoint requested does not exist. Currently 'data' is the only endpoint implemented",404

    url = 'https://python-exerc.herokuapp.com/data'
    response = requests.get(url=url, timeout=0.1)
    
    if response.status_code != 200:
        return {}, 500
    
    tree = response.json()
    pruned_tree = data_filters.get_subtree_by_id(ids,tree)
    return json.dumps(pruned_tree), 200

app.run
