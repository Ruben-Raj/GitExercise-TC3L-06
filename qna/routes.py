from flask import request, render_template, redirect, url_for, flash
from . import app, db
from .models import Question, Answer

@app.route('/', defaults={'page': 1})
@app.route('/page/<int:page>')
def index(page):
    per_page = 2
    questions = Question.query.paginate(page=page, per_page=per_page)
    return render_template('qna_question.html', questions=questions)

@app.route('/submit-question', methods=['POST'])
def submit_question():
    question_content = request.form['question']
    new_question = Question(content=question_content)
    db.session.add(new_question)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/question/<int:question_id>', methods=['GET', 'POST'])
@app.route('/question/<int:question_id>/page/<int:page>', methods=['GET', 'POST']) 
@app.route('/question/<int:question_id>', defaults={'page': 1}, methods=['GET', 'POST'])  
def view_question(question_id, page=1):  
    question = Question.query.get_or_404(question_id)
    
    if request.method == 'POST':
        answer_content = request.form['answer']
        new_answer = Answer(content=answer_content, question_id=question.id)
        db.session.add(new_answer)
        db.session.commit()
        return redirect(url_for('view_question', question_id=question.id))
    
    per_page = 2  
    answers = Answer.query.filter_by(question_id=question.id).paginate(page=page, per_page=per_page)
    
    return render_template('qna_view_question.html', question=question, answers=answers)

@app.route('/upvote/<int:answer_id>', methods=['POST'])
def upvote_answer(answer_id):
    answer = Answer.query.get_or_404(answer_id)
    answer.upvotes += 1
    db.session.commit()
    return redirect(url_for('view_question', question_id=answer.question_id))

@app.route('/delete-answer/<int:answer_id>', methods=['POST'])
def delete_answer(answer_id):
    answer = Answer.query.get_or_404(answer_id)
    db.session.delete(answer)
    db.session.commit()
    return redirect(url_for('view_question', question_id=answer.question_id))

@app.route('/delete-question/<int:question_id>', methods=['POST'])
def delete_question(question_id):
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
    question = Question.query.get_or_404(question_id)

    if request.method == 'POST':
        question.content = request.form['question']
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('edit_question.html', question=question)

@app.route('/edit-answer/<int:answer_id>', methods=['POST'])
def edit_answer(answer_id):
    answer = Answer.query.get_or_404(answer_id)
    answer.content = request.form['answer']
    db.session.commit()
    return redirect(url_for('view_question', question_id=answer.question_id))
