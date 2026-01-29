"""
Seed data script for Library Management System
This script populates the database with initial book and student data
"""
from app import app
from models import db, Book, Student
from datetime import datetime
import random

# Initial book data
INITIAL_BOOKS = [
    # Computer Science Books
    {
        'title': 'Introduction to Algorithms',
        'author': 'Thomas H. Cormen',
        'book_type': 'textbook',
        'course': 'Computer Science',
        'duration_type': 'semester',
        'duration_days': None
    },
    {
        'title': 'Clean Code',
        'author': 'Robert C. Martin',
        'book_type': 'reference',
        'course': 'Software Engineering',
        'duration_type': 'specific',
        'duration_days': 30
    },
    {
        'title': 'Design Patterns',
        'author': 'Gang of Four',
        'book_type': 'reference',
        'course': 'Software Engineering',
        'duration_type': 'specific',
        'duration_days': 21
    },
    {
        'title': 'Database System Concepts',
        'author': 'Abraham Silberschatz',
        'book_type': 'textbook',
        'course': 'Database Management',
        'duration_type': 'semester',
        'duration_days': None
    },
    {
        'title': 'Computer Networks',
        'author': 'Andrew S. Tanenbaum',
        'book_type': 'textbook',
        'course': 'Computer Networks',
        'duration_type': 'semester',
        'duration_days': None
    },
    
    # Mathematics Books
    {
        'title': 'Discrete Mathematics and Its Applications',
        'author': 'Kenneth H. Rosen',
        'book_type': 'textbook',
        'course': 'Mathematics',
        'duration_type': 'semester',
        'duration_days': None
    },
    {
        'title': 'Linear Algebra and Its Applications',
        'author': 'David C. Lay',
        'book_type': 'textbook',
        'course': 'Mathematics',
        'duration_type': 'semester',
        'duration_days': None
    },
    {
        'title': 'Calculus: Early Transcendentals',
        'author': 'James Stewart',
        'book_type': 'textbook',
        'course': 'Mathematics',
        'duration_type': 'semester',
        'duration_days': None
    },
    
    # Physics Books
    {
        'title': 'Fundamentals of Physics',
        'author': 'David Halliday',
        'book_type': 'textbook',
        'course': 'Physics',
        'duration_type': 'semester',
        'duration_days': None
    },
    {
        'title': 'Introduction to Electrodynamics',
        'author': 'David J. Griffiths',
        'book_type': 'textbook',
        'course': 'Physics',
        'duration_type': 'semester',
        'duration_days': None
    },
    
    # Engineering Books
    {
        'title': 'Engineering Mechanics: Statics',
        'author': 'J.L. Meriam',
        'book_type': 'textbook',
        'course': 'Mechanical Engineering',
        'duration_type': 'semester',
        'duration_days': None
    },
    {
        'title': 'Digital Design',
        'author': 'M. Morris Mano',
        'book_type': 'textbook',
        'course': 'Electrical Engineering',
        'duration_type': 'semester',
        'duration_days': None
    },
    
    # Business & Management Books
    {
        'title': 'Principles of Marketing',
        'author': 'Philip Kotler',
        'book_type': 'textbook',
        'course': 'Business Administration',
        'duration_type': 'semester',
        'duration_days': None
    },
    {
        'title': 'Financial Accounting',
        'author': 'Walter T. Harrison',
        'book_type': 'textbook',
        'course': 'Accounting',
        'duration_type': 'semester',
        'duration_days': None
    },
    {
        'title': 'The Lean Startup',
        'author': 'Eric Ries',
        'book_type': 'reference',
        'course': 'Entrepreneurship',
        'duration_type': 'specific',
        'duration_days': 14
    },
    
    # General Reference Books
    {
        'title': 'The Art of Computer Programming',
        'author': 'Donald E. Knuth',
        'book_type': 'reference',
        'course': 'Computer Science',
        'duration_type': 'specific',
        'duration_days': 21
    },
    {
        'title': 'Data Structures and Algorithms in Python',
        'author': 'Michael T. Goodrich',
        'book_type': 'reference',
        'course': 'Computer Science',
        'duration_type': 'specific',
        'duration_days': 30
    },
    {
        'title': 'Machine Learning Yearning',
        'author': 'Andrew Ng',
        'book_type': 'reference',
        'course': 'Artificial Intelligence',
        'duration_type': 'specific',
        'duration_days': 21
    },
    {
        'title': 'Introduction to Statistical Learning',
        'author': 'Gareth James',
        'book_type': 'reference',
        'course': 'Data Science',
        'duration_type': 'specific',
        'duration_days': 30
    },
    {
        'title': 'Python Crash Course',
        'author': 'Eric Matthes',
        'book_type': 'reference',
        'course': 'Programming',
        'duration_type': 'specific',
        'duration_days': 21
    }
]

