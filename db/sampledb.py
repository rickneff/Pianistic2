# This populates an existing DB instance with some sample data, for testing

import sqlite3 as db

con = db.connect("sample.db")
cur = con.cursor()

pianos = [
	(147381,    2, 18, 2, 'F052246',  2010, 18, '132', 1, 1, '', 0, 0, 90, 1, '0', '', '2014-09-01'),
	(147382,    2, 20, 2, 'F052247',  2010, 18, '133', 4, 1, '', 0, 0, 180, 1, '0', '', '2014-09-01'),
	(147337,    2, 20, 2, 'F051728',  2010, 18, '149', 4, 1, '', 0, 0, 90, 1, '0', '', '2014-09-01'),
	(144906,    2, 20, 2, 'F037006',  2008, 18, '153', 1, 1, 'Used as a loaner or extra piano.  Stored in SNO153', 0, 0, 180, 1, '0', '', '2014-09-01'),
	(1987655,   9, 15, 1, 'A80231',   2014,  1, '120', 1, 2, 'This piano has seen better days.', 1500, 1000, 180, 1, '0', 'Look closer ar the pedals.', '2014-09-01'),
	(143634,    9, 13, 2, 'H0060307', 2008, 18, '189', 1, 3, 'On a stage truck', 3395, 1500, 30, 1, '0', 'Squeaks when rocking back and fourth', '2014-09-01'),
	(8716384,   1,  1, 1, 'A145',     2014, 10, '123', 1, 1, 'abc',2000,1000,90,1,'NULL','xyz','2014-09-01'),
	(987123567, 1,  1, 1, 'G87265',   2014,  2, '234', 1, 1, 'abc',2000,2000,90,1,'NULL','xyz','2014-09-01'),
	(23759181,  1,  1, 1, 'G87561',   2013,  5, '101', 1, 2, 'abcd',2000,1700,90,1,'NULL','wxyz','2014-09-02'),
	(27761818,  9, 15, 1, 'Y768871',  2010,  6, '234', 1, 4, 'lasdkjflj',2000,1800,90,1,'NULL','woieruoiu','2014-09-10'),
	(9837126,   1,  1, 1, 'H98762',   2014,  5, '333', 1, 1, 'lasdkjf;lkj',2000,1900,90,1,'NULL','o2u3ozxic','2014-09-09'),
	(8377127,   1,  1, 1, 'H757777',  2014, 12, '404', 1, 1, 'lasjdf',2010,1020,60,1,'NULL','zx,cvn','2014-09-10'),
]

piano_service_histories = [
	(2, '2014-09-01', 'Tune-up', 'RN', 58, 68, 49.87),
]

todos = [
	("NULL", 1, "", "This is a todo!"),
	(     2, 1, "", "Check the gain pedal."),
	("NULL", 2, "", "Find out what room the new piano goes in.")
]

sql = "INSERT INTO piano (" + \
	"inventory_id, " + \
	"make_id, " + \
	"model_id, " + \
	"type_id, " + \
	"mfg_serial, " + \
	"year, " + \
	"building_id, " + \
	"room, " + \
	"room_type_id, " + \
	"condition_id, " + \
	"notes, " + \
	"cost, " + \
	"value, " + \
	"service_interval, " + \
	"previous_building_id, " + \
	"previous_room, " + \
	"service_notes, " + \
	"last_service_date" + \
	") " + \
	"VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);"
cur.executemany(sql, pianos);

sql = "INSERT INTO piano_service_history (" + \
	"piano_id, " + \
	"date, " + \
	"action, " + \
	"technician, " + \
	"humidity, " + \
	"temperature, " + \
	"pitch" + \
	") " + \
	"VALUES (?, ?, ?, ?, ?, ?, ?);"
cur.executemany(sql, piano_service_histories);

sql = "INSERT INTO todo (" + \
	"piano_id, " + \
	"building_id, " + \
	"room, " + \
	"notes" + \
	")" + \
	"VALUES (?, ?, ?, ?);"
cur.executemany(sql, todos);

con.commit();
