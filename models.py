from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta

db = SQLAlchemy()

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=True)
    admission_number = db.Column(db.String(8), unique=True, nullable=False)
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
    FINE_RATE_PER_DAY = 20.0  # Fine rate in rupees per day
    GRACE_PERIOD_DAYS = 12  # Grace period for re-issue or return before fine applies
    
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    issue_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    due_date = db.Column(db.DateTime, nullable=False)
    return_date = db.Column(db.DateTime, nullable=True)
    fine = db.Column(db.Float, default=0.0)
    returned = db.Column(db.Boolean, default=False)
    issue_duration = db.Column(db.Integer, nullable=True)  # Custom duration in days for this specific issue

    def __init__(self, **kwargs):
        super(Issue, self).__init__(**kwargs)
        if not self.due_date:
            # Set default due date, will be updated after commit
            self.due_date = datetime.utcnow() + timedelta(days=self.DEFAULT_DURATION_DAYS)
    
    def set_due_date_from_book(self):
        """Set due date based on custom issue_duration or the associated book's duration settings"""
        # If custom issue_duration is set, use it
        if self.issue_duration:
            self.due_date = self.issue_date + timedelta(days=self.issue_duration)
        elif self.book_id:
            book = Book.query.get(self.book_id)
            if book and book.duration_type == 'specific' and book.duration_days:
                # Use book's specific duration
                self.due_date = self.issue_date + timedelta(days=book.duration_days)
            else:
                # Default to standard duration for semester books
                self.due_date = self.issue_date + timedelta(days=self.DEFAULT_DURATION_DAYS)

    def calculate_fine(self):
        if self.returned and self.return_date:
            grace_period_end = self.due_date + timedelta(days=self.GRACE_PERIOD_DAYS)
            if self.return_date > grace_period_end:
                days_late = (self.return_date - grace_period_end).days
                self.fine = days_late * self.FINE_RATE_PER_DAY
        elif not self.returned:
            grace_period_end = self.due_date + timedelta(days=self.GRACE_PERIOD_DAYS)
            if datetime.utcnow() > grace_period_end:
                days_late = (datetime.utcnow() - grace_period_end).days
                self.fine = days_late * self.FINE_RATE_PER_DAY
    
    def get_days_late(self):
        """Get the number of days this issue is/was late"""
        grace_period_end = self.due_date + timedelta(days=self.GRACE_PERIOD_DAYS)
        if self.returned and self.return_date:
            if self.return_date > grace_period_end:
                return (self.return_date - grace_period_end).days
        elif not self.returned:
            if datetime.utcnow() > grace_period_end:
                return (datetime.utcnow() - grace_period_end).days
        return 0
    
    def get_days_issued(self):
        """Get the total number of days book has been issued"""
        if self.returned and self.return_date:
            return (self.return_date - self.issue_date).days
        else:
            return (datetime.utcnow() - self.issue_date).days
    
    def get_grace_days_remaining(self):
        """Get the number of days remaining in grace period"""
        grace_period_end = self.due_date + timedelta(days=self.GRACE_PERIOD_DAYS)
        if not self.returned:
            days_remaining = (grace_period_end - datetime.utcnow()).days
            return max(0, days_remaining)
        return 0

    def __repr__(self):
        return f'<Issue {self.id}>'
