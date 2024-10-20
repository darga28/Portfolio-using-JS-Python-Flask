from flask import Flask, make_response, render_template,request,redirect,send_file
from datetime import datetime
import pytz
# it will get the time zone of the specified location
import csv

app=Flask(__name__)
print(app)


@app.route('/') 
def blog():
	return render_template('index.html')


def write_to_data(d):
	with open('database.txt',newline='',mode='a') as database:
		n=d["name"]
		e=d["email"]
		s=d["subject"]
		m=d["message"]
		file=database.write(f'\n{n},{e},{s},{m}')


def write_to_csv(d):
	with open('database_csv.csv',mode='a') as database:
		n=d["name"]
		e=d["email"]
		s=d["subject"]
		m=d["message"]
		datetime=d['datetime']
		csv_writer_object=csv.writer(database,delimiter=',',quotechar='"',quoting=csv.QUOTE_MINIMAL)  #newline will always append to the database in new line not in same line
		csv_writer_object.writerow([n,e,s,m,datetime])



@app.route('/submit',methods=['POST','GET'])
def submit():
	# error=None
	if request.method=='POST':
		try:
			data=request.form.to_dict()
			#print(data["email"])
			IST = pytz.timezone('Asia/Kolkata')
			datetime_ist = datetime.now(IST)
			data["datetime"]=str(datetime_ist)
			write_to_csv(data)
			return render_template('/thankyou.html',name=data["name"])
		except:
			return 'Not saved to Database(CSV File)'
	else:
	 	return 'Invalid username/password'
	

@app.route('/<string:page_name>') 
def about(page_name):
	if(len(page_name)>0):
		return render_template("localhost/"+page_name)
	
@app.route('/download')
def download():
	path="DARGA ASIF ALI Resume.pdf"
	return send_file(path,as_attachment=True)


app.config['TEMPLATES_AUTO_RELOAD'] = True
if __name__ == '__main__':
	app.run(debug=True)