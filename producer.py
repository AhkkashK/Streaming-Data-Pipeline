from kafka import KafkaProducer
import json
import uuid
import random
import time
from datetime import datetime
from kafka.errors import NoBrokersAvailable

def calculate_severity(transaction):
    amount = transaction['Amount']
    transaction_type = transaction['TransactionType']

    if transaction_type == 'deposit' and amount > 900:
        return 'Critical'
    elif transaction_type in ['withdrawal', 'payment'] and amount < -900:
        return 'Critical'
    elif transaction_type == 'transfer' and (amount > 900 or amount < -900):
        return 'Critical'
    else:
        return 'Not Critical'

def generate_transaction():
    transaction_type = random.choice(['deposit', 'withdrawal', 'transfer', 'payment'])
    amount = round(random.uniform(100, 1000), 2)  # Génère un montant positif

    if transaction_type in ['withdrawal', 'payment']:
        amount = -amount  # Rendre le montant négatif pour les retraits et les paiements
    elif transaction_type == 'transfer':
        # Le montant des transferts peut être positif ou négatif
        if random.choice([True, False]):
            amount = -amount

    transaction = {
        'TransactionID': str(uuid.uuid4()),
        'AccountID': f'ACC-{random.randint(1000, 9999)}',
        'Amount': amount,
        'Currency': 'EUR',
        'TransactionDate': datetime(2024, 1, random.randint(1, 31), 
                            random.randint(0, 23), random.randint(0, 59), random.randint(0, 59)).strftime('%Y-%m-%d %H:%M:%S'),
        'Location': random.choice(['Paris', 'Marseille', 'Lyon', 'Toulouse', 'Nice', 'Nantes', 'Strasbourg', 'Montpellier', 'Bordeaux', 'Lille']),
        'TransactionType': transaction_type,
        'Severity': calculate_severity({'Amount': amount, 'TransactionType': transaction_type}),
        'Sexe':random.choice(['M','F']),
        'Age':random.randint(18,100),
        'lastUpdated': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }

    return transaction

# Attente pour Kafka
producer = None
while not producer:
    try:
        producer = KafkaProducer(
            bootstrap_servers='kafka:9092',
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
    except NoBrokersAvailable:
        print("Kafka broker non disponible, tentative de reconnexion dans 5 secondes...")
        time.sleep(5)

while True:
    transaction = generate_transaction()
    
    # Produire un message pour le topic
    producer.send('bank_data', value=transaction)
    print(f'Produced transaction: {transaction}')
    
    time.sleep(5)
