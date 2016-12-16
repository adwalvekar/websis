from flask import *
import psutil
from robobrowser import RoboBrowser
import browse
import json
app = Flask(__name__)
@app.route('/show', methods = ['POST','GET'])
def show():
	reg = request.form['regno']
	bdate = request.form['bdate']
	a = browse.show(reg,bdate)
	return json.dumps(a)
if __name__=='__main__':
	app.run(debug = True)