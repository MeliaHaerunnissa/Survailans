from flask import Flask, render_template, request, redirect, url_for
from models_pasien_dbd import MPasien_Dbd

application = Flask(__name__)

@application.route('/')
def index():
	model = surveilans()
	container = []
	container = model.selectDB()
	return render_template('pasien_dbd.html', container=container)

@application.route('/insert_data_pasien', methods=['GET', 'POST'])
def insert_data_pasien():
	if request.method == 'POST':
		tanggal_masuk = request.form['tanggal_masuk']
		no_ktp = request.form['no_ktp']
		nama_pasien = request.form['nama_pasien']
		alamat = request.form['alamat']
		tempat_tanggal_lahir = request.form['tempat_tanggal_lahir']
		jenis_kelamin = request.form['jenis_kelamin']
		pekerjaan = request.form['pekerjaan']
		data = (tanggal_masuk, no_ktp, nama_pasien, alamat, tempat_tanggal_lahir, jenis_kelamin, pekerjaan)
		models = MPasien_Dbd()
		models.insertDB(data)
		return redirect(url_for('datapasien'))
	else:
		return render_template('insert_form_pasien.html')

@application.route('/update/<no>')
def update(no):
	models = MPasien_Dbd()
	data = models.getDBbyNo(no)
	return render_template('update_form_pasien.html', data= data)

@application.route('/update_prosess', methods=['GET', 'POST'])
def update_prosess():
	no = request.form['no']
	tanggal_masuk = request.form['tanggal_masuk']
	no_ktp = request.form['no_ktp']
	nama_pasien = request.form['nama_pasien']
	alamat = request.form['alamat']
	tempat_tanggal_lahir = request.form['tempat_tanggal_lahir']
	jenis_kelamin = request.form['jenis_kelamin']
	pekerjaan = request.form['pekerjaan']
	data = (tanggal_masuk, no_ktp, nama_pasien, alamat, tempat_tanggal_lahir, jenis_kelamin, pekerjaan, no)
	models = MPasien_Dbd()
	models.updateDB(data)
	return redirect(url_for('datapasien'))

@application.route('/delete/<no>')
def delete(no):
	models = MPasien_Dbd()
	models.deleteDB(no)
	return redirect(url_for('datapasien'))