import streamlit as st
import pandas as pd
import numpy as np

# Configuration de la page
st.set_page_config(
    page_title="Sephora | Brand Affinity Tool",
    page_icon="💄",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- CSS PERSONNALISÉ (STYLE SEPHORA) ---
st.markdown("""
<style>
    /* Style global */
    .main {
        background-color: #f9f9f9;
    }
    
    /* Titre principal */
    .stTitle {
        color: #000000;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        font-weight: 900;
        text-transform: uppercase;
        letter-spacing: 2px;
        border-bottom: 5px solid #FF0101;
        padding-bottom: 10px;
        margin-bottom: 30px;
    }
    
    /* Sidebar style */
    .css-1d391kg {
        background-color: #000000;
    }
    .st-emotion-cache-6qob1r {
        background-color: #000000;
    }
    
    /* Cartes KPI */
    .metric-card {
        background-color: white;
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        border-left: 5px solid #000000;
        text-align: center;
    }
    
    /* Cartes Recommandation */
    .reco-card {
        background-color: white;
        border-radius: 15px;
        padding: 25px;
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
        border-top: 8px solid #FF0101;
        text-align: center;
        transition: transform 0.3s;
    }
    .reco-card:hover {
        transform: translateY(-10px);
    }
    
    /* Boutons personnalisés */
    .stButton>button {
        background-color: #000000;
        color: white;
        border-radius: 25px;
        padding: 10px 25px;
        font-weight: bold;
        border: none;
        width: 100%;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #FF0101;
        color: white;
    }
    
    /* Header section */
    .section-header {
        color: #000000;
        font-weight: bold;
        font-size: 24px;
        margin-top: 40px;
        margin-bottom: 20px;
        display: flex;
        align-items: center;
    }
</style>
""", unsafe_allow_html=True)

# --- CHARGEMENT DES DONNÉES ---
@st.cache_data
def load_data():
    df = pd.read_csv('sephora_light.csv')
    impact = pd.read_csv('impact_scores.csv')
    similarity = pd.read_csv('brand_similarity_matrix.csv', index_col=0)
    return df, impact, similarity

try:
    df, impact, similarity = load_data()
    
    # --- BARRE LATÉRALE ---
    with st.sidebar:
        st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/f/f3/Sephora_logo.svg/2560px-Sephora_logo.svg.png", width=200)
        st.markdown("<br>", unsafe_allow_html=True)
        page = st.radio("MENU NAVIGATION", ["👤 Dashboard Client", "🤝 Affinités Marques", "📊 KPI Marketing"])
        st.markdown("<hr>", unsafe_allow_html=True)
        st.info("💡 **Tip :** Utilisez cet outil pour préparer vos campagnes de cross-sell personnalisées.")

    # --- PAGE 1 : DASHBOARD CLIENT ---
    if page == "👤 Dashboard Client":
        st.title("SEPHORA | Customer Insights")
        
        # Sélection du client avec un champ de recherche moderne
        client_ids = impact['ID_CLIENT'].unique()
        selected_client = st.selectbox("RECHERCHER UN CLIENT (ID)", client_ids, help="Entrez l'ID unique du client pour voir ses recommandations.")
        
        if selected_client:
            client_info = impact[impact['ID_CLIENT'] == selected_client].iloc[0]
            
            # Affichage des KPI sous forme de cartes élégantes
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.markdown(f'<div class="metric-card"><h4>Score d\'Impact</h4><h2 style="color:#FF0101">{client_info["SCORE_IMPACT"]:.1f}/100</h2></div>', unsafe_allow_html=True)
            with col2:
                st.markdown(f'<div class="metric-card"><h4>Panier Moyen</h4><h2>{client_info["AVG_BASKET"]:.2f} €</h2></div>', unsafe_allow_html=True)
            with col3:
                st.markdown(f'<div class="metric-card"><h4>Fréquence</h4><h2>{int(client_info["FREQ"])} achats</h2></div>', unsafe_allow_html=True)
            with col4:
                st.markdown(f'<div class="metric-card"><h4>Trafic</h4><h2>{int(client_info["TRAFFIC"])} jours</h2></div>', unsafe_allow_html=True)
            
            # Section Recommandations avec design "Card"
            st.markdown('<div class="section-header">✨ RECOMMANDATIONS PERSONNALISÉES</div>', unsafe_allow_html=True)
            
            history = df[df['ID_CLIENT'] == selected_client].sort_values('DATE', ascending=False)
            purchased_brands = history['MARQUE'].unique()
            
            if len(purchased_brands) > 0:
                scores = similarity[purchased_brands].sum(axis=1)
                recs = scores.drop(index=purchased_brands, errors='ignore').sort_values(ascending=False).head(3)
                
                cols = st.columns(3)
                for i, (brand, score) in enumerate(recs.items()):
                    with cols[i]:
                        st.markdown(f"""
                        <div class="reco-card">
                            <h3 style="color:#000000">{brand}</h3>
                            <p style="color:#666">Score d'Affinité : <b>{score:.2f}</b></p>
                            <p style="font-size:12px">Basé sur ses achats récents</p>
                        </div>
                        """, unsafe_allow_html=True)
                        st.button(f"LANCER CAMPAGNE {brand}", key=f"btn_{brand}_{i}")
            
            # Historique d'achat
            st.markdown('<div class="section-header">📜 HISTORIQUE D\'ACHAT RÉCENT</div>', unsafe_allow_html=True)
            st.dataframe(history[['DATE', 'MARQUE', 'CATEGORIE', 'MONTANT']].style.format({"MONTANT": "{:.2f} €"}), use_container_width=True)

    # --- PAGE 2 : AFFINITÉS MARQUES ---
    elif page == "🤝 Affinités Marques":
        st.title("SEPHORA | Brand Ecosystem")
        selected_brand = st.selectbox("SÉLECTIONNEZ UNE MARQUE", similarity.columns)
        
        if selected_brand:
            st.markdown(f'<div class="section-header">🔍 MARQUES COMPLÉMENTAIRES À {selected_brand}</div>', unsafe_allow_html=True)
            proches = similarity[selected_brand].sort_values(ascending=False).iloc[1:11]
            st.bar_chart(proches, color="#FF0101")
            
            st.info("Ces marques sont les plus susceptibles d'être achetées par les mêmes clients. Idéal pour des offres groupées (Bundles).")

    # --- PAGE 3 : KPI GLOBAUX ---
    elif page == "📊 KPI Marketing":
        st.title("SEPHORA | Global Performance")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown('<div class="section-header">📈 DISTRIBUTION DE L\'IMPACT</div>', unsafe_allow_html=True)
            st.area_chart(impact['SCORE_IMPACT'].value_counts().sort_index().head(50), color="#000000")
            
        with col2:
            st.markdown('<div class="section-header">💄 TOP CATÉGORIES (Ventes)</div>', unsafe_allow_html=True)
            cat_sales = df.groupby('CATEGORIE')['MONTANT'].sum().sort_values(ascending=False)
            st.bar_chart(cat_sales, color="#FF0101")

except Exception as e:
    st.error(f"Erreur lors du chargement des données : {e}")
    st.info("Vérifiez la présence des fichiers CSV dans le répertoire.")
