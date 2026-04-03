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
st.markdown("*Exploration interactive et éducative du catalogue d'exoplanètes*")

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

# Navigation principale
nav_tabs = st.tabs([
    "📚 Introduction",
    "📊 Données & Missions",
    "📖 Paramètres Expliqués",
    "🌍 Premiers Exemples",
    "🗺️ Carte Spatiale",
    "📥 Télécharger",
    "📈 Analyses Avancées"
])

# TAB 1: INTRODUCTION
with nav_tabs[0]:
    st.header("🌌 Bienvenue dans l'Explorateur d'Exoplanètes")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### Qu'est-ce qu'une exoplanète?
        
        Une **exoplanète** est une planète qui orbite autour d'une étoile autre que le Soleil. 
        
        Pendant longtemps, nous ne connaissions que les 8 planètes de notre système solaire. 
        Depuis la découverte de la première exoplanète en 1995 (51 Pegasi b), 
        nous en avons découvert des **milliers**!
        
        ### Importance Scientifique
        
        Les exoplanètes nous aident à comprendre:
        - ✨ Comment les systèmes planétaires se forment
        - 🔭 La diversité des mondes dans l'univers
        - 🌱 Où chercher la vie extra-terrestre
        - 🚀 L'évolution future de l'astronomie
        """)
    
    with col2:
        st.metric("🪐 Total d'exoplanètes détectées", f"{len(df):,}")
        st.metric("📍 Avec distance connue", f"{df['distance'].notna().sum():,}")
        st.metric("⚖️ Avec masse connue", f"{df['masse'].notna().sum():,}")
        st.metric("🌡️ Avec température estimée", f"{df['temperature'].notna().sum():,}")

# TAB 2: DONNÉES & MISSIONS
with nav_tabs[1]:
    st.header("📊 Source des Données et Missions Spatiales")
    
    st.markdown("""
    ### 🌐 Open Exoplanet Catalogue
    
    Cette application utilise les données du **Open Exoplanet Catalogue**, 
    une base de données open-source et communautaire.
    
    **Source officielle:** https://openexoplanetcatalogue.com/
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🛰️ Missions Principales")
        st.markdown("""
        #### Kepler Space Telescope (2009-2018)
        - 🎯 **Mission:** Détection des transits planétaires
        - 📊 **Découvertes:** ~2,662 exoplanètes confirmées
        - 📍 **Champ:** Constellations du Cygne et de la Lyre
        - 🏆 La mission la plus prolifique pour les exoplanètes
        
        #### TESS (2018-present)
        - 🎯 **Mission:** Transit Exoplanet Survey Satellite
        - 📊 **Découvertes:** +5,000 exoplanètes confirmées
        - 🌍 **Couverture:** 85% du ciel
        - 🔍 Très sensible aux planètes proches
        
        #### Radial Velocity Methods
        - 🎯 **Méthode:** Mesure du "wobble" des étoiles
        - 📊 **Avantage:** Détermine directement la masse
        - 📍 **Historique:** Méthode de la première découverte
        """)
    
    with col2:
        st.subheader("🔬 Autres Techniques de Détection")
        st.markdown("""
        #### Transit Photometry
        - Mesure la légère baisse de luminosité
        - Quand une planète passe devant son étoile
        - **Plus de 70% des découvertes** utilise cette méthode
        
        #### Direct Imaging
        - Prendre des photos directes de la planète
        - Très difficile (planète ~milliards de fois moins brillante)
        - Pour les planètes jeunes et chaudes seulement
        
        #### Gravitational Microlensing
        - Utilise les effets de lentille gravitationnelle
        - Peut détecter des planètes très lointaines
        - Méthode la plus exotique
        
        #### Astrometry
        - Mesure la position apparente de l'étoile
        - Très précis avec les satellites modernes
        """)
    
    st.divider()
    
    st.subheader("📈 Évolution du Nombre de Découvertes")
    
    # Créer une tendance d'années fictives pour illustration
    st.info("""
    💡 **Observation:** Le nombre d'exoplanètes découvertes augmente exponentiellement!
    - 1995: 1 exoplanète
    - 2010: ~500 exoplanètes
    - 2020: ~4,300 exoplanètes
    - 2024: +5,500 exoplanètes
    
    Cette accélération est due à l'amélioration des télescopes et des techniques de détection.
    """)

