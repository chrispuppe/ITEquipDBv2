from flask import render_template, request, flash, redirect, url_for, session, app, make_response
from app import app, db
from app import models
from flask_login import LoginManager, login_user, login_required, logout_user
from datetime import datetime, timedelta
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length, EqualTo
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.sql import exists
import pdfkit


# validation and str to date for input
def string_to_date(d_string):
    try:
        new_date = datetime.strptime(d_string, '%m/%d/%Y')
    except:
        new_date = datetime.now().date()
    return new_date


# grabs a new employee list from DB
def fresh_employee_list():
    choose_employee = models.Employee.query.all()
    # Sort employees by name
    choose_employee.sort(key=lambda x: x.name, reverse=False)
    return choose_employee


#######################################################################
#  Session  #

# makes the session expire in 1 day instead of when you close the browser


@app.before_request
def make_session_permanent():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(days=1)


# Login  #

# Login manager setup using flask_login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


# gets the user from the database
@login_manager.user_loader
def load_user(user_id):
    return models.User.query.get(int(user_id))


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(),
                                                   Length(min=4, max=15)],
                           render_kw={"placeholder": "Username", "autofocus": ""})
    password = PasswordField('Password', validators=[InputRequired(),
                                                     Length(min=8, max=80)], render_kw={"placeholder": "Password"})
    remember = BooleanField('Remember Me')


class RegisterForm(FlaskForm):
    email = StringField('Email Address', validators=[InputRequired(), Email(message='Invalid email'),
                                                     Length(max=50)], render_kw={"placeholder": "Email Address"})
    username = StringField('Username', validators=[InputRequired(),
                                                   Length(min=4, max=15)],
                           render_kw={"placeholder": "Username", "autofocus": ""})
    password = PasswordField('Password', validators=[InputRequired(),
                                                     Length(min=8, max=80),
                                                     EqualTo('confirm', message='Passwords must match')],
                             render_kw={"placeholder": "Password"})
    confirm = PasswordField('Repeat Password', render_kw={"placeholder": "Repeat Password"})


@app.route('/')
def index():
    return redirect(url_for('all_employees'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    error = None

    # checks the username and password against the DB and logs the user in if valid
    if form.validate_on_submit():
        user = models.User.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                return redirect(url_for('all_employees'))
            else:
                error = "Invalid username or password. Please try again."

        # if not valid replies as such
        return render_template('login.html', form=form, error=error)

    return render_template('login.html', form=form)


# signs up a user to be able to use the site
# needs security to restrict users
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data,
                                                 method='sha256')
        new_user = models.User(username=form.username.data,
                               email=form.email.data,
                               password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('login'))

    else:
        pass

    return render_template('signup.html', form=form)


# User Administration #

@app.route('/admin', methods=['GET', 'POST'])
@login_required
def user_admin():
    users = models.User.query.all()

    return render_template('/user_admin.html', users=users)


#############################################################
#  User Add  #

@app.route('/add_user', methods=['GET', 'POST'])
@login_required
def user_add():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data,
                                                 method='sha256')
        new_user = models.User(username=form.username.data,
                               email=form.email.data,
                               password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('user_admin'))

    else:
        pass

    return render_template('user_add.html', form=form)


###################################################
# User Edit  #


@app.route('/edit_user/<int:id>', methods=['GET', 'POST'])
@login_required
def user_edit(id):
    user = models.User.query.get(id)

    form = RegisterForm(obj=user)

    if request.method == 'POST':
        user.username = form.username.data
        user.email = form.email.data,
        db.session.commit()

        return redirect(url_for('user_admin'))

    return render_template('user_edit.html', form=form, user=user)


###################################################
# User Password Edit  #


