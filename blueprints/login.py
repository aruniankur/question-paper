from flask import Blueprint, render_template, request, redirect, url_for, session
from .models import Quiz, QuizResult, Question

# Create blueprint for login-related routes
login_blueprint = Blueprint('login', __name__)

# Hardcoded users for simplicity
users = {
    'testperson': {'password': 'quizer', 'role': 'quizer'},
    'nakaajaaaddkc': {'password': '12345678', 'role': 'questionmaker'}
}

# Home route, redirects to login
@login_blueprint.route('/', methods=['GET'])
def home():
    return redirect(url_for('login.login'))

# Login route
@login_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Validate credentials
        if username in users and users[username]['password'] == password:
            session['username'] = username
            session['role'] = users[username]['role']

            # Redirect based on role
            if users[username]['role'] == 'quizer':
                return redirect(url_for('login.quizer_dashboard'))
            elif users[username]['role'] == 'questionmaker':
                return redirect(url_for('login.questionmaker_dashboard'))
        else:
            # Invalid login, show error
            return render_template('login.html', error='Invalid username or password')

    return render_template('login.html')



@login_blueprint.route('/dashboard/quizer', methods=['GET'])
def quizer_dashboard():
    if 'role' in session and session['role'] == 'quizer':
        quizzes = Quiz.query.all()  # Fetch all quizzes for the quizer
        # Assuming you have a function to fetch quiz results for the user
        user_id = session.get('user_id')  # Ensure you have user_id in session
        results = QuizResult.query.filter_by(user_id=1).all()  
        quiz_results = {result.quiz_id: result for result in results}
        return render_template('dashboard.html', role='quizer', quizzes=quizzes, quiz_results=quiz_results)
    return redirect(url_for('login.login'))


# Questionmaker's dashboard, fetch available quizzes for editing
@login_blueprint.route('/dashboard/questionmaker')
def questionmaker_dashboard():
    if 'role' in session and session['role'] == 'questionmaker':
        quizzes = Quiz.query.all()  # Fetch all quizzes for the questionmaker
        return render_template('quizlist.html', quizzes=quizzes)
    return redirect(url_for('login.login'))

# Logout route
@login_blueprint.route('/logout')
def logout():
    session.clear()  # Clear the session
    return redirect(url_for('login.login'))



