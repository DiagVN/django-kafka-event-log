import json
import logging
from datetime import datetime

from confluent_kafka import Producer
from django.conf import settings
from django.db import models
from rest_framework.serializers import BaseSerializer

from events.common.base_service_mixin import BaseServiceMixin
from events.models import Events

logger = logging.getLogger(__name__)

KAFKA_PRODUCER_CONFIG = {
    'bootstrap.servers': settings.KAFKA_BOOTSTRAP_SERVERS,
    'group.id': settings.KAFKA_GROUP,
    'auto.offset.reset': 'earliest',
    'security.protocol': settings.KAFKA_SECURITY_PROTOCOL,
    'sasl.mechanisms': settings.KAFKA_SASL_MECHANISMS,
    'sasl.username': settings.KAFKA_SASL_USERNAME,
    'sasl.password': settings.KAFKA_SASL_PASSWORD,
}


class PublishKafkaEventUtil(BaseServiceMixin):
    def __init__(self, event_name: str, model_object: models.Model, serializer: BaseSerializer, metadata: dict = None):
        super().__init__()
        self.event_name = event_name
        self.model_object = model_object
        self.serializer = serializer
        self.metadata = metadata
        self.topic = self.get_topic()

    def build_kafka_message(self):
        message = {
            'event_name': self.event_name,
            'metadata': self.metadata,
            'data': self.serializer(self.model_object).data,
            'timestamp': datetime.now().isoformat(),
        }

        return json.dumps(message)

    def publish_kafka_message(self, message=None, key=None, producer=None):
        if not producer:  # pragma: no cover
            producer = Producer(KAFKA_PRODUCER_CONFIG)
        producer.produce(self.topic, key=key, value=message)

        producer.flush()

    def get_topic(self) -> str:
        return f'{self.model_object._meta.app_label}.{self.model_object._meta.model_name}'

    def store_event(self, message):
        Events.objects.create(
            topic=self.topic,
            payload=message,
        )

    def exec(self):
        message = self.build_kafka_message()
        self.publish_kafka_message(message)
        self.store_event(message)
