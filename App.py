from flask import Flask, render_template, request, redirect, url_for, flash, Response
from flask_sqlalchemy import SQLAlchemy
import paramiko
import MySQLdb as mdb
import sys

app = Flask(__name__)
app.secret_key = "Secret Key"

# SqlAlchemy Database Configuration With Mysql
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost/crud'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# Creating model table for our CRUD database
class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
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
    id = db.Column(db.Integer, primary_key=True)
    platform = db.Column(db.String(100))
    ipaddress_platform = db.Column(db.String(100))
    username_platform = db.Column(db.String(100))
    password_platform = db.Column(db.String(100))
    name_platform = db.Column(db.String(100))

    def __init__(self, platform, ipaddress_platform, username_platform, password_platform, name_platform):
        self.platform = platform
        self.ipaddress_platform = ipaddress_platform
        self.username_platform = username_platform
        self.password_platform = password_platform
        self.name_platform = name_platform



# This is the index route where we are going to
# query on all our employee data
@app.route('/')
def Index():
    page = request.args.get('page', 1, type=int)
    all_data = Data.query.paginate(page=page, per_page=10)

    all_devices = Devices.query.all()

    return render_template("index.html", employees=all_data, all_devices=all_devices)


# this route is for inserting data to mysql database via html forms
@app.route('/insert', methods=['POST'])
def insert():
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

        return redirect(url_for('Index'))


# this is our update route where we are going to update our employee
@app.route('/update', methods=['GET', 'POST'])
def update():
    if request.method == 'POST':
        my_data = Data.query.get(request.form.get('id'))

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
@app.route('/delete/<id>/', methods=['GET', 'POST'])
def delete(id):
    my_data = Data.query.get(id)
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
        my_devices = Devices(platform, ipaddress_platform, username_platform, password_platform, name_platform)
        db.session.add(my_devices)
        db.session.commit()
        flash('Add Device Successfully!')

    devices_all = Devices.query.all()
    return render_template('devices.html', devices_all=devices_all)


@app.route('/edevices', methods=['GET', 'POST'])
def edvices():
    if request.method == 'POST':
        my_devices = Devices.query.get(request.form.get('id'))
        my_devices.platform = request.form['platform']
        my_devices.name_platform = request.form['name_platform']
        my_devices.ipaddress_platform = request.form['ipaddress_platform']
        my_devices.username_platform = request.form['username_platform']
        my_devices.password_platform = request.form['password_platform']
        db.session.commit()

        flash('Edit device successfully!')
        return redirect(url_for('devices'))


@app.route('/ddevices/<id>/', methods=['GET', 'POST'])
def ddevices(id):
    my_devices = Devices.query.get(id)
    db.session.delete(my_devices)
    db.session.commit()
    flash("Device Deleted Successfully")

    return redirect(url_for('devices'))


@app.route('/excute/', methods=['GET'])
def excute():
    con = None
    try:
        con = mdb.connect('localhost', 'root', 'root', 'crud')

        cur = con.cursor()

        # my_data = Devices.query.get(request.form.get('id'))

        cur.execute("SET @ids :=3;")

        cur.execute(
            "SELECT platform,name_platform,ipaddress_platform,password_platform,username_platform  FROM `crud`.`devices` WHERE id=@ids ;")

        ver = cur.fetchone()
        # ssh_client = paramiko.SSHClient()
        # ssh_client.connect(hostname='hostname', username=ver[3], password=ver[4])

        print(ver[1])

    except mdb.Error as e:

        print("Error %d: %s" % (e.args[0], e.args[1]))
        sys.exit(1)

    finally:

        if con:
            con.close()

    # ssh = paramiko.SSHClient()
    #
    # # Load SSH host keys.
    # ssh.load_system_host_keys()
    # # Add SSH host key automatically if needed.
    # ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # # Connect to router using username/password authentication.
    # ssh.connect(my_devices.ipaddress_platform,
    #             username=my_devices.username_platform,
    #             password=my_devices.password_platform,
    #             look_for_keys=False)
    #
    # # Run command.
    # ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("sho int status | begin Gi")
    #
    # output = ssh_stdout.readlines()
    #
    # # Close connection.
    # ssh.close()
    #
    # # Analyze show ip route output
    #
    # with open('outputed.txt', 'w') as f:
    #     for line in output:
    #         f.writelines(line)
    #
    # b_lines = [row for row in (list(open("outputed.txt")))]
    #
    # return render_template('excute.html', b_lines=b_lines)

    # for line in output:
    #          yield line
    #
    # return Response(g(), mimetype='text/html')
    # datas = Data.query.all()
    # return render_template("excute.html", datas=datas)


if __name__ == "__main__":
    app.run(debug=True)
