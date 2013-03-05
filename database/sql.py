import MySQLdb

try:
	db = MySQLdb.connect(
		host = 'localhost',
		user = 'root',
		passwd = '0178894',
		db = 'python'
	)
except Exception as e:
	sys.exit('We cant get into the database')

cursor = db.cursor()
cursor.execute('Select * from text')
result = cursor.fetchall()


if result:
	for z in result:
		print z[1] + ' ' + z[2]
