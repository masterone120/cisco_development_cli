from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

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
    directory_no = db.Column(db.Integer(1000))
    phone_mac = db.Column(db.String(100))
    user_directory = db.Column(db.Integer(1000))
    pass_directory = db.Column(db.String(100))
    display_name = db.Column(db.String(100))
    line1 = db.Column(db.Integer(1000))
    line2 = db.Column(db(db.Integer(1000)))

    def __init__(self, device, directory_no, phone_mac, user_directory, pass_directory, display_name, line1, line2):
        self.device = device
        self.directory_no = directory_no
        self.phone_mac = phone_mac
        self.user_directory = user_directory
        self.pass_directory = pass_directory
        self.display_name = display_name
        self.line1 = line1
        self.line2 = line2


# This is the index route where we are going to
# query on all our employee data
@app.route('/')
def Index():
    all_data = Data.query.all()

    return render_template("index.html", employees=all_data)


# this route is for inserting data to mysql database via html forms
@app.route('/insert', methods=['POST'])
def insert():
    if request.method == 'POST':
        device = request.form['device']
        directory_no = request.form['directory_no']
        phone_mac = request.form['phone_mac']
        user_directory = request.form['user_directory']
        pass_directory = request.form['pass_directory']
        display_name = request.form['display_name']
        line1 = request.form['line1']
        line2 = request.form['line2']

        my_data = Data(device, directory_no, phone_mac, user_directory, pass_directory, display_name, line1, line2)
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
        my_data.pass_directory = request.form['pass_directory']
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


if __name__ == "__main__":
    app.run(debug=True)
