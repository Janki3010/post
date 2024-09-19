from flask import Flask, render_template, request, redirect, session
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'threadpost'

mysql = MySQL(app)
app.secret_key = '122231546788'


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        id = request.form['id']
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        mno = request.form['mno']

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO user (id,uname,email,password,mobile) values (%s,%s,%s,%s,%s)",
                    (id, name, email, password, mno))
        mysql.connection.commit()
        cur.close()
        return redirect('/login')
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM user where email = %s AND password = %s", (email, password))
        account = cur.fetchone()
        if account:
            session['uid'] = account[0]
            return redirect('/addPost')
    return render_template('login.html')


@app.route('/addPost', methods=['GET', 'POST'])
def addPost():
    if request.method == "POST":
        title = request.form['title']
        content = request.form['content']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO post (uid, title, content) VALUES (%s, %s, %s)", (session['uid'], title, content))

        mysql.connection.commit()
        cur.close()
        return redirect('/dashboard')
    return render_template('addPost.html')


@app.route('/update/<pid>', methods=['GET', 'POST'])
def update(pid):
    cur = mysql.connection.cursor()
    cur.execute("select * from post where id = %s", pid)
    posts = cur.fetchone()
    t = posts[2]
    c = posts[3]
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        cur.execute("update post set title=%s , content=%s where id = %s", (title, content, pid))
        mysql.connection.commit()
        cur.close()
        return redirect('/dashboard')

    return render_template('update.html', title=t, content=c)

@app.route('/delete/<pid>',methods=['POST'])
def delete(pid):
    cur = mysql.connection.cursor()
    cur.execute("delete from threadpost.post where id=%s", pid)
    mysql.connection.commit()
    cur.close()
    return redirect('/dashboard')

@app.route('/dashboard')
def dashboard():
    cur = mysql.connection.cursor()
    cur.execute(f"select * from post where uid = {session['uid']} ")
    posts = cur.fetchall()
    return render_template('dashboard.html', posts=posts)


if __name__ == '__main__':
    app.run()
