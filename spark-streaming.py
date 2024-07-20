from pyspark.sql import SparkSession
from pyspark.sql.functions import col, udf, to_timestamp
from pyspark.sql.types import StringType
import time

# UDF pour déterminer le type de jour
def get_day_type(transaction_date):
    if transaction_date.weekday() < 5:
        return "Weekday"
    else:
        return "Weekend"

# Enregistrer l'UDF
day_type_udf = udf(get_day_type, StringType()) # fonction en spark 


# Créer une session Spark
spark = SparkSession.builder \
    .appName("MongoDBSparkAnalysis") \
    .config("spark.mongodb.read.connection.uri", "mongodb://mongodb:27017/BANK.transactions") \
    .getOrCreate()

# Schéma des données
schema = "TransactionID STRING, AccountID STRING, Amount DOUBLE, Currency STRING, TransactionDate STRING, Location STRING, TransactionType STRING, Severity STRING, Sexe STRING, Age INT,lastUpdated STRING"

# Initialise la dernière date/heure de traitement
last_processed_time = None

# Boucle infinie pour garder le conteneur en cours d'exécution
while True:
    # Construire le filtre pour récupérer les nouvelles transactions
    if last_processed_time:
        filter_query = {"lastUpdated": {"$gt": last_processed_time}}
    else:
        filter_query = {}

    # Lire les transactions de MongoDB
    transactions_df = spark.read \
        .format("com.mongodb.spark.sql.DefaultSource") \
        .option("uri", "mongodb://mongodb:27017/BANK.transactions") \
        .option("pipeline", f"[{{'$match': {filter_query}}}]") \
        .schema(schema) \
        .load()

    # Convertir la colonne TransactionDate en Timestamp
    transactions_df = transactions_df.withColumn("TransactionDate", to_timestamp(col("TransactionDate"), "yyyy-MM-dd HH:mm:ss"))

    if transactions_df.count() > 0:
        
        # Ajouter la colonne DayType
        transactions_df = transactions_df.withColumn("DayType", day_type_udf(col("TransactionDate")))

        # Supprimer les doublons basés sur les colonnes pertinentes
        transactions_df = transactions_df.dropDuplicates(["TransactionID", "AccountID", "TransactionDate"])



        # Écrire les résultats transformés dans PostgreSQL en mode "append"
        
        
        transactions_df.write \
            .format("jdbc") \
            .option("url", "jdbc:postgresql://postgres:5432/bank") \
            .option("dbtable", "transactions_data") \
            .option("user", "user") \
            .option("password", "password") \
            .option("driver", "org.postgresql.Driver") \
            .mode("append") \
            .save()


        print("Transformations processed and saved to PostgreSQL")

        # Mettre à jour la dernière date/heure de traitement
        last_processed_time = transactions_df.agg({"lastUpdated": "max"}).collect()[0][0]

    time.sleep(10)
