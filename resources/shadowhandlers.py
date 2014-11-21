# This file contains resources handlers intended to hide static
# resources.  To add a shadow, add the file or directory name
# to the dictionary as the key name, with the value shadow.
# Shadow handlers can only hide resources in the webroot.
# Directories that are shadowed will also hide all of their
# contents.



# Resource request handler index
# After each resource handler function, that function should be added
# to this dictionary.
# For an enumeration of resources, run this program as a standalone.
index = {
#	resource_name:	handler function
}

# Shadow resources (for hiding files)
# Note that these will only hide resources in the webroot.
# Shadowed directories in webroot will be entirely inaccessible
# from the browser (this includes are files in them).  Files
# in subdirectories of webroot cannot be individually
# shadowed, but files in webroot can.

# Any resources that need to be shadowed should
# point to this function.
def shadow(response):
	response.set_content("text/html")
	response.set_response(404)
	data  = "<!DOCTYPE html>"
	data += "<html><head><title>404 Not Found</title></head>"
	data += "<body><p>404: Resource not found</p>"
	data += "</html>"
	return data

# Hide the db directories that may contain sqlite or other
# database files.
index["db"] = shadow

# Resource files (including this one) should probably
# go in a shadowed directory, to avoid having to shadow
# all of them individually.
index["resources"] = shadow



if __name__ == "__main__":
	for key in index.keys():
		print key + " : " + str(index[key])
