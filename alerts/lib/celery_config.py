import os
from logging.config import dictConfig

from lib.config import LOGGING, RABBITMQ, MONGO_URL


# XXX TBD this should get wrapped into an object that provides pyconfig
if os.getenv("OPTIONS_MQPROTOCOL", "amqp") == "sqs":
    BROKER_URL = "sqs://@"
    BROKER_TRANSPORT_OPTIONS = {'region': os.getenv('OPTIONS_ALERTSQSQUEUEURL').split('.')[1], 'is_secure': True, 'port': 443}
    CELERY_RESULT_BACKEND = None
    alert_queue_name = os.getenv('OPTIONS_ALERTSQSQUEUEURL').split('/')[4]
    CELERY_DEFAULT_QUEUE = alert_queue_name
    CELERY_QUEUES = {
        alert_queue_name: {"exchange": alert_queue_name, "binding_key": alert_queue_name}
    }
else:
    BROKER_URL = "amqp://{0}:{1}@{2}:{3}//".format(
        RABBITMQ["mquser"], RABBITMQ["mqpassword"], RABBITMQ["mqserver"], RABBITMQ["mqport"]
    )
    CELERY_QUEUES = {
        "celery-default": {"exchange": "celery-default", "binding_key": "celery-default"}
    }
    CELERY_DEFAULT_QUEUE = 'celery-default'

CELERY_DISABLE_RATE_LIMITS = True
CELERYD_CONCURRENCY = 1
CELERY_IGNORE_RESULT = True
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"

CELERYBEAT_SCHEDULER = "celerybeatmongo.schedulers.MongoScheduler"
CELERY_MONGODB_SCHEDULER_DB = "alerts_celery"
CELERY_MONGODB_SCHEDULER_COLLECTION = "schedules"
CELERY_MONGODB_SCHEDULER_URL = MONGO_URL

# Load logging config
dictConfig(LOGGING)
