from flask import Flask, render_template, request, redirect, url_for, session
import pymysql.cursors

app = Flask(__name__)
app.secret_key = 'xyzsdfg'

# MySQL configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'user-system'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

# MySQL connection
mysql = pymysql.connect(
    host=app.config['MYSQL_HOST'],
    user=app.config['MYSQL_USER'],
    password=app.config['MYSQL_PASSWORD'],
    db=app.config['MYSQL_DB'],
    cursorclass=pymysql.cursors.DictCursor
)



@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    message = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        with mysql.cursor() as cursor:
            cursor.execute('SELECT * FROM user WHERE username = %s AND password = %s', (username, password))
            user = cursor.fetchone()
            if user:
                session['loggedin'] = True
                session['name'] = user['name']
                session['username'] = user['username']
                message = 'Logged in successfully!'
                return render_template('user.html', message=message)
            else:
                message = 'Invalid Credentials!'
                
    return render_template('login.html', message=message)


@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('username', None)
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    message = ''
    if request.method == 'POST':
        name = request.form['name']
        mobilenumber = request.form['mobilenumber']
        username = request.form['username']
        password = request.form['password']

        # Validate name
        if not username:
            message = 'Please enter your username!'
        elif len(name) < 2:
            message = 'Username should have at least 2 characters!'

        # Validate password
        elif not password:
            message = 'Please enter a password!'
        
        elif len(password) < 6:
            message = 'Password should have at least 6 characters!'

        else:
            # Registration logic...
            with mysql.cursor() as cursor:
                cursor.execute('SELECT * FROM user WHERE username = %s', (username,))
                account = cursor.fetchone()
                if account:
                    message = 'username already exist!!'
                else:
                    cursor.execute('INSERT INTO user (name, mobilenumber, username, password) VALUES (%s, %s, %s, %s)', (name, mobilenumber, username, password))
                    mysql.commit()
                    message = 'You have successfully registered!'
                    return render_template('user.html',message=message)
    
    return render_template('register.html', message=message)


if __name__ == "__main__":
    app.run()
