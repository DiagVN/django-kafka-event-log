import json
from datetime import datetime
from unittest import mock

import pytz
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
        self.mock_date = datetime(2021, 1, 1, 1, 0, 0, 727800, pytz.UTC)

    def tearDown(self) -> None:
        self.producer_patcher.stop()

    @mock.patch('events.utils.datetime')
    def test_build_kafka_message(self, mock_datetime):
        mock_datetime.now.return_value = self.mock_date
        message = self.util.build_kafka_message()
        expected_message = json.dumps({
            'event_name': 'Created',
            'metadata': {'purpose': 'testing'},
            'data': {'name': 'test', 'created_at': '2021-07-02T06:00:34.727800Z'},
            'timestamp': '2021-01-01T01:00:00.727800+00:00',
        })

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

    @mock.patch('events.utils.datetime')
    @mock.patch('events.utils.PublishKafkaEventUtil.publish_kafka_message', return_value=None)
    def test_exec(self, mock_publish_kafka_message, mock_datetime):
        mock_datetime.now.return_value = self.mock_date
        self.producer.return_value = mock.MagicMock()
        PublishKafkaEventUtil.call(
            event_name='Created',
            model_object=self.model_obj,
            serializer=SampleSerializer,
            metadata={'purpose': 'testing'},
        )
        message = json.dumps({
            'event_name': 'Created',
            'metadata': {'purpose': 'testing'},
            'data': {'name': 'test', 'created_at': '2021-07-02T06:00:34.727800Z'},
            'timestamp': '2021-01-01T01:00:00.727800+00:00',
        })
        mock_publish_kafka_message.assert_called_once_with(
            message,
        )
        event = Events.objects.last()
        self.assertEqual(event.topic, 'my_app.sample')
        self.assertEqual(event.payload, message)
