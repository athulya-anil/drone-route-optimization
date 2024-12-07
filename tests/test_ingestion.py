from kafka import KafkaProducer, KafkaConsumer
import unittest
import json
import time


class TestKafkaStreaming(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Kafka topic and broker configurations
        cls.topic_name = "test_topic"
        cls.bootstrap_servers = "localhost:9092"

        # Set up Kafka producer
        cls.producer = KafkaProducer(
            bootstrap_servers=cls.bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )

        # Set up Kafka consumer
        cls.consumer = KafkaConsumer(
            cls.topic_name,
            bootstrap_servers=cls.bootstrap_servers,
            auto_offset_reset="earliest",
            enable_auto_commit=True,
            value_deserializer=lambda v: json.loads(v.decode('utf-8'))
        )

    def test_kafka_producer(self):
        """Test if the Kafka producer can send messages."""
        test_message = {"key": "value", "message": "Hello, Kafka!"}
        try:
            self.producer.send(self.topic_name, value=test_message)
            self.producer.flush()
        except Exception as e:
            self.fail(f"Kafka producer failed to send a message: {e}")

    def test_kafka_consumer(self):
        """Test if the Kafka consumer can receive messages."""
        # Send a test message
        test_message = {"key": "value", "message": "Hello, Kafka!"}
        self.producer.send(self.topic_name, value=test_message)
        self.producer.flush()

        # Allow some time for the consumer to receive the message
        time.sleep(2)

        # Check the consumed message
        messages = []
        for message in self.consumer:
            messages.append(message.value)
            # Break after receiving one message to avoid infinite loop
            if len(messages) > 0:
                break

        # Validate the consumed message
        self.assertIn(test_message, messages, "The message was not consumed correctly by Kafka.")

    @classmethod
    def tearDownClass(cls):
        cls.producer.close()
        cls.consumer.close()


if __name__ == "__main__":
    unittest.main()
