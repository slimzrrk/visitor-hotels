# visitor-hotels
🏨 Prédiction du nombre de visiteurs par hôtel

(Streamlit + Random Forest)

Cette application Streamlit prédit le nombre total de visiteurs mensuels pour un hôtel donné à partir d’un jeu de données d’avis d’hôtels.
Elle s’appuie sur un modèle de régression Random Forest entraîné sur des données agrégées par hôtel, mois et année.

✨ Fonctionnalités

Interface web (Streamlit) pour :

Sélectionner un pays, un hôtel, un mois et une année.

Lancer une prédiction du nombre de visiteurs.

Prétraitement automatique des données :

Nettoyage des colonnes inutiles et des valeurs manquantes.

Extraction du nombre de personnes par séjour depuis Tags
(heuristique : Solo=1, Couple=2, Group=3, Family=4).

Encodage du nom d’hôtel (Hotel_Name) en entier.

Transformation de la date d’avis en Month et Year.

Agrégation par (Hotel, Month, Year) pour obtenir Total_Visitors.

Entraînement d’un RandomForestRegressor sur les données agrégées.

📂 Données attendues

Fichier CSV : Hotel_Reviews.csv (par ex. jeu de données Kaggle d’avis d’hôtels).

Colonnes principales utilisées : Hotel_Name, Hotel_Address, Review_Date, Tags.

Dans AI.py, le chemin du fichier est actuellement codé en dur via la variable file_path.
Adaptez ce chemin à votre environnement :

file_path = "/chemin/vers/Hotel_Reviews.csv"

🛠️ Comment ça marche

Chargement du CSV et nettoyage des colonnes inutiles.

Conversion de Review_Date en Month et Year.

Extraction de Num_People à partir de Tags (heuristique).

Encodage de Hotel_Name en Hotel_Name_Encoded.

Agrégation par hôtel/mois/année pour calculer Total_Visitors.

Entraînement d’un modèle Random Forest sur les features :
Hotel_Name_Encoded, Month, Year.

Interface Streamlit permettant de choisir :

Un pays (liste fixe),

Un hôtel filtré par pays,

Un mois,

Une année (futures 2025–2030),

Puis d’afficher la prédiction.

🚀 Installation

Pré-requis : Python 3.9+ recommandé.

Installez les dépendances :

pip install streamlit pandas scikit-learn numpy


Placez le fichier Hotel_Reviews.csv à l’emplacement attendu et mettez à jour file_path dans AI.py si nécessaire.

▶️ Exécution

Lancez l’application Streamlit :

streamlit run AI.py


Dans l’interface :

Choisissez un pays.

Sélectionnez un hôtel (filtré par pays).

Choisissez un mois et une année.

Cliquez sur Prédire.

🗂️ Structure du projet
.
├── AI.py          # Script principal Streamlit (pipeline + modèle + UI)
├── AI.ipynb       # Notebook optionnel (exploration / essais)
└── Hotel_Reviews.csv (à placer ici ou adapter le chemin)

⚠️ Limitations actuelles

Chemin du CSV codé en dur (non portable par défaut).

Heuristique simplifiée pour Num_People à partir de Tags.

Aucune séparation train/test ni métriques de performance (MAE/RMSE).

Liste de pays fixe.

Prédictions sur des années futures sans véritable modèle de séries temporelles.

Modèle réentraîné à chaque exécution (pas de persistance ni de cache).

🔮 Pistes d’amélioration

Rendre le chemin des données configurable (upload Streamlit, variables d’environnement).

Remplacer eval par ast.literal_eval pour parser Tags de manière plus sûre.

Ajouter un split train/validation et des métriques d’évaluation (MAE, RMSE).

Enrichir les features (pays, scores, effets saisonniers…).

Générer dynamiquement la liste des pays depuis Hotel_Address.

Mettre en cache la préparation des données et le modèle (st.cache_data, st.cache_resource).

Sauvegarder/charger le modèle (joblib/pickle) pour éviter de le réentraîner à chaque run.

🛠️ Technologies

Python, Streamlit

pandas, NumPy

scikit-learn (RandomForestRegressor)
