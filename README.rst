======================
Django Kafka Event Log
======================
Create an event from Django ORM object model, store the event into the database and also publish it into Kafka cluster.

Quick start
-----------
1. Install the package::

    pip install django-kafka-event-log

2. In your project's `settings.py`, include the app and add credentials for Kafka::

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

3. Note: the credential should be read from environment variables.

4. This application has only 1 interface; it is `PublishKafkaEventUtil`. Given `myapp` is where the model object locates, `MyModelSerializer` is the data presenter, we can call the Util like this::


    from events.utils import PublishKafkaEventUtil
    from myapp.serializers.mymodel_serializer import MyModelSerializer

    PublishKafkaEventUtil.call(
        event_name='Created',
        model_object=model_obj,
        serializer=ModelSerializer,
        metadata={'purpose': 'testing'},
    )


.. image:: https://codecov.io/gh/DiagVN/django-kafka-event-log/branch/develop/graph/badge.svg?token=2FtNkItJO7
      :target: https://codecov.io/gh/DiagVN/django-kafka-event-log
