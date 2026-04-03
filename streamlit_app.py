import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

# Configuration de la page
st.set_page_config(
    page_title="Explorateur d'Exoplanetes",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Titre principal
st.title("🌟 Explorateur d'Exoplanetes")
st.markdown("*Exploration interactive et educative du catalogue d'exoplanetes*")

# Chargement des donnees
@st.cache_data
def load_data():
    """Charge les donnees des exoplanetes"""
    csv_path = Path(__file__).parent / "open_exoplanet_catalogue" / "scripts" / "planets.csv"
    df = pd.read_csv(csv_path)
    return df

try:
    df = load_data()
except Exception as e:
    st.error(f"Erreur lors du chargement des donnees: {e}")
    st.stop()

# Navigation principale
nav_tabs = st.tabs([
    "📚 Introduction",
    "📊 Donnees & Missions",
    "📖 Parametres Expliques",
    "🌍 Premiers Exemples",
    "🗺️ Carte Spatiale",
    "📥 Telecharger",
    "📈 Analyses Avancees"
])

# TAB 1: INTRODUCTION
with nav_tabs[0]:
    st.header("🌌 Bienvenue dans l'Explorateur d'Exoplanetes")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### Qu'est-ce qu'une exoplanete?
        
        Une **exoplanete** est une planete qui orbite autour d'une etoile autre que le Soleil. 
        
        Pendant longtemps, nous ne connaissions que les 8 planetes de notre systeme solaire. 
        Depuis la decouverte de la premiere exoplanete en 1995 (51 Pegasi b), 
        nous en avons decouvert des **milliers**!
        
        ### Importance Scientifique
        
        Les exoplanetes nous aident a comprendre:
        - ✨ Comment les systemes planetaires se forment
        - 🔭 La diversite des mondes dans l'univers
        - 🌱 Ou chercher la vie extra-terrestre
        - 🚀 L'evolution future de l'astronomie
        """)
    
    with col2:
        st.metric("🪐 Total d'exoplanetes detectees", f"{len(df):,}")
        st.metric("📍 Avec distance connue", f"{df['distance'].notna().sum():,}")
        st.metric("⚖️ Avec masse connue", f"{df['masse'].notna().sum():,}")
        st.metric("🌡️ Avec temperature estimee", f"{df['temperature'].notna().sum():,}")

# TAB 2: DONNEES & MISSIONS
with nav_tabs[1]:
    st.header("📊 Source des Donnees et Missions Spatiales")
    
    st.markdown("""
    ### 🌐 Open Exoplanet Catalogue
    
    Cette application utilise les donnees du **Open Exoplanet Catalogue**, 
    une base de donnees open-source et communautaire.
    
    **Source officielle:** https://openexoplanetcatalogue.com/
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🛰️ Missions Principales")
        st.markdown("""
        #### Kepler Space Telescope (2009-2018)
        - 🎯 **Mission:** Detection des transits planetaires
        - 📊 **Decouvertes:** ~2,662 exoplanetes confirmees
        - 📍 **Champ:** Constellations du Cygne et de la Lyre
        - 🏆 La mission la plus prolifique pour les exoplanetes
        
        #### TESS (2018-present)
        - 🎯 **Mission:** Transit Exoplanet Survey Satellite
        - 📊 **Decouvertes:** +5,000 exoplanetes confirmees
        - 🌍 **Couverture:** 85% du ciel
        - 🔍 Tres sensible aux planetes proches
        
        #### Radial Velocity Methods
        - 🎯 **Methode:** Mesure du "wobble" des etoiles
        - 📊 **Avantage:** Determine directement la masse
        - 📍 **Historique:** Methode de la premiere decouverte
        """)
    
    with col2:
        st.subheader("🔬 Autres Techniques de Detection")
        st.markdown("""
        #### Transit Photometry
        - Mesure la legere baisse de luminosite
        - Quand une planete passe devant son etoile
        - **Plus de 70% des decouvertes** utilise cette methode
        
        #### Direct Imaging
        - Prendre des photos directes de la planete
        - Tres difficile (planete ~milliards de fois moins brillante)
        - Pour les planetes jeunes et chaudes seulement
        
        #### Gravitational Microlensing
        - Utilise les effets de lentille gravitationnelle
        - Peut detecter des planetes tres lointaines
        - Methode la plus exotique
        
        #### Astrometry
        - Mesure la position apparente de l'etoile
        - Tres precis avec les satellites modernes
        """)
    
    st.divider()
    
    st.subheader("📈 Evolution du Nombre de Decouvertes")
    
    st.info("""
    💡 **Observation:** Le nombre d'exoplanetes decouvertes augmente exponentiellement!
    - 1995: 1 exoplanete
    - 2010: ~500 exoplanetes
    - 2020: ~4,300 exoplanetes
    - 2024: +5,500 exoplanetes
    
    Cette acceleration est due a l'amelioration des telescopes et des techniques de detection.
    """)

# TAB 3: PARAMETRES EXPLIQUES
with nav_tabs[2]:
    st.header("📖 Comprendre les Parametres")
    
    st.markdown("""
    Cette base de donnees contient des informations essentielles sur chaque exoplanete.
    Voici une explication detaillee de chaque parametre:
    """)
    
    tabs_params = st.columns(2)
    
    with tabs_params[0]:
        with st.expander("📛 **NOM** - Designation de la planete", expanded=True):
            st.markdown("""
            - **Exemple:** Kepler-1032 b, HD 154857 c
            - **Format:** `[Nom du systeme] [Lettre]`
            - **Signification:** La lettre indique l'ordre de decouverte
              - `b` = premiere planete decouverte
              - `c` = deuxieme planete decouverte
              - etc.
            - **Importance:** Identifie de maniere unique la planete
            """)
        
        with st.expander("📏 **DISTANCE** - Distance du systeme"):
            st.markdown("""
            - **Unite:** Parsecs (pc)
            - **1 parsec = 3.26 annees-lumiere**
            - **Exemple:** 64.2 pc = environ 209 annees-lumiere
            - **Importance:** Distance pour etudier les proprietes intrinseques
            - **Methode:** Parallaxe stellaire (tres precis avec les satellites)
            - **Comment interpreter:**
              - < 10 pc: Tres proche (accessibles aux telescopes amateurs)
              - 10-100 pc: Proches
              - > 1000 pc: Tres lointaines (meme pour les professionnels)
            """)
        
        with st.expander("➡️ **ASCENSION DROITE** - Coordonnee celeste (horizontale)"):
            st.markdown("""
            - **Format:** Heures, minutes, secondes (h m s)
            - **Exemple:** 19 19 43.4040 = 19h 19m 43.4040s
            - **Plage:** 0h a 24h (une rotation complete)
            - **Equivalent terrestre:** La longitude sur Terre
            - **Importance:** Localise la position de l'etoile sur la sphere celeste
            - **Remarque:** Utilisee avec la declinaison pour un positionnement exact
            """)
        
        with st.expander("📍 **DECLINAISON** - Coordonnee celeste (verticale)"):
            st.markdown("""
            - **Format:** Degres, arcminutes, arcseconde
            - **Exemple:** +40 05 51.8400 = +40 05' 51.8400"
            - **Plage:** -90 (pole sud celeste) a +90 (pole nord celeste)
            - **Equivalent terrestre:** La latitude sur Terre
            - **Importance:** Localise la position de l'etoile sur la sphere celeste
            - **Remarque:** Positive au nord, negative au sud
            """)
    
    with tabs_params[1]:
        with st.expander("⚖️ **MASSE** - Poids relatif de la planete", expanded=True):
            st.markdown("""
            - **Unite:** Masses de Jupiter (M_J)
            - **1 masse de Jupiter ≈ 318 masses terrestres**
            - **Exemple:** 2.24 = 2.24 fois plus massif que Jupiter
            - **Importance:** Determine le type de planete
            - **Classification:**
              - < 0.1 M_J: Planete terrestre (super-Terre)
              - 0.1 - 1 M_J: Planete intermediaire
              - > 1 M_J: Geante gazeuse (comme Jupiter)
            - **Comment obtenir:** Spectroscopie Doppler (radial velocity)
            - **⚠️ Donnees partielles:** Beaucoup de planetes n'ont pas la masse mesuree
            """)
        
        with st.expander("🌡️ **TEMPERATURE** - Temperature estimee de la surface"):
            st.markdown("""
            - **Unite:** Kelvin (K)
            - **Conversion:** K = C + 273.15
            - **Exemple:** 336 K = 62.85C (planete chaude!)
            - **Importance:** Determine l'habitabilite potentielle
            - **Classification approximative:**
              - < 200 K: Planete froide (lointaine de son etoile)
              - 200-400 K: Zone habitable potentielle
              - > 1000 K: Planete tres chaude (proche de son etoile)
            - **Comment obtenir:** Modeles thermiques bases sur:
              - Distance a l'etoile
              - Luminosite de l'etoile
              - Albedo suppose de la planete
            - **⚠️ Incertitude:** Cette valeur est estimee, pas mesuree directement
            """)
        
        with st.expander("🏷️ **TYPE** - Classification de l'objet"):
            st.markdown("""
            - **Valeur dans cette base:** "planet" (planete)
            - **Importance:** Permet de filtrer les planetes vs autres objets
            - **Autres types possibles:** 
              - star: Etoile
              - planet: Planete confirmee
              - moonplanet: Possible lune de planete
            - **Remarque:** Cette base contient uniquement des planetes
            """)

# TAB 4: PREMIERS EXEMPLES
with nav_tabs[3]:
    st.header("🌍 Les 5 Premieres Exoplanetes (par distance)")
    
    st.markdown("""
    Voici les 5 exoplanetes les plus proches de nous, selon les donnees du catalogue.
    Ces planetes sont particulierement interessantes car elles sont accessibles aux telescopes modernes.
    """)
    
    st.markdown("""
    ### Plan pour ces 5 planetes par rapport a notre univers
    - Ces planètes se trouvent toutes dans notre bras de la Voie Lactee ou a proximite.
    - Elles sont situees a quelques dizaines ou centaines d'annees-lumiere, ce qui est tres proche sur echelle galactique.
    - Notre systeme solaire est a 0 annee-lumiere : elles sont donc a plus de 60 annees-lumiere dans ces exemples.
    - Ce sont des cibles experimentales pour l'etude des atmospheres et exobiologie futur, mais encore bien loin pour le voyage humain.

    **Objectif:** comprendre d'ou elles viennent et comment elles se comparent a notre propre systeme solaire.
    """)
    
    df_sorted = df.sort_values('distance').head(5)
    
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
                st.metric("Temperature", f"{row['temperature']:.0f} K" if pd.notna(row['temperature']) else "N/A")
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"""
                **Coordonnees Celestes:**
                - RA: {row['ascension_droite']}
                - Dec: {row['declinaison']}
                """)
            with col2:
                if pd.notna(row['distance']):
                    al = row['distance'] * 3.26156
                    st.markdown(f"""
                    **Distance en annees-lumiere:**
                    - {al:.1f} annees-lumiere
                    """)
    
    st.divider()
    
    st.subheader("📊 Tableau Complet des 5 Premieres")
    st.dataframe(
        df_sorted[['nom', 'distance', 'ascension_droite', 'declinaison', 'masse', 'temperature']],
        use_container_width=True
    )

