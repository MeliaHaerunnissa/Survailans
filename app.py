import pymysql
from flask import Flask, render_template, jsonify, json, session, \
request, redirect, url_for
from wtforms import Form, validators
from models import Survei
from models_buat_akun import MSimpanUser
from models_pasien_dbd import MPasien_Dbd
from models_data_survei import MData_Survei
from models_jumantik import MJumantik
#from models_uploadfile import UploadFile
#from models_uploadfile import UploadFile
from werkzeug import secure_filename
from datetime import datetime
import time
import os

application = Flask(__name__)
application.config['SECRET_KEY'] = '1234567890!@#$%^&*()'
application.config['UPLOAD_FOLDER'] = os.path.realpath('.') + \
	'/Fasilitas kesehatan 1.3/static/uploads'
#Satuan Byte
application.config['MAX_CONTENT_PATH'] = 10000000

@application.errorhandler(404)
def notfound(error):
    return render_template("404.html")

@application.route('/')
def index():
	if 'username' in session and session['id_level'] == '1':
		username = session['username']
		id_level = session['id_level']
		return render_template('index_faskes.html', username = username, id_level=id_level)
	elif 'username' in session and session['id_level'] == '2':
		username = session['username']
		id_level = session['id_level']
		return render_template('index_kelurahan.html', username = username, id_level=id_level)
	elif 'username' in session and session['id_level'] == '3':
		username = session['username']
		id_level = session['id_level']
		return render_template('index_jumantik.html', username = username, id_level=id_level)
	return redirect(url_for('login'))

@application.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        pengguna = Survei(username, password)
        if pengguna.authenticate():
            session['username'] = username
            session['id_level'] = pengguna.accountType()
            return redirect(url_for('index'))
        msg = 'Salah!'
        return render_template('login.html', msg = msg)
    return render_template('login.html')

@application.route('/logout')
def logout():
    session.pop('username', '')
    return redirect(url_for('index'))

@application.route('/buat_akun', methods = ['GET', 'POST'])
def buat_akun():
	if request.method == 'POST':
		id_user = request.form['id_user']
		id_level = request.form['id_level']
		username = request.form['username']
		password = request.form['password']
		nama = request.form['nama']
		tanggal_lahir = request.form['tanggal_lahir']
		jenis_kelamin = request.form['jenis_kelamin']
		no_telp = request.form['no_telp']
		dusun = request.form['dusun']
		id_desa = request.form['id_desa']
		id_kecamatan = request.form['id_kecamatan']
		id_kabupaten = request.form['id_kabupaten']
		uker = request.form['uker']
		data = (id_user, id_level, nama, username, password, tanggal_lahir, jenis_kelamin, no_telp, dusun, id_desa, id_kecamatan, id_kabupaten, uker)
		models = MSimpanUser()
		models.insertDB(data)
		return redirect(url_for('login'))
	else:
		return render_template('buat_akun.html')

#<------------------------------------------HOME FASKES-------------------------------------->
@application.route('/home_faskes')
def home_faskes():
    return render_template("index_faskes.html")

#<------------------------------------------HOME FASKES-------------------------------------->
@application.route('/home_kelurahan')
def home_kelurahan():
    return render_template("index_kelurahan.html")
    #<------------------------------------------HOME JUMANTIK-------------------------------------->
@application.route('/home_jumantik')
def home_jumantik():
    return render_template("index_jumantik.html")

#<------------------------------------------DATA SURVEI FASKES-------------------------------------->
@application.route('/datasurveifaskes')
def datasurveifaskes():
	models = MData_Survei()
	container = []
	container = models.selectDB()
	return render_template('form_survei_faskes.html',container=container)

#<------------------------------------------DATA SURVEI KELURAHAN-------------------------------------->
@application.route('/datasurveikelurahan')
def datasurveikelurahan():
	models = MData_Survei()
	container = []
	container = models.selectDB()
	return render_template('form_survei_kelurahan.html',container=container)
#<------------------------------------------FORM PASIEN DBD-------------------------------------->
@application.route('/datapasien')
def datapasien():
	models = MPasien_Dbd()
	container = []
	container = models.selectDB()
	return render_template('pasien_dbd.html',container=container)

@application.route('/insert_data_pasien', methods=['GET', 'POST'])
def insert_data_pasien():
	if request.method == 'POST':
		no_ktp = request.form['no_ktp']
		nama_pasien = request.form['nama_pasien']
		dusun = request.form['dusun']
		id_desa = request.form['id_desa']
		id_kecamatan = request.form['id_kecamatan']
		id_kabupaten = request.form['id_kabupaten']
		tempat_lahir = request.form['tempat_lahir']
		tanggal_lahir = request.form['tanggal_lahir']
		jenis_kelamin = request.form['jenis_kelamin']
		pekerjaan = request.form['pekerjaan']
		date_time = datetime.now()
		data = (date_time, no_ktp, nama_pasien, dusun, id_desa, id_kecamatan, id_kabupaten, tempat_lahir, tanggal_lahir, jenis_kelamin, pekerjaan)
		models = MPasien_Dbd()
		models.insertDB(data)
		return redirect(url_for('datapasien'))
	else:
		return render_template('insert_form_pasien.html')

