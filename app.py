from flask import Flask,request,session,url_for,redirect,render_template
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re


app=Flask(__name__)

app.secret_key = 'ypur secret key'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'todolist'

mysql=MySQL(app)

@app.route('/yash')
@app.route('/login',methods=['GET','POST'])
def login():
        msg=''
        if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
                username=request.form['username']
                password=request.form['password']
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute('SELECT * from usertable WHERE username =%s AND password = %s',(username,password,))
                account = cursor.fetchone()
                if account:
                        session['loggedin']=True
                        session['id'] = account['id']
                        session['username']=account['username']
                        msg = 'Logged in success'
                        return render_template('index.html',msg=msg)
                else:
                        msg = 'incorrect username/pass'
        return render_template('login.html',msg=msg)

@app.route('/logout')
def logout():
 session.pop('loggedin',None)
 session.pop('id',None)
 session.pop('username',None)
 return redirect(url_for('login'))

@app.route('/register' , methods=['GET','POST'])
def register():
     msg=''
     if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form and 'address' in request.form and 'state' in request.form:
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        address = request.form['address']
        state = request.form['state']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM usertable WHERE username = %s',(username,))
        account = cursor.fetchone()
        if account:
          msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
          msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', username):
          msg = 'name must contain only characters and numbers !'
        else:
          cursor.execute('INSERT INTO usertable VALUES (NULL,%s,%s,%s,%s,%s)',(username,password,email,address,state)) 
          mysql.connection.commit()
          msg = 'success'
     elif request.method == 'POST':
         msg = 'Please fill details'
     return render_template('register.html',msg=msg)

@app.route("/index")
def index():
	if 'loggedin' in session:
		return render_template("index.html")
	return redirect(url_for('login'))

@app.route('/taskadd' ,methods=['GET','POST'])
def taskadd():
        if 'loggedin' in session:
                if request.method == 'POST' and 'task_name' in request.form and 'task_desc' in request.form and 'start_date' in request.form and 'end_date' in request.form :
			task_name = request.form['task_name']
                        task_desc = request.form['task_desc']
                        start_date = request.form['start_date']
                        end_date = request.form['end_date']
                        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
			cursor.execute('SELECT * FROM task WHERE id = %s ', (id,))
			account  = cursor.fetchone()
			if account:
				msg = 
        return render_template("taskadd.html")

@app.route("/taskprogress")
def taskprogress():
        return render_template("taskprogress.html")

@app.route("/taskdone")
def taskdone():
        return render_template("taskdone.html")
           























                       
if __name__ == "__main__":
	app.run(host ="localhost", port = int("5001"))