# TAB 5: CARTE SPATIALE
with nav_tabs[4]:
    st.header("🗺️ Carte Spatiale des Exoplanetes")
    
    st.markdown("""
    Cette carte montre la distribution spatiale des systemes planetaires dans le ciel.
    
    **Axes et dimensions:**
    - **Axe X (Ascension droite):** Position Est-Ouest dans le ciel
    - **Axe Y (Declinaison):** Position Nord-Sud dans le ciel
    - **Taille des points:** Plus le point est gros, plus le systeme est loin (distance en parsecs)
    - **Etoile jaune:** Notre systeme solaire (Soleil)
    
    **Comment interpreter:**
    - Les points tout petits = systemes pres de nous (< 10 pc)
    - Les points enormes = systemes tres lointains (> 1000 pc)
    - La position du point = ou les voir dans le ciel (RA/Dec)
    """)
    
    df_spatial = df[(df['ascension_droite'].notna()) & (df['declinaison'].notna()) & (df['distance'].notna())]

    # Filtre de distance pour la carte spatiale
    min_dist, max_dist = st.slider(
        "Distance de base pour la carte (parsecs)",
        float(df_spatial['distance'].min()),
        float(df_spatial['distance'].max()),
        (float(df_spatial['distance'].min()), float(df_spatial['distance'].max()))
    )
    df_spatial = df_spatial[(df_spatial['distance'] >= min_dist) & (df_spatial['distance'] <= max_dist)]

    st.markdown(f"**Filtre distance actif:** {min_dist:.1f} - {max_dist:.1f} pc")

    if len(df_spatial) > 0:
        fig_spatial = px.scatter(
            df_spatial,
            x='ascension_droite',
            y='declinaison',
            size='distance',
            color='distance',
            hover_name='nom',
            hover_data={
                'distance': ':.1f',
                'masse': ':.2f',
                'temperature': ':.0f',
                'ascension_droite': False,
                'declinaison': False
            },
            title="Distribution spatiale des systemes planetaires",
            labels={
                'ascension_droite': "Ascension droite",
                'declinaison': "Declinaison",
                'distance': 'Distance (pc)'
            },
            size_max=30,
            color_continuous_scale='Viridis'
        )

        fig_spatial.add_scatter(
            x=['12'],
            y=['0'],
            mode='markers+text',
            marker=dict(
                size=15,
                color='gold',
                symbol='star',
                line=dict(color='orange', width=2)
            ),
            text=['Soleil'],
            textposition='top center',
            hovertemplate='<b>Notre Systeme Solaire</b><br>Distance: 0 pc<extra></extra>',
            name='Soleil',
            showlegend=True
        )

        fig_spatial.update_layout(
            height=600,
            showlegend=True,
            hovermode='closest',
            legend=dict(
                x=0.01,
                y=0.99,
                bgcolor='rgba(255,255,255,0.8)'
            )
        )

        st.plotly_chart(fig_spatial, use_container_width=True)

        st.info(f"📊 {len(df_spatial):,} systemes sur la carte")
    else:
        st.warning("Pas de donnees spatiales disponibles")