@application.route('/update/<id_pasien>')
def update(id_pasien):
	models = MPasien_Dbd()
	data = models.getDBbyNo(id_pasien)
	return render_template('update_form_pasien.html', data= data)

@application.route('/update_prosess', methods=['GET', 'POST'])
def update_prosess():
	id_pasien = request.form['id_pasien']
	tanggal_masuk = request.form['tanggal_masuk']
	no_ktp = request.form['no_ktp']
	nama_pasien = request.form['nama_pasien']
	dusun = request.form['dusun']
	id_desa = request.form['id_desa']
	id_kecamatan = request.form['id_kecamatan']
	id_kabupaten = request.form['id_kabupaten']
	tempat_lahir = request.form['tempat_lahir']
	tanggal_lahir = request.form['tanggal_lahir']
	jenis_kelamin = request.form['jenis_kelamin']
	pekerjaan = request.form['pekerjaan']
	data = ( tanggal_masuk, no_ktp, nama_pasien, dusun, id_desa, id_kecamatan, id_kabupaten, tempat_lahir, tanggal_lahir, jenis_kelamin, pekerjaan, id_pasien)
	models = MPasien_Dbd()
	models.updateDB(data)
	return redirect(url_for('datapasien'))

@application.route('/delete/<id_pasien>')
def delete(id_pasien):
	models = MPasien_Dbd()
	models.deleteDB(id_pasien)
	return redirect(url_for('datapasien'))

#<------------------------------------- FORM SURVEI JUMANTIK ---------------------->
@application.route('/data_survei_jumantik')
def data_survei_jumantik():
	models = MData_Survei()
	container = []
	container = models.selectDB()
	return render_template('form_survei_jumantik.html', container=container)

@application.route('/insert_data_survei_jumantik', methods=['GET', 'POST'])
def insert_data_survei_jumantik():
	if request.method == 'POST':
		no = request.form['no']
		id_jumantik = request.form['id_jumantik']
		no_kk = request.form['no_kk']
		nama_kepala_keluarga = request.form['nama_kepala_keluarga']
		no_telp = request.form['no_telp']
		dusun = request.form['dusun']
		id_desa = request.form['id_desa']
		id_kecamatan = request.form['id_kecamatan']
		bak_mandi = request.form['bak_mandi']
		drum = request.form['drum']
		kaleng_bekas = request.form['kaleng_bekas']
		tempayan = request.form['tempayan']
		lain_lain = request.form['lain_lain']
		status = request.form['status']
		jumlah_tpa = request.form ['jumlah_tpa']
		date_time = datetime.now()
		data = (no, date_time, id_jumantik, no_kk, nama_kepala_keluarga, no_telp, dusun, id_desa, id_kecamatan, bak_mandi, drum, kaleng_bekas, tempayan, lain_lain, status, jumlah_tpa)
		models = MData_Survei()
		models.insertDB(data)
		return redirect(url_for('data_survei_jumantik'))
	else:
		return render_template('insert_form_survei.html')

@application.route('/update_form_survei/<no>')
def update_form_survei(no):
	models = MData_Survei()
	data = models.get_surveiDBbyNo(no)
	return render_template('update_form_survei.html', data= data)

@application.route('/update_prosess_survei', methods=['GET', 'POST'])
def update_prosess_survei():
	no = request.form['no']
	tanggal_survei = request.form['tanggal_survei']
	id_jumantik = request.form['id_jumantik']
	no_kk = request.form['no_kk']
	nama_kepala_keluarga = request.form['nama_kepala_keluarga']
	no_telp = request.form['no_telp']
	dusun = request.form['dusun']
	id_desa = request.form['id_desa']
	id_kecamatan = request.form['id_kecamatan']
	bak_mandi = request.form['bak_mandi']
	drum = request.form['drum']
	kaleng_bekas = request.form['kaleng_bekas']
	tempayan = request.form['tempayan']
	lain_lain = request.form['lain_lain']
	status = request.form['status']
	jumlah_tpa = request.form ['jumlah_tpa']
	data = (tanggal_survei, id_jumantik, no_kk, nama_kepala_keluarga, no_telp, dusun, id_desa, id_kecamatan, bak_mandi, drum, kaleng_bekas, tempayan, lain_lain, status, jumlah_tpa, no)
	models = MData_Survei()
	models.update_surveiDB(data)
	return redirect(url_for('data_survei_jumantik'))

@application.route('/delete_survei/<no>')
def delete_survei(no):
	models = MData_Survei()
	models.deleteDB(no)
	return redirect(url_for('data_survei_jumantik'))

#<--------------------------------DATA FILE SURVEI JUMANTIK-------------------------------->

#<------------------------------------FORM DATA JUMANTIK----------------------------------->
@application.route('/datajumantik')
def datajumantik():
	models = MJumantik()
	container = []
	container = models.selectDB()
	return render_template('jumantik.html',container=container)

