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
def getpiano(response):
	response.set_content("text/html")
	response.set_response(200)
	data  = "<!DOCTYPE html>"
	data += "<html><head><title>Piano</title></head>"
	data += "<body><p>Got a piano with:</p>"
	data += "<p>" + str(response.query) + "</p></body>"
	data += "</html>"
	return data

index["getpiano"] = getpiano





if __name__ == "__main__":
	for key in index.keys():
		print key + " : " + str(index[key])
