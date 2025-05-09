import asyncio
import os
import random
import logging
from azure.eventhub.aio import EventHubProducerClient
from azure.eventhub import EventData
from faker import Faker
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Setup logging
logger = logging.getLogger("eventhub-feedback")
stream_handler = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)
logger.setLevel(logging.INFO)

# Faker instance (French locale)
fake = Faker('fr_FR')

def generer_avis():
    """Génère un avis client aléatoire avec des attributs variés"""
    q = random.randint(1, 5)
    p = round(random.uniform(10.0, 500.0), 2)
    return {
        "nom": fake.name(),
        "email": fake.email(),
        "adresse": fake.address().replace('\n', ', '),
        "date_avis": fake.date_between(start_date='-30d', end_date='today').isoformat(),
        "note": random.randint(1, 5),
        "commentaire": random.choice([
            "Excellent service!",
            "Très satisfait.",
            "Peut être amélioré.",
            "Je ne suis pas content.",
            "Expérience formidable!",
            "Service médiocre.",
            "Livraison rapide et efficace.",
            "Produit de mauvaise qualité.",
            "Support client exceptionnel.",
            "Je recommande vivement!"
        ]),
        "produit": fake.word().capitalize(),
        "categorie": random.choice(['Électronique', 'Vêtements', 'Alimentation', 'Maison', 'Loisirs']),
        "prix_unitaire": p,
        "quantite": q,
        "total": round(p * q, 2),
        "mode_paiement": random.choice(['Carte de crédit', 'PayPal', 'Virement bancaire', 'Espèces']),
        "statut_livraison": random.choice(['Livré', 'En cours', 'Retardé', 'Annulé'])
    }

async def envoyer_avis():
    """Connexion à Azure Event Hub et envoi continu d'avis clients"""
    try:
         
        # Read Event Hub connection string from env
        connection_str = os.getenv("EVENT_HUB_CONNECTION_STR")
        event_hub_name = os.getenv("EVENT_HUB_NAME")

        if not connection_str or not event_hub_name:
            raise ValueError("Les variables d'environnement EVENT_HUB_CONNECTION_STRING et EVENT_HUB_NAME sont requises.")

        producer = EventHubProducerClient.from_connection_string(
            conn_str=connection_str,
            eventhub_name=event_hub_name
        )

        logger.info("Connexion au Event Hub réussie. Envoi d'avis toutes les 5 secondes...")

        async with producer:
            while True:
                avis = generer_avis()
                event_data = EventData(str(avis))
                await producer.send_batch([event_data])
                logger.info(f"Avis envoyé : {avis}")
                await asyncio.sleep(5)

    except Exception as e:
        logger.error(f"Erreur lors de l'envoi des avis : {e}")

if __name__ == "__main__":
    asyncio.run(envoyer_avis())
