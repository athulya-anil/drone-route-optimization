import unittest
import json
from kafka import KafkaProducer, KafkaConsumer
import time

class TestDynamicDataSimulation(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Kafka topic and server details
        cls.input_topic = "dynamic_data_topic"
        cls.output_topic = "graph_update_topic"
        cls.bootstrap_servers = "localhost:9092"

        # Set up Kafka producer
        cls.producer = KafkaProducer(
            bootstrap_servers=cls.bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )

        # Set up Kafka consumer
        cls.consumer = KafkaConsumer(
            cls.output_topic,
            bootstrap_servers=cls.bootstrap_servers,
            auto_offset_reset="earliest",
            enable_auto_commit=True,
            value_deserializer=lambda v: json.loads(v.decode('utf-8'))
        )

    def test_dynamic_data_simulation(self):
        """Simulate dynamic data changes and validate system output."""
        # Dynamic updates to simulate weather and traffic data
        updates = [
            {"type": "weather", "location": "A", "condition": "storm"},
            {"type": "traffic", "location": "B", "condition": "congestion"},
            {"type": "weather", "location": "C", "condition": "clear"},
        ]

        # Send updates to the Kafka input topic
        for update in updates:
            self.producer.send(self.input_topic, value=update)
        self.producer.flush()

        # Allow time for the Flink pipeline to process the updates
        time.sleep(5)

        # Collect processed messages from the output topic
        processed_updates = []
        for message in self.consumer:
            processed_updates.append(message.value)
            if len(processed_updates) == len(updates):
                break

        # Validate the output
        expected_output = [
            {"type": "weather", "location": "A", "status": "updated", "condition": "storm"},
            {"type": "traffic", "location": "B", "status": "updated", "condition": "congestion"},
            {"type": "weather", "location": "C", "status": "updated", "condition": "clear"},
        ]
        self.assertEqual(processed_updates, expected_output, "Dynamic data simulation failed.")

    @classmethod
    def tearDownClass(cls):
        """Clean up Kafka producer and consumer."""
        cls.producer.close()
        cls.consumer.close()


if __name__ == "__main__":
    unittest.main()
