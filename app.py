from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase
import random

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'

firebaseConfig = {
	"apiKey": "AIzaSyA-4dzHC9GHjDugpy7BhE2cnfVGboMsQs4",
	"authDomain": "individual-project-ec272.firebaseapp.com",
	"projectId": "individual-project-ec272",
	"storageBucket": "individual-project-ec272.appspot.com",
	"messagingSenderId": "1034924739805",
	"appId": "1:1034924739805:web:30ad738607d8da1ae19f34",
	"measurementId": "G-0BCQFCSC5T",
	"databaseURL":"https://individual-project-ec272-default-rtdb.europe-west1.firebasedatabase.app/"
}
# app = initializeApp(firebaseConfig)
# analytics = getAnalytics(app)
firebase= pyrebase.initialize_app(firebaseConfig)
auth= firebase.auth()
db= firebase.database()
app= Flask(__name__)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
	error= ""
	if request.method=="POST":
		emailadress= request.form['emailadress']
		password=request.form['password']
		try:
			login_session['user']= auth.create_user_with_email_and_password(emailadress,password)
			user={"emailadress": request.form['emailadress'],
			"fullname": request.form['fullname'],
			"password": request.form['password'],
			"preference": request.form['adjective']
			}
			db.child('Users').child(login_session['user']['localId']).set(user)

		except:
			error="Creating an account Failed"
	return render_template('signup.html')
# 'ADD  WHEN HOME PAGE IS READY'

@app.route('/login', methods=['GET', 'POST'])
def login():
	error = ""
	if request.method == 'POST':
		emailadress = request.form['emailadress']
		password = request.form['password']
		try:
			login_session['user'] = auth.sign_in_with_email_and_password(emailadress, password)
			# return redirect(url_for('ADD THIS WHEN HOME PAGE IS READY'))
		except:
			 error = "Authentication failed"
	return render_template("login.html")

@app.route('/add_idea', methods=['GET', 'POST'])
def add_idea():
	error= ""
	if request.method=="POST":
		# try:
		idea={"Title": request.form['Title'],
		"Description": request.form['Description'],
		"Image": request.form['Image'],
		"uid": login_session['user']['localId']}
		db.child("Pins").child(request.form['adjective']).push(idea)
		return redirect(url_for('home'))
		# except:
		#   print("Couldn't add idea")
	return render_template("add_idea.html")

@app.route('/home', methods=['GET', 'POST'])
def home():
	#Ideas= db.child('Pins').get().val()

		#adjectives = db.child("Users").child(login_session['user']['localId']).child("Interests").get().val() #["Coding", "Sports"]#["Makeup And Fashion", "Sports", "Technology", "Animals", "Science"]# self.request.get('adjective', allow_multiple=True)
	adjectives=["Technology", "Sports", "Animals", "Science", "Makeup And Fashion"]
	temp = []
	for a in adjectives:
		# increment count
		temp.extend(db.child("Pins").child(a).get().val().values())
	random.shuffle(temp)

	return render_template('home.html', Ideas=temp)

@app.route('/', methods=['GET', 'POST'])
def start():
	return render_template('start.html')	

if __name__ == '__main__':
	app.run(debug=True)
	#post()