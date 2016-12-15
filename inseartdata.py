import json,requests
def inseart_data():
	payload=[]
	url="https://flask-test-ml.mybluemix.net/inseart"
	headers = {'content-type': "application/json"}
	with open("receipe.json","r") as fp:
		payload=json.load(fp)
	print "hi"
	for i in payload:		
		response = requests.request("POST", url, data=json.dumps(i), headers=headers)
		print response.text
		
	return "hi"

inseart_data()

