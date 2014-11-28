# This contains all of the data object definitions, as well
# as the code for populating object instances from the database
# and writing changes back.
import sqlite3 as db
import json as j

dbfile = "db/sample.db"

# Database tables:
#	piano_type
#	piano_make
#	piano_model
#	piano_condition
#	building
#	room_type
#	piano_service_history
#	piano
#	todo

# Objects:
#	piano
#		piano_type
#		piano_make
#		piano_model
#		piano_condition
#		building
#		room_type
#	piano_service_history
#		piano
#	todo
#		piano
#		building

class Piano(object):
# Instance variables:
#	Variable Name		Database name		Contents
#	id			id			Primary key in database
#	inventory_id		inventory_id		ID used by the school (unique?)
#	make			make_id->value		Make from piano_make table
#	model			model_id->value		Model from piano_model table
#	type			type_id->value		Piano type (grand or upright)
#	mfg_serial		mfg_serial		Serial number
#	year			year			Production year
#	building		building_id->value	Current building
#	room			room			Room number
#	room_type		room_type_id->value
#	condition		condition_id->value
#	notes			notes
#	cost			cost			Original cost
#	value			value			Current value
#	service_interval	service_interval	interval between service
#	previous_building	previous_building_id->value
#	previous_room		previous_room
#	service_notes		service_notes
#	last_service_date	last_service_date

	def __init__(self, id = None, inventory_id = None, json = None):
		# Initialize DB connection
		# and set a cursor
		global dbfile
		self.con = db.connect(dbfile)
		self.cur = self.con.cursor()

		if (id or inventory_id):
			self.fromdb(id, inventory_id)
		elif (json):
			self.fromjson(json)

	def __del__(self):
		self.con.close()

	# Initializes the Piano object from the database, using the
	# database id or inventory_id of the piano.
	def fromdb(self, id, inventory_id):
		args = ()
		sql =   "SELECT "                                     + \
			"    p.id, "                                  + \
			"    p.inventory_id, "                        + \
			"    make.value, "                            + \
			"    model.value, "                           + \
			"    type.value, "                            + \
			"    p.mfg_serial, "                          + \
			"    p.year, "                                + \
			"    building.value, "                        + \
			"    p.room, "                                + \
			"    room_type.value, "                       + \
			"    condition.value, "                       + \
			"    p.notes, "                               + \
			"    p.cost, "                                + \
			"    p.value, "                               + \
			"    p.service_interval, "                    + \
			"    pbuilding.value, "                       + \
			"    p.previous_room, "                       + \
			"    p.service_notes, "                       + \
			"    p.last_service_date "                    + \
		        "  FROM "                                     + \
			"    piano AS p JOIN "                        + \
			"    piano_type AS type JOIN "                + \
			"    piano_make AS make JOIN "                + \
			"    piano_model AS model JOIN "              + \
			"    piano_condition AS condition JOIN "      + \
			"    building JOIN "                          + \
			"    building AS pbuilding JOIN "             + \
			"    room_type "                              + \
			"  WHERE "                                    + \
			"    p.make_id = make.id AND "                + \
			"    p.model_id = model.id AND "              + \
			"    p.type_id = type.id AND "                + \
			"    p.building_id = building.id AND "        + \
			"    p.room_type_id = room_type.id AND "      + \
			"    p.condition_id = condition.id AND "      + \
			"    p.previous_building_id = pbuilding.id "
		if (id):
			sql += "AND p.id = ? "
			args += (id,)
		if (inventory_id):
			sql += "AND p.inventory_id = ? "
			args += (inventory_id,)
		sql += ";"

		self.cur.execute(sql, args)

		results = self.cur.fetchall()

		if len(results) < 1:
			raise RecordNotFoundError("No matching result",
			                          {"id"          : id,
			                           "inventory_id": inventory_id})
		elif len(results) > 1:
			raise NonUniqueSelectorError("Multiple results found",
			                             {"id"           : id,
			                              "inventory_id" : inventory_id})

		# Create and populate instance variables from database
		# This must be the same order as the values in the
		# SELECT statement.
		(
			self.id,
			self.inventory_id,
			self.make,
			self.model,
			self.type,
			self.mfg_serial,
			self.year,
			self.building,
			self.room,
			self.room_type,
			self.condition,
			self.notes,
			self.cost,
			self.value,
			self.service_interval,
			self.previous_building,
			self.previous_room,
			self.service_notes,
			self.last_service_date
		) = results[0]


	# Initializes the Piano object with data from a json string
	# (presumably passed in from the client).
	def fromjson(self, json):
		# Convert the JSON string into a dictionary
		data = j.loads(json)

		# Because we are not filtering, this could add attributes that
		# are not normally part of the Piano class.  It can also allow
		# attributes to be skipped.  Since this does not always cause
		# errors, we will not check for consistency here.
		for k, v in data.iteritems():
			setattr(self, k, v)


	# This returns a string that could be used to create an
	# identical object to this one.
	def __repr__(self):
		return "Piano(json = '" + str(self) + "')";

	# This returns a JSON string representation of
	# this object (to send to the client).
	def __str__(self):
		json = "{"

		for i in [
				"id",
				"inventory_id",
				"make",
				"model",
				"type",
				"mfg_serial",
				"year",
				"building",
				"room",
				"room_type",
				"condition",
				"notes",
				"cost",
				"value",
				"service_interval",
				"previous_building",
				"previous_room",
				"service_notes",
				"last_service_date"
			]:
			if i in self.__dict__:
				v = getattr(self, i)
				json += '"' + i + '":'
				if isinstance(v, (int, long, float)):
					json += str(v)
				else:
					json += '"' + v + '"'
				json += ", "

		# Take off the following comma, if there is one
		# then add the closing brace.
		if json[-2:] == ', ':
			json = json[:-2] + "}"

		return json

	# Write this object to the DB
	def write(self):
		# Check if this is already in the DB,
		# and send to the appropriate handler
		if "id" in dir(self):
			sql = "SELECT id FROM piano WHERE id = ?;"
			self.cur.execute(sql, (self.id,))

			if self.cur.fetchall():
				self._update()
			else:
				raise RecordNotFoundError("Cannot update nonexistent record")
		else:
			self._insert()

	# Delete a record from the DB
	def delete(self):
		if "id" not in dir(self):
			raise RecordNotFoundError("Cannot delete record without id")

		sql = "DELETE FROM piano WHERE id = ?;"
		self.cur.execute(sql, (self.id,))

		self.con.commit()

	# Insert a new record
	def _insert(self):
		# Make sure all necessary data is present
		error = ""

		# Mandatory attributes
		attr = [
			"make",
			"model",
			"type",
			"mfg_serial",
			"building",
			"room",
			"room_type",
			"condition",
		]

		for i in attr:
			if i not in dir(self):
				error += i + ", "

		# Throw error if we are missing anything
		if error:
			error = error[:-2] + " not found"
			raise InsufficientDataError(error)


		# Set defaults
		# Default attributes
		default = {
			"inventory_id"		: 0,
			"year"			: "NULL",
			"notes"			: "",
			"cost"			: 0,
			"value"			: 0,
			"service_interval"	: 90,
			"previous_building"	: "None",
			"previous_room"		: "",
			"service_notes"		: "",
			"last_service_date"	: "now",
		}

		for k, v in default.iteritems():
			setattr(self, k, getattr(self, k, v))

		# Prepare insertion SQL statement (the parenths automatically concat)
		sql  = (
			"INSERT INTO piano ("
			"  inventory_id, "
			"  make_id, "
			"  model_id, "
			"  type_id, "
			"  mfg_serial, "
			"  year, "
			"  building_id, "
			"  room, "
			"  room_type_id, "
			"  condition_id, "
			"  notes, "
			"  cost, "
			"  value, "
			"  service_interval, "
			"  previous_building_id, "
			"  previous_room, "
			"  service_notes, "
			"  last_service_date"
			") "
			"VALUES ("
			"  ?, "							# inventory_id
			"  (SELECT id FROM piano_make WHERE value=?), "		# make_id
			"  (SELECT id FROM piano_model WHERE value=?), "	# model_id
			"  (SELECT id FROM piano_type WHERE value=?), "		# type_id
			"  ?, "							# mfg_serial
			"  ?, "							# year
			"  (SELECT id FROM building WHERE value=?), "		# building_id
			"  ?, "							# room
			"  (SELECT id FROM room_type WHERE value=?), "		# room_type_id
			"  (SELECT id FROM piano_condition WHERE value=?), "	# condition_id
			"  ?, "							# notes
			"  ?, "							# cost
			"  ?, "							# value
			"  ?, "							# service_interval
			"  (SELECT id FROM building WHERE value=?), "		# previous_building_id
			"  ?, "							# previous_room
			"  ?, "							# service_notes
			"  date(?)"						# last_service_date
			");")

		# Setup the argument list
		args = (
			self.inventory_id,
			self.make,
			self.model,
			self.type,
			self.mfg_serial,
			self.year,
			self.building,
			self.room,
			self.room_type,
			self.condition,
			self.notes,
			self.cost,
			self.value,
			self.service_interval,
			self.previous_building,
			self.previous_room,
			self.service_notes,
			self.last_service_date,
		)

		# Finally, insert and commit
		self.cur.execute(sql, args)
		self.con.commit()

	# Update an existing record
	def _update(self):
		attr = {
			"inventory_id"      : "inventory_id=?, ",
			"make"              : "make_id=(SELECT id FROM piano_make WHERE value=?), ",
			"model"             : "model_id=(SELECT id FROM piano_model WHERE value=?), ",
			"type"              : "type_id=(SELECT id FROM piano_type WHERE value=?), ",
			"mfg_serial"        : "mfg_serial=?, ",
			"year"              : "year=?, ",
			"building"          : "building_id=(SELECT id FROM building WHERE value=?), ",
			"room"              : "room=?, ",
			"room_type"         : "room_type_id=(SELECT id FROM room_type WHERE value=?), ",
			"condition"         : "condition_id=(SELECT id FROM piano_condition WHERE value=?), ",
			"notes"             : "notes=?, ",
			"cost"              : "cost=?, ",
			"value"             : "value=?, ",
			"service_interval"  : "service_interval=?, ",
			"previous_building" : "previous_building_id=(SELECT id FROM building WHERE value=?), ",
			"previous_room"     : "previous_room=?, ",
			"service_notes"     : "service_notes=?, ",
			"last_service_date" : "last_service_date=date(?), ",
		}

		sql = "UPDATE piano SET "

		args = tuple()

		for k, v in attr.iteritems():
			if k in dir(self):
				sql += v
				args += (getattr(self, k),)

		sql = sql[:-2] + " WHERE id=?;"

		args += (self.id,)
		self.cur.execute(sql, args)
		self.con.commit()

