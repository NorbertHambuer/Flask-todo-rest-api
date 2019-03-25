from flask import Flask, render_template, jsonify, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from datetime import date
from json import dumps

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS '] = False
POSTGRES = {
    'user': 'postgres',
    'pw': 'ad',
    'db': 'postgres',
    'host': 'localhost',
    'port': '5432',
}

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres+psycopg2://postgres:ad@localhost:5432/flask_crud'
db = SQLAlchemy(app)

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

class TaskModel(db.Model):
    __tablename__ = "tasks"
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.VARCHAR(250))
    deadline = db.Column(db.Date)
    completed = db.Column(db.Boolean)

    def __init__(self, description = '', deadline = '1990-01-01', completed = False):
        self.description = description
        self.deadline = deadline
        self.completed = completed

    def to_json(self):  # New special method.
        """ Convert to JSON format string representation. """
        return {
            'description': self.description,
            'deadline': self.deadline,
            'completed': self.completed
        }

    def __repr__(self):
        return "asdasd"

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self, description, deadline, completed):
        self.description = description if description != '' else self.description
        self.deadline = deadline if deadline != '' else self.deadline
        self.completed = bool(completed) if completed != '' else self.completed
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get_all_tasks():
        return TaskModel.query.all()

    @staticmethod
    def get_one_task(id):
        return TaskModel.query.get(id)

    @classmethod
    def from_json(cls, json):
        obj = cls()
        obj.description = json['description']
        obj.deadline = json['deadline']
        obj.completed = json['completed']
        return obj


@app.route('/')
def index():
    return render_template('home.html')


@app.route("/tasks", methods=['POST'])
def add_task():
    if 'description' in request.values and 'deadline' in request.values:
        try:
            task = TaskModel(
                request.values['description'],
                request.values['deadline'],
                request.values['completed'] if 'completed' in request.values else False
            )
            task.save()
            return "Task saved!"
        except Exception as ex:
            return str(ex)
    else:
        return "Description and Deadline are required!"


@app.route("/tasks", methods=['GET'])
def get_task():
    if 'id' in request.args:
        try:
            task = TaskModel.get_one_task(request.values['id'])
            return jsonify(task.to_json())
        except Exception as ex:
            return str(ex)
    else:
        try:
            tasks = TaskModel.get_all_tasks()
            return jsonify(tasks=[task.to_json() for task in tasks])
        except Exception as ex:
            return str(ex)


@app.route("/tasks", methods=['PUT'])
def update_task():
    if 'id' in request.values:
        try:
            task = TaskModel.get_one_task(request.values['id'])
            task.update(request.values['description'] if 'description' in request.values else '',
                        request.values['deadline'] if 'deadline' in request.values else '',
                        request.values['completed'] if 'completed' in request.values else '')
            return "Task updated!"
        except Exception as ex:
            return str(ex)
    else:
        return "Task id is required!"


@app.route("/tasks", methods=['DELETE'])
def delete_task():
    if 'id' in request.values:
        try:
            task = TaskModel.get_one_task(request.values['id'])
            task.delete()
            return "Task deleted!"
        except Exception as ex:
            return str(ex)
    else:
        return "Task id is required!"


@app.route("/test_ajax", methods=['GET', 'POST'])
def ajax():
    """clicked = None
    if request.method == "POST":
        clicked = request.json['data']"""
    task = TaskModel(
        "SecondTask",
        date.today(),
        True
    )
    task.save()

    if request.method == "POST":
        return "POST"
    elif request.method == "GET":
        return "GET"
    else:
        return "NONE"

if __name__ == '__main__':
    print("Run")
    manager.run()
