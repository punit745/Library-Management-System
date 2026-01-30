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
    
    return render_template('student_profile.html', 
                         student=student, 
                         issues=issues,
                         current_issues=current_issues,
                         returned_issues=returned_issues,
                         total_fine=total_fine)
