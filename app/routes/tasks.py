from flask import Blueprint, session, flash, render_template, request, redirect, url_for
from app import db
from app.models import Task

tasks_bp = Blueprint('tasks', __name__)

@tasks_bp.route('/')
def view_task():
    if 'user' not in session:
        return redirect(url_for('auth.login'))
    
    user_id = session.get('user_id')
    tasks = Task.query.filter_by(user_id=user_id).all()
    return render_template('tasks.html', tasks=tasks)

@tasks_bp.route('/add', methods=["POST"])
def add_task():
    if 'user' not in session:
        return redirect(url_for('auth.login'))
    
    title = request.form.get('title')
    user_id = session.get('user_id')

    if title:
        new_task = Task(title=title, status='Pending', user_id=user_id)
        db.session.add(new_task)
        db.session.commit()
        flash("Task added successfully", "success")

    return redirect(url_for('tasks.view_task'))

@tasks_bp.route('/toggle/<int:task_id>', methods=["POST"])
def toggle_status(task_id):
    task = Task.query.get(task_id)
    if task:
        if task.status == 'Pending':
            task.status = 'Working'
        elif task.status == 'Working':
            task.status = 'Done'
        else: 
            task.status = 'Pending'
        db.session.commit()

    return redirect(url_for('tasks.view_task'))

@tasks_bp.route('/delete/<int:task_id>', methods=["POST"])
def delete_task(task_id):
    if 'user' not in session:
        return redirect(url_for('auth.login'))
    
    task = Task.query.get(task_id)
    if task:
        db.session.delete(task)
        db.session.commit()
        flash("Task deleted successfully", "success")

    return redirect(url_for('tasks.view_task'))

@tasks_bp.route('/clear', methods=['POST'])
def clear_tasks():
    user_id = session.get('user_id')
    Task.query.filter_by(user_id=user_id).delete()
    db.session.commit()
    flash("All tasks are cleared", "info")
    return redirect(url_for('tasks.view_task'))