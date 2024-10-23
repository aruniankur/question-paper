from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from .models import Quiz, db, Question, QuizResult

create_blueprint = Blueprint('create', __name__)

@create_blueprint.route('/create_quiz', methods=['GET', 'POST'])
def create_quiz():
    if 'role' not in session or session['role'] != 'questionmaker':
        flash('You are not authorized to view this page. Please log in.', 'error')
        return redirect(url_for('login.logout')) 
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        time_limit = request.form.get('time_limit')
        total_questions = request.form.get('total_questions')
        difficulty = request.form.get('difficulty')
        topic = request.form.get('topic')

        # Check for missing information
        if not all([title, description, time_limit, total_questions, difficulty, topic]):
            flash('All fields are required to create a quiz!', 'error')
            return redirect(url_for('create.create_quiz'))

        # Create a new quiz
        new_quiz = Quiz(
            title=title,
            description=description,
            time_limit=int(time_limit),
            total_questions=int(total_questions),
            difficulty=difficulty,
            topic=topic
        )
        db.session.add(new_quiz)
        db.session.commit()
        flash('Quiz created successfully!', 'success')
        return redirect(url_for('create.quiz_list'))

    return render_template('create_quiz.html')


@create_blueprint.route('/quiz_list', methods=['GET'])
def quiz_list():
    if 'role' not in session or session['role'] != 'questionmaker':
        flash('You are not authorized to view this page. Please log in.', 'error')
        return redirect(url_for('login.logout')) 
    quizzes = Quiz.query.all()  # Fetch all existing quizzes
    return render_template('quizlist.html', quizzes=quizzes)


@create_blueprint.route('/delete_quiz/<int:quiz_id>', methods=['POST'])
def delete_quiz(quiz_id):
    if 'role' not in session or session['role'] != 'questionmaker':
        flash('You are not authorized to view this page. Please log in.', 'error')
        return redirect(url_for('login.logout')) 
    quiz_to_delete = Quiz.query.get(quiz_id)
    if quiz_to_delete:
        db.session.delete(quiz_to_delete)
        db.session.commit()
        flash('Quiz deleted successfully!', 'success')
    else:
        flash('Quiz not found!', 'error')
    return redirect(url_for('create.quiz_list'))


@create_blueprint.route('/edit_quiz/<int:quiz_id>', methods=['GET', 'POST'])
def edit_quiz(quiz_id):
    if 'role' not in session or session['role'] != 'questionmaker':
        flash('You are not authorized to view this page. Please log in.', 'error')
        return redirect(url_for('login.logout')) 
    quiz = Quiz.query.get(quiz_id)
    if not quiz:
        flash('Quiz not found!', 'error')
        return redirect(url_for('create.quiz_list'))

    if request.method == 'POST':
        quiz.title = request.form.get('title')
        quiz.description = request.form.get('description')
        quiz.time_limit = request.form.get('time_limit')
        quiz.total_questions = request.form.get('total_questions')
        quiz.difficulty = request.form.get('difficulty')
        quiz.topic = request.form.get('topic')

        # Check for missing information
        if not all([quiz.title, quiz.description, quiz.time_limit, quiz.total_questions, quiz.difficulty, quiz.topic]):
            flash('All fields are required to edit a quiz!', 'error')
            return redirect(url_for('create.edit_quiz', quiz_id=quiz.id))

        db.session.commit()
        flash('Quiz updated successfully!', 'success')
        return redirect(url_for('create.quiz_list'))

    return render_template('create_quiz.html', quiz=quiz)


@create_blueprint.route('/manage_questions/<int:quiz_id>', methods=['GET', 'POST'])
def manage_questions(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    questions = Question.query.filter_by(quiz_id=quiz_id).all()

    if request.method == 'POST':
        if len(questions) < quiz.total_questions:
            question_text = request.form['question_text']
            option_1 = request.form['option_1']
            option_2 = request.form['option_2']
            option_3 = request.form['option_3']
            option_4 = request.form['option_4']
            correct_option = int(request.form['correct_option'])

            new_question = Question(
                quiz_id=quiz_id,
                question_text=question_text,
                option_1=option_1,
                option_2=option_2,
                option_3=option_3,
                option_4=option_4,
                correct_option=correct_option
            )
            db.session.add(new_question)
            db.session.commit()
            flash('Question added successfully!', 'success')
        else:
            flash('You have reached the maximum number of questions for this quiz.', 'error')

    return render_template('manage_questions.html', quiz=quiz, questions=questions)

@create_blueprint.route('/delete_question/<int:question_id>', methods=['POST'])
def delete_question(question_id):
    if 'role' not in session or session['role'] != 'questionmaker':
        flash('You are not authorized to view this page. Please log in.', 'error')
        return redirect(url_for('login.logout')) 
    question_to_delete = Question.query.get(question_id)
    if question_to_delete:
        db.session.delete(question_to_delete)
        db.session.commit()
        flash('Question deleted successfully!', 'success')
    else:
        flash('Question not found!', 'error')
    return redirect(url_for('create.manage_questions', quiz_id=question_to_delete.quiz_id))
