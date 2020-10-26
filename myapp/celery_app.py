from celery import Celery

from config import access_key, secret_key, db_endpoint, db_name, db_key, region


app = Celery(
    'tasks',
    broker='sqs://{}:{}@'.format(access_key, secret_key),
    # backend='db+sqlite:///results.sqlite',
    backend=f'db+postgresql://{db_name}:{db_key}@{db_endpoint}',
    include=['celery_tasks'],
    broker_transport_options={'region': region, 'queue_name_prefix': 'celery-'},
)
