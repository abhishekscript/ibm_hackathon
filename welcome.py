# Copyright 2015 IBM Corp. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
from flask import Flask, jsonify,Response,request
from pymongo import MongoClient
import json
from bson import json_util
from services import ElasticModule
from werkzeug.utils import secure_filename
import requests
import subprocess
# insert your connection details here
#MONGO_URL = 'mongodb://<dbuser>:<pass>@<database URL>'

# connect to the MongoDB server



client = MongoClient("mongodb://admin:BQBAACMCNRPKYIBG@sl-us-dal-9-portal.1.dblayer.com:17559,sl-us-dal-9-portal.2.dblayer.com:17559/admin?ssl=true", ssl_ca_certs="ca-cert.pem")

db = client.get_default_database()

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = os.getcwd()+"/static"

def watsonClassifier( imgName ):
    url = "https://gateway-a.watsonplatform.net/visual-recognition/api/v3/classify/foods"

    querystring = {"api_key":"2452d8f19929b019ad5bb74bec898d38cadb6db8","url":"https://flask-test-ml.mybluemix.net/static/ActiOn_2.jpg","version":"2016-05-19"}

    headers = {
        'cache-control': "no-cache",
        'postman-token': "a7322ca2-9441-c3e3-dcfb-2e75431793fc"
        }

    response = requests.request("POST", url, headers=headers, params=querystring)

    return response.text

@app.route('/')
def Welcome():
    return app.send_static_file('index.html')

@app.route('/myapp')
def WelcomeToMyapp():
    return 'Welcome again to my app running on Bluemix!'


@app.route("/uploadimage", methods=[ 'POST' ] )
def uploadImag():
    #return str(request.files)
    file = request.files['avatar']
    filename = secure_filename(file.filename)
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename ))
    return jsonify({ "message" : "done" })

@app.route("/inseart", methods=[ 'POST' ] )
def inseart():
    #return str(request.files)
    data=request.json
    #docid=data.get("id",None)
    res=ElasticModule.add("receipe_db","receipe_table", None, data)
    print res
    return jsonify({"hi":res})

@app.route("/search",methods=['POST'])
def searchData():
    try:
        items = request.json['items']
        searchStr = ' '.join(items)
        query = { "query" : { "match" : {  "ingredients" : searchStr  } } }

        data = ElasticModule.search("receipe_db","receipe_table", query)['hits']['hits']
        return jsonify({"data" : data })

    except Exception as e:
        return jsonify({"message" : str(e) })




port = os.getenv('PORT', '5000')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(port),debug=True)


