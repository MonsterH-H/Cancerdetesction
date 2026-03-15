import streamlit as st
import os
import sys

# Ensure root directory is in path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.styles import apply_custom_styles, render_premium_header, render_section_title, render_logo

st.set_page_config(page_title="Aide - OncoAI", layout="wide")
apply_custom_styles()
render_logo()

render_premium_header("Centre d'Expertise", "Ressources cliniques, guides et support technique OncoAI PRO.", icon_class="fa-solid fa-circle-question", badge="Support Client")

st.markdown("<div class='card'>", unsafe_allow_html=True)
render_section_title("Guides de Procédures", "fa-solid fa-graduation-cap")
with st.expander("Comment initialiser un dossier patient ?"):
    st.write("""
    1. Accédez au module **Diagnostic**.
    2. Sélectionnez un patient existant dans la liste ou créez-en un nouveau.
    3. Remplissez les 23 paramètres basés sur les analyses biologiques.
    4. Validez pour obtenir l'inférence immédiate et le rapport PDF.
    """)

with st.expander("Interconnectivité du module Patients"):
    st.write("""
    Chaque analyse est liée dynamiquement à un patient unique. Vous pouvez suivre l'évolution de la santé d'un patient 
    directement depuis son profil dans le module **Gestion Patients**.
    """)
st.markdown("</div>", unsafe_allow_html=True)

render_section_title("Architecture des Données", "fa-solid fa-database")
st.markdown("""
La solution repose sur un noyau SQL structuré :
- **Patients** : Répertoire central des identités.
- **Analyses** : Historique des diagnostics liés aux patients.
- **Audit** : Journalisation de toutes les actions pour conformité RGPD/Médicale.
""")

st.write("---")
render_section_title("Assistance Médicale", "fa-solid fa-hospital")
st.info("Besoin d'aide technique ? Contactez notre centre de maintenance : **pro-support@oncoai.cloud**")
