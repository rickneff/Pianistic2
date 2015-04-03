import sqlite3 as db

con = db.connect("pianistic.db")
cur = con.cursor()

# <Enumerations> ------------------------------------------------------
# (SQLite does not support actual ENUMs, so we will
# have to simulate them with tables.)

# Enum names
enums = [
	"piano_type",
	"piano_make",
	"piano_model",
	"piano_condition",
	"building",
	"room_type",
]

# Enum values
piano_type = [
	"Grand",
	"Upright",
]

piano_make = [
	"Baldwin",
	"Kawai",
	"Knabe",
	"Mason & Hamlin",
	"Petrof",
	"Roland",
	"Sojin",
	"Steinway",
	"Yamaha",
]

piano_model = [
	"A",
	"B",
	"D",
	"G12",
	"GC2",
	"GX2",
	"KG2C",
	"KG2D",
	"L",
	"M",
	"M50",
	"O",
	"P22",
	"R",
	"RX2",
	"S",
	"Upright",
	"UST7",
	"UST8",
	"UST9",
]

piano_condition = [
	"Excellent",
	"Good",
	"Fair",
	"Poor",
]

building = [
	"None",
	"Austin",
	"Barnes Hall",
	"BCTR",
	"Benson",
	"Chapman Hall",
	"Hart",
	"Hinckley",
	"Kerr Hall",
	"Kirkham",
	"Lamprecht Hall",
	"Perkins Hall",
	"Ricks",
	"Romney",
	"Smith",
	"Spori",
	"Stadium",
	"Taylor",
	"Snow",
]

room_type = [
	"Classroom",
	"Concert Hall",
	"Lounge",
	"Office",
	"Practice Room",
	"Recital Hall",
	"Other",
]

# Bind enum names to data sets
bindings = {
	"piano_type"      : piano_type,
	"piano_make"      : piano_make,
	"piano_model"     : piano_model,
	"piano_condition" : piano_condition,
	"building"        : building,
	"room_type"       : room_type,
}

# First create all of the tables
sql = \
	"CREATE TABLE {} ( " + \
	"	id	INTEGER		PRIMARY KEY AUTOINCREMENT," + \
	"	value	VARCHAR(32)	NOT NULL UNIQUE" + \
	");";

for i in enums:
	# Formatting replaces the {} in the string with i
	cur.execute(sql.format(i))


# Next, populate the tables with the data
sql = "INSERT INTO {} (value) VALUES (?);"
for i in enums:
	# SQL wants a list of tuples
	data = [(j,) for j in bindings[i]]
	# Using format() again to insert table name
	cur.executemany(sql.format(i), data)

con.commit()

# Display the created tables
sql = "SELECT * FROM {};"
for i in enums:
	cur.execute(sql.format(i))
	print i
	for j in cur.fetchall():
		print "\t" + str(j[0]) + ", " + str(j[1])
	print ""

# </Enumerations> -----------------------------------------------------



# <Tables> ------------------------------------------------------------
sql = \
	"CREATE TABLE piano ( " + \
	"  id		INTEGER		PRIMARY KEY AUTOINCREMENT, " + \
	"  inventory_id	INTEGER, " + \
	"  make_id	INTEGER		REFERENCES piano_make (id), " + \
	"  model_id	INTEGER		REFERENCES piano_model (id), " + \
	"  type_id	INTEGER		REFERENCES piano_type (id), " + \
	"  mfg_serial	VARCHAR(32), " + \
	"  year		DATE, " + \
	"  building_id	INTEGER		REFERENCES building (id), " + \
	"  room		VARCHAR(16), " + \
	"  room_type_id	INTEGER		REFERENCES room_type (id), " + \
	"  condition_id	INTEGER		REFERENCES piano_condition (id), " + \
	"  notes	VARCHAR(256), " + \
	"  cost		INTEGER, " + \
	"  value	INTEGER, " + \
	"  service_interval	INTEGER, " + \
	"  previous_building_id	INTEGER	NOT NULL REFERENCES building (id), " + \
	"  previous_room	VARCHAR(16), " + \
	"  service_notes	VARCHAR(256), " + \
	"  last_service_date	DATE " + \
	");"
cur.execute(sql)

sql = \
	"CREATE TABLE piano_service_history ( " + \
	"  id		INTEGER		PRIMARY KEY AUTOINCREMENT, " + \
	"  piano_id	INTEGER		NOT NULL REFERENCES piano (id), " + \
	"  date		DATE		NOT NULL, " + \
	"  action	VARCHAR(256)	NOT NULL, " + \
	"  technician	VARCHAR(256)	NOT NULL, " + \
	"  humidity	INTEGER, " + \
	"  temperature	INTEGER, " + \
	"  pitch	FLOAT " + \
	");"
cur.execute(sql)

sql = \
	"CREATE TABLE todo ( " + \
	"  id		INTEGER		PRIMARY KEY AUTOINCREMENT, " + \
	"  piano_id	INTEGER		REFERENCES piano (id), " + \
	"  building_id	INTEGER		REFERENCES building (id), " + \
	"  room		VARCHAR(16), " + \
	"  notes	VARCHAR(256) " + \
	");"
cur.execute(sql)

con.commit()

# List tables
sql = "SELECT name FROM sqlite_master WHERE type='table';"
cur.execute(sql)

print "Tables:"
for i in cur.fetchall():
	print "\t" + i[0]

# </Tables> -----------------------------------------------------------

con.close()
