from flask import Flask, jsonify, request, abort, make_response, send_file
import requests
import json
import logging
app = Flask(__name__)

@app.route('/')
def index():
	return "Tervetuloa Apiin!", 200

@app.route('/shipping', methods=['POST'])
def getShipping():
	username = "KAMPMVQHRFI27NUW"
	password = "KZT7RJ2CRR6NSOEZ2X676C3C"
	data = request.data
	content = request.get_json(silent="true")
	pdfConfig = {
		"target4XOffset": 0,
		"target2YOffset": 0,
		"target1Media": "laser-ste",
		"target1YOffset": 0,
		"target3YOffset": 0,
		"target2Media": "laser-a4",
		"target4YOffset": 0,
		"target4Media": "null",
		"target3XOffset": 0,
		"target3Media": "null",
		"target1XOffset": 0,
		"target2XOffset": 0,
	}
	if not request.json:
		abort(make_response("Call has to be in JSON format",400))

	#if not content["shipment"][""]

	dataa = request.data
	#print(content)
	number = content["shipment"]["receiver"]["phone"]
	email = content["shipment"]["receiver"]["email"]
	address = content["shipment"]["receiver"]["address1"]


	headers = {'Content-type': 'application/json'}
	r = requests.post("https://api.unifaun.com/rs-extapi/v1/shipments", auth=(username, password), data=data, headers=headers)
	trackids = []
	d = r.json()
	print(d)
	#if d[0]["type"]=="error":
		#return jsonify(d)

	for trackid in d[0]["parcels"]:
		trackids.append({"trackid": trackid["parcelNo"]})
	pdfs = []
	for pdf in d[0]["pdfs"]:
		pdfs.append({"href": pdf["href"]})
	print(pdfs)
	print(trackids)
	if r.status_code == 201:
		message = "Tilaus luotu"
	else:
		message = "error"

	postvalue = {"status": r.status_code, "message": message, "data":{"ordernumber": d[0]["orderNo"],"name":d[0]["sndName"],"email":email,"phone": number, "address": address, "city": d[0]["sndCity"], "zipcode": d[0]["sndZipcode"], "country": d[0]["sndCountry"]}}

	postaddress = pdfs[0]["href"]
	headers = {'Content-type': 'application/pdf'}

	r = requests.get(postaddress, auth=(username, password), headers=headers)
	#returnvalue = make_response(r.content);
	response = make_response(r.content)
	response.headers["Content-Disposition"] =  "attachment; filename='test.pdf'"
	response.mimetype = "application/pdf"
	print(response)
	try:
		return jsonify(postvalue)

	except Exception as e:
		return str(e)

	print(postaddress)

	if r.status_code == 201:
		status = "success"
	else:
		status="error"

	return response
if __name__ =='__main__':
	app.run()
