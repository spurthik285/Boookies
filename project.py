from flask import * 
from flask_mysqldb import MySQL
import MySQLdb.cursors
from werkzeug.utils import secure_filename
import os
import re
from fpdf import FPDF
from datetime import datetime
from random import randint

date = datetime.now()

app=Flask(__name__)
app.secret_key = 'abc'

app.config['MYSQL_HOST']= 'localhost'
app.config['MYSQL_USER']= 'root'
app.config['MYSQL_PASSWORD']= 'mysql'
app.config['MYSQL_DB']= 'books'

UPLOAD_FOLDER = 'static/uploads'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

mysql = MySQL(app)

@app.route('/')
def home():
    if 'login' in session:
        cur = mysql.connection.cursor()
        query = "select * from addbook"
        cur.execute(query,)
        data = cur.fetchall()
        cur.close()
        return render_template("home.html", book=data)
    else:
        return redirect("/")   

@app.route('/catogary')
def catogary():
    return render_template("catogary.html")


@app.route('/profile')
def profile():
    return render_template("profile.html")

@app.route('/adminhome')
def adminhome():
    if 'login' in session:
        dispcat = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        dispcat.execute('select * from addcatogary')
        cat = dispcat.fetchall()
        dispcat.close()
        book = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        book.execute('select * from addbook')
        books = book.fetchall()
        book.close()
        return render_template("adminhome.html", cat = cat, books = books)
    else:
        return redirect("/adminlogin")

    
@app.route('/adminlogin', methods=['GET', 'POST'])
def adminlogin():
    if 'login' in session:
        return redirect('/adminhome')
    else:
        msg=''
        if request.method == 'POST' and 'username' in request.form  and 'password' in request.form:
            username = request.form['username']
            #email = request.form['email']
            password = request.form['password']
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM admin WHERE username = %s AND password = %s', (username, password))
            account = cursor.fetchone()
            if account:
                session['login'] = True
                session['username'] = account['username']
                # cursor.close()
                return redirect('/adminhome')
                # return render_template('adminhome.html', msg=msg)
            else:
                msg = 'Incorrect email/password!'
        return render_template('adminlogin.html', msg=msg)

@app.route('/adminlogout')
def adminlogout():
    session.pop('login', None)
    return redirect(url_for('adminlogin'))



@app.route('/addbook', methods = ['GET', 'POST'])
def addbook():
    if 'login' not in  session:
        return redirect('/adminhome')
    else:
        dispcat = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        dispcat.execute('select * from addcatogary')
        cat = dispcat.fetchall()
        print(cat)
        dispcat.close()
        msg = ''
        book = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        book.execute('select * from addbook')
        books = book.fetchall()
        book.close()
        
        if request.method == 'POST':
            # catname='0'
            # cur.execute('select * from addcatogary where catid=%s' %(session['cat_id']),)
            catid = request.form['catid']
            catname = request.form['cat_name']
            bookid = randint(10000000,99999999)
            bookname = request.form['book_name']
            edition = request.form['edition']
            authorname = request.form['author_name']
            coauthor = request.form['coauthor_name']
            bookdescription = request.form['book_description']
            profile = request.files['file']
            img = secure_filename(profile.filename)
            # profile.save(pro)
            profile.save(os.path.join(app.config['UPLOAD_FOLDER'], img))
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('INSERT INTO addbook values (%s, %s, %s, %s, %s, %s, %s, %s, %s)', (catid, catname, bookid, bookname, edition, authorname, coauthor, bookdescription, img))
            try:

                mysql.connection.commit()
                cursor.close()
                msg = "Book added Successfully!"
                book = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                book.execute('select * from addbook')
                books = book.fetchall()
                book.close()
                return render_template('addbook.html', msg = msg, cat = cat, books = books)
            except:
                book.close()
                msg = 'Please enter data correctly!!'
    return render_template('addbook.html', msg = msg, cat = cat, books = books)
    

@app.route('/addcatogary', methods = ['GET', 'POST'])
def addcatogary():
    if 'login' not in session:
        return redirect('/adminhome')
    else:
        catid = ''
        dispcat = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        dispcat.execute('select * from addcatogary where catid = %s',(catid,))
        cat = dispcat.fetchall()
        dispcat.close()
        #print(cat)
        dispcat = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        dispcat.execute('select * from addcatogary')
        cat = dispcat.fetchall()
        print(cat)
        dispcat.close()
        msg = ''
        # cat = ''
        if request.method == 'POST':
            catid = randint(100000,999999)
            catname = request.form['catname']
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            #return (request.form)
            cursor.execute('INSERT INTO addcatogary values (%s, %s)', (catid, catname))
            try:
                mysql.connection.commit()
                cursor.close()
                msg = "Category added Successfully"
                # session['cat_id'] = True
                dispcat = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                dispcat.execute('select * from addcatogary')
                cat = dispcat.fetchall()
                print(cat)
                dispcat.close()
                return render_template('addbook.html', msg = msg, cat = cat)
            except:
                cursor.close()
                msg = 'Please enter data correctly'

    return render_template('addcatogary.html', msg = msg, cat = cat)