@app.route('/edit_user_password/<int:id>', methods=['GET', 'POST'])
@login_required
def user_edit_password(id):
    user = models.User.query.get(id)

    form = RegisterForm(obj=user)

    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data,
                                                 method='sha256')
        # if request.method == 'POST':
        #     user.username=form.username.data
        #     user.email=form.email.data,
        user.password = hashed_password
        db.session.commit()

        return redirect(url_for('user_admin'))

    else:
        pass

    return render_template('user_edit_password.html', form=form, user=user)


###################################################
#  User Delete  #


@app.route('/delete_user/<int:id>', methods=['GET', 'POST'])
@login_required
def user_delete(id):
    user = models.User.query.get(id)
    db.session.delete(user)
    db.session.commit()
    flash('deleted')

    return redirect(url_for('user_admin'))


#############################################################
#  Logout  #


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


################################################
#  Employees  #


@app.route('/employee')
@login_required
def all_employees():
    post = fresh_employee_list()
    return render_template('employee/employees.html', post=post)


@app.route('/employee/add', methods=['POST', 'GET'])
@login_required
def employee_add():
    # gathers POSTed info and creates an employee
    if request.method == 'POST':
        post = models.Employee(
            request.form['name_form'], request.form['skill_level_form'],
            request.form['email_address_form'], request.form['trade_form']
        )
        db.session.add(post)
        db.session.commit()

    else:
        pass

    return render_template('employee/add.html')


@app.route('/employee/edit/<int:id>', methods=['POST', 'GET'])
@login_required
def edit_employee(id):
    # Getting user by primary key:
    # Validate url to ensure id exists
    post = models.Employee.query.get(id)
    if not post:
        flash('Invalid post id: {0}'.format(id))
        return redirect(url_for('index'))

    # raise exception
    if request.method == 'POST':
        post.name = request.form.get('name_form')
        post.skill_level = request.form['skill_level_form']
        post.email_address = request.form['email_address_form']
        post.trade = request.form['trade_form']
        if 'inactive' in request.form:
            post.inactive = True
        else:
            post.inactive = False
        db.session.commit()
        return redirect(url_for('index'))
    else:
        return render_template('employee/edit.html', post=post)


@app.route('/employee/delete/<id>', methods=['POST', 'GET'])
@login_required
def delete_employee(id):
    employee = models.Employee.query.get(id)
    if not employee:
        flash('Invalid employee id: {0}'.format(id))
        return redirect(url_for('index'))

    error = None

    device_list = db.session.query(exists().where(models.Device.assigned_to == id))
    # Redirects to employee report if the employee has devices assigned to them
    if device_list.scalar():
        assigned_computers = models.Computers.query.all()
        assigned_phones = models.Phone_Account.query.all()
        assigned_printers = models.Printers.query.all()
        assigned_fobs = models.Fob.query.all()
        assigned_ipads = models.Ipads.query.all()
        error = "The current user still has devices assigned."

        return render_template('employee/employee_report.html', employee=employee,
                               assigned_computers=assigned_computers,
                               assigned_phones=assigned_phones,
                               assigned_fobs=assigned_fobs,
                               assigned_ipads=assigned_ipads,
                               assigned_printers=assigned_printers,
                               error=error)

    db.session.delete(employee)
    db.session.commit()
    flash('deleted')

    return redirect(url_for('index'))


#  Employee Report  #


@app.route('/employee/report/<int:id>', methods=['POST', 'GET'])
@login_required
def employee_report(id):
    # Getting user by primary key:
    # Validate url to ensure id exists
    employee = models.Employee.query.get(id)
    if not employee:
        flash('Invalid employee id: {0}'.format(id))
        return redirect(url_for('index'))
    # get device tables to get all user assigned items
    assigned_computers = models.Computers.query.all()
    assigned_phones = models.Phone_Account.query.all()
    assigned_printers = models.Printers.query.all()
    assigned_fobs = models.Fob.query.all()
    assigned_ipads = models.Ipads.query.all()
    # raise exception

    return render_template('employee/employee_report.html', employee=employee,
                           assigned_computers=assigned_computers,
                           assigned_phones=assigned_phones,
                           assigned_fobs=assigned_fobs,
                           assigned_ipads=assigned_ipads,
                           assigned_printers=assigned_printers)


