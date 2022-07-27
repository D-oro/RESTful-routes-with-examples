from flask import Flask, render_template, request, redirect
from repositories import task_repository, user_repository
from models.task import Task

from flask import Blueprint

tasks_blueprint = Blueprint("tasks", __name__)

# RESTful CRUD Routes

# INDEX
# GET '/tasks'
@tasks_blueprint.route("/tasks")
def tasks():
    tasks = task_repository.select_all() # NEW
    return render_template("tasks/index.html", all_tasks = tasks)

# NEW
# GET '/tasks/new'

@tasks_blueprint.route('/tasks/new')
def new():
    users = user_repository.select_all()
    return render_template('/tasks/new.html', all_users=users)

# CREATE
# POST '/tasks'

@tasks_blueprint.route('/tasks', methods = ['POST'])
def create():
    description = request.form['description']
    duration = request.form['duration']
    completed = request.form['completed']
    user_id = request.form['user_id']
    user = user_repository.select(user_id)
    task = Task(description, user, duration, completed)
    task_repository.save(task)
    return redirect('/tasks')

# SHOW
# GET '/tasks/<id>'

@tasks_blueprint.route('/tasks/<id>')
def show(id):
    task = task_repository.select(id)
    return render_template("/tasks/show.html", task=task)

# EDIT
# GET '/tasks/<id>/edit'

@tasks_blueprint.route('/tasks/<id>/edit')
def edit(id):
    task = task_repository.select(id)
    users = user_repository.select_all()
    return render_template('/tasks/edit.html', task=task, all_users=users)

# UPDATE
# PUT '/tasks/<id>'
@tasks_blueprint.route('/tasks/<id>', methods=['POST'])
def update(id):
    description = request.form['description']
    duration = request.form['duration']
    completed = request.form['completed']
    user_id = request.form['user_id']
    user = user_repository.select(user_id)
    task = Task(description, user, duration, completed, id)
    task_repository.update(task)
    return redirect('/tasks/' + id)

# DELETE
# DELETE '/tasks/<id>'
@tasks_blueprint.route('/tasks/<id>/delete', methods=['POST'])
def delete(id):
    task_repository.delete(id)
    return redirect('/tasks')
