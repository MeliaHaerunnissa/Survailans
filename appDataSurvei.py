from flask import Flask, render_template, request, redirect, url_for
from models_data_survei import MData_Survei

aplication = Flaks(__name__)

@aplication.route('/')
def index():
	model = Jumantik()
	container = []
	container = model.selectDB()
	return render_template('jumantik.html', container=container)

@application.route('/data_survei_jumantik')
def data_survei_jumantik():
	models = MData_Survei()
	container = []
	container = models.selectDB()
	return render_template('form_survei_jumantik.html', container=container)

@application.route('/insert_data_survei_jumantik', methods=['GET', 'POST'])
def insert_data_survei_jumantik():
	if request.method == 'POST':
		tanggal_survei = request.form['tanggal_survei']
		nama_jumantik = request.form['nama_jumantik']
		no_kk = request.form['no_kk']
		nama_kepala_keluarga = request.form['nama_kepala_keluarga']
		no_telp = request.form['no_telp']
		alamat = request.form['alamat']
		jumlah_tpa = request.form ['jumlah_tpa']
		status = request.form['status']
		data = (tanggal_survei, nama_jumantik, no_kk, nama_kepala_keluarga, no_telp, alamat, jumlah_tpa, status)
		models = MData_Survei()
		models.insertDB(data)
		return redirect(url_for('data_survei_jumantik'))
	else:
		return render_template('insert_form_survei_jumantik.html')

@application.route('/update_form_survei/<no>')
def update_form_survei(no):
	models = MData_Survei()
	data = models.get_surveiDBbyNo(no)
	return render_template('update_form_survei_jumantik.html', data= data)

@application.route('/update_prosess_survei', methods=['GET', 'POST'])
def update_prosess_survei():
	no = request.form['no']
	tanggal_survei = request.form['tanggal_survei']
	nama_jumantik = request.form['nama_jumantik']
	no_kk = request.form['no_kk']
	nama_kepala_keluarga = request.form['nama_kepala_keluarga']
	no_telp = request.form['no_telp']
	alamat = request.form['alamat']
	jumlah_tpa = request.form['jumlah_tpa']
	status = request.form['status']
	data = (tanggal_survei, nama_jumantik, no_kk, nama_kepala_keluarga, no_telp, alamat, jumlah_tpa, status, no)
	models = MData_Survei()
	models.update_surveiDB(data)
	return redirect(url_for('data_survei_jumantik'))

@application.route('/delete_survei/<no>')
def delete_survei(no):
	models = MData_Survei()
	models.deleteDB(no)
	return redirect(url_for('data_survei_jumantik'))