from flask import Flask
from flask_migrate import Migrate
from models import db
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
migrate = Migrate(app, db)

# Import routes
from routes import book_routes, student_routes, issue_routes

# Register blueprints
app.register_blueprint(book_routes.bp)
app.register_blueprint(student_routes.bp)
app.register_blueprint(issue_routes.bp)

@app.route('/')
def index():
    from flask import render_template
    return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=True)
