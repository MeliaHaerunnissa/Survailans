import pymysql
import config

db = cursor = None

class MJumantik:
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

	def openDB(self):
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
		m = "SELECT u.id_user, l.level, u.nama, u.username, u.password, u.tanggal_lahir, u.jenis_kelamin, u.no_telp, u.dusun, d.desa, k.kecamatan, kab.kabupaten, u.uker \
		FROM user u, level l, desa d, kecamatan k, kabupaten kab \
		where u.id_level=l.id_level and u.id_level='3' and u.id_desa=d.id_desa and u.id_kecamatan=k.id_kecamatan and u.id_kabupaten=kab.id_kabupaten order by u.id_user DESC "
		cursor.execute(m)
		container = []
		for id_user, level, nama, username, password, tanggal_lahir, jenis_kelamin, no_telp, dusun, desa,kecamatan, kabupaten, uker in cursor.fetchall():
			container.append((id_user, level, nama, username, password, tanggal_lahir, jenis_kelamin, no_telp, dusun, desa,kecamatan, kabupaten, uker))
		self.closeDB()
		return container

	def insertDB(self, data):
		self.openDB()
		cursor.execute("INSERT INTO user (id_user, level, nama, username, password, tanggal_lahir, jenis_kelamin, no_telp, dusun, desa,kecamatan, kabupaten, uker) VALUES('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % data)
		db.commit()
		self.closeDB()
		
	def getDBbyNo(self, id_user):
		self.openDB()
		cursor.execute("SELECT * FROM user WHERE id_user='%s'" % id_user)
		data = cursor.fetchone()
		return data

	def updateDB(self, data):
		self.openDB()
		cursor.execute("UPDATE user SET id_level='%s', nama='%s', username= '%s', password='%s', tanggal_lahir= '%s',jenis_kelamin='%s',no_telp='%s', dusun='%s', id_desa='%s', id_kecamatan='%s', uker='%s' WHERE id_user='%s' " % data)
		db.commit()
		self.closeDB()

	def deleteDB(self, id_user):
		self.openDB()
		cursor.execute("DELETE FROM user WHERE id_user=%s" % id_user)
		db.commit()
		self.closeDB()