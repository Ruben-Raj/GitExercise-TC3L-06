from flask import Flask, request, render_template, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(80))

    def __int__(self, username, password):
        self.username = username
        self.password = password


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exist,Please choose a different username')
            return redirect(url_for('register'))
        else:
            new_user = User(
            username = request.form['username'],
            password = generate_password_hash(request.form.get('password')))
            db.session.add(new_user)
            db.session.commit()
            flash('You have successfully registered,Please login')
            return redirect(url_for('register'))

    return render_template('register.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        username = request.form['username']
        password = request.form.get('password')

        query_user = User.query.filter_by(username=username).first()

        if query_user:
            if check_password_hash(query_user.password, password):
                session['logged_in'] = True
                return redirect(url_for('home'))
            else:
                flash('Username/email or password is wrong')
                return redirect(url_for('login'))
        else:
            flash('Username/email or password is wrong')
            return redirect(url_for('login'))



@app.route('/')
def home():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    else:
        return render_template('index.html')


@app.route('/logout')
def logout():
    session['logged_in'] = False
    return redirect(url_for('login'))
    

if __name__ == '__main__':
    app.app_context().push()
    app.debug = True
    db.create_all()
    app.secret_key = '\xe3\xdeN~\xed<\xb6.Wy\xe7H\x8f\xb3\xc1\x9d\x8f\x80e\xf0\xab\xd4I\xfc'
    app.run(host='127.0.0.1', port=8080)
