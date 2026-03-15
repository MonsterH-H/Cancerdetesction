import streamlit as st
import pandas as pd
import os
import sys
import matplotlib.pyplot as plt
import seaborn as sns

# Ensure root directory is in path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.styles import apply_custom_styles, render_premium_header, render_section_title, render_logo
from src.database import get_db_session, PatientAnalysis
from src.ai_advisor import AIAdvisor
from src.analytics import AnalyticsManager

# Configuration de la page
st.set_page_config(page_title="Exploration Clinique - OncoAI PRO", layout="wide", page_icon="📊")
apply_custom_styles()
render_logo()

if 'user' not in st.session_state:
    st.warning("⚠️ Accès restreint aux analystes certifiés. Veuillez vous authentifier.")
    st.stop()

render_premium_header(
    "Exploration Épidémiologique", 
    "Analyse statistique profonde, corrélations cliniques et tendances de santé publique.", 
    icon_class="fa-solid fa-chart-column", 
    badge="Intelligence Analytique v6.3"
)

session = get_db_session()
ai_advisor = AIAdvisor()
analytics = AnalyticsManager() # Uses raw data for cohort comparison if needed, but we prefer DB

# Fetch DB Data
df = pd.read_sql(session.query(PatientAnalysis).statement, session.bind)

if not df.empty:
    # --- KPI SECTION ---
    render_section_title("Métriques de Performance Globale", "fa-solid fa-square-poll-vertical")
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Analyses Indexées", len(df))
    k2.metric("Moyenne Confiance IA", f"{df['confidence_score'].mean()*100:.1f}%")
    high_p = (len(df[df['risk_level'].isin(['High', 'Élevé'])]) / len(df)) * 100
    k3.metric("Ratio Haut Risque", f"{high_p:.1f}%", delta=f"{high_p-25:.1f}%" if high_p > 25 else None, delta_color="inverse")
    k4.metric("Âge Médian", int(df['age'].median()))

    # --- IA SYNTHESIS ---
    render_section_title("Rapport de Synthèse IA (Mistral 7B)", "fa-solid fa-wand-magic-sparkles")
    with st.spinner("Génération de l'analyse de cohorte..."):
        summary = ai_advisor.generate_summary(df)
        st.markdown(f"""
            <div class='card' style='background: #f0fdfa; border-left: 10px solid #0d9488;'>
                <p style='font-size:1.1rem; line-height:1.6; color:#0f172a;'>{summary}</p>
                <p style='font-size:0.8rem; color:#64748b; margin-top:10px;'><i>Note : Cette synthèse est générée en temps réel sur la base des données SQL actuelles.</i></p>
            </div>
        """, unsafe_allow_html=True)

    # --- ADVANCED ANALYTICS ---
    render_section_title("Répartitions & Corrélations Cliniques", "fa-solid fa-microscope")
    
    col_a, col_b = st.columns(2)
    
    with col_a:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.write("#### 📈 Distribution du Risque par Âge")
        fig_age, ax_age = plt.subplots(figsize=(10, 6), facecolor='none')
        sns.kdeplot(data=df, x='age', hue='risk_level', fill=True, palette='viridis', ax=ax_age)
        ax_age.set_title("Densité Épidémiologique", weight='bold')
        st.pyplot(fig_age)
        st.markdown("</div>", unsafe_allow_html=True)

    with col_b:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.write("#### 📊 Facteurs d'Exposition (Top Corrélations)")
        # Calculate correlations for key features
        features_cols = ['air_pollution', 'alcohol_use', 'smoking', 'obesity', 'genetic_risk', 'passive_smoker']
        corr_df = df[features_cols].corr()
        fig_corr, ax_corr = plt.subplots(figsize=(10, 6))
        sns.heatmap(corr_df, annot=True, cmap='GnBu', ax=ax_corr, fmt=".2f")
        st.pyplot(fig_corr)
        st.markdown("</div>", unsafe_allow_html=True)

    # --- EXPOSURE IMPACT ---
    render_section_title("Impact des Biomarqueurs", "fa-solid fa-virus-covid")
    target_feat = st.selectbox("Sélectionner un biomarqueur pour analyse d'impact", 
                               ['smoking', 'alcohol_use', 'air_pollution', 'obesity', 'genetic_risk', 'fatigue'])
    
    fig_impact, ax_impact = plt.subplots(figsize=(12, 4))
    sns.countplot(data=df, x=target_feat, hue='risk_level', palette='mako', ax=ax_impact)
    ax_impact.set_title(f"Impact de {target_feat.replace('_', ' ').title()} sur le Niveau de Risque", weight='bold')
    st.pyplot(fig_impact)

    # --- DATA EXPORT ---
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("📥 GÉNÉRER UN DATASET D'ÉTUDE (CSV)", use_container_width=True):
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("Confirmer le téléchargement", csv, "oncoai_research_data.csv", "text/csv")

else:
    st.info("📊 Le registre est actuellement vide. Les analyses statistiques seront disponibles après les premiers diagnostics.")
    st.markdown("""
        <div style='text-align:center; padding:50px;'>
            <a href='01_Diagnostic.py' target='_self'>Effectuer un premier diagnostic →</a>
        </div>
    """, unsafe_allow_html=True)

session.close()
