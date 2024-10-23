from flask import Blueprint, render_template, redirect, url_for, session, request
from .models import Quiz, Question, QuizResult, db
import time

# Create blueprint for quiz-related routes
quiz_blueprint = Blueprint('quiz', __name__)

# Route to start a quiz
@quiz_blueprint.route('/quiz/start/<int:quiz_id>')
def start_quiz(quiz_id):
    if 'role' in session and session['role'] == 'quizer':
        quiz = Quiz.query.get_or_404(quiz_id)
        questions = Question.query.filter_by(quiz_id=quiz_id).all()

        # Start the quiz, record the start time (could be used later for time tracking)
        session['quiz_start_time'] = time.time()

        return render_template('quiz_page.html', quiz=quiz, questions=questions)
    return redirect(url_for('login.login'))

@quiz_blueprint.route('/quiz/submit/<int:quiz_id>', methods=['POST'])
def submit_quiz(quiz_id):
    if 'role' in session and session['role'] == 'quizer':
        quiz = Quiz.query.get_or_404(quiz_id)
        questions = Question.query.filter_by(quiz_id=quiz_id).all()

        total_questions = len(questions)
        score = 0
        correct_answers = 0

        # Evaluate answers
        for question in questions:
            selected_option = request.form.get(f'question_{question.id}')
            
            if selected_option:
                selected_option = int(selected_option)  # Convert to integer
                if selected_option == question.correct_option:
                    score += 3  # +3 for correct answer
                    correct_answers += 1
                else:
                    score -= 1  # -1 for incorrect answer
            # If selected_option is None, score remains 0 (unanswered)

        # Calculate time taken for the quiz
        start_time = session.get('quiz_start_time')
        time_taken = int(time.time() - start_time) if start_time else 0

        # Check if the result already exists for the user and quiz
        existing_result = QuizResult.query.filter_by(user_id=1, quiz_id=quiz.id).first()  # Change user_id as needed

        if existing_result:
            # Update the existing result
            existing_result.score = score
            existing_result.total_questions = total_questions
            existing_result.correct_answers = correct_answers
            existing_result.time_taken = time_taken
            existing_result.has_taken = True
        else:
            # Create a new result
            result = QuizResult(
                user_id=1,  # Hardcoded for now, as per your earlier preference
                quiz_id=quiz.id,
                score=score,
                total_questions=total_questions,
                correct_answers=correct_answers,
                time_taken=time_taken,
                has_taken=True
            )
            db.session.add(result)

        # Commit changes
        db.session.commit()

        # Clear the session start time
        session.pop('quiz_start_time', None)

        # Redirect to result page
        return redirect(url_for('quiz.view_result', quiz_id=quiz.id, result_id=existing_result.id if existing_result else result.id))
    
    return redirect(url_for('login.login'))

# Route to view quiz result
@quiz_blueprint.route('/quiz/result/<int:quiz_id>/<int:result_id>')
def view_result(quiz_id, result_id):
    if 'role' in session and session['role'] == 'quizer':
        result = QuizResult.query.get_or_404(result_id)
        quiz = Quiz.query.get_or_404(quiz_id)

        return render_template('quiz_result.html', quiz=quiz, result=result)
    return redirect(url_for('login.login'))
