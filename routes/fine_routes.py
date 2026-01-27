from flask import Blueprint, render_template, request
from models import db, Issue, Student, Book
from datetime import datetime, timedelta

bp = Blueprint('fines', __name__, url_prefix='/fines')

@bp.route('/')
def fine_calculator():
    # Get all issues with fines
    all_issues = Issue.query.all()
    
    # Calculate current fines
    for issue in all_issues:
        issue.calculate_fine()
    db.session.commit()
    
    # Get issues with fines
    issues_with_fines = [issue for issue in all_issues if issue.fine > 0]
    
    # Calculate total fines
    total_fines = sum(issue.fine for issue in issues_with_fines)
    total_outstanding = sum(issue.fine for issue in issues_with_fines if not issue.returned)
    total_collected = sum(issue.fine for issue in issues_with_fines if issue.returned)
    
    return render_template('fine_calculator.html', 
                         issues=issues_with_fines,
                         total_fines=total_fines,
                         total_outstanding=total_outstanding,
                         total_collected=total_collected)

@bp.route('/calculate', methods=['POST'])
def calculate_fine():
    """Calculate fine based on manual input"""
    try:
        days_late = int(request.form.get('days_late', 0))
        fine_rate = float(request.form.get('fine_rate', 5.0))
        
        calculated_fine = days_late * fine_rate
        
        return render_template('fine_calculator.html',
                             manual_calculation={
                                 'days_late': days_late,
                                 'fine_rate': fine_rate,
                                 'calculated_fine': calculated_fine
                             })
    except (ValueError, TypeError):
        return render_template('fine_calculator.html',
                             error="Invalid input. Please enter valid numbers.")
