from kafka import KafkaConsumer
import json
import time
import logging
from kafka.errors import NoBrokersAvailable
from pymongo import MongoClient, errors

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Connexion à Kafka
consumer = None
while not consumer:
    try:
        consumer = KafkaConsumer(
            'bank_data',
            bootstrap_servers='kafka:9092',
            auto_offset_reset='earliest',
            enable_auto_commit=True,
            group_id='my-group',
            value_deserializer=lambda x: json.loads(x.decode('utf-8'))
        )
        logger.debug("Kafka Consumer connecté avec succès")
    except NoBrokersAvailable:
        logger.debug("Kafka broker non disponible, tentative de reconnexion dans 5 secondes...")
        time.sleep(5)

# Connexion à MongoDB
mongo_client = None
while not mongo_client:
    try:
        mongo_client = MongoClient('mongodb://mongodb:27017/')
        mongo_client.admin.command('ismaster')  # Test de la connexion
        logger.debug("Client MongoDB connecté avec succès")
    except errors.ConnectionFailure:
        logger.debug("MongoDB non disponible, tentative de reconnexion dans 5 secondes...")
        time.sleep(5)

# Sélection de la base de données et des collections
db = mongo_client['BANK']
transactions_collection = db['transactions']

# Consommation des messages Kafka et insertion dans MongoDB
for message in consumer:
    transaction = message.value
    logger.debug(f'Consumed transaction: {transaction}')
    try:
        result = transactions_collection.insert_one(transaction)
        logger.debug(f'Transaction écrite avec succès dans MongoDB: {result.inserted_id}')
    except Exception as e:
        logger.error(f"Échec de l'écriture de la transaction dans MongoDB: {e}")