# *****************************************************************
# This is low priority.  The current front end takes a complete
# list and does filtering on the client side.
#
# Function for getting a list of Pianos that match certain criteria
# Start out by querying the DB for a list of ids for matching
# pianos, then map Piano() to the list of ids.


def piano_list():
	# Return a JSON string consisting of all pianos
	con = db.connect(dbfile)
	cur = con.cursor()

	sql = "SELECT id FROM piano;"

	cur.execute(sql)

	pianos = [Piano(id=i[0]) for i in cur.fetchall()]
	json = '{' + ', '.join([str(i) for i in pianos]) + '}'

	con.close()

	return json


# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# We need objects for service history records and todos, as
# well as functions for generating lists of each.


# Custom Exceptions ---------------------------------------------

# If an inventory_id selector returns multiple records, we cannot
# just guess which is the right one, so throw this.
class NonUniqueSelectorError(Exception):
	pass

# If an id and/or inventory_id is used as the selector, but there
# is no matching record, throw this.
class RecordNotFoundError(Exception):
	pass

# When writing to the DB, certain data is essential
# This error is thrown when such data is not available.
class InsufficientDataError(Exception):
	pass


# Test suite ------------------------------------------------
if __name__ == "__main__":

	# If this is being run from resources/, then
	# we have to go back down to webroot before
	# going into db/.
	dbfile = "../db/sample.db"

	# Test looking up a piano by inventory_id
	p0 = Piano(inventory_id = 8377127);
	print "-------------------- p0 ---------------------"
	print p0
	print ""
	print p0.__repr__()

	print ""

	# Test looking up a piano by primary key
	p1 = Piano(id = 1)
	print "-------------------- p1 ---------------------"
	print p1
	print ""
	print p1.__repr__()

	print ""

	# Test creating a piano object from a JSON string
	p3 = Piano(json = '{"id":99, "inventory_id":6665, "make":"Suzuki"}')
	print "-------------------- p3 ---------------------"
	print p3
	print ""
	print p3.__repr__()

	print ""

	# Test generating a JSON string from a piano object, then
	# using it to create a new piano object
	p4 = Piano(json = str(p0))
	print "-------------------- p4 ---------------------"
	print p4
	print ""
	print p4.__repr__()

	print ""

	# Test to determine if the old and new objects created using
	# JSON to store the object are actually identical
	print "----------------- p0 == p4 ------------------"
	print (str(p4) == str(p0))

	print ""

	# Test the RecordNotFoundError exception
	try:
		px = Piano(id = 1313) # Non-existent id
		raise Exception("Failed to raise RecordNotFoundError")
	except RecordNotFoundError as e:
		print "Caught exception:"
		print "\tMessage: " + e[0]
		print "\tData:    " + str(e[1])

	print ""

	print "------------ Delete without id --------------"
	# Test delete without id
	px = Piano(json = '{"inventory_id": 999}')
	try:
		px.delete()
		raise Exception("Should have failed to delete, due to no id")
	except RecordNotFoundError as e:
		print "Caught exception:"
		print "\tMessage: " + e[0]

	print ""


	# Test write new piano and delete
	print "-------- Insert, Update, and Delete ---------"
	attribs = {
		"inventory_id":666,
		"make":"Knabe",
		"model":"D",
		"type":"Grand",
		"mfg_serial":"A94TSG",
		"building":"Benson",
		"room":"A12",
		"room_type":"Lounge",
		"condition":"Good",
	}
	json = "{"
	for k, v in attribs.iteritems():
		json += '"' + k + '":"' + str(v) + '", '
	json = json[:-2] + "}"
	px = Piano(json = json)

	print px
	print
	px.write()

	px = Piano(inventory_id = 666)

	failed = False
	for k, v in attribs.iteritems():
		if getattr(px, k) != v:
			print k + " comparison failed: " + str(getattr(px, k)) + " != " + str(v)
			failed = True

	if not failed:
		print "Write successful"
	else:
		print "Write failed"

	px = Piano(json = '{"id":' + str(px.id) + ', "make":"Yamaha"}')
	px.write()
	px = Piano(inventory_id = 666)
	if px.make == "Yamaha":
		print "Update successful"
	else:
		print "Update failed"

	px.delete()

	try:
		px = Piano(inventory_id = 666)
		raise Exception("This should have been deleted!")
	except:
		print "Delete successful"

	print ""


	# Test the NonUniqueSelectorError exception
	print "---------- NonUniqueSelector Error ----------"

	attribs = {
		"inventory_id":666,
		"make":"Knabe",
		"model":"D",
		"type":"Grand",
		"mfg_serial":"A94TSG",
		"building":"Benson",
		"room":"A12",
		"room_type":"Lounge",
		"condition":"Good",
	}
	json = "{"
	for k, v in attribs.iteritems():
		json += '"' + k + '":"' + str(v) + '", '
	json = json[:-2] + "}"
	px = Piano(json = json)
	# Write 2 of these, with the same inventory_id
	px.write()
	px.write()

	try:
		px = Piano(inventory_id = 666)
		raise Exception("This should have failed, with a NonUniqueSelector Error")
	except NonUniqueSelectorError as e:
		print "Caught exception:"
		print "\tMessage: " + str(e[0])
		print "\tData: " + str(e[1])

	sql = "DELETE FROM piano WHERE inventory_id = 666;"
	px.cur.execute(sql)
	px.con.commit()

	print ""

	print "---------------- Piano List -----------------"
	print piano_list()

	print ""
