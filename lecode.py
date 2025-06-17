import json
import re
from collections import Counter
from textblob import TextBlob
import matplotlib.pyplot as plt
 
 

def charge_tweets(file_path):
    """
    Charge les tweets depuis un fichier JSON ou texte.
    
    Args:
        file_path (str): Chemin du fichier contenant les tweets.
        
    Returns:
        list: Une liste de tweets (chaque tweet est représenté par un dictionnaire).
    """
    tweets = []
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            if file_path.endswith('.json'):
                # Chargement pour un fichier JSON structuré (liste complète)
                tweets = json.load(file)  # Utilisez json.load pour lire tout le fichier
            else:
                # Chargement pour un fichier texte ligne par ligne
                for line in file:
                    tweet = json.loads(line.strip())  # Chaque ligne est un JSON
                    tweets.append(tweet)
    except FileNotFoundError:
        print(f"Erreur : Le fichier '{file_path}' est introuvable.")
    except json.JSONDecodeError as e:
        print(f"Erreur : Le fichier '{file_path}' contient des données non valides : {e}")
    return tweets

       


def valider_structure_tweet(tweet, required_keys=None):
    """
    Valide la structure d'un tweet.
    
    Args:
        tweet (dict): Un dictionnaire représentant un tweet.
        required_keys (list): Liste des clés obligatoires (par défaut : ["author_id", "text", "created_at"]).
        
    Returns:
        bool: True si le tweet contient toutes les clés requises, False sinon.
    """
    
    # Vérifier si tweet est un dictionnaire
    if not isinstance(tweet, dict):
        print("Le paramètre tweet doit être un dictionnaire.")
    
    # Définir les clés requises si elles ne sont pas fournies
    
    required_keys = ["author_id", "text", "created_at"]
    
    # Vérifier la présence des clés requises
    for key in required_keys:
        if key not in tweet:
            return False
    return True
    
   
def clean_tweet(tweet):
    
    """
    Nettoie le contenu d'un tweet en supprimant les caractères spéciaux, emojis et espaces inutiles.
    
    Args:
        tweet (dict): Un dictionnaire représentant un tweet.
        
    Returns:
        dict: Un tweet nettoyé (modification en place).
    """
    #definir la fonction issue de la bibliothèque re
   # qui va supprimer les emojis
    emoji_pattern = re.compile(
    "[\U0001F600-\U0001F64F"  # Smileys
    "\U0001F300-\U0001F5FF"  # Symboles divers
    "\U0001F680-\U0001F6FF"  # Transport et autres symboles
    "\U0001F700-\U0001F77F"  # Alchimie
    "\U0001F780-\U0001F7FF"  # Géométrie
    "\U0001F800-\U0001F8FF"  # Suppléments divers
    "\U0001F900-\U0001F9FF"  # Visages supplémentaires
    "\U0001FA00-\U0001FA6F"  # Objets divers
    "\U0001FA70-\U0001FAFF"  # Symboles supplémentaires
    "\U00002700-\U000027BF"  # Dingbats
    "\U0001F1E6-\U0001F1FF"  # Drapeaux régionaux
    "\U00002500-\U00002BEF"  # Encadrés, flèches, etc.
    "]+",
    flags=re.UNICODE
    )
    if "text" in tweet:
        # Supprimer les caractères spéciaux sauf hashtags et mentions
        cleaned_content = re.sub(r"[^a-zA-Z0-9@#\s]", "", tweet["text"])
        
        # Supprimer les emojis du contenu
        cleaned_content = emoji_pattern.sub("", cleaned_content)
        
        # Supprimer les espaces multiples
        cleaned_content = re.sub(r"\s+", " ", cleaned_content).strip()
        tweet["text"] = cleaned_content
    return tweet

def à_zone_daterissage(tweets, zone_ater):
   
    """
     Enregistre les tweets nettoyés dans un fichier de la zone d'atterrissage.
    
    Args:
        tweets (list): Liste de dictionnaires représentant des tweets.
        zone_ater (str): Chemin du fichier de sortie.
    """
    try:
        with open(zone_ater, 'w',encoding='utf-8') as file:
            
            # écrire les tweetts ligne par ligne dans un autre fichier
            for tweet in tweets:
                json_line = json.dumps(tweet)
                file.write(json_line + '\n')
        print(f"Les tweets ont été enregistrés dans la zone d'atterrissage : {zone_ater}")
    except Exception as e:
        print(f"Erreur lors de l'enregistrement : {e}")