# TAB 6: TELECHARGER
with nav_tabs[5]:
    st.header("📥 Telecharger les Donnees")
    
    st.markdown("""
    Vous pouvez telecharger l'ensemble des donnees des exoplanetes.
    Choisissez selon vos besoins:
    """)
    
    st.subheader("Options de Telechargement")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        ### TOUTES les planetes
        
        - {len(df)} planetes
        - Certaines valeurs vides
        - Distance: {df['distance'].isna().sum()} manquantes
        - Masse: {df['masse'].isna().sum()} manquantes
        - Temperature: {df['temperature'].isna().sum()} manquantes
        """)
        
        csv_full = df.to_csv(index=False)
        st.download_button(
            label="Telecharger TOUTES les planetes (CSV)",
            data=csv_full,
            file_name="exoplanetes_complete.csv",
            mime="text/csv",
            use_container_width=True,
            key="dl_complete"
        )
    
    with col2:
        df_complete = df[(df['distance'].notna()) & (df['masse'].notna()) & (df['temperature'].notna())]
        st.markdown(f"""
        ### Donnees COMPLETES uniquement
        
        - {len(df_complete)} planetes
        - 100% des donnees presentes
        - Aucune valeur vide
        - Ideale pour analyse rigoureuse
        """)
        
        csv_complete = df_complete.to_csv(index=False)
        st.download_button(
            label="Donnees COMPLETES (CSV)",
            data=csv_complete,
            file_name="exoplanetes_donnees_completes.csv",
            mime="text/csv",
            use_container_width=True,
            key="dl_complete_data"
        )
    
    st.divider()
    
    st.subheader("Guide de Travail")
    
    st.markdown("""
    **Format recommande:** Donnees COMPLETES

    **Pourquoi:**
    - Donnees verifiees et coherentes
    - Plus facile a justifier
    - Moins de problemes de nettoyage
    """)
    
    report_steps = st.expander("Etapes cles pour votre analyse", expanded=True)
    with report_steps:
        st.markdown("""
        **1. Introduction & Contexte**
        - Qu'est-ce qu'une exoplanete?
        - Importance scientifique
        - Histoire des decouvertes

        **2. Source des Donnees**
        - Source: Open Exoplanet Catalogue
        - Date de telechargement
        - Nombre de planetes: 1393
        - Criteres de selection: donnees completes

        **3. Methodologie**
        - Quels parametres analysez-vous?
        - Comment avez-vous traite les donnees?

        **4. Resultats**
        - Graphiques et visualisations
        - Statistiques
        - Patterns identifies

        **5. Conclusion**
        - Principaux resultats
        - Implications scientifiques
        - Questions ouvertes
        """)

    st.divider()
    
    st.subheader("🔧 Comment Filtrer ou Separer les Donnees")
    
    tool_tabs = st.tabs(["Excel", "Python/Pandas", "Google Sheets"])
    
    with tool_tabs[0]:
        st.markdown("""
