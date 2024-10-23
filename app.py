from flask import Flask
from blueprints.models import db
from config import Config
from blueprints.login import login_blueprint
from blueprints.quiz import quiz_blueprint
from blueprints.create import create_blueprint
from blueprints.chatgpt2 import api_blueprint

app = Flask(__name__)
app.config.from_object(Config)

# Initialize the SQLAlchemy instance with the app
db.init_app(app)

# Register blueprints
app.register_blueprint(login_blueprint)
app.register_blueprint(quiz_blueprint, url_prefix='/quiz')
app.register_blueprint(create_blueprint)
app.register_blueprint(api_blueprint)


if __name__ == '__main__':
    app.run(debug=True)