# TAB 3: PARAMÈTRES EXPLIQUÉS
with nav_tabs[2]:
    st.header("📖 Comprendre les Paramètres")
    
    st.markdown("""
    Cette base de données contient des informations essentielles sur chaque exoplanète.
    Voici une explication détaillée de chaque paramètre:
    """)
    
    # Créer des expanders pour chaque paramètre
    tabs_params = st.columns(2)
    
    with tabs_params[0]:
        with st.expander("📛 **NOM** - Désignation de la planète", expanded=True):
            st.markdown("""
            - **Exemple:** Kepler-1032 b, HD 154857 c
            - **Format:** `[Nom du système] [Lettre]`
            - **Signification:** La lettre indique l'ordre de découverte
              - `b` = première planète découverte
              - `c` = deuxième planète découverte
              - etc.
            - **Importance:** Identifie de manière unique la planète
            """)
        
        with st.expander("📏 **DISTANCE** - Distance du système"):
            st.markdown("""
            - **Unité:** Parsecs (pc)
            - **1 parsec = 3.26 années-lumière**
            - **Exemple:** 64.2 pc = environ 209 années-lumière
            - **Importance:** Distance pour étudier les propriétés intrinsèques
            - **Méthode:** Parallaxe stellaire (très précis avec les satellites)
            - **Comment interpréter:**
              - < 10 pc: Très proche (accessibles aux télescopes amateurs)
              - 10-100 pc: Proches
              - > 1000 pc: Très lointaines (même pour les professionnels)
            """)
        
        with st.expander("➡️ **ASCENSION DROITE** - Coordonnée céleste (horizontale)"):
            st.markdown("""
            - **Format:** Heures, minutes, secondes (h m s)
            - **Exemple:** 19 19 43.4040 = 19h 19m 43.4040s
            - **Plage:** 0h à 24h (une rotation complète)
            - **Équivalent terrestre:** La longitude sur Terre
            - **Importance:** Localise la position de l'étoile sur la sphère céleste
            - **Remarque:** Utilisée avec la déclinaison pour un positionnement exact
            """)
        
        with st.expander("📍 **DÉCLINAISON** - Coordonnée céleste (verticale)"):
            st.markdown("""
            - **Format:** Degrés, arcminutes, arcseconde (° ' ")
            - **Exemple:** +40 05 51.8400 = +40° 05' 51.8400"
            - **Plage:** -90° (pôle sud céleste) à +90° (pôle nord céleste)
            - **Équivalent terrestre:** La latitude sur Terre
            - **Importance:** Localise la position de l'étoile sur la sphère céleste
            - **Remarque:** Positive au nord, négative au sud
            """)
    
    with tabs_params[1]:
        with st.expander("⚖️ **MASSE** - Poids relatif de la planète", expanded=True):
            st.markdown("""
            - **Unité:** Masses de Jupiter (M_J)
            - **1 masse de Jupiter ≈ 318 masses terrestres**
            - **Exemple:** 2.24 = 2.24 fois plus massif que Jupiter
            - **Importance:** Détermine le type de planète
            - **Classification:**
              - < 0.1 M_J: Planète terrestre (super-Terre)
              - 0.1 - 1 M_J: Planète intermédiaire
              - > 1 M_J: Géante gazeuse (comme Jupiter)
            - **Comment obtenir:** Spectroscopie Doppler (radial velocity)
            - **⚠️ Données partielles:** Beaucoup de planètes n'ont pas la masse mesurée
            """)
        
        with st.expander("🌡️ **TEMPÉRATURE** - Température estimée de la surface"):
            st.markdown("""
            - **Unité:** Kelvin (K)
            - **Conversion:** K = °C + 273.15
            - **Exemple:** 336 K = 62.85°C (planète chaude!)
            - **Importance:** Détermine l'habitabilité potentielle
            - **Classification approximative:**
              - < 200 K: Planète froide (lointaine de son étoile)
              - 200-400 K: Zone habitable potentielle
              - > 1000 K: Planète très chaude (proche de son étoile)
            - **Comment obtenir:** Modèles thermiques basés sur:
              - Distance à l'étoile
              - Luminosité de l'étoile
              - Albédo supposé de la planète
            - **⚠️ Incertitude:** Cette valeur est estimée, pas mesurée directement
            """)
        
        with st.expander("🏷️ **TYPE** - Classification de l'objet"):
            st.markdown("""
            - **Valeur dans cette base:** "planet" (planète)
            - **Importance:** Permet de filtrer les planètes vs autres objets
            - **Autres types possibles:** 
              - star: Étoile
              - planet: Planète confirmée
              - moonplanet: Possible lune de planète
            - **Remarque:** Cette base contient uniquement des planètes
            """)

