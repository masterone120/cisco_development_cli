import sys
import time
import mysql
from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Length
import paramiko
import MySQLdb as mdb
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)
app.secret_key = "Secret Key"

# SqlAlchemy Database Configuration With Mysql
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost/crud'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


# Creating model table for our CRUD database
class Data(db.Model):
    id_data = db.Column(db.Integer, primary_key=True)
    device = db.Column(db.String(100))
    directory_no = db.Column(db.String(100))
    phone_mac = db.Column(db.String(100))
    user_directory = db.Column(db.String(100))
    password_directory = db.Column(db.String(100))
    display_name = db.Column(db.String(100))
    line1 = db.Column(db.String(100))
    line2 = db.Column(db.String(100))

    def __init__(self, device, directory_no, phone_mac, user_directory, password_directory, display_name, line1, line2):
        self.device = device
        self.directory_no = directory_no
        self.phone_mac = phone_mac
        self.user_directory = user_directory
        self.password_directory = password_directory
        self.display_name = display_name
        self.line1 = line1
        self.line2 = line2


class Devices(db.Model):
    id_devices = db.Column(db.Integer, primary_key=True)
    platform = db.Column(db.String(100))
    ipaddress_platform = db.Column(db.String(100))
    username_platform = db.Column(db.String(100))
    password_platform = db.Column(db.String(100))
    name_platform = db.Column(db.String(100))
    protocol_platform = db.Column(db.String(100))

    def __init__(self, platform, ipaddress_platform, username_platform, password_platform, name_platform,
                 protocol_platform):
        self.platform = platform
        self.ipaddress_platform = ipaddress_platform
        self.username_platform = username_platform
        self.password_platform = password_platform
        self.name_platform = name_platform
        self.protocol_platform = protocol_platform


class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    email = db.Column(db.String(100))
    password = db.Column(db.String(100))

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('remember me')


class RegisterForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Length(min=4, max=80)])
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])


@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')