# Initial student data
INITIAL_STUDENTS = [
    {
        'name': 'John Smith',
        'email': 'john.smith@university.edu',
        'course': 'Computer Science'
    },
    {
        'name': 'Emma Johnson',
        'email': 'emma.johnson@university.edu',
        'course': 'Software Engineering'
    },
    {
        'name': 'Michael Brown',
        'email': 'michael.brown@university.edu',
        'course': 'Computer Science'
    },
    {
        'name': 'Sarah Davis',
        'email': 'sarah.davis@university.edu',
        'course': 'Mathematics'
    },
    {
        'name': 'James Wilson',
        'email': 'james.wilson@university.edu',
        'course': 'Physics'
    },
    {
        'name': 'Emily Martinez',
        'email': 'emily.martinez@university.edu',
        'course': 'Electrical Engineering'
    },
    {
        'name': 'Daniel Anderson',
        'email': 'daniel.anderson@university.edu',
        'course': 'Mechanical Engineering'
    },
    {
        'name': 'Jessica Taylor',
        'email': 'jessica.taylor@university.edu',
        'course': 'Business Administration'
    },
    {
        'name': 'Christopher Thomas',
        'email': 'christopher.thomas@university.edu',
        'course': 'Computer Science'
    },
    {
        'name': 'Ashley Garcia',
        'email': 'ashley.garcia@university.edu',
        'course': 'Data Science'
    },
    {
        'name': 'Matthew Rodriguez',
        'email': 'matthew.rodriguez@university.edu',
        'course': 'Software Engineering'
    },
    {
        'name': 'Amanda Lee',
        'email': 'amanda.lee@university.edu',
        'course': 'Accounting'
    },
    {
        'name': 'Joshua White',
        'email': 'joshua.white@university.edu',
        'course': 'Computer Science'
    },
    {
        'name': 'Stephanie Harris',
        'email': 'stephanie.harris@university.edu',
        'course': 'Mathematics'
    },
    {
        'name': 'Andrew Clark',
        'email': 'andrew.clark@university.edu',
        'course': 'Physics'
    }
]

def seed_database():
    """Populate database with initial data"""
    with app.app_context():
        # Check if data already exists
        if Book.query.first() is not None:
            print("Database already contains books. Skipping book seeding.")
        else:
            print("Seeding books...")
            for book_data in INITIAL_BOOKS:
                # Ensure category is set
                if 'category' not in book_data:
                    book_data['category'] = 'general'
                
                # Generate book code
                # Note: In a real app, strict sequential generation might need locking, 
                # but for seeding it's fine.
                book_code = Book.generate_book_code(book_data['category'])
                
                book = Book(**book_data)
                book.book_code = book_code
                book.generate_barcode()
                
                db.session.add(book)
                # Commit strictly to ensure sequential numbering works if it queries DB
                db.session.commit()
            print(f"Added {len(INITIAL_BOOKS)} books to the database.")
        
        if Student.query.first() is not None:
            print("Database already contains students. Skipping student seeding.")
        else:
            print("Seeding students...")
            for student_data in INITIAL_STUDENTS:
                # Generate random 8-digit admission number
                while True:
                    admission_number = ''.join([str(random.randint(0, 9)) for _ in range(8)])
                    if not Student.query.filter_by(admission_number=admission_number).first():
                        break
                
                student = Student(**student_data)
                student.admission_number = admission_number
                db.session.add(student)
            db.session.commit()
            print(f"Added {len(INITIAL_STUDENTS)} students to the database.")
        
        print("Database seeding completed!")

if __name__ == '__main__':
    seed_database()
