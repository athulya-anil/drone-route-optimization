# **Dynamic Route Optimization for Delivery Drones Using Real-Time Data**

## **Overview**
This project implements a system for optimizing delivery drone routes using real-time data. The objective is to ensure drones can dynamically adapt to changes in weather, traffic, and airspace conditions. By leveraging Apache Kafka for data ingestion and Apache Flink for real-time processing, the system computes efficient, safe, and timely delivery paths. Additionally, a visualization tool displays routes and drone statuses on an interactive map.

---

## **Setup Instructions**

### **1. Prerequisites**
- **Software**:
  - Apache Kafka (Version: 3.5.0+)
  - Apache Flink (Version: 1.20.0+)
  - Python 3.9+ or Java 11+
  - GraphX (or NetworkX for testing route optimization)
  - Folium or OpenStreetMap for visualization
- **API Key**:
  - Obtain an API key from [OpenWeatherMap](https://openweathermap.org/).

### **2. Installation**

#### **a. Kafka**
1. Download Kafka from the [official website](https://kafka.apache.org/).
2. Extract the downloaded archive and start the Zookeeper and Kafka servers:
   
### **b. Flink**
1. Download Flink from the [Apache Flink website](https://flink.apache.org/downloads.html).
2. Unzip the archive and start the Flink cluster:
   
### **c. Python Libraries**
Install the required Python packages: pip install -r requirements.txt

---

### **Running Instructions**

### **1. Start Kafka Topics**
Create the necessary topics for ingesting data:

- bin/kafka-topics.sh --create --topic weather-data --bootstrap-server localhost:9092
- bin-kafka-topics.sh --create --topic traffic-data --bootstrap-server localhost:9092

### **2. Run Flink Job**
Compile and execute the Flink program:

flink run -c com.example.DroneRouteOptimizer target/DroneRouteOptimizer.jar

### **3. Run Visualization**
Start the visualization tool to display drone routes and updates:

python visualize_routes.py

----
                                           

## **Experiments and Test Cases**

### **Tests Conducted**
1. **Edge Cases**:
   - **Blocked Routes**: Testing scenarios where no-fly zones obstruct direct paths.
   - **Extreme Weather**: Handling severe weather data to reroute drones dynamically.
2. **Performance**:
   - Measuring latency between data ingestion and route updates.
   - Evaluating Kafka and Flink throughput under various loads.

### **Replication Steps**
1. Set up Kafka topics and start the servers.
2. Run the Flink job with simulated data or real API inputs.
3. Monitor route updates and drone statuses on the visualization tool.
4. Log processing times and route changes for analysis.

---

## **Dependencies**

### **Libraries and Packages**
- **Python**:
  - `kafka-python`: For Kafka integration.
  - `apache-flink`: For stream processing.
  - `folium`: For map-based visualization.
  - `requests`: For API calls.
- **Java/Scala**:
  - Apache Flink (1.20.0+)
  - GraphX (for route optimization)

### **Software Versions**
- **Apache Kafka**: 3.5.0+
- **Apache Flink**: 1.20.0+
- **Python**: 3.9+
- **Java**: 11+

---

## **Possible Improvements**
- Implement machine learning models to predict weather and traffic trends for enhanced route optimization.
- Scale the system to handle multiple drones and larger datasets.
- Add fault-tolerance mechanisms to handle Kafka or Flink node failures seamlessly.

---

## **Contributors**
- Athulya Anil
- Varsha Ravichandran
- Pranav Pesaladinne



   
