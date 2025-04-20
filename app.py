from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv
import re

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "chronicle_secret_2025")

DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', 'dbs123'),
    'database': os.getenv('DB_NAME', 'new')
}

def get_db_connection():
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
    return None

def generate_id(prefix, table, id_column):
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = cursor.fetchone()[0]
            new_id = f"{prefix}{str(count + 1).zfill(4)}"
            cursor.execute(f"SELECT * FROM {table} WHERE {id_column} = %s", (new_id,))
            if cursor.fetchone():
                return generate_id(prefix, table, id_column)
            return new_id
        except Error as e:
            print(f"Error generating ID: {e}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
    return f"{prefix}0001"  

def validate_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def get_newsgroups():
    connection = get_db_connection()
    newsgroups = []
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT NewsGroupID, NewsGroupName FROM NewsGroup")
            newsgroups = cursor.fetchall()
        except Error as e:
            print(f"Error fetching newsgroups: {e}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
    return newsgroups

@app.route('/')
def index():
    newsgroups = get_newsgroups()
    return render_template('index.html', newsgroups=newsgroups)

@app.route('/register_user', methods=['POST'])
def register_user():
    if request.method == 'POST':
        name = request.form.get('userName')
        email = request.form.get('userEmail')
        password = request.form.get('userPassword')
        
        # Validate inputs
        if not all([name, email, password]):
            flash('All fields are required', 'error')
            return redirect(url_for('index'))
        
        if not validate_email(email):
            flash('Invalid email format', 'error')
            return redirect(url_for('index'))
        
        connection = get_db_connection()
        if connection:
            try:
                cursor = connection.cursor()
                
                cursor.execute("SELECT * FROM Users WHERE Email = %s", (email,))
                if cursor.fetchone():
                    flash('Email already registered', 'error')
                    return redirect(url_for('index'))
                
                user_id = generate_id('U', 'Users', 'User_ID')
                query = """
                INSERT INTO Users (User_ID, name, password, Email, Total_Articles_Read, Total_Articles_Rated, Last_Active_Date)
                VALUES (%s, %s, %s, %s, %s, %s, CURDATE())
                """
                cursor.execute(query, (user_id, name, password, email, 0, 0))
                connection.commit()
                
                flash('User registered successfully!', 'success')
            except Error as e:
                print(f"Error registering user: {e}")
                flash('An error occurred during registration', 'error')
            finally:
                if connection.is_connected():
                    cursor.close()
                    connection.close()
        else:
            flash('Database connection error', 'error')
        
        return redirect(url_for('index'))

@app.route('/register_writer', methods=['POST'])
def register_writer():
    if request.method == 'POST':
        name = request.form.get('writerName')
        email = request.form.get('writerEmail')
        password = request.form.get('writerPassword')
        newsgroup_id = request.form.get('newsGroup')
        if not all([name, email, password, newsgroup_id]):
            flash('All fields are required', 'error')
            return redirect(url_for('index'))
        
        if not validate_email(email):
            flash('Invalid email format', 'error')
            return redirect(url_for('index'))
        
        connection = get_db_connection()
        if connection:
            try:
                cursor = connection.cursor()
                
                cursor.execute("SELECT * FROM Writer WHERE email = %s", (email,))
                if cursor.fetchone():
                    flash('Email already registered as a writer', 'error')
                    return redirect(url_for('index'))
               
                writer_id = generate_id('W', 'Writer', 'Writer_ID')
                
                query = """
                INSERT INTO Writer (Writer_ID, name, email, password, NewsGroupID)
                VALUES (%s, %s, %s, %s, %s)
                """
                cursor.execute(query, (writer_id, name, email, password, newsgroup_id))
                connection.commit()
                
                flash('Writer registered successfully!', 'success')
            except Error as e:
                print(f"Error registering writer: {e}")
                flash('An error occurred during registration', 'error')
            finally:
                if connection.is_connected():
                    cursor.close()
                    connection.close()
        else:
            flash('Database connection error', 'error')
        
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)