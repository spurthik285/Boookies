from flask import Flask, render_template, request, url_for, flash, redirect, send_from_directory
from flask_mysqldb import MySQL
import MySQLdb.cursors
from werkzeug.utils import secure_filename
import os
from random import randint

app = Flask(__name__)
app.secret_key = 'aa702881350703655f5a16243360d64d'


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'pratik23'
app.config['MYSQL_DB'] = 'db'

UPLOAD_FOLDER = 'static/uploads'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

mysql = MySQL(app)

@app.route('/',methods = ['GET', 'POST'])
def index():
    return render_template('home.html')

@app.route('/insert', methods = ['POST','GET'])
def insert():
    if request.method == "POST":
        id = randint(10000000,99999999)
        name = request.form['name']
        email = request.form['email']
        profile = request.files['file']
        pro = secure_filename(profile.filename)
        # profile.save(pro)
        profile.save(os.path.join(app.config['UPLOAD_FOLDER'], pro))
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor) #MySQLdb.cursors.DictCursor
        cur.execute('insert into stud values (%s, %s, %s, %s)',(id, name, email, pro))
        mysql.connection.commit()
        cur.close()
        print(pro)
        return redirect(url_for('index'))
    return render_template('insert.html')

@app.route('/select', methods = ['POST','GET'])
def admin():
    if request.method == "POST":
        sid = request.form.get('sid')
    cur = mysql.connection.cursor()
    query = "select * from db.stud where id = %s"
    cur.execute(query, (sid,))
    data = cur.fetchall()
    cur.close()
    return render_template("display.html", stud1=data)


#<!-----------------################ HTML Files ###############------------------------------!>

home.html file :-
<!DOCTYPE html>
<html lang="en" dir="ltr">
  <head>
    <meta charset="utf-8">
    <title>Python - Flask </title>
    <!-- Bootstrap CSS -->
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.5.3/dist/css/bootstrap.min.css" integrity="sha384-TX8t27EcRE3e/ihU7zmQxVncDAy5uIKz4rEkgIXeMed4M0jlfIDPvg6uqKI2xXr2" crossorigin="anonymous">

    <!-- Bootstrap Scripts -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@4.5.3/dist/js/bootstrap.bundle.min.js" integrity="sha384-ho+j7jyWK8fNQe+A12Hb8AhRq26LrZ/JpcUGGOn+Y7RsweNrtN/tE3MoK7ZeZDyx" crossorigin="anonymous"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
    <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js" integrity="sha384-DfXdz2htPH0lsSSs5nCTpuj/zy4C+OGpamoFVy38MVBnE+IbbVYUew+OrCXaRkfj" crossorigin="anonymous"></script>

    <!-- dataTables Scripts -->
    <script src="https://cdn.datatables.net/1.10.16/js/jquery.dataTables.js"></script>
    <script src="https://cdn.datatables.net/1.10.16/js/dataTables.bootstrap4.min.js"></script>
    <script src="https://cdn.datatables.net/keytable/2.6.1/js/dataTables.keyTable.min.js"></script>

    <!-- dataTables CSS -->
    <link rel="stylesheet" href="https://cdn.datatables.net/1.10.16/css/dataTables.bootstrap4.min.css">
    <link rel="stylesheet" href="https://cdn.datatables.net/keytable/2.6.1/css/keyTable.bootstrap4.min.css">
  </head>
  <body>
    <div>
      {% block body %}

      {% endblock %}
    </div>


    <script type="text/javascript">
        $(document).ready(function() {
          $('#example').DataTable( {
              "aLengthMenu": [[3, 5, 10, 25, -1], [3, 5, 10, 25, "All"]],
              "iDisplayLength":3
              // keys: true
          } );
        } );

        var loadFile = function(event) {
            var image = document.getElementById('output');
            image.src = URL.createObjectURL(event.target.files[0]);
        };

    </script>
  </body>
</html>




insert.html file :-

{% extends "home.html" %}
{% block body %}
  <div class="content">
      <form class="text" method = "post" action = "{{ url_for('insert') }}" enctype="multipart/form-data">
        <fieldset class="form-group">
            <legend class="border-bottom mb-4">Add Student</legend>
            <div class="form-group">
              <label>Name</label>
              <input type="text" name="name" required class="form-control">
            </div>
            <div class="form-group">
              <label>Email</label>
              <input type="email" name="email" required class="form-control">
            </div>
            <div class="form-group">
              <label>Profile Pic</label>
              <p><input type="file" name="file" accept="image/*" name="image" id="file"  onchange="loadFile(event)" style="display: none;"></p>
              <p><img id="output" width="89" /></p>
              <p><label for="file" name='file' style="cursor: pointer;" class="btn btn-primary">Upload Photo</label></p>
            </div>
         </fieldset>
          <div class="form-group">
            <button type="submit" class="btn btn-primary">Add Student</button>
          </div>
      </form>
  </div>

{% endblock %}


display.html file :-

{% extends "home.html" %}

{% block body %}
  <div class="col-md-8 text">
    <table id="example" class="table table-striped table-bordered table-dark table-hover" style="width:100%; margin-top:50px;">
      <thead>
        <tr>
          <th scope="col">ID</th>
          <th scope="col">Name</th>
          <th scope="col">Email</th>
          <th scope="col">Profile Pic</th>
        </tr>
      </thead>
      <tbody>
        {% for data in stud1 %}
          <tr>
            <th scope="row">{{ data[0] }}</th>
            <td>{{ data[1] }}</td>
            <td>{{ data[2] }}</td>
            <td>{{ data[3] }}</td>
          </tr>

        {% endfor %}
      </tbody>
    </table>
    <p>
      {% for data in stud1 %}
        {% set fn = namespace( filename = data[3]) %}
        <img src="{{url_for('static', filename='uploads/') }}{{ fn.filename }}" alt="{{fn.filename}}" width="400" height="400" />
      {% endfor %}
    </p>
  </div>
  <br><br><br><br><br><br><br><br><br><br><br>

{% endblock %}