#  Employee PDF Report  #

@app.route('/report/pdf/<int:id>', methods=['POST', 'GET'])
@login_required
def employee_report_pdf(id):
    # Getting user by primary key:
    # Validate url to ensure id exists
    employee = models.Employee.query.get(id)
    if not employee:
        flash('Invalid employee id: {0}'.format(id))
        return redirect(url_for('index'))
    # get device tables to get all user assigned items
    assigned_computers = models.Computers.query.all()
    assigned_phones = models.Phone_Account.query.all()
    assigned_printers = models.Printers.query.all()
    assigned_fobs = models.Fob.query.all()
    assigned_ipads = models.Ipads.query.all()
    # raise exception

    rendered_report = render_template('reports/pdf_employee_report.html', employee=employee,
                                      assigned_computers=assigned_computers,
                                      assigned_phones=assigned_phones,
                                      assigned_fobs=assigned_fobs,
                                      assigned_ipads=assigned_ipads,
                                      assigned_printers=assigned_printers)

    css = 'app/static/css/bootstrap.css'
    pdf_report = pdfkit.from_string(rendered_report, False, css=css)  # , configuration=pdfkit_config)

    pdf_response = make_response(pdf_report)
    pdf_response.headers['Content-type'] = 'application/pdf'
    pdf_response.headers['Content-Disposition'] = 'attachment; {}.pdf'.format(employee.name)

    return pdf_response


#  Computers  #


@app.route('/devices/computers', methods=['POST', 'GET'])
@login_required
def all_computers():
    post = models.Computers.query.all()
    employees = models.Employee.query.all()
    return render_template('/devices/computers.html', employees=employees, post=post)


@app.route('/devices/computer_add', methods=['POST', 'GET'])
@login_required
def computer_add():
    # gathers POSTed info and creates a computer
    employee_list = fresh_employee_list()
    # raise exception
    if request.method == 'POST':
        post = models.Computers(
            request.form['computer_name'], request.form['brand'],
            request.form['model'], request.form['serial'],
            request.form['computer_type'], request.form['operating_system'],
            request.form['notes'],
            string_to_date(request.form['aquired_date']),
            request.form['purchase_price'], request.form['vendor_id'],
            request.form['warranty_length'], request.form['assigned_to']
        )

        db.session.add(post)
        db.session.commit()
    return render_template('devices/computer_add.html', employee_list=employee_list)


@app.route('/devices/computer_edit/<int:id>', methods=['POST', 'GET'])
@login_required
def computer_edit(id):
    # new employee list for form
    employee_list = fresh_employee_list()

    # Validate url to ensure id exists
    post = models.Computers.query.get(id)
    if not post:
        flash('Invalid post id: {0}'.format(id))
        return redirect(url_for('index'))

    # raise exception
    if request.method == 'POST':
        # raise exception

        post.computer_name = request.form.get('computer_name')
        post.brand = request.form['brand']
        post.model = request.form['model']
        post.serial = request.form['serial']
        post.computer_type = request.form['computer_type']
        post.operating_system = request.form['operating_system']
        post.notes = request.form['notes']
        post.aquired_date = string_to_date(request.form['aquired_date'])
        post.purchase_price = request.form['purchase_price']
        post.vendor_id = request.form['vendor_id']
        post.warranty_length = request.form['warranty_length']
        post.assigned_to = request.form['assigned_to']

        db.session.commit()
        return redirect(url_for('all_computers'))
    else:
        return render_template('devices/computer_edit.html', employee_list=employee_list,
                               post=post)