### Excel - Methode Simple

**Etape 1: Ouvrir le fichier CSV**
- Double-cliquer sur le CSV
- Excel ouvrira une fenetre d'import
- Cocher "Delimite" et "Virgule"

**Etape 2: Ajouter un filtre**
- Selectionner les donnees (Ctrl+A)
- Aller a: Donnees > AutoFiltre
- Des fleches aparaissent dans l'en-tete

**Etape 3: Supprimer les lignes vides**
- Cliquer sur la fleche de "masse"
- Decocher "(vide)"
- Repeter pour "temperature" et "distance"

**Etape 4: Sauvegarder**
- Selectionner le filtre (Ctrl+A)
- Copier (Ctrl+C)
- Nouveau classeur
- Coller (Ctrl+V)
- Enregistrer sous: Format CSV
        """)
    
    with tool_tabs[1]:
        st.markdown("""
### Python/Pandas

**Installer pandas:**
```bash
pip install pandas
```

**Lire le CSV:**
```python
import pandas as pd
df = pd.read_csv('exoplanetes_complete.csv')
```

**Filtrer les donnees manquantes:**
```python
# Supprimer les lignes ou masse est vide
df_clean = df.dropna(subset=['masse'])

# Donnees completes
df_complete = df.dropna(subset=['distance', 'masse', 'temperature'])
```

