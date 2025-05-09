import asyncio
import random
import time
from azure.eventhub.aio import EventHubProducerClient
from azure.eventhub import EventData
from azure.identity.aio import DefaultAzureCredential
from faker import Faker
fake = Faker('fr_FR')

def generer_avis():
    # Générer des informations de base
    nom = fake.name()
    email = fake.email()
    adresse = fake.address().replace('\n', ', ')
    date_avis = fake.date_between(start_date='-30d', end_date='today').isoformat()
    
    # Générer des détails de l'avis
    note = random.randint(1, 5)
    commentaires = [
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
    ]
    commentaire = random.choice(commentaires)
    
    # Générer des informations supplémentaires
    produit = fake.word().capitalize()
    categorie = random.choice(['Électronique', 'Vêtements', 'Alimentation', 'Maison', 'Loisirs'])
    prix = round(random.uniform(10.0, 500.0), 2)
    quantite = random.randint(1, 5)
    total = round(prix * quantite, 2)
    mode_paiement = random.choice(['Carte de crédit', 'PayPal', 'Virement bancaire', 'Espèces'])
    statut_livraison = random.choice(['Livré', 'En cours', 'Retardé', 'Annulé'])
    
    avis = {
        "nom": nom,
        "email": email,
        "adresse": adresse,
        "date_avis": date_avis,
        "note": note,
        "commentaire": commentaire,
        "produit": produit,
        "categorie": categorie,
        "prix_unitaire": prix,
        "quantite": quantite,
        "total": total,
        "mode_paiement": mode_paiement,
        "statut_livraison": statut_livraison
    }
    
    return avis

# async def envoyer_avis()
#     credential = DefaultAzureCredential()
#     producer = EventHubProducerClient(
#         fully_qualified_namespace=os.environ[EVENT_HUB_NAMESPACE],
#         eventhub_name=os.environ[EVENT_HUB_NAME],
#         credential=credential
#     )

#     async with producer
#         while True
#             avis = generer_avis()
#             event_data = EventData(str(avis))
#             await producer.send_batch([event_data])
#             print(fAvis envoyé {avis})
#             await asyncio.sleep(5)

#     await credential.close()

if __name__ == "__main__":
    # asyncio.run(envoyer_avis())
    avis=generer_avis()
    print(avis)