from flask import Flask, jsonify, request
import mysql.connector as mysql
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

mycon = mysql.connect(host = "localhost", user = "root", password = "0129", database = "to_do_list")
cursor = mycon.cursor()

@app.route('/add_task', methods = ['POST'])
def add_task():
    data = request.get_json()
    task = data['task']
    cursor.execute("INSERT into tasks (tasks) values(%s)", (task,))
    mycon.commit()
    return jsonify({'message': 'Task added successfully'}), 201

@app.route('/get_tasks', methods = ['GET'])
def get_tasks():
    cursor.execute("SELECT * from tasks")
    tasks = cursor.fetchall()
    task_list = [{'id': row[0], 'task': row[1]} for row in tasks]
    return jsonify(task_list), 200

@app.route('/delete_tasks/<int:task_id>', methods = ['DELETE'])
def delete_task(task_id):
    cursor.execute("DELETE from tasks where id = %s", (task_id,))
    mycon.commit()
    return jsonify({'message': 'Task deleted successfully'}), 200

if __name__ == '__main__':
    app.run(debug=True)