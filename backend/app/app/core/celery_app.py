from celery import Celery

celery_app = Celery("worker", broker="amqp://guest@queue:5672//")
