from flask_wtf import Form
from wtforms import FileField, SubmitField
from datetime import datetime
import pymysql
import config

class MSimpanUser:
	def __init__ (self, id_user=None, id_level=None, nama=None, username=None, password=None, tanggal_lahir=None, jenis_kelamin=None, no_telp=None, dusun=None, id_desa=None, id_kecamatan=None, id_kabupaten=None, uker=None):
		self.id_user = id_user
		self.id_level = id_level
		self.nama = nama
		self.username = username
		self.password = password
		self.tanggal_lahir = tanggal_lahir
		self.jenis_kelamin = jenis_kelamin
		self.no_telp = no_telp
		self.dusun = dusun
		self.id_desa = id_desa
		self.id_kecamatan = id_kecamatan
		self.id_kabupaten = id_kabupaten
		self.uker = uker

	def openDB (self):
		global db, cursor
		db = pymysql.connect(
			config.DB_HOST,
			config.DB_USER,
			config.DB_PASSWORD,
			config.DB_NAME)
		cursor = db.cursor()

	def closeDB(self):
		global db, cursor
		db.close()

	def selectDB(self):
		self.openDB()
		cursor.execute("SELECT * FROM user")
		container = []
		self.closeDB()
		return container

	def insertDB(self, data):
		self.openDB()
		cursor.execute("INSERT INTO user (id_user, id_level, nama, username, password, tanggal_lahir, jenis_kelamin, no_telp, dusun, id_desa, id_kecamatan, id_kabupaten, uker) VALUES( '%s','%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % data)
		db.commit()
		self.closeDB()

	def getuserDB(self, username):
		self.openDB()
		cursor.execute("SELECT * FROM user where $_SESSION['username']=$username" % username)
		db.commit()
		self.closeDB()

