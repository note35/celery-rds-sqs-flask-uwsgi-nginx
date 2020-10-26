from random import randint

from flask import Blueprint, jsonify, url_for, redirect

from celery_tasks import add


base_bp = Blueprint('base', __name__)


@base_bp.route('/', methods=['GET'])
def longtask():
    task = add.delay(randint(-100, 100), randint(-100, 100))
    return redirect(url_for('base.taskstatus', task_id=task.id))


@base_bp.route('/status/<task_id>')
def taskstatus(task_id):
    task = add.AsyncResult(task_id)
    if task.state == 'PENDING':
        response = {
            'queue_state': task.state,
            'status': 'Process is ongoing...',
            'status_update': url_for('base.taskstatus', task_id=task.id)
        }
    else:
        response = {
            'queue_state': task.state,
            'result': task.wait()
        }
    return jsonify(response)
