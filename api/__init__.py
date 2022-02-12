from config import Config
from celery import Celery

celery = Celery(__name__,
                backend=Config.CELERY_RESULT_BACKEND,
                broker=Config.CELERY_BROKER_URL,
                include=Config.CELERY_TASKS)


def init_celery(app, celery):

    celery.conf.update(app.config)

    class ContextTask(celery.Task):

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
