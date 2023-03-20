import pymysql
import config

db = cursor = None

class MData_Survei:
	def __init__ (self, no=None, tanggal_survei=None, id_jumantik=None, no_kk=None, nama_kepala_keluarga=None, 
		no_telp=None, dusun=None, id_desa=None, id_kecamatan=None, bak_mandi=None,drum=None, kaleng_bekas=None,tempayan=None, lain_lain=None, status=None, jumlah_tpa=None):
		self.no = no
		self.tanggal_survei = tanggal_survei
		self.id_jumantik = id_jumantik
		self.no_kk = no_kk
		self.nama_kepala_keluarga = nama_kepala_keluarga
		self.no_telp = no_telp
		self.dusun = dusun
		self.id_desa = id_desa
		self.id_kecamatan = id_kecamatan
		self.bak_mandi = bak_mandi
		self.drum = drum
		self.kaleng_bekas =  kaleng_bekas
		self.tempayan = tempayan
		self.lain_lain = lain_lain
		self.status = status
		self.jumlah_tpa = jumlah_tpa

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
		cursor.execute("SELECT ds.no, ds.tanggal_survei, j.nama, ds.no_kk, ds.nama_kepala_keluarga, ds.no_telp, ds.dusun, d.desa, k.kecamatan, ds.bak_mandi, ds.drum, ds.kaleng_bekas, ds.tempayan, ds.lain_lain, ds.status, ds.jumlah_tpa\
			from data_survei ds, desa d, kecamatan k, jumantik j\
			where ds.id_desa=d.id_desa and ds.id_kecamatan=k.id_kecamatan and ds.id_jumantik=j.id_jumantik\
			order by ds.no DESC")
		container = []
		for no, tanggal_survei, nama, no_kk, nama_kepala_keluarga, no_telp, dusun, id_desa, id_kecamatan, bak_mandi, drum, kaleng_bekas,tempayan, lain_lain, status, jumlah_tpa in cursor.fetchall():
			container.append((no, tanggal_survei, nama, no_kk,nama_kepala_keluarga, no_telp, dusun, id_desa, id_kecamatan, bak_mandi, drum, kaleng_bekas,tempayan, lain_lain, status, jumlah_tpa))
		self.closeDB()
		return container

	def insertDB(self, data):
		self.openDB()
		cursor.execute("INSERT INTO data_survei (no, tanggal_survei, id_jumantik, no_kk, nama_kepala_keluarga, no_telp, dusun, id_desa, id_kecamatan, bak_mandi, drum, kaleng_bekas, tempayan, lain_lain, status, jumlah_tpa) VALUES('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % data)
		db.commit()
		self.closeDB()

	def get_surveiDBbyNo(self, no):
		self.openDB()
		cursor.execute("SELECT * FROM data_survei WHERE no='%s'" % no)
		data = cursor.fetchone()
		return data

	def update_surveiDB(self, data):
		self.openDB()
		cursor.execute("UPDATE data_survei SET tanggal_survei='%s', id_jumantik='%s', no_kk='%s', nama_kepala_keluarga='%s', no_telp='%s', dusun='%s', id_desa='%s', id_kecamatan='%s', bak_mandi='%s', drum='%s', kaleng_bekas='%s',tempayan='%s', lain_lain='%s', status='%s', jumlah_tpa='%s' WHERE no=%s" % data)
		db.commit()
		self.closeDB()

	def deleteDB(self, no):
		self.openDB()
		cursor.execute("DELETE FROM data_survei WHERE no=%s" % no)
		db.commit()
		self.closeDB()

	def grafikjumlahdatasurvei(self):
		self.openDB()
		q = "SELECT count(tanggal_survei), status from data_survei group by status"
		container = []
		cursor.execute(q)
		for  tanggal_survei, status in cursor.fetchall():
			container.append((tanggal_survei, status))
		self.closeDB()
		return container