# TAB 4: PREMIERS EXEMPLES
with nav_tabs[3]:
    st.header("🌍 Les 5 Premières Exoplanètes (par distance)")
    
    st.markdown("""
    Voici les 5 exoplanètes les plus proches de nous, selon les données du catalogue.
    Ces planètes sont particulièrement intéressantes car elles sont accessibles aux télescopes modernes.
    """)
    
    # Trier par distance et prendre les 5 premières
    df_sorted = df.sort_values('distance').head(5)
    
    # Afficher chaque planète
    for idx, (_, row) in enumerate(df_sorted.iterrows(), 1):
        with st.container(border=True):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown(f"### #{idx} - {row['nom']}")
                st.markdown(f"**Type:** {row['type']}")
            
            with col2:
                st.metric("Distance", f"{row['distance']:.2f} pc" if pd.notna(row['distance']) else "N/A")
                st.metric("Masse", f"{row['masse']:.2f} M_J" if pd.notna(row['masse']) else "N/A")
            
            with col3:
                st.metric("Température", f"{row['temperature']:.0f} K" if pd.notna(row['temperature']) else "N/A")
            
            # Détails supplémentaires
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"""
                **Coordonnées Célestes:**
                - RA: {row['ascension_droite']}
                - Dec: {row['declinaison']}
                """)
            with col2:
                # Calcul de la distance en années-lumière
                if pd.notna(row['distance']):
                    al = row['distance'] * 3.26156
                    st.markdown(f"""
                    **Distance en années-lumière:**
                    - {al:.1f} années-lumière
                    """)
    
    st.divider()
    
    st.subheader("📊 Tableau Complet des 5 Premières")
    st.dataframe(
        df_sorted[['nom', 'distance', 'ascension_droite', 'declinaison', 'masse', 'temperature']],
        use_container_width=True
    )

# TAB 5: CARTE SPATIALE
with nav_tabs[4]:
    st.header("🗺️ Carte Spatiale des Exoplanètes")
    
    st.markdown("""
    Cette carte montre la distribution spatiale des systèmes planétaires dans le ciel.
    - **Axe X:** Ascension droite (position E-O)
    - **Axe Y:** Déclinaison (position N-S)
    - **Taille des points:** Proportionnelle à la distance du système
    """)
    
    # Filtrer les données avec coordonnées valides
    df_spatial = df[(df['ascension_droite'].notna()) & (df['declinaison'].notna())]
    
    if len(df_spatial) > 0:
        # Créer la visualisation
        fig_spatial = px.scatter(
            df_spatial,
            x='ascension_droite',
            y='declinaison',
            size='distance',
            hover_name='nom',
            hover_data={
                'distance': ':.1f',
                'masse': ':.2f',
                'temperature': ':.0f',
                'ascension_droite': False,
                'declinaison': False
            },
            title="Distribution spatiale des systèmes planétaires",
            labels={
                'ascension_droite': "Ascension droite (h m s)",
                'declinaison': "Déclinaison (° ' \")",
                'distance': 'Distance (pc)'
            },
            size_max=30,
            color_discrete_sequence=['#1f77b4']
        )
        
        fig_spatial.update_layout(
            height=600,
            showlegend=False,
            hovermode='closest'
        )
        
        st.plotly_chart(fig_spatial, use_container_width=True)
        
        st.info(f"📊 {len(df_spatial):,} systèmes affichés sur la carte")
    else:
        st.warning("Pas de données spatiales disponibles")

