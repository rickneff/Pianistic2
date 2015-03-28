# This contains all of the data object definitions, as well
# as the code for populating object instances from the database
# and writing changes back.
import sqlite3 as db
import json as js

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
		data = js.loads(json)

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
					json += '"' + str(v) + '"'
				json += ", "

		# Take off the following comma, if there is one
		# then add the closing brace.
		if json[-2:] == ', ':
			json = json[:-2] + "}"

		return json.replace("\n", r"\n")

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
			if not getattr(self, i, None):
				error += i + ", "

		# Throw error if we are missing anything
		if error:
			error = "Mandatory attributes " + error[:-2] + " not found."
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


class Pianos(object):
# Loads and encapsulates a list of Piano objects that match
# certain criteria.

	# Pass this a dict of search criteria that must be met
	def __init__(self, criteria = {}):
		# We will need a DB connection for the initial search
		con = db.connect(dbfile)
		cur = con.cursor()

		# We will allow criteria to be a JSON object, by
		# converting it to a dict if it is a string
		if (type(criteria) == type(str())):
			criteria = js.loads(criteria)
		elif (type(criteria) == type(None)):
			criteria = {}

		fields = {
			"make_id"              : "make_id=?, ",
			"make"                 : "make_id=(SELECT id FROM piano_make WHERE value=?), ", # By name
			"model_id"             : "model_id=?, ",
			"model"                : "model_id=(SELECT id FROM piano_model WHERE value=?), ", # By name
			"type_id"              : "type_id=?, ",
			"type"                 : "type_id=(SELECT id FROM piano_type WHERE value=?), ", # By name
			"year"                 : "year=?, ",
			"building_id"          : "building_id=?, ",
			"building"             : "building_id=(SELECT id FROM building WHERE value=?), ", # By name
			"room"                 : "room=?, ",
			"room_type_id"         : "room_type_id=?, ",
			"room_type"            : "room_type_id=(SELECT id FROM room_type WHERE value=?), ", # By name
			"condition_id"         : "condition_id=?, ",
			"condition"            : "condition_id=(SELECT id FROM piano_condition WHERE value=?), ", # By name
			"service_interval"     : "service_interval=?, ",
			"previous_building_id" : "previous_building_id=?, ",
			"previous_building"    : "previous_building_id=(SELECT id FROM building WHERE value=?), ", # By name
			"previous_room"        : "previous_room=?, ",
			"last_service_date"    : "last_service_date=date(?), ",
		}

		sql  = "SELECT id FROM piano WHERE "
		args = ()

		for k, v in criteria.iteritems():
			if k in fields:
				sql  += fields[k]
				args += (v,)

		if len(criteria) == 0:
			sql = "SELECT id FROM piano  "

		sql = sql[:-2] + ";"

		cur.execute(sql, args)
		ids = cur.fetchall()

		# That is all we needed from the DB
		con.close()

		self.records = []
		for id in ids:
			self.records.append(Piano(id = id[0]))

		self.criteria = criteria

	def __repr__(self):
		return "Pianos(" + repr(self.criteria) + ")"

	def __str__(self):
		json = "["
		for i in self.records:
			json += str(i) + ", "

		if len(self.records) > 0:
			json = json[:-2]

		json += "]"
		return json

	def __getitem__(self, index):
		return self.records[index]

	def __len__(self):
		return len(self.records)


