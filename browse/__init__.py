from robobrowser import RoboBrowser
import json
import re	
def show(RegNo, bdate):
	url = "http://websismit.manipal.edu/websis/control/clearSession"
	br = RoboBrowser(history=True,parser='html.parser')
	try:
		br.open(url)
	except Exception as e:
		return {"status":False, "Description": "Not Available"}
	form = br.get_form(method = 'post')
	if form is not None:
		form
		form['idValue'].value = RegNo
		form['birthDate_i18n'].value = bdate
		form['birthDate'].value = bdate
		br.submit_form(form)
		if br.parsed.find("table") is None:
			return {'status':False,'Description':"Invalid login"}
		details = getDetails(br.parsed)
		br.open('http://websismit.manipal.edu/websis/control/ListCTPEnrollment')
		scores = getScores(br.parsed)
		attendence = getAttendence(br.parsed)
		gpa = getGPA(br.parsed)
		data = {}
		details['Branch'] = gpa.keys()[-1]
		data['Scores'] = scores
		data['Attendance'] = attendence
		data['GPA'] = gpa
		data['User Data'] = details
		return data
	else:
		return {"status":False, "Description": "Not Available2"}
def getAttendence(html):
	tables =  html.find("table", attrs={"id":"ListAttendanceSummary_table"})
	headings = [th.get_text().strip('\n').strip(' ').title() for th in tables.find("tr").find_all("th")]
	headings.pop()
	datasets = []
	for row in tables.find_all("tr")[1:]:
		dataset = zip(headings, (td.get_text().title() for td in row.find_all("td")))
		a=[]
		for td in row.find_all("td"):
			text = td.get_text().strip('\n').strip(' ').title()
			a.append(text) 
		a.pop()
		datasets.append(a)
	final_list = []
	for i in range(0,len(datasets)):
		temp = {}
		for j in range(0,len(headings)):
			temp[headings[j]] = datasets[i][j]
		f = temp
		final_list.append(f)
	return final_list
def getScores(html):
	tableset =  html.find_all("table", attrs={"id":"ListAssessmentScores_table"})
	tot_set = {}
	ia = 0
	divset =  html.find_all("div", attrs={"class":"screenlet"})
	y = []
	for i in divset:
		l =i.find("li", attrs={"class":"h3"})
		for x in l:
			if 'Internal' in x:
				y.append(int(re.search(r'\d+', x).group()))
	print str(y)
	for tables in tableset:
		headings = [th.get_text().strip('\n').strip(' ').title() for th in tables.find("tr").find_all("th")]
		datasets = []
		for row in tables.find_all("tr")[1:]:
			dataset = zip(headings, (td.get_text() for td in row.find_all("td")))
			a=[]
			for td in row.find_all("td"):
				text = td.get_text().strip('\n').strip(' ').title()
				a.append(text) 
			datasets.append(a)
		final_list = []
		for i in range(0,len(datasets)):
			temp = {}
			for j in range(0,len(headings)):
				temp[headings[j]] = datasets[i][j]
			f =temp
			final_list.append(f)
			text = 'Internal Assesment '+str(y[ia])
			print str(y[ia])
		tot_set[text] = final_list
		ia+=1
	return tot_set
def getScores2():
	url = "http://websismit.manipal.edu/websis/control/clearSession"
	br = RoboBrowser(history=True,parser='html.parser')
	br.open(url)
	form = br.get_form(method = 'post')
	if form is not None:
		form
		form['idValue'].value = '140953332'
		form['birthDate_i18n'].value = '1995-11-06'
		form['birthDate'].value = '1995-11-06'
		br.submit_form(form)
		if br.parsed.find("table") is None:
			return {'status':False,'Description':"Invalid login"}
		details = getDetails(br.parsed)
		br.open('http://websismit.manipal.edu/websis/control/ListCTPEnrollment')
	divset =  br.parsed.find_all("div", attrs={"class":"screenlet"})
	y = []
	for i in divset:
		l =i.find("li", attrs={"class":"h3"})
		for x in l:
			if 'Internal' in x:
				y.append(int(re.search(r'\d+', x).group()))
	print str(y)
def getGPA(html):
	tables =  html.find("table", attrs={"id":"ProgramAdmissionItemSummary_table"})
	gpa = []
	headings =[]
	for row in tables.find_all("tr")[0:]:
		i=0
		for dat in row.find_all("td"):
			text = dat.get_text().strip('\n').strip(' ')
			i+=1
			if i%2 == 0:
				gpa.append(text)
			else:
				headings.append(text.title())
	final_list = dict(zip(headings,gpa))
	return final_list

def getDetails(html):
	name = html.find('span', attrs = {'id':"cc_ProfileTitle_name"}).get_text().strip('\n').strip(' ').title()
	regno = html.find('span', attrs = {'id':"cc_ProfileTitle_idValue"}).get_text().strip('\n').strip(' ').title()
	return {'Name':name,'Registration Number':regno}