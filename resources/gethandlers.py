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
def getpiano(response):
	responsecode = 200
	content = "application/json"
	json = ""

	try:
		if type(response.query) is not dict or \
		   ("id" not in response.query and \
		   "inventory_id" not in response.query):
			responsecode = 400 # Bad Request
			json = '{"error":"Invalid identifying data"}'
		elif "id" in response.query:
			json = str(model.Piano(id=response.query["id"]))
		elif "inventory_id" in response.query:
			json = str(model.Piano(inventory_id=response.query["inventory_id"]))

	except model.NonUniqueSelectorError as e:
		responsecode = 400 # Bad Request
		json = '{{"error":{}}}'.format(e)
	except model.RecordNotFoundError as e:
		responsecode = 404
		json = '{{"error":{}}}'.format(e)
	except Exception as e:
		print e
		responsecode = 500
		content = "text/plain"
		json = "Internal Server Error"

	response.set_content(content)
	response.set_response(responsecode)
	return json
index["getpiano"] = getpiano

if __name__ == "__main__":
	for key in index.keys():
		print key + " : " + str(index[key])
