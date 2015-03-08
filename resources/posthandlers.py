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

	jform = response.postjson

	try:
		p = model.Piano(json=jform)
		p.write()

		json = '{"success":"Wrote piano successfully"}'
	except ValueError:
		responsecode = 400
		json = '{"error":"Invalid JSON object"}'
	except model.InsufficientDataError as e:
		responsecode = 400
		json = '{{"error":"{}"}}'.format(e)
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

	jform = response.postjson

	try:
		s = model.ServiceRecord(json=jform)
		s.write()

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# We need to check the resetInterval element (if it
# exists), and reset the last service date for the piano
# to the value of the date element, if it is true.
		print "\033[1;37m!!! Resetting last service date not yet implemented !!!\033[0;37m"

		json = '{"success":"Wrote service record successfully"}'
	except ValueError:
		responsecode = 400
		json = '{"error":"Invalid JSON object"}'
	except model.InsufficientDataError as e:
		responsecode = 400
		json = '{{"error":"{}"}}'.format(e)
	except Exception as e:
		responsecode = 500
		content = "text/plain"
		json = "Internal Server Error"


	response.set_content(content)
	response.set_response(responsecode)
	return json
index["service_record"] = service_record

def todo(response):
	responsecode = 200
	content = "application/json"
	json = ''

	jform = response.postjson

	try:
		t = model.Todo(json=jform)
		t.write()

		json = '{"success":"Wrote todo successfully"}'
	except ValueError:
		responsecode = 400
		json = '{"error":"Invalid JSON object"}'
	except model.InsufficientDataError as e:
		responsecode = 400
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
