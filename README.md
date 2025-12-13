# Library Management System

A comprehensive Flask-based Library Management System designed to streamline library operations in colleges and universities. This system tracks student profiles, manages book inventory, handles book issuance/returns, calculates fines for late returns, and correlates books with course curriculum.

## Features

### 1. Student Management
- Add and manage student profiles with name, email, and course information
- View all registered students
- Delete student records

### 2. Book Management
- Add books to the library system with title, author, type, and course correlation
- Book types: Textbooks and Reference Books
- Track book availability status
- Delete books from the system

### 3. Issue/Return Books
- Issue books to students with automatic due date calculation (14 days)
- Track currently issued books
- Return books with automatic fine calculation
- View issue history with due dates and fines

### 4. Fine Management
- Automatic fine calculation for overdue books
- Fine rate: $5 per day for late returns
- Visual indicators for overdue books

### 5. Course-Book Integration
- Map books to specific courses
- Track which books are relevant to each course curriculum

### 6. User Interface
- Clean and intuitive web interface
- Responsive design for mobile and desktop
- Flash messages for user feedback
- Color-coded status indicators

## Project Structure

```
Library-Management-System/
├── app.py                      # Main application entry point
├── models.py                   # Database models (Student, Book, Issue)
├── config.py                   # Configuration settings
├── routes/
│   ├── __init__.py            # Routes package initializer
│   ├── book_routes.py         # Book management routes
│   ├── student_routes.py      # Student management routes
│   └── issue_routes.py        # Issue/return book routes
├── templates/
│   ├── base.html              # Base template with navigation
│   ├── home.html              # Homepage
│   ├── manage_students.html   # Student management page
│   ├── manage_books.html      # Book management page
│   └── issue_books.html       # Issue/return books page
├── static/
│   └── style.css              # Custom CSS styling
├── migrations/                 # Database migration files (auto-generated)
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

## Installation & Setup

### Prerequisites
- Python 3.7 or higher
- pip (Python package manager)

### Step 1: Clone the Repository
```bash
git clone https://github.com/punit745/Library-Management-System.git
cd Library-Management-System
```

### Step 2: Create Virtual Environment
```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Initialize Database
```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

### Step 5: Run the Application
```bash
flask run
```

### Step 6: Access the Application
Open your web browser and navigate to:
```
http://127.0.0.1:5000
```

## Usage Guide

### Managing Students
1. Navigate to **Students** from the navigation menu
2. Fill in the student form with name, email, and course
3. Click "Add Student" to register a new student
4. View all students in the table below
5. Delete students using the "Delete" button

### Managing Books
1. Navigate to **Books** from the navigation menu
2. Fill in the book form with title, author, type, and optional course
3. Select book type: "Textbook" or "Reference Book"
4. Click "Add Book" to add the book to the library
5. View book availability status in the table
6. Delete books using the "Delete" button

### Issuing Books
1. Navigate to **Issue/Return** from the navigation menu
2. Select a student from the dropdown
3. Select an available book from the dropdown
4. Click "Issue Book" to issue the book to the student
5. The due date is automatically set to 14 days from the issue date

### Returning Books
1. Navigate to **Issue/Return** from the navigation menu
2. View all currently issued books in the table
3. Click "Return" button for the book being returned
4. If returned late, the fine will be automatically calculated and displayed
5. Fine rate: $5 per day after the due date

## Database Models

### Student Model
- `id`: Primary key
- `name`: Student's full name
- `email`: Unique email address
- `course`: Course/program enrolled in

### Book Model
- `id`: Primary key
- `title`: Book title
- `author`: Book author
- `book_type`: Type (textbook/reference)
- `course`: Related course (optional)
- `available`: Availability status

### Issue Model
- `id`: Primary key
- `student_id`: Foreign key to Student
- `book_id`: Foreign key to Book
- `issue_date`: Date of issuance
- `due_date`: Return due date (14 days from issue)
- `return_date`: Actual return date
- `fine`: Calculated fine amount
- `returned`: Return status

## Technologies Used

- **Backend**: Flask (Python web framework)
- **Database**: SQLite with SQLAlchemy ORM
- **Migrations**: Flask-Migrate
- **Frontend**: HTML5, CSS3
- **Templating**: Jinja2

## Configuration

The application uses the following default configurations (defined in `config.py`):

- **SECRET_KEY**: Used for session management (change in production)
- **DATABASE**: SQLite database (`library.db`)
- **SQLALCHEMY_TRACK_MODIFICATIONS**: Disabled for performance

To modify configurations, edit the `config.py` file or set environment variables.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the MIT License.

## Support

For issues, questions, or suggestions, please open an issue on GitHub.

## Future Enhancements

- User authentication and authorization
- Advanced search and filtering
- Book reservation system
- Email notifications for due dates
- Reports and analytics
- Export functionality (PDF, CSV)
- Barcode scanning for books
- Multiple copies of the same book
- Book categories and tags