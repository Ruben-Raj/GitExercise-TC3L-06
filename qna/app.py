import os
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, 'instance', 'database.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "Foobar@2024"

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(80))

    def __init__(self, username, password):
        self.username = username
        self.password = password

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)

class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)
    question = db.relationship('Question', backref=db.backref('answers', lazy=True))
    upvotes = db.Column(db.Integer, default=0)

with app.app_context():
    db.create_all()

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists. Please choose a different username.')
            return redirect(url_for('register'))
        else:
            new_user = User(
                username=username,
                password=generate_password_hash(request.form.get('password'))
            )
            db.session.add(new_user)
            db.session.commit()
            flash('You have successfully registered. Please login.')
            return redirect(url_for('login'))

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
                session['user_id'] = query_user.id  
                return redirect(url_for('index'))  
            else:
                flash('Username/email or password is incorrect.')
                return redirect(url_for('login'))
        else:
            flash('Username/email or password is incorrect.')
            return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('logged_in', None)  
    session.pop('user_id', None)      
    return redirect(url_for('login'))

@app.route('/', defaults={'page': 1})
@app.route('/page/<int:page>')
def index(page):
    per_page = 2  
    questions = Question.query.paginate(page=page, per_page=per_page)
    return render_template('qna_question.html', questions=questions)

@app.route('/submit-question', methods=['POST'])
def submit_question():
    if 'logged_in' not in session:  
        flash('You must be logged in to submit a question.')
        return redirect(url_for('login'))
    
    question_content = request.form['question']
    new_question = Question(content=question_content)
    db.session.add(new_question)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/question/<int:question_id>', methods=['GET', 'POST'])
def view_question(question_id):  
    question = Question.query.get_or_404(question_id)
    
    if request.method == 'POST':
        if 'logged_in' not in session:  
            flash('You must be logged in to answer a question.')
            return redirect(url_for('login'))
        
        answer_content = request.form['answer']
        new_answer = Answer(content=answer_content, question_id=question.id)
        db.session.add(new_answer)
        db.session.commit()
        return redirect(url_for('view_question', question_id=question.id))
    
    per_page = 2  
    answers = Answer.query.filter_by(question_id=question.id).paginate(page=1, per_page=per_page)
    
    return render_template('qna_view_question.html', question=question, answers=answers)

@app.route('/delete-answer/<int:answer_id>', methods=['POST'])
def delete_answer(answer_id):
    if 'logged_in' not in session:  
        flash('You must be logged in to delete an answer.')
        return redirect(url_for('login'))

    answer = Answer.query.get_or_404(answer_id)
    db.session.delete(answer)
    db.session.commit()
    return redirect(url_for('view_question', question_id=answer.question_id))

@app.route('/delete-question/<int:question_id>', methods=['POST'])
def delete_question(question_id):
    if 'logged_in' not in session:  
        flash('You must be logged in to delete a question.')
        return redirect(url_for('login'))

    question = Question.query.get_or_404(question_id)
    db.session.delete(question)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/search', methods=['GET'])
def search_questions():
    query = request.args.get('query')
    questions = Question.query.filter(Question.content.like(f'%{query}%')).all()
    return render_template('qna_question.html', questions=questions)

@app.route('/edit-question/<int:question_id>', methods=['GET', 'POST'])
def edit_question(question_id):
    if 'logged_in' not in session:  
        flash('You must be logged in to edit a question.')
        return redirect(url_for('login'))

    question = Question.query.get_or_404(question_id)
    
    if request.method == 'POST':
        question.content = request.form['question']
        db.session.commit()
        return redirect(url_for('index'))
    
    return render_template('edit_question.html', question=question)

@app.route('/edit-answer/<int:answer_id>', methods=['POST'])
def edit_answer(answer_id):
    if 'logged_in' not in session:  
        flash('You must be logged in to edit an answer.')
        return redirect(url_for('login'))

    answer = Answer.query.get_or_404(answer_id)
    answer.content = request.form['answer']
    db.session.commit()
    return redirect(url_for('view_question', question_id=answer.question_id))

@app.route('/upvote/<int:answer_id>', methods=['POST'])
def upvote_answer(answer_id):
    if 'logged_in' not in session:  
        flash('You must be logged in to upvote an answer.')
        return redirect(url_for('login'))

    answer = Answer.query.get_or_404(answer_id)
    answer.upvotes += 1
    db.session.commit()
    return redirect(url_for('view_question', question_id=answer.question_id))

if __name__ == '__main__':
    app.run(debug=True)
