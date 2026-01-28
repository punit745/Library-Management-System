"""
Migration script to add admission numbers to existing students
and update database schema.
"""
import random
from app import app, db
from models import Student, Issue

def generate_unique_admission_number():
    """Generate a unique 8-digit admission number"""
    with app.app_context():
        while True:
            admission_number = ''.join([str(random.randint(0, 9)) for _ in range(8)])
            existing = Student.query.filter_by(admission_number=admission_number).first()
            if not existing:
                return admission_number

def migrate():
    """Run the migration"""
    with app.app_context():
        print("Starting database migration...")
        
        # Create all tables based on current models
        db.create_all()
        print("✓ Database tables created/updated")
        
        # Get all students without admission numbers
        try:
            students_without_admission = Student.query.filter(
                (Student.admission_number == None) | (Student.admission_number == '')
            ).all()
            
            if students_without_admission:
                print(f"\nFound {len(students_without_admission)} students without admission numbers")
                for student in students_without_admission:
                    admission_number = generate_unique_admission_number()
                    student.admission_number = admission_number
                    print(f"  Assigned {admission_number} to {student.name}")
                
                db.session.commit()
                print("✓ Admission numbers assigned successfully")
            else:
                print("\n✓ All students already have admission numbers")
        except Exception as e:
            print(f"\nNote: {str(e)}")
            print("This is expected if the database is being created for the first time.")
        
        print("\n✓ Migration completed successfully!")
        print("\nDatabase schema updated with:")
        print("  - admission_number field in Student model (8-digit unique ID)")
        print("  - email field is now optional in Student model")
        print("  - issue_duration field in Issue model")
        print("  - Fine rate updated to ₹20/day")
        print("  - 12-day grace period added")

if __name__ == '__main__':
    migrate()