class ServiceRecord(object):
# Instance variables:
#	Variable Name		Database name		Contents
#	id			id			Primary key in DB
#	piano_id		piano_id		Piano ID for record
#	date			date			Date of service
#	action			action			Service performed
#	technician		technician		Who performed the service
#	humidity		humidity		Humidity at time of service
#	temperature		temperature		Temperature at time of service
#	pitch			pitch			Piano pitch at time of service

	def __init__(self, id = None, json = None):
		# Setup DB connection for this object
		self.con = db.connect(dbfile)
		self.cur = self.con.cursor()

		if (id):
			self.fromdb(id)
		elif (json):
			self.fromjson(json)

	def __del__(self):
		self.con.close()

	def fromdb(self, id):
		args = (id,)
		sql =   "SELECT "                                     + \
			"    id, "                                    + \
			"    piano_id, "                              + \
			"    date, "                                  + \
			"    action, "                                + \
			"    technician, "                            + \
			"    humidity, "                              + \
			"    temperature, "                           + \
			"    pitch "                                  + \
		        "  FROM "                                     + \
			"    piano_service_history "                  + \
			"  WHERE "                                    + \
			"    id = ?;"

		self.cur.execute(sql, args)

		results = self.cur.fetchall()

		if len(results) < 1:
			raise RecordNotFoundError("No matching result",
			                          {"id"          : id})
		elif len(results) > 1:
			raise NonUniqueSelectorError("Multiple results found",
			                             {"id"           : id})

		# Create and populate instance variables from database
		# This must be the same order as the values in the
		# SELECT statement.
		(
			self.id,
			self.piano_id,
			self.date,
			self.action,
			self.technician,
			self.humidity,
			self.temperature,
			self.pitch,
		) = results[0]

	# Initializes the object with data from a json string
	# (presumably passed in from the client).
	def fromjson(self, json):
		# Convert the JSON string into a dictionary
		data = js.loads(json)

		# Because we are not filtering, this could add attributes that
		# are not normally part of this class.  It can also allow
		# attributes to be skipped.  Since this does not always cause
		# errors, we will not check for consistency here.
		for k, v in data.iteritems():
			setattr(self, k, v)

	# This returns a string that could be used to create an
	# identical object to this one.
	def __repr__(self):
		return "ServiceRecord(json = '" + str(self) + "')";

	# This returns a JSON string representation of
	# this object (to send to the client).
	def __str__(self):
		json = "{"

		for i in [
				"id",
				"piano_id",
				"date",
				"action",
				"technician",
				"humidity",
				"temperature",
				"pitch",
			]:
			if i in self.__dict__:
				v = getattr(self, i)
				json += '"' + i + '":'
				if isinstance(v, (int, long, float)):
					json += str(v)
				else:
					json += '"' + str(v) + '"'
				json += ", "

		# Take off the following comma, if there is one
		# then add the closing brace.
		if json[-2:] == ', ':
			json = json[:-2] + "}"

		return json.replace("\n", r"\n")
	
	# Write this object to the DB
	def write(self):
		# Check if this is already in the DB,
		# and send to the appropriate handler
		if "id" in dir(self):
			sql = "SELECT id FROM piano_service_history WHERE id = ?;"
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

		sql = "DELETE FROM piano_service_history WHERE id = ?;"
		self.cur.execute(sql, (self.id,))

		self.con.commit()

	# Insert a new record
	def _insert(self):
		# Make sure all necessary data is present
		error = ""

		# Mandatory attributes
		attr = [
			"piano_id",
			"action",
			"technician",
		]

		for i in attr:
			if not getattr(self, i, None):
				error += i + ", "

		# Throw error if we are missing anything
		if error:
			error = error[:-2] + " not found"
			raise InsufficientDataError(error)


		# Set defaults
		# Default attributes
		default = {
			"date"			: "now",
			"humidity"		: "",
			"temperature"		: "",
			"pitch"			: "",
		}

		for k, v in default.iteritems():
			setattr(self, k, getattr(self, k, v))

		# Prepare insertion SQL statement (the parenths automatically concat)
		sql  = (
			"INSERT INTO piano_service_history ("
			"  piano_id, "
			"  date, "
			"  action, "
			"  technician, "
			"  humidity, "
			"  temperature, "
			"  pitch "
			") "
			"VALUES ("
			"  ?, "							# piano_id
			"  date(?), "						# date
			"  ?, "							# action
			"  ?, "							# technician
			"  ?, "							# humidity
			"  ?, "							# temperature
			"  ?"							# pitch
			");")

		# Setup the argument list
		args = (
			self.piano_id,
			self.date,
			self.action,
			self.technician,
			self.humidity,
			self.temperature,
			self.pitch,
		)

		# Finally, insert and commit
		self.cur.execute(sql, args)
		self.con.commit()

	# Update an existing record
	def _update(self):
		attr = {
			"piano_id"    : "piano_id=?, ",
			"date"        : "date=date(?), ",
			"action"      : "action=?, ",
			"technician"  : "technician=?, ",
			"humidity"    : "humidity=?, ",
			"temperature" : "temperature=?, ",
			"pitch"       : "pitch=?, ",
		}

		sql = "UPDATE piano_service_history SET "

		args = tuple()

		for k, v in attr.iteritems():
			if k in dir(self):
				sql += v
				args += (getattr(self, k),)

		sql = sql[:-2] + " WHERE id=?;"

		args += (self.id,)
		self.cur.execute(sql, args)
		self.con.commit()
		
