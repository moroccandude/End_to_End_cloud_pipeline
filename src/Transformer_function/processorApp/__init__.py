import os
import re
import json
import logging

import azure.functions as func
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential

# Logger
logger = logging.getLogger("AvisProcessor")
logger.setLevel(logging.INFO)


def clean_text(text: str) -> str:
    """Enlève tous les caractères non-alphanumériques (hors espaces)."""
    return re.sub(r"[^\w\s]", "", text)


def merge_title_comment(avis: dict) -> str:
    """
    Concatène le champ 'titre' (s'il existe) avec le 'commentaire'.
    Résultat : 'Titre Commentaire...'
    """
    titre = avis.get("titre", "").strip()
    comm = avis.get("commentaire", "").strip()
    if titre:
        return f"{titre} {comm}"
    return comm


def get_text_analytics_client() -> TextAnalyticsClient:
    """
    Authentifie vers Text Analytics à partir des variables d'env :
      - COG_SERVICE_ENDPOINT
      - COG_SERVICE_KEY
    """
    endpoint = os.getenv("COG_SERVICE_ENDPOINT")
    key = os.getenv("COG_SERVICE_KEY")
    if not endpoint or not key:
        raise ValueError("Il faut définir COG_SERVICE_ENDPOINT et COG_SERVICE_KEY en App Settings.")
    return TextAnalyticsClient(endpoint=endpoint, credential=AzureKeyCredential(key))


# Instancier une seule fois le client pour réutilisation
ta_client = get_text_analytics_client()


async def main(events: func.EventHubEvent):
    """
    Cette fonction se déclenche pour chaque batch de messages reçus depuis l'Event Hub.
    Elle nettoie et transforme le texte, puis appelle Text Analytics.
    """
    for e in events:
        raw = e.get_body().decode("utf-8")

        # Votre EventData original est un str(dict), donc on remplace ' par " pour JSON
        try:
            avis = json.loads(raw.replace("'", '"'))
        except json.JSONDecodeError:
            logger.error(f"Impossible de parser le message: {raw}")
            continue

        # 1) Nettoyage & fusion
        texte = merge_title_comment(avis)
        texte_nettoye = clean_text(texte)
        logger.info(f"Texte nettoyé : {texte_nettoye}")

        # 2) Appel à Text Analytics (exemple : sentiment analysis)
        try:
            poll = ta_client.analyze_sentiment(documents=[texte_nettoye])[0]
            logger.info(
                f"Sentiment: {poll.sentiment}, "
                f"Scores => positif {poll.confidence_scores.positive:.2f}, "
                f"négatif {poll.confidence_scores.negative:.2f}, "
                f"neutre {poll.confidence_scores.neutral:.2f}"
            )
        except Exception as ex:
            logger.error(f"Erreur Text Analytics: {ex}")

      
    