import unittest
from pyflink.datastream import StreamExecutionEnvironment
from pyflink.datastream.connectors import FlinkKafkaConsumer, FlinkKafkaProducer
from pyflink.common.serialization import SimpleStringSchema
import json
import os

class TestFlinkGraphXIntegration(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Set up Kafka topic and server details
        cls.input_topic = "input_topic"
        cls.output_topic = "output_topic"
        cls.bootstrap_servers = "localhost:9092"

        # Set up the Flink execution environment
        cls.env = StreamExecutionEnvironment.get_execution_environment()
        cls.env.set_parallelism(1)

    def test_flink_to_graphx_pipeline(self):
        """Test the integration between Flink and GraphX"""
        # Simulate incoming Kafka messages
        input_data = [
            json.dumps({"node": "A", "edges": ["B", "C"]}),
            json.dumps({"node": "B", "edges": ["C", "D"]}),
        ]

        # Simulate Kafka producer
        producer = FlinkKafkaProducer(
            topic=self.input_topic,
            serialization_schema=SimpleStringSchema(),
            producer_config={"bootstrap.servers": self.bootstrap_servers},
        )

        # Send input data to the Kafka topic
        for record in input_data:
            producer.invoke(record)

        # Create Kafka consumer for Flink to consume input data
        consumer = FlinkKafkaConsumer(
            topics=self.input_topic,
            deserialization_schema=SimpleStringSchema(),
            properties={"bootstrap.servers": self.bootstrap_servers},
        )

        # Create Kafka producer to send processed data to another topic
        producer_out = FlinkKafkaProducer(
            topic=self.output_topic,
            serialization_schema=SimpleStringSchema(),
            producer_config={"bootstrap.servers": self.bootstrap_servers},
        )

        # Flink data pipeline
        input_stream = self.env.add_source(consumer)
        processed_stream = input_stream.map(
            lambda x: self.mock_graphx_process(x)
        )  # Simulate processing with GraphX
        processed_stream.add_sink(producer_out)

        # Execute the Flink pipeline
        self.env.execute("Flink to GraphX Integration Test")

        # Simulate Kafka consumer to verify output
        output_consumer = FlinkKafkaConsumer(
            topics=self.output_topic,
            deserialization_schema=SimpleStringSchema(),
            properties={"bootstrap.servers": self.bootstrap_servers},
        )
        output_stream = self.env.add_source(output_consumer)

        # Collect processed results
        results = []
        output_stream.add_sink(lambda x: results.append(json.loads(x)))

        # Check results
        expected_output = [
            {"node": "A", "edges_processed": ["B", "C"]},
            {"node": "B", "edges_processed": ["C", "D"]},
        ]
        self.assertEqual(results, expected_output, "Flink to GraphX integration failed.")

    def mock_graphx_process(self, record):
        """Simulate GraphX processing"""
        record = json.loads(record)
        processed_edges = [edge + "_processed" for edge in record["edges"]]
        return json.dumps({"node": record["node"], "edges_processed": processed_edges})

    @classmethod
    def tearDownClass(cls):
        """Clean up after tests"""
        # This is where you would clean up Kafka topics or other resources
        pass


if __name__ == "__main__":
    unittest.main()
