======================
Django Kafka Event Log
======================
Store an event and publish the event to Kafka

Quick start
-----------
1. Install package::

    pip install django-kafka-event-log

2. Add "events" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'events',
    ]

3. Set up Kafka credential in "settings.py" like this::

    KAFKA_GROUP = 'KAFKA_GROUP'
    KAFKA_BOOTSTRAP_SERVERS = 'KAFKA_BOOTSTRAP_SERVERS'
    KAFKA_SECURITY_PROTOCOL = 'KAFKA_SECURITY_PROTOCOL'
    KAFKA_SASL_MECHANISMS = 'KAFKA_SASL_MECHANISMS'
    KAFKA_SASL_USERNAME = 'KAFKA_SASL_USERNAME'
    KAFKA_SASL_PASSWORD = 'KAFKA_SASL_PASSWORD'


4. Store and send event::

    from events.utils import PublishKafkaEventUtil
    from myapp.serializers.mymodel_serializer import MyModelSerializer

    PublishKafkaEventUtil.call(
        event_name='Created',
        model_object=model_obj,
        serializer=ModelSerializer,
        metadata={'purpose': 'testing'},
    )

Author: Diag
