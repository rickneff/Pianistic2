import datamodel as model

# Resource request handler index
# After each resource handler function, that function should be added
# to this dictionary.
# For an enumeration of resources, run this program as a standalone.
index = {
#	resource_name:	handler function
}


# Handler functions
#
# Handlers take a single argument, which is the response object for the
# request.  Handlers should set_content for content type and
# set_response for response code, for each request.  The data should be
# returned in the return value.

# 
def piano(response):
	responsecode = 200
	content = "application/json"
	json = ''

	try:
		if type(response.query) is not dict or \
		   "id" not in response.query:
			responsecode = 400 # Bad Request
			json = '{"error":"Invalid identifying data"}'
		else:
			p = model.Piano(id=query["id"])
			p.delete()
			json = '{"success":"Deleted piano successfully"}'

	except model.RecordNotFoundError as e:
		responsecode = 404
		json = '{{"error":{}}}'.format(e)
	except Exception as e:
		responsecode = 500
		json = '{"error":"Internal Server Error"}'


	response.set_content(content)
	response.set_response(responsecode)
	return json
index["piano"] = piano

def service_record(response):
	responsecode = 200
	content = "application/json"
	json = ''

	try:
#		s = model.ServiceRecord(json=jform)
#		s.write()
		responsecode = 501
		json = '{"error":"Not implemented"}'

#		json = '{"success":"Wrote service record successfully"}'
	except ValueError:
		responsecode = 400
		json = '{"error":"Invalid JSON object"}'
	except model.InsufficientDataError as e:
		responsecode = 400
		json = '{{"error":"{}"}}'.format(e)
	except Exception as e:
		print e
		responsecode = 500
		json = '{"error":"Internal Server Error"}'


	response.set_content(content)
	response.set_response(responsecode)
	return json
index["service_record"] = service_record

def todo(response):
	responsecode = 200
	content = "application/json"
	json = ''

	try:
		if type(response.query) is not dict or \
		   "id" not in response.query:
			responsecode = 400 # Bad request
			json = '{"error":"Invalid identifying information"}'
		else:
			t = model.Todo(id=response.query["id"])
			t.delete()
			json = '{"success":"Deleted todo successfully"}'
	except model.RecordNotFoundError as e:
		responsecode = 404
		json = '{{"error":"{}"}}'.format(e)
	except Exception as e:
		responsecode = 500
		json = '{"error":"Internal Server Error"}'

	response.set_content(content)
	response.set_response(responsecode)
	return json
index["todo"] = todo





if __name__ == "__main__":
	for key in index.keys():
		print key + " : " + str(index[key])