**Filtrer par criteres:**
```python
# Planetes proches (< 100 pc)
df_proche = df[df['distance'] < 100]

# Planetes chaudes (> 500K)
df_chaude = df[df['temperature'] > 500]

# Combinaison
df_special = df[(df['distance'] < 50) & (df['temperature'] > 300)]
```

**Exporter:**
```python
df_clean.to_csv('exoplanetes_filtrees.csv', index=False)
```
        """)
    
    with tool_tabs[2]:
        st.markdown("""
### Google Sheets

**Importer le CSV:**
1. Aller a https://sheets.google.com
- Creer un nouveau classeur
- Fichier > Ouvrir > Telecharger CSV

**Ajouter un filtre:**
1. Selectionner les donnees
2. Donnees > Creer un filtre
3. Des fleches aparaissent

**Filtrer:**
- Cliquer sur la fleche de "masse"
- Cocher "Filtrer par condition"
- Selectionner "N'est pas vide"

**Exporter:**
- Fichier > Telecharger > CSV

**Avantage:** Pas besoin d'installer, facile a partager
        """)

# TAB 7: ANALYSES AVANCEES
with nav_tabs[6]:
    st.header("📈 Analyses et Visualisations Avancees")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Distribution de la Distance")
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
        st.subheader("Distribution de la Masse")
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
        st.subheader("Distribution de la Temperature")
        df_temp = df[df['temperature'].notna()]
        if len(df_temp) > 5:
            fig_temp = px.histogram(
                df_temp,
                x='temperature',
                nbins=40,
                title="Distribution des temperatures",
                labels={'temperature': 'Temperature (Kelvin)'},
                color_discrete_sequence=['#2ca02c']
            )
            st.plotly_chart(fig_temp, use_container_width=True)
    
    with col2:
        st.subheader("Relation Masse vs Temperature")
        df_scatter = df[(df['masse'].notna()) & (df['temperature'].notna()) & (df['distance'].notna())]
        if len(df_scatter) > 5:
            fig_scatter = px.scatter(
                df_scatter,
                x='masse',
                y='temperature',
                hover_name='nom',
                title="Correlation entre masse et temperature",
                labels={'masse': 'Masse (M_J)', 'temperature': 'Temperature (K)'},
                color='distance',
                size='distance'
            )
            st.plotly_chart(fig_scatter, use_container_width=True)
