from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Initialize SQLAlchemy
db = SQLAlchemy()

# Quiz model
class Quiz(db.Model):
    __tablename__ = 'quizzes'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    time_limit = db.Column(db.Integer)  # Time limit in minutes
    total_questions = db.Column(db.Integer)
    difficulty = db.Column(db.String(50))  # e.g., 'easy', 'medium', 'hard'
    topic = db.Column(db.String(100))  # e.g., 'Math', 'Science'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationship with the Question model
    questions = db.relationship('Question', backref='quiz', cascade="all, delete-orphan", lazy=True)

    def __repr__(self):
        return f'<Quiz {self.title}>'

# Question model
class Question(db.Model):
    __tablename__ = 'questions'

    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quizzes.id', ondelete='CASCADE'))
    question_text = db.Column(db.Text, nullable=False)
    option_1 = db.Column(db.Text)
    option_2 = db.Column(db.Text)
    option_3 = db.Column(db.Text)
    option_4 = db.Column(db.Text)
    correct_option = db.Column(db.Integer)  # 1, 2, 3, or 4 indicating which option is correct

    def __repr__(self):
        return f'<Question {self.question_text[:50]}>'

# QuizResult model
class QuizResult(db.Model):
    __tablename__ = 'quiz_results'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)  # Hardcoded for you and your friend, or dynamic if expanded
    quiz_id = db.Column(db.Integer, db.ForeignKey('quizzes.id', ondelete='CASCADE'))
    score = db.Column(db.Integer, default=0)
    total_questions = db.Column(db.Integer)
    correct_answers = db.Column(db.Integer)
    time_taken = db.Column(db.Integer)  # Time taken to complete in seconds (optional)
    has_taken = db.Column(db.Boolean, default=False)
    completed_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<QuizResult for quiz_id {self.quiz_id}, user_id {self.user_id}>'