class ServiceRecords(object):
# Loads and encapsulates a list of ServiceRecord objects that match
# certain criteria.

	# Pass this a dict of search criteria that must be met
	def __init__(self, criteria = {}):
		# We will need a DB connection for the initial search
		con = db.connect(dbfile)
		cur = con.cursor()

		# We will allow criteria to be a JSON object, by
		# converting it to a dict if it is a string
		if (type(criteria) == type(str())):
			criteria = js.loads(criteria)
		elif (type(criteria) == type(None)):
			criteria = {}

		fields = {
			"piano_id"    : "piano_id=?, ",
			"date"        : "date=date(?), ",
			"action"      : "action=?, ",
			"technician"  : "technician=?, ",
			"humidity"    : "humidity=?, ",
			"temperature" : "temperature=?, ",
			"pitch"       : "pitch=?, ",
		}

		sql  = "SELECT id FROM piano_service_history WHERE "
		args = ()

		for k, v in criteria.iteritems():
			if k in fields:
				sql  += fields[k]
				args += (v,)

		if len(criteria) == 0:
			sql = "SELECT id FROM piano_service_history  "

		sql = sql[:-2] + " ORDER BY date DESC;"

		cur.execute(sql, args)
		ids = cur.fetchall()

		# That is all we needed from the DB
		con.close()

		self.records = []
		for id in ids:
			self.records.append(ServiceRecord(id = id[0]))

		self.criteria = criteria

	def __repr__(self):
		return "ServiceRecords(" + repr(self.criteria) + ")"

	def __str__(self):
		json = '['
		for i in self.records:
			json += str(i) + ", "

		if len(self.records) > 0:
			json = json[:-2]

		json += "]"

		return json

	def __getitem__(self, index):
		return self.records[index]

	def __len__(self):
		return len(self.records)


class Todo(object):
# Instance variables:
#	Variable Name		Database name		Contents
#	id			id			Primary key in DB
#	mfg_serial		piano->mfg_serial	Piano serial number
#	building		building_id->value	Building note refers to
#	room			room			Room note refers to
#	notes			notes			Actual note text
	def __init__(self, id = None, json = None):
		# Setup DB connection for this object
		self.con = db.connect(dbfile)
		self.cur = self.con.cursor()

		if (id):
			self.fromdb(id)
		elif (json):
			self.fromjson(json)

	def __del__(self):
		self.con.close()

	def fromdb(self, id):
		args = (id,)
		sql =   "SELECT "                      + \
			"    t.id, "                   + \
			"    (SELECT mfg_serial FROM piano WHERE id = t.piano_id), " + \
			"    b.value, "                + \
			"    t.room, "                 + \
			"    t.notes "                 + \
		        "  FROM "                      + \
			"    todo AS t JOIN "          + \
			"    building AS b "           + \
			"  WHERE "                     + \
			"    t.building_id = b.id AND" + \
			"    t.id = ?;"

		self.cur.execute(sql, args)

		results = self.cur.fetchall()

		if len(results) < 1:
			raise RecordNotFoundError("No matching result",
			                          {"id"          : id})
		elif len(results) > 1:
			raise NonUniqueSelectorError("Multiple results found",
			                             {"id"           : id})

		# Create and populate instance variables from database
		# This must be the same order as the values in the
		# SELECT statement.
		(
			self.id,
			self.mfg_serial,
			self.building,
			self.room,
			self.notes,
		) = results[0]

	# Initializes the object with data from a json string
	# (presumably passed in from the client).
	def fromjson(self, json):
		# Convert the JSON string into a dictionary
		data = js.loads(json)

		# Because we are not filtering, this could add attributes that
		# are not normally part of this class.  It can also allow
		# attributes to be skipped.  Since this does not always cause
		# errors, we will not check for consistency here.
		for k, v in data.iteritems():
			setattr(self, k, v)

	# This returns a string that could be used to create an
	# identical object to this one.
	def __repr__(self):
		return "Todo(json = '" + str(self) + "')";

	# This returns a JSON string representation of
	# this object (to send to the client).
	def __str__(self):
		json = "{"

		for i in [
				"id",
				"mfg_serial",
				"building",
				"room",
				"notes",
			]:
			if i in self.__dict__:
				v = getattr(self, i)
				json += '"' + i + '":'
				if isinstance(v, (int, long, float)):
					json += str(v)
				else:
					json += '"' + str(v) + '"'
				json += ", "

		# Take off the following comma, if there is one
		# then add the closing brace.
		if json[-2:] == ', ':
			json = json[:-2] + "}"

		return json.replace("\n", r"\n")
	
	# Write this object to the DB
	def write(self):
		# Check if this is already in the DB,
		# and send to the appropriate handler
		if "id" in dir(self):
			sql = "SELECT id FROM todo WHERE id = ?;"
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

		sql = "DELETE FROM todo WHERE id = ?;"
		self.cur.execute(sql, (self.id,))

		self.con.commit()

	# Insert a new record
	def _insert(self):
		# Make sure all necessary data is present
		error = ""

		# Mandatory attributes
		attr = [
			"notes",
		]

		for i in attr:
			if not getattr(self, i, None):
				error += i + ", "

		# Throw error if we are missing anything
		if error:
			error = error[:-2] + " not found"
			raise InsufficientDataError(error)


		# Set defaults
		# Default attributes
		default = {
			"mfg_serial"		: "NULL",
			"building"		: "None",
			"room"			: "NULL",
		}

		for k, v in default.iteritems():
			setattr(self, k, getattr(self, k, v))

		# Prepare insertion SQL statement (the parenths automatically concat)
		sql  = (
			"INSERT INTO todo ("
			"  piano_id, "
			"  building_id, "
			"  room, "
			"  notes "
			") "
			"VALUES ("
			"  (SELECT id FROM piano WHERE mfg_serial=?), "		# piano_id
			"  (SELECT id FROM building WHERE value=?), "		# building_id
			"  ?, "							# room
			"  ?"							# notes
			");")

		# Setup the argument list
		args = (
			self.mfg_serial,
			self.building,
			self.room,
			self.notes,
		)

		# Finally, insert and commit
		self.cur.execute(sql, args)
		self.con.commit()

	# Update an existing record
	def _update(self):
		attr = {
			"piano_id" : "piano_id=?, ",
			"building" : "building_id=(SELECT id FROM building WHERE value=?), ",
			"room"     : "room=?, ",
			"notes"    : "notes=?, ",
		}

		sql = "UPDATE todo SET "

		args = tuple()

		for k, v in attr.iteritems():
			if k in dir(self):
				sql += v
				args += (getattr(self, k),)

		sql = sql[:-2] + " WHERE id=?;"

		args += (self.id,)
		self.cur.execute(sql, args)
		self.con.commit()