@app.route('/devices/computer_delete/<id>', methods=['POST', 'GET'])
@login_required
def delete_computer(id):
    post = models.Computers.query.get(id)
    db.session.delete(post)
    db.session.commit()
    flash('deleted')

    return redirect(url_for('all_computers'))


# Phones  #


@app.route('/devices/phones', methods=['POST', 'GET'])
@login_required
def all_phones():
    post = models.Phone_Account.query.all()
    employees = models.Employee.query.all()
    return render_template('/devices/phones.html', employees=employees, post=post)


@app.route('/devices/phone_add', methods=['POST', 'GET'])
@login_required
def phone_add():
    # gathers POSTed info and creates a phone
    employee_list = fresh_employee_list()
    # raise exception
    if request.method == 'POST':
        post = models.Phone_Account(
            request.form['phone_number'], request.form['phone_model'],
            request.form['phone_os'], request.form['notes'],
            request.form['assigned_to']
        )
        db.session.add(post)
        db.session.commit()
    return render_template('devices/phone_add.html', employee_list=employee_list)


@app.route('/devices/phone_edit/<int:id>', methods=['POST', 'GET'])
@login_required
def phone_edit(id):
    # new employee list for form
    employee_list = fresh_employee_list()

    # Validate url to ensure id exists
    post = models.Phone_Account.query.get(id)
    if not post:
        flash('Invalid post id: {0}'.format(id))
        return redirect(url_for('index'))

    # raise exception
    if request.method == 'POST':
        # raise exception

        post.phone_number = request.form['phone_number']
        post.phone_model = request.form['phone_model']
        post.phone_os = request.form['phone_os']
        post.notes = request.form['notes']
        post.assigned_to = request.form['assigned_to']

        db.session.commit()
        return redirect(url_for('all_phones'))
    else:
        return render_template('devices/phone_edit.html', employee_list=employee_list,
                               post=post)


@app.route('/devices/phone_delete/<id>', methods=['POST', 'GET'])
@login_required
def phone_delete(id):
    post = models.Phone_Account.query.get(id)
    db.session.delete(post)
    db.session.commit()
    flash('deleted')

    return redirect(url_for('all_phones'))


#  FOB  #
@app.route('/devices/fobs', methods=['POST', 'GET'])
@login_required
def all_fobs():
    post = models.Fob.query.all()
    employees = models.Employee.query.all()
    return render_template('/devices/fobs.html', employees=employees, post=post)


@app.route('/devices/fob_add', methods=['POST', 'GET'])
@login_required
def fob_add():
    # gathers POSTed info and creates a fob
    employee_list = fresh_employee_list()
    # raise exception
    if request.method == 'POST':
        post = models.Fob(
            request.form['fob_number'], request.form['fob_serial'],
            request.form['assigned_to']
        )
        db.session.add(post)
        db.session.commit()
    return render_template('devices/fob_add.html', employee_list=employee_list)


@app.route('/devices/fob_edit/<int:id>', methods=['POST', 'GET'])
@login_required
def fob_edit(id):
    # new employee list for form
    employee_list = fresh_employee_list()

    # Validate url to ensure id exists
    post = models.Fob.query.get(id)
    if not post:
        flash('Invalid post id: {0}'.format(id))
        return redirect(url_for('index'))

    # raise exception
    if request.method == 'POST':
        # raise exception

        post.fob_number = request.form['fob_number']
        post.fob_serial = request.form['fob_serial']
        post.assigned_to = request.form['assigned_to']

        db.session.commit()
        return redirect(url_for('all_fobs'))
    else:
        return render_template('devices/fob_edit.html', employee_list=employee_list,
                               post=post)


@app.route('/devices/fob_delete/<id>', methods=['POST', 'GET'])
@login_required
def fob_delete(id):
    post = models.Fob.query.get(id)
    db.session.delete(post)
    db.session.commit()
    flash('deleted')

    return redirect(url_for('all_fobs'))


