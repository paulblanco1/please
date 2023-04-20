from flask import Flask, request, render_template, redirect, url_for
import sqlite3

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'

# create the database table
with sqlite3.connect('tasks.db') as conn:
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS tasks
                      (id INTEGER PRIMARY KEY AUTOINCREMENT,
                       task TEXT NOT NULL,
                       completed BOOLEAN NOT NULL)''')

# add a task to the database
def add_task(task):
    with sqlite3.connect('tasks.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO tasks (task, completed) VALUES (?, ?)''',
                       (task, False))

# get all tasks from the database
def get_tasks():
    with sqlite3.connect('tasks.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''SELECT id, task, completed FROM tasks''')
        tasks = cursor.fetchall()
        return tasks

# delete a task from the database
def delete_task(task_id):
    with sqlite3.connect('tasks.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''DELETE FROM tasks WHERE id = ?''', (task_id,))

# mark a task as completed in the database
def complete_task(task_id):
    with sqlite3.connect('tasks.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''UPDATE tasks SET completed = ? WHERE id = ?''', (True, task_id))

# mark a task as incomplete in the database
def incomplete_task(task_id):
    with sqlite3.connect('tasks.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''UPDATE tasks SET completed = ? WHERE id = ?''', (False, task_id))

# the home page displays all tasks
@app.route('/')
def home():
    tasks = get_tasks()
    return render_template('home.html', tasks=tasks)

# add a new task
@app.route('/add', methods=['POST'])
def add():
    task = request.form['task']
    add_task(task)
    return redirect(url_for('home'))

# delete a task
@app.route('/delete/<int:task_id>')
def delete(task_id):
    delete_task(task_id)
    return redirect(url_for('home'))

# mark a task as completed
@app.route('/complete/<int:task_id>')
def complete(task_id):
    complete_task(task_id)
    return redirect(url_for('home'))

# mark a task as incomplete
@app.route('/incomplete/<int:task_id>')
def incomplete(task_id):
    incomplete_task(task_id)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
