from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta

db = SQLAlchemy()

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    course = db.Column(db.String(100), nullable=False)
    issues = db.relationship('Issue', backref='student', lazy=True)

    def __repr__(self):
        return f'<Student {self.name}>'

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    book_type = db.Column(db.String(50), nullable=False)  # textbook or reference
    course = db.Column(db.String(100), nullable=True)  # Course correlation
    duration_type = db.Column(db.String(50), nullable=False, default='semester')  # semester or specific
    duration_days = db.Column(db.Integer, nullable=True)  # For specific period books
    available = db.Column(db.Boolean, default=True)
    issues = db.relationship('Issue', backref='book', lazy=True)

    def __repr__(self):
        return f'<Book {self.title}>'

class Issue(db.Model):
    DEFAULT_DURATION_DAYS = 14  # Default duration for semester books
    FINE_RATE_PER_DAY = 50.0  # Fine rate in rupees per day
    
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    issue_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    due_date = db.Column(db.DateTime, nullable=False)
    return_date = db.Column(db.DateTime, nullable=True)
    fine = db.Column(db.Float, default=0.0)
    returned = db.Column(db.Boolean, default=False)

    def __init__(self, **kwargs):
        super(Issue, self).__init__(**kwargs)
        if not self.due_date:
            # Set default due date, will be updated after commit
            self.due_date = datetime.utcnow() + timedelta(days=self.DEFAULT_DURATION_DAYS)
    
    def set_due_date_from_book(self):
        """Set due date based on the associated book's duration settings"""
        if self.book_id:
            book = Book.query.get(self.book_id)
            if book and book.duration_type == 'specific' and book.duration_days:
                # Use book's specific duration
                self.due_date = self.issue_date + timedelta(days=book.duration_days)
            else:
                # Default to standard duration for semester books
                self.due_date = self.issue_date + timedelta(days=self.DEFAULT_DURATION_DAYS)

    def calculate_fine(self):
        if self.returned and self.return_date:
            if self.return_date > self.due_date:
                days_late = (self.return_date - self.due_date).days
                self.fine = days_late * self.FINE_RATE_PER_DAY
        elif not self.returned:
            if datetime.utcnow() > self.due_date:
                days_late = (datetime.utcnow() - self.due_date).days
                self.fine = days_late * self.FINE_RATE_PER_DAY
    
    def get_days_late(self):
        """Get the number of days this issue is/was late"""
        if self.returned and self.return_date:
            if self.return_date > self.due_date:
                return (self.return_date - self.due_date).days
        elif not self.returned:
            if datetime.utcnow() > self.due_date:
                return (datetime.utcnow() - self.due_date).days
        return 0

    def __repr__(self):
        return f'<Issue {self.id}>'