# EXTRACTION ET ANALYSE DES DONNEES

def extraire_auteur(tweet):
    """
    Extrait l'auteur d'un tweet.
    Args:
        tweet (dict): Dictionnaire representant un tweet.
    Returns:
        str: L'ID de l'auteur.
    """
    return tweet.get("author_id", "Inconnu")

def extraire_hashtags(tweet):
    """
    Extrait les hashtags d'un tweet.
    Args:
        tweet (dict): Dictionnaire representant un tweet.
    Returns:
        list: Liste des hashtags extraits.
    """
    hashtags = re.findall(r"#\w+", tweet.get("text", ""))
    return hashtags

def extraire_mentions(tweet):
    """
    Extrait les mentions d'un tweet.
    Args:
        tweet (dict): Dictionnaire representant un tweet.
    Returns:
        list: Liste des mentions extraites.
    """
    #on utilise get() pour empêcher l'apparition d'une erreur si la clé "text" 
    # est manquante ,on renvoie donc une chaine vide.
    mentions = re.findall(r"@\w+", tweet.get("text", ""))
    return mentions

def analyse_sentiment(tweet):
    """
    Analyse le sentiment d'un tweet (positif, negatif ou neutre).
    Args:
        tweet (dict): Dictionnaire representant un tweet.
    Returns:
        str: Sentiment (positif, negatif ou neutre).
    """
    analyse = TextBlob(tweet.get("text", ""))
    if analyse.sentiment.polarity > 0:
        return "positif"
    elif analyse.sentiment.polarity < 0:
        return "negatif"
    else:
        return "neutre"

def identifier_topics(tweet):
    """
    Identifie les mots cles comme des sujets dans un tweet.
    Args:
        tweet (dict): Dictionnaire representant un tweet.
    Returns:
        list: Liste des mots cles consideres comme sujets.
    """
    words = re.findall(r"\b[a-zA-Z]{4,}\b", tweet.get("text", ""))  # Mots de 4 lettres ou plus
    return words


#2 GENERATION DES STATISTIQUES

def top_k_items(items, k):
    """
    Retourne les K elements les plus frequents dans une liste.
    Args:
        items (list): Liste d'elements.
        k (int): Nombre d'elements a retourner.
    Returns:
        list: Liste des K elements les plus frequents avec leur frequence.
    """
    counter = Counter(items)
    return counter.most_common(k)

def tweet_par_utilisateur(tweets):
    """
    Compte le nombre de tweets par utilisateur.
    Args:
        tweets (list): Liste des tweets (dictionnaires).
    Returns:
        dict: Dictionnaire avec l'auteur et le nombre de tweets.
    """
    

    # Initialiser un dictionnaire pour compter les occurrences
    author_counts = {}

    # Parcourir les tweets
    for tweet in tweets:
        author_id = tweet.get("author_id", "Inconnu")  # Récupérer l'author_id ou "Inconnu"
        if author_id in author_counts:
            author_counts[author_id] += 1  # Incrémenter le compteur
        else:
            author_counts[author_id] = 1   # Initialiser le compteur à 1
            
    return author_counts
   


def filtrer_tweets(tweets, user):
    """
    Filtre les tweets d'un utilisateur specifique.
    Args:
        tweets (list): Liste des tweets (dictionnaires).
        user (str): ID de l'utilisateur a filtrer.
    Returns:
        list: Liste des tweets de l'utilisateur.
    """
    return [tweet for tweet in tweets 
            if tweet.get("author_id") == user]

def filtrer_par_mention(tweets, mention):
    """
    Filtre les tweets contenant une mention specifique.
    Args:
        tweets (list): Liste des tweets (dictionnaires).
        mention (str): Mention a rechercher (ex: '@user').
    Returns:
        list: Liste des tweets contenant la mention.
    """
    result = []  # Liste pour stocker les tweets correspondants
    for tweet in tweets:
        if mention in extraire_mentions(tweet):  # Vérifier si la mention est présente
            result.append(tweet)  # Ajouter le tweet à la liste
    return result


#3 VISUALISATION DES RESULTATS

