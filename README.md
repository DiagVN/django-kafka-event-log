[![codecov](https://codecov.io/gh/DiagVN/django-kafka-event-log/branch/develop/graph/badge.svg?token=2FtNkItJO7)](https://codecov.io/gh/DiagVN/django-kafka-event-log)

# Kafka Event

Create an event from Django ORM object model, store the event into the database and also publish it into Kafka cluster. The Kafka topic name is `django_app_name.model_name`.

## Setup

Install the package:

```shell
pip install django-kafka-event-log
```

In your project's `settings.py`, include the app and add credentials for Kafka:

```python
INSTALLED_APPS = [
    ...
    'events',
]

KAFKA_GROUP = 'KAFKA_GROUP'
KAFKA_BOOTSTRAP_SERVERS = 'KAFKA_BOOTSTRAP_SERVERS'
KAFKA_SECURITY_PROTOCOL = 'KAFKA_SECURITY_PROTOCOL'
KAFKA_SASL_MECHANISMS = 'KAFKA_SASL_MECHANISMS'
KAFKA_SASL_USERNAME = 'KAFKA_SASL_USERNAME'
KAFKA_SASL_PASSWORD = 'KAFKA_SASL_PASSWORD'
```

Note: the credential should be read from environment variables.

Create the topic in Kafka cluster: `django_app_name.model_name`. This is where the event log will be pushed into.

## Usage

This application has only 1 interface; it is `PublishKafkaEventUtil`. Given `myapp` is where the model object
locates, `MyModelSerializer` is the data presenter, we can call the Util like this:

```python
from events.utils import PublishKafkaEventUtil
from myapp.serializers.mymodel_serializer import MyModelSerializer

PublishKafkaEventUtil.call(
    event_name='Created',
    model_object=model_obj,
    serializer=ModelSerializer,
    metadata={'purpose': 'testing'},
)
```

## How To Release:

This package is configured to release if the Git tag version is the same as the VERSION in `setup.py`. So, make sure
their values are correct.

```shell
git commit -m "..."
git tag <version>
git push origin develop
git push origin tag
```
