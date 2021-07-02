from datetime import datetime
from unittest import mock

from django.test import TransactionTestCase

from events.models import Events
from events.tests.models.sample import Sample
from events.tests.serializers.sample_serializer import SampleSerializer
from events.utils import PublishKafkaEventUtil


class TestPublishKafkaEventUtil(TransactionTestCase):

    def setUp(self) -> None:
        self.model_obj = Sample(
            name='test',
            created_at=datetime(2021, 7, 2, 6, 0, 34, 727800),
        )
        self.util = PublishKafkaEventUtil(
            event_name='Created',
            model_object=self.model_obj,
            serializer=SampleSerializer,
            metadata={'purpose': 'testing'},
        )
        self.producer_patcher = mock.patch('events.utils.Producer')
        self.producer = self.producer_patcher.start()

    def tearDown(self) -> None:
        self.producer_patcher.stop()

    def test_build_kafka_message(self):
        message = self.util.build_kafka_message()
        expected_message = {
            'event_name': 'Created',
            'metadata': {'purpose': 'testing'},
            'data': {'name': 'test', 'created_at': '2021-07-02T06:00:34.727800Z'},
        }

        self.assertEqual(message, expected_message)

    def test_get_topic(self):
        self.assertEqual('my_app.sample', self.util.get_topic())

    def test_store_event(self):
        self.util.store_event('a message')
        event = Events.objects.last()
        self.assertEqual(event.topic, 'my_app.sample')
        self.assertEqual(event.payload, 'a message')

    def test_push_message_kafka(self):
        self.producer.return_value = mock.MagicMock()
        self.util.publish_kafka_message(message='a message', key=None, producer=self.producer)
        self.producer.produce.assert_called_once_with(
            'my_app.sample',
            key=None,
            value='a message',
        )
        self.producer.flush.assert_called_once()

    @mock.patch('events.utils.PublishKafkaEventUtil.publish_kafka_message', return_value=None)
    def test_exec(self, mock_publish_kafka_message):
        self.producer.return_value = mock.MagicMock()
        PublishKafkaEventUtil.call(
            event_name='Created',
            model_object=self.model_obj,
            serializer=SampleSerializer,
            metadata={'purpose': 'testing'},
        )
        message = {
            'event_name': 'Created',
            'metadata': {'purpose': 'testing'},
            'data': {'name': 'test', 'created_at': '2021-07-02T06:00:34.727800Z'},
        }
        mock_publish_kafka_message.assert_called_once_with(
            message,
        )
        event = Events.objects.last()
        self.assertEqual(event.topic, 'my_app.sample')
        self.assertEqual(event.payload, message)