# This is the index route where we are going to
# query on all our employee data
@app.route('/')
@login_required
def Index():
    return redirect(url_for('dashboard'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                return redirect(url_for('Index'))
        return redirect(url_for('login'))
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_user = Users(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return '<h1> New User Has Been Created!'

    return render_template('signup.html', form=form)


# this route is for inserting data to mysql database via html forms
@app.route('/insert', methods=['GET', 'POST'])
def insert():
    page = request.args.get('page', 1, type=int)
    all_data = Data.query.paginate(page=page, per_page=10)

    all_devices = Devices.query.all()

    if request.method == 'POST':
        device = request.form['device']
        directory_no = request.form['directory_no']
        phone_mac = request.form['phone_mac']
        user_directory = request.form['user_directory']
        password_directory = request.form['password_directory']
        display_name = request.form['display_name']
        line1 = request.form['line1']
        line2 = request.form['line2']

        my_data = Data(device, directory_no, phone_mac, user_directory, password_directory, display_name, line1, line2)
        db.session.add(my_data)
        db.session.commit()

        flash("Phone Device Inserted Successfully")

        return redirect(url_for('dashboard'))
    return render_template("insert.html", employees=all_data, all_devices=all_devices)


# this is our update route where we are going to update our employee
@app.route('/update', methods=['GET', 'POST'])
def update():
    if request.method == 'POST':
        my_data = Data.query.get(request.form.get('id_data'))

        my_data.device = request.form['device']
        my_data.directory_no = request.form['directory_no']
        my_data.phone_mac = request.form['phone_mac']
        my_data.user_directory = request.form['user_directory']
        my_data.password_directory = request.form['password_directory']
        my_data.display_name = request.form['display_name']
        my_data.line1 = request.form['line1']
        my_data.line2 = request.form['line2']

        db.session.commit()
        flash("Phone Device Updated Successfully")

        return redirect(url_for('Index'))


# This route is for deleting our employee
@app.route('/delete/<id_data>/', methods=['GET', 'POST'])
def delete(id_data):
    my_data = Data.query.get(id_data)
    db.session.delete(my_data)
    db.session.commit()
    flash("Phone Device Deleted Successfully")

    return redirect(url_for('Index'))


@app.route('/devices', methods=['GET', 'POST'])
def devices():
    if request.method == 'POST':
        platform = request.form['platform']
        ipaddress_platform = request.form['ipaddress_platform']
        username_platform = request.form['username_platform']
        password_platform = request.form['password_platform']
        name_platform = request.form['name_platform']
        protocol_platform = request.form['protocol_platform']
        my_devices = Devices(platform, ipaddress_platform, username_platform, password_platform, name_platform,
                             protocol_platform)
        db.session.add(my_devices)
        db.session.commit()
        flash('Add Device Successfully!')

    devices_all = Devices.query.all()
    return render_template('devices.html', devices_all=devices_all)


@app.route('/edevices', methods=['GET', 'POST'])
def edvices():
    if request.method == 'POST':
        my_devices = Devices.query.get(request.form.get('id_devices'))
        my_devices.platform = request.form['platform']
        my_devices.name_platform = request.form['name_platform']
        my_devices.ipaddress_platform = request.form['ipaddress_platform']
        my_devices.username_platform = request.form['username_platform']
        my_devices.password_platform = request.form['password_platform']
        my_devices.protocol_platform = request.form['protocol_platform']
        db.session.commit()

        flash('Edit device successfully!')

        return redirect(url_for('devices'))


@app.route('/ddevices/<id_devices>/', methods=['GET', 'POST'])
def ddevices(id_devices):
    my_devices = Devices.query.get(id_devices)
    db.session.delete(my_devices)
    db.session.commit()
    flash("Device Deleted Successfully")

    return redirect(url_for('devices'))


@app.route('/trunk', methods=['GET', 'POST'])
@login_required
def trunk():
    return render_template('trunks/inout.html')


@app.route('/excute/', methods=['GET', 'POST'])
def excute():
    con = mdb.connect('localhost', 'root', 'root', 'crud')

    cur = con.cursor()
    id = request.form.get('id_datas')
    cur.execute(
        "SELECT id_data,device,directory_no,phone_mac,display_name,line1,line2  FROM `crud`.`data` WHERE id_data=%s " % id)

    ver = cur.fetchone()
    device = str(ver[1])
    cur.execute(
        "SELECT id_devices,platform,name_platform,ipaddress_platform,username_platform,password_platform,protocol_platform  FROM `crud`.`devices` WHERE name_platform='%s' " % device)

    ver2 = cur.fetchone()

    b_lines1 = [row for row in ver]
    b_lines2 = [row for row in ver2]

    return render_template('excute.html', b_lines1=b_lines1, b_lines2=b_lines2)


@app.route('/resulted/', methods=['GET', 'POST'])
def resulted():
    con = mdb.connect('localhost', 'root', 'root', 'crud')

    cur = con.cursor()
    ids = request.form.get('id_devicess')
    cur.execute(
        "SELECT id_devices,platform,name_platform,ipaddress_platform,username_platform,password_platform,protocol_platform  FROM `crud`.`devices` WHERE id_devices='%s' " % ids)

    ver11 = cur.fetchone()
    device = str(ver11[2])
    cur.execute(
        "SELECT id_data,device,directory_no,phone_mac,display_name,line1,line2  FROM `crud`.`data` WHERE device='%s' " % device)

    ver22 = cur.fetchone()
    ssh = paramiko.SSHClient()

    ipaddress_platform = ver11[3]
    username_platform = ver11[4]
    password_platform = ver11[5]
    protocol_platform = ver11[6]
    if protocol_platform == 'Telnet':
        protocol_platform = 23
    else:
        protocol_platform = 22
    # Load SSH host keys.
    ssh.load_system_host_keys()
    # Add SSH host key automatically if needed.
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # Connect to router using username/password authentication.
    ssh.connect(ipaddress_platform,
                port=protocol_platform,
                username=username_platform,
                password=password_platform,
                look_for_keys=False)

    # Run command.
    chan = ssh.invoke_shell()

    # turn off paging
    chan.send('terminal length 0\n')
    time.sleep(1)
    resp = chan.recv(9999)
    output = resp.decode('ascii').split(',')
    # print (''.join(output))

    # Display output of first command
    chan.send('conf t')
    chan.send('\n')
    time.sleep(1)
    resp = chan.recv(9999)
    output = resp.decode('ascii').split(',')
    print(''.join(output))

    # Display output of second command
    chan.send('do sho int status')
    chan.send('\n')
    time.sleep(1)
    resp = chan.recv(9999)
    output = resp.decode('ascii').split(',')
    print(''.join(output))

    # Close connection.
    ssh.close()

    # Analyze show ip route output

    with open('outputed.txt', 'w') as f:
        for line in output:
            f.writelines(line)

    # return redirect(url_for('devices'))
    flash("Deploy Configuration was Successfully!")

    return render_template('resulted.html')


if __name__ == "__main__":
    app.run(debug=True)
