import pymysql
import config

db = cursor = None

class MPasien_Dbd:
    def __init__ (self, no=None, tanggal_masuk=None, no_ktp=None, nama_pasien=None, dusun=None, id_desa=None, id_kecamatan=None, id_kabupaten= None, 
        tempat_lahir=None, tanggal_lahir=None, jenis_kelamin=None, pekerjaan=None):
        self.no = no
        self.tanggal_masuk = tanggal_masuk
        self.no_ktp= no_ktp
        self.nama_pasien = nama_pasien
        self.dusun = dusun
        self.id_desa = id_desa
        self.id_kecamatan = id_kecamatan
        self.id_kabupaten = id_kabupaten
        self.tempat_lahir = tempat_lahir
        self.tanggal_lahir = tanggal_lahir
        self.jenis_kelamin = jenis_kelamin
        self.pekerjaan = pekerjaan

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
        cursor.execute("SELECT p.id_pasien, p.tanggal_masuk, p.no_ktp, p.nama_pasien, p.dusun, d.desa, k.kecamatan, kab.kabupaten, p.tempat_lahir, p.tanggal_lahir, p.jenis_kelamin, p.pekerjaan\
            from pasien_dbd p, desa d, kecamatan k, kabupaten kab\
            where p.id_desa=d.id_desa and p.id_kecamatan=k.id_kecamatan and kab.id_kabupaten=p.id_kabupaten\
            order by id_pasien desc")
        container = []
        for  id_pasien, tanggal_masuk, no_ktp, nama_pasien, dusun, desa, kecamatan, kabupaten, tempat_lahir, tanggal_lahir, jenis_kelamin, pekerjaan in cursor.fetchall():
            container.append(( id_pasien, tanggal_masuk, no_ktp, nama_pasien, dusun, desa, kecamatan, kabupaten, tempat_lahir, tanggal_lahir, jenis_kelamin, pekerjaan))
        self.closeDB()
        return container

    def insertDB(self, data):
        self.openDB()
        cursor.execute("INSERT INTO pasien_dbd (id_pasien, tanggal_masuk, no_ktp, nama_pasien, dusun, id_desa, id_kecamatan, id_kabupaten, tempat_lahir, tanggal_lahir, jenis_kelamin, pekerjaan) VALUES('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s', '%s')" % data)
        db.commit()
        self.closeDB()
        
    def getDBbyNo(self, id_pasien):
        self.openDB()
        cursor.execute("SELECT * FROM pasien_dbd WHERE id_pasien='%s'" % id_pasien)
        data = cursor.fetchone()
        return data

    def updateDB(self, data):
        self.openDB()
        cursor.execute("UPDATE pasien_dbd SET tanggal_masuk='%s', no_ktp='%s', nama_pasien='%s', dusun='%s', id_desa='%s', id_kecamatan='%s', id_kabupaten='%s', tempat_lahir='%s', tanggal_lahir='%s', jenis_kelamin='%s', pekerjaan='%s' WHERE no=%s" % data)
        db.commit()
        self.closeDB()

    def deleteDB(self, id_pasien):
        self.openDB()
        cursor.execute("DELETE FROM pasien_dbd WHERE id_pasien=%s" % id_pasien)
        db.commit()
        self.closeDB()
    
    def grafikjumlahpasienjk(self):
        self.openDB()
        q= ("SELECT count(id_pasien), jenis_kelamin from pasien_dbd group by jenis_kelamin")
        container = []
        cursor.execute(q)
        for id_pasien, jenis_kelamin in cursor.fetchall():
            container.append((id_pasien,jenis_kelamin))
        self.closeDB()
        return container

    def grafik_alamat_pasienjk(self):
        self.openDB()
        q= ("SELECT count(p.tanggal_masuk), d.desa from pasien_dbd p, desa d WHERE p.id_desa=d.id_desa group by d.desa")
        container = []
        cursor.execute(q)
        for tanggal_masuk, desa in cursor.fetchall():
            container.append((tanggal_masuk,desa))
        self.closeDB()
        return container