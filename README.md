# Kafka Event

Store an event and publish the event to Kafka

## Setup

Install package:

```shell
pip install git+https://github.com/DiagVN/django-kafka-event-log.git
```

In `settings.py`:

```python
LOCAL_APPS = [
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

## Usage

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
