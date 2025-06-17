

# Projet : Analyse de tweets avec InPoDa


**Description :**  
Ce projet consiste à collecter, nettoyer, analyser et visualiser des tweets. Les étapes incluent le traitement des données JSON, l'extraction de métadonnées, l'analyse de sentiment, et la visualisation des résultats.


# Instructions pour le projet Twitter Analysis


## Pré-requis
- Python 3.6 et plus


## Exécution du projet


Le projet peut être exécuté dans un environnement Jupyter Notebook. Suivez les étapes ci-dessous pour exécuter le projet de manière autonome :


1. **Installez les bibliothèques nécessaires** :
   Exécutez la cellule suivante pour installer toutes les bibliothèques Python nécessaires pour ce projet. Ces bibliothèques incluent `json`, `re`, `textblob`, `matplotlib`, et d'autres qui sont utilisées pour le traitement des tweets, l'analyse des sentiments, et la génération des visualisations.


2. **Chargez le fichier contenant les tweets** :
   Téléchargez le fichier `versailles_tweets.json` (ou tout autre fichier contenant des tweets au format JSON). Vous pouvez aussi remplacer le chemin du fichier dans le code par le chemin d'un autre fichier de votre choix.


3. **Exécutez les différentes étapes dans l'ordre** :
   Le notebook est conçu pour être exécuté dans l'ordre, sans nécessiter de modification. Une fois le fichier téléchargé et les bibliothèques installées, vous pouvez lancer chaque cellule dans l'ordre pour :
   - Charger et valider les tweets
   - Nettoyer et analyser le contenu
   - Extraire des informations pertinentes (hashtags, mentions, sentiments)
   - Générer des visualisations interactives des résultats.
   
## **Note** : les captures d'écran de l'éxecution résultante sur ma machine sont jointes.  


## Résultat de l'exécution :
- Après l'exécution des cellules, le projet traitera les tweets, générera des graphiques interactifs, et affichera des informations statistiques, telles que les tweets les plus fréquents, les sentiments globaux et les hashtags populaires.


## Étapes du projet


### 1. **Chargement des tweets**
Les tweets sont chargés depuis un fichier JSON ou texte, chaque tweet étant représenté par un dictionnaire.


### 2. **Validation de la structure des tweets**
La structure des tweets est vérifiée pour s'assurer qu'ils contiennent les informations essentielles telles que l'ID de l'auteur, le texte et la date de création.


### 3. **Nettoyage des tweets**
Les tweets sont nettoyés en supprimant les caractères spéciaux, les emojis et les espaces inutiles.


### 4. **Extraction des informations**
Les informations extraites incluent l'auteur, les hashtags, les mentions, ainsi que l'analyse des sentiments (positif, négatif, neutre) et des mots-clés.


### 5. **Analyse et Statistiques**
Des statistiques sont générées, telles que le nombre de tweets par utilisateur, les hashtags les plus fréquents et la répartition des sentiments.


### 6. **Visualisation**
Les résultats sont affichés sous forme de graphiques pour visualiser les hashtags les plus fréquents, la répartition des sentiments et l'activité des utilisateurs.



##  Auteur
** Graichi hemama **  
GitHub: https://github.com/hemamagr