@application.route('/insert_data_jumantik', methods=['GET', 'POST'])
def insert_data_jumantik():
	if request.method == 'POST':
		id_user = request.form['id_user']
		id_level = request.form['id_level']
		username = request.form['username']
		password = request.form['password']
		nama = request.form['nama']
		tanggal_lahir = request.form['tanggal_lahir']
		jenis_kelamin = request.form['jenis_kelamin']
		no_telp = request.form['no_telp']
		dusun = request.form['dusun']
		id_desa = request.form['id_desa']
		id_kecamatan = request.form['id_kecamatan']
		id_kabupaten = request.form['id_kabupaten']
		uker = request.form['uker']
		data = (id_user, id_level, nama, username, password, tanggal_lahir, jenis_kelamin, no_telp, dusun, id_desa, id_kecamatan, id_kabupaten, uker)
		models = MSimpanUser()
		models.insertDB(data)
		return redirect(url_for('datajumantik'))
	else:
		return render_template('insert_data_jumantik.html')

@application.route('/update_jumantik/<id_user>')
def update_jumantik(id_user):
	models = MJumantik()
	data = models.getDBbyNo(id_user)
	return render_template('update_jumantik.html', data= data)

@application.route('/update_prosess_jumantik', methods=['GET', 'POST'])
def update_prosess_jumantik():
	id_user = request.form['id_user']
	id_level = request.form['id_level']
	username = request.form['username']
	password = request.form['password']
	nama = request.form['nama']
	tanggal_lahir = request.form['tanggal_lahir']
	jenis_kelamin = request.form['jenis_kelamin']
	no_telp = request.form['no_telp']
	dusun = request.form['dusun']
	id_desa = request.form['id_desa']
	id_kecamatan = request.form['id_kecamatan']
	id_kabupaten = request.form['id_kabupaten']
	uker = request.form['uker']
	data = (id_level, nama, username, password, tanggal_lahir, jenis_kelamin, no_telp, dusun, id_desa, id_kecamatan, id_kabupaten, uker, id_user)
	models = MJumantik()
	models.updateDB(data)
	return redirect(url_for('datajumantik'))

@application.route('/delete_jumantik/<id_user>')
def delete_jumantik(id_user):
	models = MJumantik()
	models.deleteDB(id_user)
	return redirect(url_for('datajumantik'))
#<------------------------------------CETAK DATA SURVEI----------------------------------->
@application.route('/cetak_data_survei', methods=['GET'])
def cetak_data_survei():
	if request.method=='GET':
		models = MData_Survei()
		container = []
		container = models.selectDB()
		date_time = datetime.now()
		tanggal = date_time.strftime("%d %b %Y")
		return render_template('cetak_data_survei.html', container=container, tanggal=tanggal)
#<------------------------------------GRAFIK----------------------------------->
@application.route('/grafik')
def grafik():
	datapasien = MPasien_Dbd()
	alamat = MPasien_Dbd()
	datasurvei = MData_Survei()
	data = datapasien.grafikjumlahpasienjk()
	data1 = datasurvei.grafikjumlahdatasurvei()
	data2 = alamat.grafik_alamat_pasienjk()
	no = []
	jenis_kelamin= []
	tanggal_survei = []
	status = []
	tanggal_masuk = []
	desa = []
	for i in data:
		no.append(i[0])
		jenis_kelamin.append(i[1])
	for i in data1:
		tanggal_survei.append(i[0])
		status.append(i[1])
	for i in data2:
		tanggal_masuk.append(i[0])
		desa.append(i[1])

	return render_template('dashboard.html', datapasien= json.dumps(data), no= json.dumps(no), jenis_kelamin= json.dumps(jenis_kelamin), datasurvei=json.dumps(data1), tanggal_survei=json.dumps(tanggal_survei),status=json.dumps(status),alamat=json.dumps(data2), tanggal_masuk= json.dumps(tanggal_masuk),desa=json.dumps(desa))

#<------------------------------------GRAFIK----------------------------------->
@application.route('/grafikkelurahan')
def grafikkelurahan():
	pasien = MPasien_Dbd()
	grafik1= pasien.grafik_alamat_pasienjk()
	datasurvei = MData_Survei()
	data1 = datasurvei.grafikjumlahdatasurvei()
	tanggal_masuk = []
	desa = []
	tanggal_survei = []
	status = []
	for i in grafik1:
		tanggal_masuk.append(i[0])
		desa.append(i[1])
	for i in data1:
		tanggal_survei.append(i[0])
		status.append(i[1])
	
	return render_template('dashboard_kelurahan.html', pasien=json.dumps(grafik1), tanggal_masuk= json.dumps(tanggal_masuk),desa=json.dumps(desa),datasurvei=json.dumps(data1), tanggal_survei=json.dumps(tanggal_survei),status=json.dumps(status))
#<------------------------------------FORM DATA JUMANTIK----------------------------------->

if __name__ == '__main__':
	application.run(debug=True)