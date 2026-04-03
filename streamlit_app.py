import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

# Configuration de la page
st.set_page_config(
    page_title="Explorateur d'Exoplanètes",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Titre principal
st.title("🌟 Explorateur d'Exoplanètes")
st.markdown("*Exploration interactive du catalogue d'exoplanètes*")

# Chargement des données
@st.cache_data
def load_data():
    """Charge les données des exoplanètes"""
    csv_path = Path(__file__).parent / "open_exoplanet_catalogue" / "scripts" / "planets.csv"
    df = pd.read_csv(csv_path)
    return df

try:
    df = load_data()
except Exception as e:
    st.error(f"Erreur lors du chargement des données: {e}")
    st.stop()

# Barre latérale - Filtres
with st.sidebar:
    st.header("⚙️ Filtres")
    
    # Filtre par distance
    distance_min, distance_max = st.slider(
        "Distance du système (parsecs)",
        float(df['distance'].min()),
        float(df['distance'].max()),
        (float(df['distance'].min()), float(df['distance'].max()))
    )
    
    # Filtre par masse (exclure les valeurs NaN)
    df_with_mass = df[df['masse'].notna()]
    if len(df_with_mass) > 0:
        masse_min, masse_max = st.slider(
            "Masse (masses de Jupiter)",
            float(df_with_mass['masse'].min()),
            float(df_with_mass['masse'].max()),
            (float(df_with_mass['masse'].min()), float(df_with_mass['masse'].max()))
        )
    else:
        masse_min, masse_max = 0, 1
    
    # Filtre par température
    df_with_temp = df[df['temperature'].notna()]
    if len(df_with_temp) > 0:
        temp_min, temp_max = st.slider(
            "Température (Kelvin)",
            int(df_with_temp['temperature'].min()),
            int(df_with_temp['temperature'].max()),
            (int(df_with_temp['temperature'].min()), int(df_with_temp['temperature'].max()))
        )
    else:
        temp_min, temp_max = 0, 1000

# Appliquer les filtres
df_filtered = df[
    (df['distance'] >= distance_min) &
    (df['distance'] <= distance_max)
]

if len(df_with_mass) > 0:
    df_filtered = df_filtered[
        (df_filtered['masse'].isna()) | 
        ((df_filtered['masse'] >= masse_min) & (df_filtered['masse'] <= masse_max))
    ]

if len(df_with_temp) > 0:
    df_filtered = df_filtered[
        (df_filtered['temperature'].isna()) | 
        ((df_filtered['temperature'] >= temp_min) & (df_filtered['temperature'] <= temp_max))
    ]

# Affichage des statistiques
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("📊 Total d'exoplanètes", len(df_filtered))

with col2:
    st.metric("📍 Avec distance", df_filtered['distance'].notna().sum())

with col3:
    st.metric("⚖️ Avec masse", df_filtered['masse'].notna().sum())

with col4:
    st.metric("🌡️ Avec température", df_filtered['temperature'].notna().sum())

st.divider()

# Onglets pour différentes visualisations
tab1, tab2, tab3, tab4 = st.tabs(["📈 Distribution", "🗺️ Spatiale", "📋 Tableau", "ℹ️ À propos"])

with tab1:
    col1, col2 = st.columns(2)
    
    with col1:
        # Distribution de la distance
        if len(df_filtered) > 0:
            fig_distance = px.histogram(
                df_filtered,
                x='distance',
                nbins=50,
                title="Distribution de la distance",
                labels={'distance': 'Distance (parsecs)'},
                color_discrete_sequence=['#1f77b4']
            )
            st.plotly_chart(fig_distance, use_container_width=True)
    
    with col2:
        # Distribution de la masse (exclure NaN)
        df_mass = df_filtered[df_filtered['masse'].notna()]
        if len(df_mass) > 0:
            fig_mass = px.histogram(
                df_mass,
                x='masse',
                nbins=30,
                title="Distribution de la masse",
                labels={'masse': 'Masse (masses de Jupiter)'},
                color_discrete_sequence=['#ff7f0e']
            )
            st.plotly_chart(fig_mass, use_container_width=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Distribution de la température
        df_temp = df_filtered[df_filtered['temperature'].notna()]
        if len(df_temp) > 0:
            fig_temp = px.histogram(
                df_temp,
                x='temperature',
                nbins=40,
                title="Distribution de la température",
                labels={'temperature': 'Température (Kelvin)'},
                color_discrete_sequence=['#2ca02c']
            )
            st.plotly_chart(fig_temp, use_container_width=True)
    
    with col2:
        # Relation Masse vs Température
        df_scatter = df_filtered[(df_filtered['masse'].notna()) & (df_filtered['temperature'].notna())]
        if len(df_scatter) > 0:
            fig_scatter = px.scatter(
                df_scatter,
                x='masse',
                y='temperature',
                hover_name='nom',
                title="Relation Masse vs Température",
                labels={'masse': 'Masse (MJ)', 'temperature': 'Température (K)'},
                color_discrete_sequence=['#d62728']
            )
            st.plotly_chart(fig_scatter, use_container_width=True)

with tab2:
    # Visualisation spatiale (simples projections)
    df_spatial = df_filtered[(df_filtered['ascension_droite'].notna()) & (df_filtered['declinaison'].notna())]
    
    if len(df_spatial) > 0:
        st.subheader("Distribution spatiale des systèmes")
        
        # Créer une projection simple (juste pour visualiser)
        fig_spatial = px.scatter(
            df_spatial,
            x='ascension_droite',
            y='declinaison',
            size='distance',
            hover_name='nom',
            title="Position des systèmes planétaires",
            labels={
                'ascension_droite': "Ascension droite (h m s)",
                'declinaison': "Déclinaison (° \' \")"
            },
            color_discrete_sequence=['#9467bd']
        )
        st.plotly_chart(fig_spatial, use_container_width=True)
    else:
        st.info("Pas de données spatiales disponibles pour les filtres sélectionnés.")

with tab3:
    st.subheader("Données filtrées")
    
    # Sélection de colonnes à afficher
    cols_to_show = st.multiselect(
        "Colonnes à afficher:",
        df_filtered.columns.tolist(),
        default=['nom', 'distance', 'masse', 'temperature']
    )
    
    if cols_to_show:
        # Afficher le tableau
        st.dataframe(
            df_filtered[cols_to_show].sort_values('distance', ascending=True),
            use_container_width=True,
            height=500
        )
        
        # Option de téléchargement
        csv = df_filtered[cols_to_show].to_csv(index=False)
        st.download_button(
            label="📥 Télécharger les données (CSV)",
            data=csv,
            file_name="exoplanetes_filtrees.csv",
            mime="text/csv"
        )
    else:
        st.warning("Sélectionnez au moins une colonne à afficher.")

with tab4:
    st.subheader("À propos de ce projet")
    st.markdown("""
    ### 🌍 Exploration d'Exoplanètes
    
    Cette application explore les données du **Open Exoplanet Catalogue**, 
    une base de données communautaire d'exoplanètes découvertes.
    
    #### 📊 Données disponibles:
    - **Nom**: Désignation officielle de l'exoplanète
    - **Distance**: Distance du système par rapport au Soleil (parsecs)
    - **Ascension droite & Déclinaison**: Coordonnées célestes
    - **Masse**: Masse relative à Jupiter
    - **Température**: Température estimée de la planète
    
    #### 💡 Utilisation:
    1. Utilisez les filtres dans la barre latérale pour affiner votre recherche
    2. Explorez les distributions et relations entre les variables
    3. Consultez la carte spatiale des systèmes
    4. Téléchargez les données filtrées
    
    #### 📚 Source:
    [Open Exoplanet Catalogue](https://openexoplanetcatalogue.com/)
    """)
    
    st.divider()
    st.info(f"Total d'exoplanètes dans la base: {len(df)}")