def top_k_hashtags(tweets, k):
    """
    Affiche les Top K hashtags les plus fréquents dans les tweets.
    
    Args:
        tweets (list): Liste des tweets (dictionnaires).
        k (int): Nombre de hashtags à afficher.
    """
    all_hashtags = []  # Liste pour stocker tous les hashtags
    for tweet in tweets:
        hashtags = extraire_hashtags(tweet)  # Extraire les hashtags du tweet
        for hashtag in hashtags:  # Parcourir les hashtags extraits
            all_hashtags.append(hashtag)  # Ajouter chaque hashtag à la liste

    if not all_hashtags:
        print("Aucun hashtag trouvé dans les tweets.")
        return
    
    top_hashtags = top_k_items(all_hashtags, k)  # Utilise la fonction top_k_items
    labels, values = zip(*top_hashtags)
    
    plt.figure(figsize=(10, 6))
    plt.bar(labels, values, color='grey')
    plt.title(f"Top {k} Hashtags")
    plt.xlabel("Hashtags")
    plt.ylabel("Fréquence")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def plot_sentiment_distribution(tweets):
    """
    Affiche la répartition des sentiments (positif, négatif, neutre) dans les tweets.
    
    Args:
        tweets (list): Liste des tweets (dictionnaires).
    """
    all_sentiments = []  # Liste pour stocker les résultats d'analyse de sentiment
    for tweet in tweets:
        if "text" in tweet:  # Vérifier si le champ "text" existe dans le tweet
            sentiment = analyse_sentiment(tweet)  # Analyser le sentiment du tweet
            all_sentiments.append(sentiment)  # Ajouter le résultat à la liste

    if not all_sentiments:
        print("Aucun sentiment n'a pu être analysé dans les tweets.")
        return
    
    sentiment_counts = Counter(all_sentiments)  # Compte les occurrences des sentiments
    labels = sentiment_counts.keys()
    sizes = sentiment_counts.values()
    colors = ['lightgreen', 'lightcoral', 'lightgrey']  # Couleurs pour positif, négatif et neutre

    plt.figure(figsize=(8, 8))
    plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
    plt.title("Répartition des Sentiments des Tweets")
    plt.axis('equal')  # Assure que le graphique reste circulaire
    plt.tight_layout()
    plt.show()


def plot_user_activity(tweets, top_n=10):
    """
    Affiche les utilisateurs les plus actifs avec un graphique en barres.
    
    Args:
        tweets (list): Liste des tweets (dictionnaires).
        top_n (int): Nombre d'utilisateurs à afficher.
    """
    user_counts = tweet_par_utilisateur(tweets)  # Compte le nombre de tweets par utilisateur
    if not user_counts:
        print("Aucune activité d'utilisateur trouvée.")
        return
    
    top_users = user_counts.most_common(top_n)  # Utilise Counter pour les utilisateurs les plus actifs
    labels, values = zip(*top_users)
    
    plt.figure(figsize=(12, 6))
    plt.bar(labels, values, color='orange')
    plt.title(f"Top {top_n} Utilisateurs les Plus Actifs")
    plt.xlabel("ID des Utilisateurs")
    plt.ylabel("Nombre de Tweets")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
   file_path = "versailles_tweets.json"  
   tweets = charge_tweets(file_path)

valid_tweets = []  # Liste pour stocker les tweets valides

if tweets:  # Vérifier si la liste de tweets n'est pas vide
    for tweet in tweets:
        if valider_structure_tweet(tweet):  # Vérifier si le tweet a une structure valide
            cleaned_tweet = clean_tweet(tweet)  # Nettoyer le tweet
            valid_tweets.append(cleaned_tweet)  # Ajouter le tweet nettoyé à la liste

    
    print(f"Nombre de tweets valides après nettoyage : {len(valid_tweets)}")
    
    # 2-Extraction et statistiques
    print("Extraction des hashtags...")

    all_hashtags = []  # Liste pour stocker tous les hashtags extraits
    for tweet in valid_tweets:  # Parcourir chaque tweet valide
        hashtags = extraire_hashtags(tweet)  # Extraire les hashtags pour ce tweet
        all_hashtags.extend(hashtags)  # Ajouter les hashtags à la liste globale

    # Afficher le nombre total de hashtags extraits
    print(f"Nombre total de hashtags trouvés : {len(all_hashtags)}\n")

    # 3-Visualisation
    print("Visualisation des Top 5 hashtags :")
    top_k_hashtags(valid_tweets, k=5)
    
    print("Visualisation de la répartition des sentiments :")
    plot_sentiment_distribution(valid_tweets)
    
    print("Visualisation des utilisateurs les plus actifs (Top 10) :")
    plot_user_activity(valid_tweets, top_n=10)
    
else:
    print("Aucune donnée à traiter.")