#  iPad  #
@app.route('/devices/ipads', methods=['POST', 'GET'])
@login_required
def all_ipads():
    post = models.Ipads.query.all()
    employees = models.Employee.query.all()
    return render_template('/devices/ipads.html', employees=employees, post=post)


@app.route('/devices/ipad_add', methods=['POST', 'GET'])
@login_required
def ipad_add():
    # gathers POSTed info and creates a iPad
    employee_list = fresh_employee_list()
    # raise exception
    if request.method == 'POST':
        post = models.Ipads(
            request.form['serial'], request.form['model'],
            request.form['storage_capacity'], string_to_date(request.form['date_purchased']),
            request.form['assigned_to']
        )
        db.session.add(post)
        db.session.commit()
    return render_template('devices/ipad_add.html', employee_list=employee_list)


@app.route('/devices/ipad_edit/<int:id>', methods=['POST', 'GET'])
@login_required
def ipad_edit(id):
    # new employee list for form
    employee_list = fresh_employee_list()

    # Validate url to ensure id exists
    post = models.Ipads.query.get(id)
    if not post:
        flash('Invalid post id: {0}'.format(id))
        return redirect(url_for('index'))

    # raise exception
    if request.method == 'POST':
        # raise exception

        post.serial = request.form['serial']
        post.model = request.form['model']
        post.storage_capacity = request.form['storage_capacity']
        post.date_purchased = string_to_date(request.form['date_purchased'])
        post.assigned_to = request.form['assigned_to']

        db.session.commit()
        return redirect(url_for('all_ipads'))
    else:
        return render_template('devices/ipad_edit.html', employee_list=employee_list,
                               post=post)


@app.route('/devices/ipad_delete/<id>', methods=['POST', 'GET'])
@login_required
def ipad_delete(id):
    post = models.Ipads.query.get(id)
    db.session.delete(post)
    db.session.commit()
    flash('deleted')

    return redirect(url_for('all_phones'))


#  Printer  #
@app.route('/devices/printers', methods=['POST', 'GET'])
@login_required
def all_printers():
    post = models.Printers.query.all()
    employees = models.Employee.query.all()
    return render_template('/devices/printers.html', employees=employees, post=post)


@app.route('/devices/printer_add', methods=['POST', 'GET'])
@login_required
def printer_add():
    # gathers POSTed info and creates a printer
    employee_list = fresh_employee_list()
    # raise exception
    if request.method == 'POST':
        post = models.Printers(
            request.form['brand'], request.form['model'],
            request.form['printer_type'], request.form['serial'],
            string_to_date(request.form['aquired_date']),
            request.form['vendor_id'], request.form['assigned_to']
        )
        db.session.add(post)
        db.session.commit()
    else:
        pass
    return render_template('devices/printer_add.html', employee_list=employee_list)


@app.route('/devices/printer_edit/<int:id>', methods=['POST', 'GET'])
@login_required
def printer_edit(id):
    # new employee list for form
    employee_list = fresh_employee_list()

    # Validate url to ensure id exists
    post = models.Printers.query.get(id)
    if not post:
        flash('Invalid post id: {0}'.format(id))
        return redirect(url_for('index'))

    # raise exception
    if request.method == 'POST':
        # raise exception

        post.brand = request.form['brand']
        post.model = request.form['model']
        post.printer_type = request.form['printer_type']
        post.aquired_date = string_to_date(request.form['aquired_date'])
        post.vendor_id = request.form['vendor_id']
        post.assigned_to = request.form['assigned_to']

        db.session.commit()
        return redirect(url_for('all_printers'))
    else:
        return render_template('devices/printer_edit.html', employee_list=employee_list,
                               post=post)


@app.route('/devices/printer_delete/<int:id>', methods=['POST', 'GET'])
@login_required
def printer_delete(id):
    post = models.Printers.query.get(id)
    db.session.delete(post)
    db.session.commit()
    flash('deleted')

    return redirect(url_for('all_printers'))
