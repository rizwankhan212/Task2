from flask import render_template, redirect, url_for, flash, request, abort
from flask_login import login_user, logout_user, login_required, current_user
from database import db
from models import User, Employee
from forms import LoginForm, EmployeeForm, RegisterForm
from datetime import datetime

def configure_routes(app):

    @app.route('/')
    @login_required
    def index():
        return redirect(url_for('dashboard'))

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if current_user.is_authenticated:
            return redirect(url_for('dashboard'))
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()
            if user and user.check_password(form.password.data) and user.is_admin: # Only admin can log in
                login_user(user)
                flash('Logged in successfully!', 'success')
                return redirect(url_for('dashboard'))
            else:
                flash('Invalid username, password, or not an administrator.', 'danger')
        return render_template('login.html', form=form)

    @app.route('/register', methods=['GET', 'POST'])
    @login_required
    def register():
        if not current_user.is_admin:
            abort(403) # Forbidden
        form = RegisterForm()
        if form.validate_on_submit():
            existing_user = User.query.filter_by(username=form.username.data).first()
            if existing_user:
                flash('Username already exists. Please choose a different one.', 'danger')
            else:
                user = User(username=form.username.data, is_admin=True) # New users created via register are admins
                user.set_password(form.password.data)
                db.session.add(user)
                db.session.commit()
                flash('New administrator registered successfully!', 'success')
                return redirect(url_for('dashboard')) # Or redirect to user management page
        return render_template('register.html', form=form)


    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        flash('You have been logged out.', 'info')
        return redirect(url_for('login'))

    @app.route('/dashboard')
    @login_required
    def dashboard():
        return render_template('dashboard.html')

    # Employee CRUD Operations

    @app.route('/employees')
    @login_required
    def list_employees():
        employees = Employee.query.all()
        return render_template('employees/list.html', employees=employees)

    @app.route('/employees/create', methods=['GET', 'POST'])
    @login_required
    def create_employee():
        form = EmployeeForm()
        if form.validate_on_submit():
            # Check if email already exists
            existing_employee = Employee.query.filter_by(email=form.email.data).first()
            if existing_employee:
                flash('An employee with this email already exists.', 'danger')
                return render_template('employees/create.html', form=form)

            new_employee = Employee(
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                email=form.email.data,
                phone=form.phone.data,
                position=form.position.data,
                hire_date=form.hire_date.data,
                salary=form.salary.data
            )
            db.session.add(new_employee)
            db.session.commit()
            flash('Employee added successfully!', 'success')
            return redirect(url_for('list_employees'))
        return render_template('employees/create.html', form=form)

    @app.route('/employees/<int:employee_id>')
    @login_required
    def view_employee(employee_id):
        employee = Employee.query.get_or_404(employee_id)
        # Add this line to create and populate the form
        form = EmployeeForm(obj=employee) 
        # Pass the form object to the template
        return render_template('employees/view.html', employee=employee, form=form) 
    
    @app.route('/employees/<int:employee_id>/edit', methods=['GET', 'POST'])
    @login_required
    def edit_employee(employee_id):
        employee = Employee.query.get_or_404(employee_id)
        form = EmployeeForm(obj=employee) # Populate form with existing data

        if form.validate_on_submit():
            # Check for email conflicts with other employees
            existing_employee_with_email = Employee.query.filter(
                Employee.email == form.email.data,
                Employee.id != employee_id
            ).first()
            if existing_employee_with_email:
                flash('Another employee with this email already exists.', 'danger')
                return render_template('employees/edit.html', form=form, employee=employee)

            form.populate_obj(employee) # Update employee object with form data
            db.session.commit()
            flash('Employee updated successfully!', 'success')
            return redirect(url_for('view_employee', employee_id=employee.id))
        return render_template('employees/edit.html', form=form, employee=employee)

    @app.route('/employees/<int:employee_id>/delete', methods=['POST'])
    @login_required
    def delete_employee(employee_id):
        employee = Employee.query.get_or_404(employee_id)
        db.session.delete(employee)
        db.session.commit()
        flash('Employee deleted successfully!', 'success')
        return redirect(url_for('list_employees'))