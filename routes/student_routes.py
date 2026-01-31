from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db, Student, Issue
import random

bp = Blueprint('students', __name__, url_prefix='/students')

@bp.route('/')
def manage_students():
    search_query = request.args.get('search', '')
    if search_query:
        students = Student.query.filter(
            (Student.name.ilike(f'%{search_query}%')) |
            (Student.admission_number.ilike(f'%{search_query}%')) |
            (Student.course.ilike(f'%{search_query}%'))
        ).all()
        
        # Redirect to student profile if exactly one match or exact admission number match
        if len(students) == 1:
            return redirect(url_for('students.student_profile', admission_number=students[0].admission_number))
        
        # Check for exact admission number match
        exact_match = Student.query.filter_by(admission_number=search_query).first()
        if exact_match:
            return redirect(url_for('students.student_profile', admission_number=exact_match.admission_number))
    else:
        students = Student.query.all()
    return render_template('manage_students.html', students=students, search_query=search_query)

@bp.route('/add', methods=['POST'])
def add_student():
    name = request.form.get('name')
    email = request.form.get('email')
    course = request.form.get('course')
    admission_number = request.form.get('admission_number')
    
    # Generate a random 8-digit admission number if not provided
    if not admission_number:
        while True:
            admission_number = ''.join([str(random.randint(0, 9)) for _ in range(8)])
            # Check if this admission number already exists
            existing = Student.query.filter_by(admission_number=admission_number).first()
            if not existing:
                break
    
    if name and course and admission_number:
        # Validate admission number is 8 digits
        if not admission_number.isdigit() or len(admission_number) != 8:
            flash('Admission number must be exactly 8 digits!', 'error')
            return redirect(url_for('students.manage_students'))
        
        # Check if admission number already exists
        existing_student = Student.query.filter_by(admission_number=admission_number).first()
        if existing_student:
            flash('A student with this admission number already exists!', 'error')
            return redirect(url_for('students.manage_students'))
        
        # Email is now optional, but if provided, check for uniqueness
        if email:
            existing_email = Student.query.filter_by(email=email).first()
            if existing_email:
                flash('A student with this email already exists!', 'error')
                return redirect(url_for('students.manage_students'))
        
        student = Student(name=name, email=email if email else None, course=course, admission_number=admission_number)
        try:
            db.session.add(student)
            db.session.commit()
            flash('Student added successfully!', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Error adding student: {str(e)}', 'error')
    else:
        flash('Name, course, and admission number are required!', 'error')
    
    return redirect(url_for('students.manage_students'))

@bp.route('/delete/<int:id>', methods=['POST'])
def delete_student(id):
    student = Student.query.get_or_404(id)
    try:
        db.session.delete(student)
        db.session.commit()
        flash('Student deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting student: {str(e)}', 'error')
    
    return redirect(url_for('students.manage_students'))

@bp.route('/profile/<admission_number>')
def student_profile(admission_number):
    """View detailed profile of a student by admission number"""
    student = Student.query.filter_by(admission_number=admission_number).first_or_404()
    
    # Get all issues for this student
    issues = Issue.query.filter_by(student_id=student.id).order_by(Issue.issue_date.desc()).all()
    
    # Calculate fines for all active issues
    for issue in issues:
        issue.calculate_fine()
    db.session.commit()
    
    # Separate current and returned issues
    current_issues = [issue for issue in issues if not issue.returned]
    returned_issues = [issue for issue in issues if issue.returned]
    
    # Calculate total outstanding fine
    total_fine = sum(issue.fine for issue in current_issues if issue.fine > 0)
    
    # Get all available books for issuing
    from models import Book
    available_books = Book.query.filter_by(available=True).all()
    
    return render_template('student_profile.html', 
                         student=student, 
                         issues=issues,
                         current_issues=current_issues,
                         returned_issues=returned_issues,
                         total_fine=total_fine,
                         available_books=available_books)

@bp.route('/profile/<admission_number>/issue', methods=['POST'])
def issue_book_to_student(admission_number):
    """Issue a book to a student from their profile page"""
    student = Student.query.filter_by(admission_number=admission_number).first_or_404()
    
    book_id = request.form.get('book_id')
    barcode_input = request.form.get('barcode_scan')
    issue_duration = request.form.get('issue_duration')
    
    from models import Book
    
    # If barcode is provided, find the book by barcode
    if barcode_input:
        book = Book.query.filter(
            (Book.barcode == barcode_input) | 
            (Book.book_code == barcode_input)
        ).first()
        if book:
            book_id = book.id
        else:
            flash(f'No book found with barcode/code: {barcode_input}', 'error')
            return redirect(url_for('students.student_profile', admission_number=admission_number))
    
    if book_id:
        book = Book.query.get(book_id)
        
        if book and book.available:
            # Create issue with custom duration if provided
            duration = None
            if issue_duration and issue_duration != 'default':
                try:
                    duration = int(issue_duration)
                    if duration < 1 or duration > 365:
                        flash('Duration must be between 1 and 365 days!', 'error')
                        return redirect(url_for('students.student_profile', admission_number=admission_number))
                except ValueError:
                    flash('Invalid duration value!', 'error')
                    return redirect(url_for('students.student_profile', admission_number=admission_number))
            
            issue = Issue(student_id=student.id, book_id=book_id, issue_duration=duration)
            book.available = False
            
            try:
                db.session.add(issue)
                db.session.flush()
                issue.set_due_date_from_book()
                db.session.commit()
                flash(f'Book "{book.title}" (Code: {book.book_code}) issued to {student.name} successfully!', 'success')
            except Exception as e:
                db.session.rollback()
                flash(f'Error issuing book: {str(e)}', 'error')
        else:
            flash('Invalid book or book not available!', 'error')
    else:
        flash('Please select a book!', 'error')
    
    return redirect(url_for('students.student_profile', admission_number=admission_number))

@bp.route('/profile/<admission_number>/return/<int:issue_id>', methods=['POST'])
def return_book_from_profile(admission_number, issue_id):
    """Return a book from the student profile page"""
    from datetime import datetime
    from models import Book
    
    student = Student.query.filter_by(admission_number=admission_number).first_or_404()
    issue = Issue.query.get_or_404(issue_id)
    
    # Verify the issue belongs to this student
    if issue.student_id != student.id:
        flash('Invalid operation!', 'error')
        return redirect(url_for('students.student_profile', admission_number=admission_number))
    
    if not issue.returned:
        issue.returned = True
        issue.return_date = datetime.utcnow()
        issue.calculate_fine()
        
        book = Book.query.get(issue.book_id)
        book.available = True
        
        try:
            db.session.commit()
            if issue.fine > 0:
                flash(f'Book "{book.title}" (Code: {book.book_code}) returned successfully! Fine: ₹{issue.fine:.2f}', 'warning')
            else:
                flash(f'Book "{book.title}" (Code: {book.book_code}) returned successfully!', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Error returning book: {str(e)}', 'error')
    else:
        flash('Book already returned!', 'error')
    
    return redirect(url_for('students.student_profile', admission_number=admission_number))
