from flask import *
import psutil
from robobrowser import RoboBrowser
import browse
import json
app = Flask(__name__)

@app.route('/show', methods = ['POST'])
def show():
	reg = request.form['regno']
	bdate = request.form['bdate']
	a = browse.show(reg,bdate)
	return json.dumps(a)

@app.route('/getAttendence', methods = ['POST'])
def attendence():
	reg = request.form['regno']
	bdate = request.form['bdate']
	a = browse.getAttendence(browse.getHTML(reg,bdate))
	return json.dumps({'Attendence':a})

@app.route('/getScores', methods = ['POST'])
def marks():
	reg = request.form['regno']
	bdate = request.form['bdate']
	a = browse.getScores(browse.getHTML(reg,bdate))
	return json.dumps({'Scores':a})

@app.route('/getDetails', methods = ['POST'])
def details():
	reg = request.form['regno']
	bdate = request.form['bdate']
	a = browse.getHTML2(reg,bdate)
	return json.dumps(a)

@app.route('/getGrades', methods = ['POST'])
def grades():
	reg = request.form['regno']
	bdate = request.form['bdate']
	a = browse.getGrades(browse.getHTML(reg,bdate))
	return json.dumps({'Attendence':a})
if __name__=='__main__':
	app.run(debug = True)