class Todos(object):
# Loads and encapsulates a list of Todo objects that match
# certain criteria.

	# Pass this a dict of search criteria that must be met
	def __init__(self, criteria = {}):
		# We will need a DB connection for the initial search
		con = db.connect(dbfile)
		cur = con.cursor()

		# We will allow criteria to be a JSON object, by
		# converting it to a dict if it is a string
		if (type(criteria) == type(str())):
			criteria = js.loads(criteria)
		elif (type(criteria) == type(None)):
			criteria = {}

		fields = {
			"piano_id"    : "piano_id=?, ",
			"building"    : "building_id=(SELECT id FROM building WHERE value=?), ", # By name
			"building_id" : "building_id=?, ",
			"room"        : "room=?, ",
		}

		sql  = "SELECT id FROM todo WHERE "
		args = ()

		for k, v in criteria.iteritems():
			if k in fields:
				sql  += fields[k]
				args += (v,)

		if len(criteria) == 0:
			sql = "SELECT id FROM todo  "

		sql = sql[:-2] + ";"

		cur.execute(sql, args)
		ids = cur.fetchall()

		# That is all we needed from the DB
		con.close()

		self.records = []
		for id in ids:
			self.records.append(Todo(id = id[0]))

		self.criteria = criteria

	def __repr__(self):
		return "Todos(" + repr(self.criteria) + ")"

	def __str__(self):
		json = '['
		for i in self.records:
			json += str(i) + ", "

		if len(self.records) > 0:
			json = json[:-2]

		json += "]"

		return json

	def __getitem__(self, index):
		return self.records[index]

	def __len__(self):
		return len(self.records)


# Enumeration Getters
def get_piano_types():
	return _get_enum("piano_type")

def get_piano_makes():
	return _get_enum("piano_make")

def get_piano_models():
	return _get_enum("piano_model")

def get_piano_conditions():
	return _get_enum("piano_condition")

def get_buildings():
	return _get_enum("building")

def get_room_types():
	return _get_enum("room_type")

