from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db, Book

bp = Blueprint('books', __name__, url_prefix='/books')

@bp.route('/')
def manage_books():
    books = Book.query.all()
    return render_template('manage_books.html', books=books)

@bp.route('/add', methods=['POST'])
def add_book():
    title = request.form.get('title')
    author = request.form.get('author')
    book_type = request.form.get('book_type')
    course = request.form.get('course')
    duration_type = request.form.get('duration_type', 'semester')
    duration_days = request.form.get('duration_days')
    
    if title and author and book_type:
        try:
            # Validate duration_days if provided
            duration_days_value = None
            if duration_days:
                duration_days_value = int(duration_days)
                if duration_days_value < 1:
                    flash('Duration days must be a positive number!', 'error')
                    return redirect(url_for('books.manage_books'))
            
            book = Book(
                title=title, 
                author=author, 
                book_type=book_type, 
                course=course,
                duration_type=duration_type,
                duration_days=duration_days_value
            )
            db.session.add(book)
            db.session.commit()
            flash('Book added successfully!', 'success')
        except ValueError:
            db.session.rollback()
            flash('Invalid duration days. Please enter a valid number!', 'error')
        except Exception as e:
            db.session.rollback()
            flash(f'Error adding book: {str(e)}', 'error')
    else:
        flash('Title, author, and type are required!', 'error')
    
    return redirect(url_for('books.manage_books'))

@bp.route('/delete/<int:id>', methods=['POST'])
def delete_book(id):
    book = Book.query.get_or_404(id)
    try:
        db.session.delete(book)
        db.session.commit()
        flash('Book deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting book: {str(e)}', 'error')
    
    return redirect(url_for('books.manage_books'))
