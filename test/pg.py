import psycopg2
conn = psycopg2.connect(dbname='db03iu5pd5i2eb', user='wdxndskvwpomqk', 
                        password='cd32056b9db9997ab731803715a8330c9a317b358587eeae719638a3405af609', host='ec2-54-217-204-34.eu-west-1.compute.amazonaws.com')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE "user_ball" (
	"user_id"	INTEGER NOT NULL,
	"user_choose"	INTEGER NOT NULL,
	"math_p"	INTEGER NOT NULL,
	"russ"	INTEGER NOT NULL,
	"obsh"	INTEGER NOT NULL,
	"biol"	INTEGER NOT NULL,
	"phys"	INTEGER NOT NULL,
	"isto"	INTEGER NOT NULL,
	"info"	INTEGER NOT NULL,
	"himi"	INTEGER NOT NULL,
	"lite"	INTEGER NOT NULL,
	"geog"	INTEGER NOT NULL,
	"lang_e"	INTEGER NOT NULL
)''')
cursor.close()
conn.close()