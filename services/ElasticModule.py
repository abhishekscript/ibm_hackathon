from datetime import datetime
from elasticsearch import Elasticsearch
import requests
import json, os
baseurl = os.environ.get('es_url','https://admin:TFJPIAPRVDAYKSMA@sl-us-dal-9-portal2.dblayer.com:17586/')

es = Elasticsearch(['https://admin:TFJPIAPRVDAYKSMA@sl-us-dal-9-portal2.dblayer.com:17586/'])


def add(index_data, type_data, doc_id, doc_body):
	try:
		if doc_id is not None:
			return es.index(index=index_data, doc_type=type_data, id=doc_id, body=doc_body )
			
		return es.index(index=index_data, doc_type=type_data, body=doc_body )
	except Exception as e:
		return e
def getById(index_data, type_data, doc_id ):
	try:
		return es.get(index=index_data, doc_type=type_data, id=doc_id)
	except Exception as e:
		return e
def search(index_data , type_data, body_query):
	try:
		return es.search(index=index_data, doc_type=type_data, body=body_query )
	except Exception as e:
		return e
def update(index_data, type_data, doc_id, doc_body):
	try:
		#index_data, type_data, doc_id, doc_body
		return es.update(index=index_data,doc_type=type_data,id=doc_id, body=doc_body)
	except Exception as e:
		return e

def addDBbyRest(dbname):
	try:
		url = baseurl+"/"+dbname
		headers = {'content-type': "application/json"}
		response = requests.request("PUT", url, headers=headers)
		return { "message" : response.text , "status" : 200 } 
	except Exception as e:
		return { "message" : str(e) , "status" : 400 }


def updateSuggestByRest(dbname, typename, doc_id, doc_body):
	try:
		url = baseurl+"/"+dbname+"/data"+"/"+doc_id
		# print url
		headers = {
    		'content-type': "application/json"
    	}

		response = requests.request("POST", url, data=doc_body, headers=headers)
		#print(response.text)
		return { "message" : response.text , "status" : 200 }
	except Exception as e:
		return { "message" : str(e), "status" : 400 }