# TAB 6: TÉLÉCHARGER
with nav_tabs[5]:
    st.header("📥 Télécharger les Données")
    
    st.markdown("""
    Vous pouvez télécharger l'ensemble des données des exoplanètes en différents formats.
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Télécharger CSV complet
        csv_full = df.to_csv(index=False)
        st.download_button(
            label="📥 Télécharger TOUTES les planètes (CSV)",
            data=csv_full,
            file_name="exoplanetes_complete.csv",
            mime="text/csv",
            use_container_width=True
        )
        
        st.markdown(f"**Nombre de planètes:** {len(df)}")
        st.markdown(f"**Taille du fichier:** ~{len(csv_full) / 1024:.1f} KB")
    
    with col2:
        # Télécharger seulement les planètes avec données complètes
        df_complete = df[(df['distance'].notna()) & 
                         (df['masse'].notna()) & 
                         (df['temperature'].notna())]
        csv_complete = df_complete.to_csv(index=False)
        st.download_button(
            label="📥 Planètes avec DONNÉES COMPLÈTES (CSV)",
            data=csv_complete,
            file_name="exoplanetes_donnees_completes.csv",
            mime="text/csv",
            use_container_width=True
        )
        
        st.markdown(f"**Nombre de planètes:** {len(df_complete)}")
        st.markdown(f"**Taille du fichier:** ~{len(csv_complete) / 1024:.1f} KB")
    
    st.divider()
    
    st.subheader("📊 Aperçu des données")
    st.markdown("**Colonnes disponibles:**")
    cols_info = {
        'nom': 'Désignation unique de la planète',
        'distance': 'Distance du système (parsecs)',
        'ascension_droite': 'Coordonnée céleste horizontale',
        'declinaison': 'Coordonnée céleste verticale',
        'masse': 'Masse relative à Jupiter',
        'temperature': 'Température estimée (Kelvin)',
        'type': 'Classification de l\'objet'
    }
    
    for col, desc in cols_info.items():
        st.markdown(f"- **{col}:** {desc}")

# TAB 7: ANALYSES AVANCÉES
with nav_tabs[6]:
    st.header("📈 Analyses et Visualisations Avancées")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Distribution de la Distance")
        if len(df) > 0:
            fig_distance = px.histogram(
                df,
                x='distance',
                nbins=50,
                title="Distribution des distances",
                labels={'distance': 'Distance (parsecs)'},
                color_discrete_sequence=['#1f77b4']
            )
            st.plotly_chart(fig_distance, use_container_width=True)
    
    with col2:
        st.subheader("⚖️ Distribution de la Masse")
        df_mass = df[df['masse'].notna()]
        if len(df_mass) > 5:
            fig_mass = px.histogram(
                df_mass,
                x='masse',
                nbins=40,
                title="Distribution des masses",
                labels={'masse': 'Masse (masses de Jupiter)'},
                color_discrete_sequence=['#ff7f0e']
            )
            st.plotly_chart(fig_mass, use_container_width=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🌡️ Distribution de la Température")
        df_temp = df[df['temperature'].notna()]
        if len(df_temp) > 5:
            fig_temp = px.histogram(
                df_temp,
                x='temperature',
                nbins=40,
                title="Distribution des températures",
                labels={'temperature': 'Température (Kelvin)'},
                color_discrete_sequence=['#2ca02c']
            )
            st.plotly_chart(fig_temp, use_container_width=True)
    
    with col2:
        st.subheader("📈 Relation Masse vs Température")
        df_scatter = df[(df['masse'].notna()) & (df['temperature'].notna())]
        if len(df_scatter) > 5:
            fig_scatter = px.scatter(
                df_scatter,
                x='masse',
                y='temperature',
                hover_name='nom',
                title="Corrélation entre masse et température",
                labels={'masse': 'Masse (M_J)', 'temperature': 'Température (K)'},
                color='distance',
                size='distance',
                color_discrete_sequence=['#d62728']
            )
            st.plotly_chart(fig_scatter, use_container_width=True)
