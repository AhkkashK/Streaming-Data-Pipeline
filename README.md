# Banking Transactions Processing Pipeline

## Project Overview

This project sets up a pipeline for real-time processing of banking transactions. We have simulated transactions for January 2024 in France, using a combination of modern technologies to manage and analyze the data from end to end.

## Objective

1. **Generate Data**: Simulate banking transactions every 5 seconds.
2. **Process Data**: Analyze transactions in real-time using Apache Spark.
3. **Store Data**: Save raw transactions in MongoDB.
4. **Analyze Data**: Store analysis results in PostgreSQL.
5. **Visualize Data**: Create dashboards with Grafana.

## Pipeline Architecture

1. **Data Producer** (`producer.py`)
   - Generates simulated banking transactions.
   - Publishes data to the Kafka topic `bank_data`.

2. **Kafka**
   - **Role**: Message broker for real-time transaction streaming.
   - **Reason**: Kafka is highly reliable, scalable, and suitable for handling real-time data streams, ensuring that our generated transactions can be efficiently queued and processed.

3. **Zookeeper**
   - **Role**: Coordinates Kafka brokers to ensure their proper functioning.
   - **Reason**: Zookeeper is necessary for managing the Kafka cluster, providing configuration management, synchronization, and naming registry, which is crucial for maintaining Kafka's high availability.

4. **MongoDB**
   - **Role**: Stores raw transactions in JSON format.
   - **Reason**: MongoDB's flexible schema and ease of integration with Python make it an excellent choice for storing diverse and rapidly changing data like banking transactions.

5. **Apache Spark** (`spark-streaming.py`)
   - **Role**: Real-time processing and analysis of transactions.
   - **Reason**: Apache Spark provides powerful processing capabilities, allowing us to handle large volumes of data efficiently. Its integration with both MongoDB and PostgreSQL facilitates seamless data transformation and analysis.

6. **PostgreSQL**
   - **Role**: Stores analysis results for detailed queries.
   - **Reason**: PostgreSQL is a robust relational database with strong support for complex queries and transactions, making it ideal for storing and querying processed data.

7. **Grafana**
   - **Role**: Visualizes data and metrics.
   - **Reason**: Grafana is widely used for monitoring and visualization, providing a rich set of features for creating interactive dashboards, which helps in visualizing the transaction data insights effectively.


## Files

### `producer.py`

Generates banking transactions and sends them to Kafka.

**Features:**
- Generates transactions with various amounts and types.
- Publishes transactions to the Kafka topic `bank_data`.

### `consumer.py`

Consumes transactions from the Kafka topic and stores them in MongoDB.

**Features:**
- Connects to Kafka to read transactions.
- Inserts transactions into MongoDB.

### `spark-streaming.py`

Processes transactions in real-time with Apache Spark and stores results in PostgreSQL.

**Features:**
- Reads transactions from MongoDB.
- Adds a "DayType" column to classify days as weekday or weekend.
- Writes results to PostgreSQL.

### `docker-compose.yml`

Defines the services required for the pipeline.

**Services:**
- **Zookeeper**: Coordinates Kafka brokers.
- **Kafka**: Message broker.
- **MongoDB**: Stores raw transactions.
- **Producer**: Generates and sends transactions to Kafka.
- **Consumer**: Consumes transactions from Kafka and stores them in MongoDB.
- **Spark**: Processes and stores results in PostgreSQL.
- **PostgreSQL**: Database for analysis results.
- **Grafana**: Visualizes data.

## Deployment and Configuration

### Prerequisites

- Docker
- Docker Compose

### Installation

Clone the repository and run the following command : 
```bash
docker-compose up
````