def _get_enum(name):
	con = db.connect(dbfile)
	cur = con.cursor()

	sql = "SELECT value FROM " + name + ";"
	cur.execute(sql)

	results = cur.fetchall()
	con.close()

	json = '['

	for result in results:
		json += '"' + result[0] + '", '

	if len(results) > 0:
		json = json[:-2]

	json += ']'

	return json.replace("\n", r"\n")

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


	# Test retrieving service record from DB
	print "----------- Select Service Record -----------"
	sr = ServiceRecord(id = 1)
	print sr

	print ""


	# Test creating new service record, modifying it, then
	# deleting it
	print "---------- Interact Service Record ----------"
	record = {
		"piano_id":4,
		"date":"2014-12-05",
		"action":"Replaced pads",
		"technician":"Me!",
		"humidity":70,
		"temperature":72,
		"pitch":43.5,
	}

	json = "{"
	for k, v in record.iteritems():
		json += '"' + k + '":"' + str(v) + '", '
	json = json[:-2] + "}"

	sr = ServiceRecord(json = json)

	if (cmp(js.loads(json), js.loads(str(sr)))):
		print "Failed to produce record from json"
		print "json:", json
		print "str(sr):", str(sr)
	else:
		print "Successfully loaded record from JSON"

	sr.write()
	print "Successfully wrote record"

	sql = "SELECT id FROM piano_service_history WHERE piano_id=? AND action=? AND technician=?;"
	args = (sr.piano_id, sr.action, sr.technician)

	sr.cur.execute(sql, args)
	id = sr.cur.fetchall()[0][0]

	srx = ServiceRecord(id = id)

	if (str(sr) == str(srx)):
		print "Successfully read record"

	srx.technician = "Not me anymore."
	srx.write()

	sr = ServiceRecord(id = id)

	if (sr.technician == "Not me anymore."):
		print "Successfully updated record"
	else:
		print "Update failed"

	sr.delete()

	try:
		sr = ServiceRecord(id = id)
		raise Exception("Delete must have failed", {"id":id})
	except Exception as e:
		print "Successfully deleted record"

	print ""


	# Test various ServiceRecords things
	print "--------- Interact Service Records ----------"
	records = [
	{
		u"piano_id":666,
		u"date":"2014-12-01",
		u"action":"Replaced pads",
		u"technician":"Me!",
		u"humidity":50,
		u"temperature":70,
		u"pitch":40.1,
	},
	{
		u"piano_id":666,
		u"date":"2014-12-05",
		u"action":"Replaced pads",
		u"technician":"Me!",
		u"humidity":75,
		u"temperature":65,
		u"pitch":40.2,
	},
	{
		u"piano_id":666,
		u"date":"2014-12-02",
		u"action":"Replaced pads",
		u"technician":"Me!",
		u"humidity":90,
		u"temperature":75,
		u"pitch":40.3,
	}]



	for i in records:
		json = "{"
		for k, v in i.iteritems():
			json += '"' + k + '":"' + str(v) + '", '
		json = json[:-2] + "}"

		ServiceRecord(json = json).write()
	
	srs = ServiceRecords({"piano_id":666})

	success = True
	if len(srs) == len(records):
		tr = [records[1], records[2], records[0]]
		for s, r in zip(srs, tr):
			s = js.loads(str(s))
			del s["id"]
			if cmp(s, r):
				success = False
				print s
				print r

		if success:
			print "Successfully loaded list of records"
		else:
			print "Failed to load the correct records"
	else:
		print "Failed to load the correct number of records"

	date = "2014-12-32"
	success = True
	for i in srs:
		if i.date > date:
			success = False
		date = i.date

	if success:
		print "Successfully read sorted list of records"
	else:
		print "Failed to sort records correctly"

	sql = "DELETE FROM piano_service_history WHERE piano_id=666;"
	srs[0].cur.execute(sql)
	srs[0].con.commit()

	print ""


	# Todo list tests
	print "----------- Interact Todo Records -----------"
	print "This needs to be rewritten!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
	print Todo(id=2)
