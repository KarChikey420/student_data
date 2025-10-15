from flask import Flask,jsonify,request,render_template,redirect,url_for
import psycopg2
import psycopg2.extras 
from dotenv import load_dotenv
import os

load_dotenv()

app=Flask(__name__)

def get_db_connection():
    conn=psycopg2.connect(
        user=os.getenv('user'),
        host=os.getenv('host'),
        password=os.getenv('password'),
        port=os.getenv('port'),
        database=os.getenv('database')
    )
    print("Database connection established")
    cursor=conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    return cursor,conn

@app.route('/')
def index():
    cursor,conn=get_db_connection()
    cursor.execute('select * from students')
    students=cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('index.html',students=students)

@app.route('/add_student',methods=['GET','POST'])
def add_student():
    cursor,conn=get_db_connection()
    if request.method=='POST':
        name=request.form['name']
        age=request.form['age']
        email=request.form['email']
        cursor.execute('insert into students (name,age,email) values (%s,%s,%s)',(name,age,email))
        conn.commit()
        cursor.close()
        return redirect(url_for('index'))
    return render_template('add_student.html')

@app.route('/edit_student/<int:id>',methods=['GET','POST'])
def edit_student(id):
    cursor,conn=get_db_connection()
    if request.method=='POST':
        name=request.form['name']
        age=request.form['age']
        email=request.form['email']
        cursor.execute('update students set name=%s,age=%s,email=%s where id=%s',(name,age,email,id))
        conn.commit()
        cursor.close()
        return redirect(url_for('index'))
    cursor.execute('select * from students where id=%s',(id,))
    student=cursor.fetchone()
    cursor.close()
    return render_template('edit_student.html',student=student)

@app.route('/delete_student/<int:id>')
def delete_student(id):
    cursor,conn=get_db_connection()
    cursor.execute('delete from students where id=%s', (id, ))
    conn.commit()
    cursor.close()
    return redirect(url_for('index'))

if __name__=='__main__':
    app.run(debug=True)
    