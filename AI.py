#!/usr/bin/env python
# coding: utf-8

# In[1]:


import streamlit as st
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
import numpy as np


# In[11]:


# Charger les données
file_path = 'c:/Users/Asus/Downloads/archive (2)/Hotel_Reviews.csv'  
data = pd.read_csv(file_path)



# In[12]:


# Nettoyer les données
columns_to_drop = [ 'lat', 'lng', 'days_since_review', 'Positive_Review', 'Negative_Review']
data = data.drop(columns=columns_to_drop, axis=1)
data = data.dropna()


# In[13]:


# Fonction pour extraire le nombre de personnes
if 'Tags' in data.columns:
    def extract_num_people(tags):
        try:
            tags_list = eval(tags) if isinstance(tags, str) else tags
            if any("Couple" in tag for tag in tags_list):
                return 2
            elif any("Family" in tag for tag in tags_list):
                return 4
            elif any("Solo" in tag for tag in tags_list):
                return 1
            elif any("Group" in tag for tag in tags_list):
                return 3
            else:
                return 2
        except:
            return 2

    data['Num_People'] = data['Tags'].apply(extract_num_people)
    data = data.drop(['Tags'], axis=1)


# In[14]:


# Encoder le nom de l'hôtel
encoder = LabelEncoder()
data['Hotel_Name_Encoded'] = encoder.fit_transform(data['Hotel_Name'])

# Transformer Review_Date en datetime
data['Review_Date'] = pd.to_datetime(data['Review_Date'], errors='coerce')
data['Month'] = data['Review_Date'].dt.month
data['Year'] = data['Review_Date'].dt.year
data = data.drop(columns=['Review_Date'])

# Regrouper les données pour calculer la somme des visiteurs
aggregated_data = data.groupby(['Hotel_Name_Encoded', 'Month', 'Year'], as_index=False).agg(
    Total_Visitors=('Num_People', 'sum')
)


# In[15]:


# Préparer les données pour le modèle
features = ['Hotel_Name_Encoded', 'Month', 'Year']
X = aggregated_data[features]
y = aggregated_data['Total_Visitors']

# Entraîner le modèle
model = RandomForestRegressor(n_estimators=300, random_state=42)
model.fit(X, y)


# In[ ]:


# Streamlit App
st.title("Prédiction des visiteurs d'un hôtel")

# Liste fixe des pays extraits des adresses
countries = ["United Kingdom", "France", "Netherlands", "Italy", "Spain", "Austria"]

# Bouton radio pour sélectionner un pays
country = st.radio("Sélectionnez le pays", countries)

# Filtrer les hôtels par pays sélectionné
filtered_hotels = data[data['Hotel_Address'].str.contains(country, na=False)]['Hotel_Name'].unique()

# Ajouter un selectbox pour les hôtels filtrés
hotel_name = st.selectbox("Sélectionnez l'hôtel", filtered_hotels)

# Ajouter un selectbox pour le mois
month_dict = {
    "Janvier": 1, "Février": 2, "Mars": 3, "Avril": 4, "Mai": 5,
    "Juin": 6, "Juillet": 7, "Août": 8, "Septembre": 9,
    "Octobre": 10, "Novembre": 11, "Décembre": 12
}
month = st.selectbox("Sélectionnez le mois", list(month_dict.keys()))

# Ajouter un selectbox pour les années futures
future_years = list(range(2025, 2031))  # Années futures pour les prédictions
year = st.selectbox("Sélectionnez l'année", future_years)

# Prédire avec les sélections
if st.button("Prédire", key="predict_button"):
    hotel_name_encoded = encoder.transform([hotel_name])[0]
    new_data = pd.DataFrame({
        'Hotel_Name_Encoded': [hotel_name_encoded],
        'Month': [month_dict[month]],  # Convertir le mois en entier
        'Year': [year]
    })

    predicted_visitors = model.predict(new_data)[0]
    st.write(f"Nombre total de visiteurs prédits pour {hotel_name} en {month} {year} : {predicted_visitors:.0f}")