#	todos = [
#		{"piano_id":2, "notes":"This piano needs some serious work"},
#		{"building":"Perkins Hall", "notes":"This building needs some serious work"},
#		{"room":"2", "notes":"This room needs some serious work"},
#		{"notes":"Today has been an interesting day"},
#	]
#
#	for i in todos:
#		json = "{"
#		for k, v in i.iteritems():
#			json += '"' + k + '":"' + str(v) + '", '
#		json = json[:-2] + "}"
#
#		Todo(json = json).write()
#	
#	sql = "SELECT id FROM todo;"
#	srs[0].cur.execute(sql)
#	
#	ids = srs[0].cur.fetchall()
#
#	if len(ids) == len(todos):
#		print "Successfully wrote records"
#	else:
#		print "Record count mismatch"
#
#	records = 0
#	for i in ids:
#		todo = Todo(id = i[0])
#		for j in todos:
#			if Todo(id = i[0]).notes == j["notes"]:
#				records += 1
#
#	if records == len(ids):
#		print "Successfully read all records"
#	else:
#		print "Failed to find all records"
#
#	alltodos = Todos()
#	p2todos = Todos({"piano_id":2})
#	phtodos = Todos('{"building":"Perkins Hall"}')
#	r2todos = Todos({"room":2})
#
#	if len(alltodos) >= 4:
#		print "Sucessfully read all todos with Todos class"
#	else:
#		print "Failed to read all todos with Todos class"
#
#	if len(p2todos) >= 1:
#		print "Sucessfully read piano_id == 2 todos with Todos class"
#	else:
#		print "Failed to read piano_id == 2 todos with Todos class"
#
#	if len(phtodos) >= 1:
#		print "Sucessfully read building == Perkins Hall todos with Todos class"
#	else:
#		print "Failed to read building == Perkins Hall todos with Todos class"
#
#	if len(r2todos) >= 1:
#		print "Sucessfully read room == 2 todos with Todos class"
#	else:
#		print "Failed to read room == 2 todos with Todos class"
#
#	for i in ids:
#		Todo(id = i[0]).delete()
#
#	sql = "SELECT id FROM todo;"
#	srs[0].cur.execute(sql)
#	ids = srs[0].cur.fetchall()
#
#	if len(ids) > 0:
#		print "Failed to delete records"
#	else:
#		print "Successfully deleted records"
#
	print ""



	print "---------- Interact Pianos Records ----------"
	# Test get all pianos
	allpianos = Pianos()

	# Count the pianos
	srs[0].cur.execute("SELECT COUNT(*) FROM piano;")
	count = srs[0].cur.fetchall()[0][0]

	if len(allpianos) == count:
		print "Successfully loaded all pianos"
	else:
		print "Failed to load all pianos"


	# Test get pianos by make name
	balpianos = Pianos('{"make":"Baldwin"}')

	# Count the Baldwin pianos
	srs[0].cur.execute("SELECT COUNT(*) FROM piano WHERE make_id=(SELECT id FROM piano_make WHERE value='Baldwin');")
	count = srs[0].cur.fetchall()[0][0]

	if len(balpianos) == count:
		print "Successfully loaded all Baldwin pianos by make name"
	else:
		print "Failed to load all Baldwin pianos by make name"


	# Test get pianos by building id
	srs[0].cur.execute("SELECT id FROM building WHERE value='Austin';")
	building_id = srs[0].cur.fetchall()[0][0]

	auspianos = Pianos({"building_id":building_id})

	# Count pianos in Austin
	srs[0].cur.execute("SELECT COUNT(*) FROM piano WHERE building_id=(SELECT id FROM building WHERE value='Austin');")
        count = srs[0].cur.fetchall()[0][0]

	if len(auspianos) == count:
		print "Successfully loaded all pianos in Austin by building_id"
	else:
		print "Failed to load all pianos in Austin by building_id"

	print ""

	print "------------ Enumeration Getters ------------"

	print "Get piano types"
	print get_piano_types()
	print


	print "Get piano makes"
	print get_piano_makes()
	print

	print "Get piano models"
	print get_piano_models()
	print

	print "Get piano conditions"
	print get_piano_conditions()
	print

	print "Get buildings"
	print get_buildings()
	print

	print "Get room types"
	print get_room_types()
	print

'''
We can abstract out a bunch of stuff, because most of the DB reader classes
use very similar code.  If we can take out the table specific stuff, we can
make a parent class that handles most of the DB access.

To do this, each child class will need to contain information about how its
table is arranged.  This information will be used by the parent class to
handle selecting, inserting, and updating.

DBRecord(object)
members:
	sql query for selecting (including dereferencing)
	list of columns, by name
	defaults for insert (anything not here should be mandatory)
	sql query for inserting (including referencing)
	sql query dict for updating (including referencing)

A similar parent might be created for the record list objects as well.
'''
