"""
Migration script to add barcode and book code fields to existing books
"""
from app import app, db
from models import Book

def migrate_books():
    """Run the migration for books"""
    with app.app_context():
        print("Starting book barcode migration...")
        
        # Create all tables based on current models
        db.create_all()
        print("✓ Database tables created/updated")
        
        # Get all books without book codes
        try:
            books_without_codes = Book.query.filter(
                (Book.book_code == None) | (Book.book_code == '')
            ).all()
            
            if books_without_codes:
                print(f"\nFound {len(books_without_codes)} books without book codes")
                
                for book in books_without_codes:
                    # Assign default category if not present
                    if not hasattr(book, 'category') or not book.category:
                        # Try to infer category from book_type
                        if book.book_type == 'textbook':
                            book.category = 'general'
                        else:
                            book.category = 'general'
                    
                    # Generate book code
                    book_code = Book.generate_book_code(book.category)
                    book.book_code = book_code
                    
                    # Generate barcode
                    book.generate_barcode()
                    
                    print(f"  Book: {book.title}")
                    print(f"    Category: {book.category}")
                    print(f"    Code: {book_code}")
                    print(f"    Barcode: {book.barcode}")
                
                db.session.commit()
                print("\n✓ Book codes and barcodes assigned successfully")
            else:
                print("\n✓ All books already have book codes")
        except Exception as e:
            print(f"\nError during migration: {str(e)}")
            db.session.rollback()
            print("Migration failed. Please check the error above.")
            return False
        
        print("\n✓ Migration completed successfully!")
        print("\nBarcode System Summary:")
        print("  - Each book has a 6-digit code (2-digit category + 4-digit number)")
        print("  - Category codes: Technology=01, Medical=02, Science=03, Arts=04, etc.")
        print("  - Barcode format: LIB + 6-digit code (e.g., LIB010001)")
        print("  - Use barcode scanning for quick issue/return operations")
        return True

if __name__ == '__main__':
    success = migrate_books()
    exit(0 if success else 1)