@app.route('/edit/<catid>', methods = ['POST','GET'])
def edit(catid):
    cursor = mysql.connection.cursor()
    query = 'SELECT * FROM addcatogary WHERE catid = %s'
    cursor.execute(query,(catid,))
    data = cursor.fetchall()
    cursor.close()
    # print(data)
    return render_template('edit.html', cat = data)

@app.route('/update/<nid>', methods = ['POST'])
def update(nid):
    if request.method == 'POST':
        cat_name = request.form['cat_name']
        cursor = mysql.connection.cursor()
        query = 'UPDATE addcatogary SET cat_name = %s where catid = %s'
        cursor.execute(query,(cat_name,nid))
        flash('Category Updated Successfully')
        mysql.connection.commit()
        return redirect(url_for('addcatogary'))

@app.route('/delete/<nid>', methods = ['POST', 'GET'])
def delete(nid):
    cursor = mysql.connection.cursor()
    cursor.execute('DELETE FROM addcatogary where cat_name = {1}'.format(nid))
    mysql.connection.commit()
    print(nid)
    flash('Category Removed Successfully')
    return redirect(url_for('addcatogary'))

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if 'loggedin' in session:
        return redirect('/')
    else:
        msg=''
        if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
            #username = request.form['username']
            email = request.form['email']
            password = request.form['password']
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM userdata WHERE email = %s and password = %s', (email,password))
            account = cursor.fetchone()
            if account:
                session['loggedin'] = True
                session['email'] = account['email']
                session['username'] = account['username']
                msg = 'Logged in successfully!'
                return render_template('home.html', msg=msg)
            else:
                msg = 'Incorrect email/password!'
        return render_template('login.html', msg=msg)
        

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    #session.pop('id', None )
    #session.pop('username' , None)
    return redirect(url_for('home'))


@app.route('/register', methods = ['GET','POST'])
def register():
    if 'loggedin' in session:
        return redirect('/login')
    else:
        msg = ''
        if request.method == 'POST' and 'username' in request.form and 'email' in request.form and 'password' in request.form:
            username = request.form['username']
            email = request.form['email']
            password = request.form['password']
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM userdata WHERE username = %s and email = %s', (username, email))
            account = cursor.fetchone()
            if account:
                msg = 'Account already exists!'
            elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
                msg = 'Invalid email address!'
            elif not re.match(r'[A-Za-z0-9]+', username):
                msg = 'Username must contain only characters and numbers!'
            elif not username or not password or not email:
                msg = 'Please fill out the form !'
            else:
                cursor.execute('INSERT INTO userdata VALUES (%s, %s, %s)', (username, email, password))
                mysql.connection.commit()
                msg = 'You have successfully registered!'
            return render_template('login.html')
        elif request.method == 'POST':
            msg = 'Please fill out the form!'
        return render_template('register.html', msg = msg)  


@app.route('/upload')
def upload_form():
    return render_template('download.html')


@app.route('/download/report/pdf/', methods = ['GET', 'POST'])
def download_report():
    #catid = request.form.get('catid')
    now = date.today()
    cursor = mysql.connection.cursor()
    query = "SELECT book_id,cat_name,book_name FROM addbook"
    cursor.execute(query,)
    result = cursor.fetchall()
    pdf = FPDF()
    pdf.add_page()
    page_width = pdf.w - 2 * pdf.l_margin
    pdf.set_font('Times','B',14.0)
    pdf.cell(page_width, 0.0, "Book Report", align = 'C')
    pdf.ln(10)
    pdf.set_font('Times', 'B', 12.0)
    pdf.cell(page_width, 0.0, 'Date :- '+str(date.strftime("%d / %m / %y")), align = 'L')
    pdf.ln(10)
    pdf.set_font('Courier', '', 12)
    col_width = page_width/4
    pdf.ln(1)

    th = pdf.font_size
    i = 1
    pdf.cell(col_width,th,"Sr.No",border = 1)
    pdf.cell(col_width,th,"BookID",border = 1)
    pdf.cell(col_width,th,"CatName",border = 1)
    pdf.cell(col_width,th,"BookName",border = 1)
    pdf.ln(th)
    for row in result:
        pdf.cell(col_width, th, str(i), border = 1)
        pdf.cell(col_width, th, str(row[0]), border = 1)
        pdf.cell(col_width, th, row[1], border = 1)
        pdf.cell(col_width, th, row[2], border = 1)
        i = i+1
        pdf.ln(th)

    pdf.ln(10)

    pdf.set_font('Times','', 10.0)
    pdf.cell(page_width, 0.0, '- end of report -', align = 'C')

    return Response(pdf.output(dest = 'S').encode('latin-1'), mimetype = 'application/pdf', headers = {'Content-Disposition':'attachment; filename= books_report.pdf'})







if __name__ == '__main__':
    app.run(debug=True)