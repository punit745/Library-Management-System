from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db, Issue, Student, Book
from datetime import datetime, timedelta

bp = Blueprint('issues', __name__, url_prefix='/issues')

@bp.route('/')
def issue_books():
    students = Student.query.all()
    books = Book.query.filter_by(available=True).all()
    issues = Issue.query.filter_by(returned=False).all()
    
    # Calculate fines for all active issues
    for issue in issues:
        issue.calculate_fine()
    db.session.commit()
    
    return render_template('issue_books.html', students=students, books=books, issues=issues)

@bp.route('/issue', methods=['POST'])
def issue_book():
    student_id = request.form.get('student_id')
    book_id = request.form.get('book_id')
    
    if student_id and book_id:
        student = Student.query.get(student_id)
        book = Book.query.get(book_id)
        
        if student and book and book.available:
            issue = Issue(student_id=student_id, book_id=book_id)
            book.available = False
            
            try:
                db.session.add(issue)
                db.session.commit()
                flash(f'Book "{book.title}" issued to {student.name} successfully!', 'success')
            except Exception as e:
                db.session.rollback()
                flash(f'Error issuing book: {str(e)}', 'error')
        else:
            flash('Invalid student or book, or book not available!', 'error')
    else:
        flash('Please select both student and book!', 'error')
    
    return redirect(url_for('issues.issue_books'))

@bp.route('/return/<int:id>', methods=['POST'])
def return_book(id):
    issue = Issue.query.get_or_404(id)
    
    if not issue.returned:
        issue.returned = True
        issue.return_date = datetime.utcnow()
        issue.calculate_fine()
        
        book = Book.query.get(issue.book_id)
        book.available = True
        
        try:
            db.session.commit()
            if issue.fine > 0:
                flash(f'Book returned successfully! Fine: ${issue.fine:.2f}', 'warning')
            else:
                flash('Book returned successfully!', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Error returning book: {str(e)}', 'error')
    else:
        flash('Book already returned!', 'error')
    
    return redirect(url_for('issues.issue_books'))
