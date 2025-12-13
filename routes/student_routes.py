from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db, Student

bp = Blueprint('students', __name__, url_prefix='/students')

@bp.route('/')
def manage_students():
    students = Student.query.all()
    return render_template('manage_students.html', students=students)

@bp.route('/add', methods=['POST'])
def add_student():
    name = request.form.get('name')
    email = request.form.get('email')
    course = request.form.get('course')
    
    if name and email and course:
        student = Student(name=name, email=email, course=course)
        try:
            db.session.add(student)
            db.session.commit()
            flash('Student added successfully!', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Error adding student: {str(e)}', 'error')
    else:
        flash('All fields are required!', 'error')
    
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
