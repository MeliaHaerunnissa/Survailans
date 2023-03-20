from flask import Flask, render_template, request, redirect, url_for
from models_jumantik import MJumantik

app = Flask(__name__)

@app.route('/')
def index():
	model = Jumantik()
	container = []
	container = model.selectDB()
	return render_template('jumantik.html', container=container)

@application.route('/insert_data_jumantik', methods=['GET', 'POST'])
def insert_data_jumantik():
	if request.method == 'POST':
		id_jumantik = request.form['id_jumantik']
		nama = request.form['nama']
		alamat = request.form['alamat']
		no_telp = request.form['no_telp']
		jenis_kelamin = request.form['jenis_kelamin']
		area_kerja = request.form['area_kerja']
		data = (id_jumantik,nama, alamat, no_telp, jenis_kelamin, area_kerja)
		models = MJumantik()
		models.insertDB(data)
		return redirect(url_for('insert_data_jumantik'))
	else:
		return render_template('insert_form_survei_jumantik.html')

@application.route('/update_jumantik/<no>')
def update_jumantik(no):
	models = MJumantik()
	data = models.getDBbyNo(no)
	return render_template('update_form_jumantik.html', data= data)

@application.route('/update_prosess_jumantik', methods=['GET', 'POST'])
def update_proses_jumantik():
	no = request.form['no']
	id_jumantik = request.form['id_jumantik']
	nama = request.form['nama']
	alamat = request.form['alamat']
	no_telp = request.form['no_telp']
	jenis_kelamin = request.form['jenis_kelamin']
	area_kerja = request.form['area_kerja']
	data = (id_jumantik, nama, alamat, no_telp, jenis_kelamin, area_kerja, no)
	models = MJumantik()
	models.updateDB(data)
	return redirect(url_for('datajumantik'))

@application.route('/delete_jumantik/<no>')
def delete_jumantik(no):
	models = MJumantik()
	models.deleteDB(no)
	return redirect(url_for('datajumantik'))

if __name__ == '__main__':
	application.run(debug=True)