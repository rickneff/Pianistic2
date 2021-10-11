import datamodel as model
import json as js

# Resource request handler index
# After each resource handler function, that function should be added
# to this dictionary.
# For an enumeration of resources, run this program as a standalone.
index = {
#  resource_name:  handler function
}


# Handler functions
#
# Handlers take a single argument, which is the response object for the
# request.  Handlers should set_content for content type and
# set_response for response code, for each request.  The data should be
# returned in the return value.
def piano(response):
  # Get a piano using either id or inventory_id
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
    print(e)
    responsecode = 500
    content = "text/plain"
    json = "Internal Server Error"

  response.set_content(content)
  response.set_response(responsecode)
  return json
index["piano"] = piano


def pianos(response):
  # Get a list of pianos filtering by a list of criteria
  # sent as either a regular query or a JSON query string
  responsecode = 200
  content = "application/json"
  json = ""

  try:
    json = str(model.Pianos(response.query))
  except ValueError as e:
    print(e)
    responsecode = 400 # Bad Request
    json = '{"error":"Malformed query"}'
  except Exception as e:
    print(e)
    responsecode = 500
    content = "text/plain"
    json = "Internal Server Error"

  response.set_content(content)
  response.set_response(responsecode)
  return json
index["pianos"] = pianos


def service_record(response):
  # Get a service record by id (or an error...)
  responsecode = 200
  content = "application/json"
  json = ""

  try:
    if type(response.query) is not dict or \
       "id" not in response.query:
      responsecode = 400 # Bad Request
      json = '{"error":"Invalid identifying data"}'
    elif "id" in response.query:
      json = str(model.ServiceRecord(id=response.query["id"]))

  except model.NonUniqueSelectorError as e:
    responsecode = 400 # Bad Request
    json = '{{"error":{}}}'.format(e)
  except model.RecordNotFoundError as e:
    responsecode = 404
    json = '{{"error":{}}}'.format(e)
  except Exception as e:
    print(e)
    responsecode = 500
    content = "text/plain"
    json = "Internal Server Error"

  response.set_content(content)
  response.set_response(responsecode)
  return json
index["service_record"] = service_record


def service_records(response):
  # Get a list of service records filtering by a list of criteria
  # sent as either a regular query or a JSON query string
  responsecode = 200
  content = "application/json"
  json = ""

  try:
    json = str(model.ServiceRecords(response.query))
  except ValueError as e:
    print(e)
    responsecode = 400 # Bad Request
    json = '{"error":"Malformed query"}'
  except Exception as e:
    print(e)
    responsecode = 500
    content = "text/plain"
    json = "Internal Server Error"

  response.set_content(content)
  response.set_response(responsecode)
  return json
index["service_records"] = service_records


def todo(response):
  # Get a todo by id
  responsecode = 200
  content = "application/json"
  json = ""

  try:
    if type(response.query) is not dict or \
       "id" not in response.query:
      responsecode = 400 # Bad Request
      json = '{"error":"Invalid identifying data"}'
    elif "id" in response.query:
      json = str(model.Todo(id=response.query["id"]))

  except model.NonUniqueSelectorError as e:
    responsecode = 400 # Bad Request
    json = '{{"error":{}}}'.format(e)
  except model.RecordNotFoundError as e:
    responsecode = 404
    json = '{{"error":{}}}'.format(e)
  except Exception as e:
    print(e)
    responsecode = 500
    content = "text/plain"
    json = "Internal Server Error"

  response.set_content(content)
  response.set_response(responsecode)
  return json
index["todo"] = todo


def todos(response):
  # Get a list of todos filtering by a list of criteria
  # sent as either a regular query or a JSON query string
  responsecode = 200
  content = "application/json"
  json = ""

  try:
    json = str(model.Todos(response.query))
  except ValueError as e:
    print(e)
    responsecode = 400 # Bad Request
    json = '{"error":"Malformed query"}'
  except Exception as e:
    print(e)
    responsecode = 500
    content = "text/plain"
    json = "Internal Server Error"

  response.set_content(content)
  response.set_response(responsecode)

  return json
index["todos"] = todos

def enum(response):
  responsecode = 200
  content = "application/json"
  json = ""

  enums = {
    "piano_type"      : model.get_piano_types,
    "piano_make"      : model.get_piano_makes,
    "piano_model"     : model.get_piano_models,
    "piano_condition" : model.get_piano_conditions,
    "building"        : model.get_buildings,
    "room_type"       : model.get_room_types,
  }

  if response.subpath in enums:
    json = enums[response.subpath]()
  else:
    responsecode = 404
    json = '{{"error":"Enum {} not found"}}'.format(response.subpath)

  response.set_content(content)
  response.set_response(responsecode)
  return json

index["enum"] = enum


if __name__ == "__main__":
  for key in index.keys():
    print(key + " : " + str(index[key]))
