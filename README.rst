======================
Django Kafka Event Log
======================
Store an event and publish the event to Kafka

Quick start
-----------
1. Install package::

    pip install git+https://github.com/DiagVN/django-kafka-event-log.git

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


4.
