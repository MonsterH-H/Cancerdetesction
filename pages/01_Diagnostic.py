import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import sys
from datetime import datetime

# Ensure root directory is in path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.styles import apply_custom_styles, render_premium_header, render_section_title, render_logo
from src.engine import PredictionEngine
from src.storage import HistoryManager
from src.reporting import ReportGenerator
from src.ai_advisor import AIAdvisor
from src.database import get_db_session, Patient, AuditLog

# Configuration de la page
st.set_page_config(page_title="Diagnostic - OncoAI PRO", layout="wide", page_icon="🔬")
apply_custom_styles()
render_logo()

if 'user' not in st.session_state:
    st.warning("⚠️ Authentification requise pour accéder au module de diagnostic.")
    st.stop()

render_premium_header(
    "Diagnostic Prédictif", 
    "Saisie des biomarqueurs et analyse par intelligence artificielle (RF-v2.8).", 
    icon_class="fa-solid fa-dna", 
    badge="Inférence Certifiée"
)

# Initialisation des moteurs
@st.cache_resource
def load_engines():
    return PredictionEngine(), HistoryManager(), ReportGenerator(), AIAdvisor()

engine, hm, reporter, ai_advisor = load_engines()

# --- ETAPE 1 : IDENTIFICATION DU PATIENT ---
if 'analysis_started' not in st.session_state:
    st.session_state.analysis_started = False

if not st.session_state.analysis_started:
    with st.container():
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        render_section_title("Dossier d'Analyse", "fa-solid fa-folder-plus")
        
        col_t1, col_t2 = st.columns([2, 1])
        with col_t1:
            a_title = st.text_input("Référence de l'Analyse", placeholder="Ex: Consultation Routine - Mars 2024")
        with col_t2:
            a_source = st.selectbox("Canal d'Admission", ["Examen Clinique", "Transfert Dossier", "Téléconsultation"])

        st.markdown("<br>", unsafe_allow_html=True)
        
        # PATIENT SELECTION
        session_db = get_db_session()
        patients = session_db.query(Patient).order_by(Patient.last_name).all()
        p_options = {f"[{p.clin_id}] {p.last_name} {p.first_name}": p for p in patients}
        session_db.close()
        
        selected_p_str = st.selectbox("Sélectionner un Patient (Base SQL)", ["--- Choisir dans la base ---"] + list(p_options.keys()))
        
        st.markdown("<div style='text-align:center; margin: 15px 0; color:#94a3b8;'>&mdash; OU &mdash;</div>", unsafe_allow_html=True)
        
        create_new = st.checkbox("➕ Enregistrer un NOUVEAU Patient pour cette analyse")
        
        if create_new:
            c1, c2 = st.columns(2)
            with c1:
                new_p_id = st.text_input("Identifiant HID Unique", placeholder="H-XXXXXX")
            with c2:
                st.info("Les informations complémentaires seront saisies à l'étape suivante.")

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("DÉMARRER LA SAISIE DES BIOMARQUEURS", width='stretch'):
            if create_new:
                if a_title and new_p_id:
                    st.session_state.analysis_meta = {"title": a_title, "source": a_source, "p_id": new_p_id, "is_new": True}
                    st.session_state.analysis_started = True
                    st.rerun()
                else: st.warning("Veuillez remplir le titre et l'identifiant HID.")
            else:
                if a_title and selected_p_str != "--- Choisir dans la base ---":
                    p_obj = p_options[selected_p_str]
                    st.session_state.analysis_meta = {
                        "title": a_title, "source": a_source, "p_id": p_obj.clin_id, "is_new": False,
                        "p_name": p_obj.first_name, "p_surname": p_obj.last_name, "p_gender": p_obj.gender
                    }
                    st.session_state.analysis_started = True
                    st.rerun()
                else: st.warning("Veuillez configurer le titre et sélectionner un patient.")
        st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# --- ETAPE 2 : FORMULAIRE CLINIQUE (23 FEATURES) ---
meta = st.session_state.analysis_meta
st.markdown(f"""
    <div style='background: #f1f5f9; padding: 10px 20px; border-radius: 10px; margin-bottom: 20px; border-left: 5px solid #0d9488;'>
        <b>Dossier Actif :</b> {meta['title']} | <b>Patient :</b> {meta.get('p_surname', 'Nouveau')} ({meta['p_id']})
    </div>
""", unsafe_allow_html=True)

if st.button("⬅️ CHANGER DE PATIENT / DOSSIER"):
    st.session_state.analysis_started = False
    st.rerun()

with st.form("clinical_form_v6"):
    render_section_title("Informations Fondamentales", "fa-solid fa-user-doctor")
    f1, f2, f3 = st.columns(3)
    with f1:
        p_name = st.text_input("Prénom", value=meta.get('p_name', ''))
    with f2:
        p_surname = st.text_input("Nom de famille", value=meta.get('p_surname', ''))
    with f3:
        p_age = st.number_input("Âge Patient", 1, 120, 45)

    render_section_title("Biomarqueurs & Exposition (Scores 1-9)", "fa-solid fa-flask-vial")
    c1, c2, c3 = st.columns(3)
    
    with c1:
        gender_options = ["Homme", "Femme"]
        default_g = 0 if meta.get('p_gender') == 1 else (1 if meta.get('p_gender') == 2 else 0)
        gender = st.selectbox("Sexe Biologique", gender_options, index=default_g)
        pollution = st.slider("Pollution de l'Air", 1, 8, 4)
        alcohol = st.slider("Consommation d'Alcool", 1, 8, 4)
        allergy = st.slider("Allergie à la Poussière", 1, 8, 4)
        hazards = st.slider("Risques Professionnels", 1, 8, 4)
        genetic = st.slider("Risque Génétique", 1, 7, 4)
        lung = st.slider("Maladie Pulmonaire Chronique", 1, 7, 4)
        
    with c2:
        diet = st.slider("Régime Équilibré", 1, 7, 4)
        obesity = st.slider("Indice d'Obésité", 1, 7, 4)
        smoking = st.slider("Tabagisme", 1, 8, 4)
        passive = st.slider("Fumeur Passif", 1, 8, 4)
        chest = st.slider("Douleur Thoracique", 1, 9, 4)
        blood = st.slider("Toux de Sang (Hémoptysie)", 1, 9, 4)
        fatigue = st.slider("Fatigue", 1, 9, 4)
        weight = st.slider("Perte de Poids", 1, 8, 4)
        
    with c3:
        breath = st.slider("Essoufflement", 1, 9, 4)
        wheezing = st.slider("Sifflement Respiratoire", 1, 8, 4)
        swallowing = st.slider("Difficulté de Déglutition", 1, 8, 4)
        clubbing = st.slider("Hippocratisme Digital", 1, 9, 4)
        cold = st.slider("Rhumes Fréquents", 1, 7, 4)
        dry = st.slider("Toux Sèche", 1, 7, 4)
        snoring = st.slider("Ronflement", 1, 7, 4)

    st.markdown("<br>", unsafe_allow_html=True)
    submit = st.form_submit_button("LANCER L'ANALYSE PRÉDICTIVE ONCOAI", use_container_width=True)

if submit:
    if not p_surname: 
        st.error("❌ Le nom du patient est obligatoire pour l'archivage.")
        st.stop()
        
    g_val = 1 if gender == "Homme" else 2
    # Construction du vecteur de 23 features
    features = [
        p_age, g_val, pollution, alcohol, allergy, hazards, genetic, lung, 
        diet, obesity, smoking, passive, chest, blood, fatigue, weight, 
        breath, wheezing, swallowing, clubbing, cold, dry, snoring
    ]
    
    with st.spinner("🧠 Inférence en cours via le moteur Random Forest..."):
        pred, probs = engine.predict(features)
        conf = float(max(probs)) if probs is not None else 0.0
        
        # Mapping de la prédiction si numérique
        if not isinstance(pred, str):
            mapping = {0: "High", 1: "Low", 2: "Medium"}
            pred = mapping.get(pred, str(pred))
        
        # Interprétation IA (Mistral ou Fallback)
        interpretation = ai_advisor.generate_clinical_interpretation({"age": p_age}, pred, conf)
        
        # Sauvegarde en Base de Données
        p_info = {"name": p_name, "surname": p_surname, "clin_id": meta['p_id'], "gender": g_val}
        analysis_id = hm.save_prediction_full(
            st.session_state.user['id'], 
            p_info, 
            features, 
            pred, 
            probs, 
            interpretation, 
            {"title": meta['title'], "source": meta['source']}
        )
        
    st.success(f"✅ Analyse #{analysis_id} finalisée et archivée avec succès.")

    # --- AFFICHAGE DES RÉSULTATS ---
    render_section_title("Interprétation Clinique", "fa-solid fa-chart-line")
    
    res_l, res_r = st.columns([1, 2])
    with res_l:
        risk_color = "#dc2626" if pred == "High" else ("#d97706" if pred == "Medium" else "#0d9488")
        st.markdown(f"""
            <div class='card' style='text-align:center; border-top:8px solid {risk_color};'>
                <p style="text-transform:uppercase; font-weight:700; color:#64748b; margin:0;">Niveau de Risque</p>
                <h1 style="font-size:3.5rem; margin:15px 0; color:{risk_color} !important;">{str(pred).upper()}</h1>
                <div style="font-size:1.8rem; font-weight:800; color:{risk_color};">{conf*100:.1f}%</div>
                <p style="font-size:0.85rem; color:#94a3b8; font-weight:600;">Indice de Confiance IA</p>
            </div>
        """, unsafe_allow_html=True)
        
    with res_r:
        st.markdown(f"""
            <div class='card' style='height: 100%;'>
                <h4 style='margin-top:0; color:#0f172a;'>Synthèse du Diagnostic IA</h4>
                <p style='font-size:1.1rem; line-height:1.6; color:#334155;'>{interpretation}</p>
                <div style='margin-top:20px; padding:10px; background:#f8fafc; border-radius:8px; font-size:0.85rem; color:#64748b;'>
                    <b>Note technique :</b> Le modèle Random Forest v2.8 a analysé les 23 biomarqueurs fournis. 
                    Les probabilités calculées sont : Low: {probs[1]*100:.1f}%, Med: {probs[2]*100:.1f}%, High: {probs[0]*100:.1f}%.
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    # Facteurs de Risque
    render_section_title("Poids des Variables (Analyse Locale)", "fa-solid fa-brain")
    importance_df = engine.get_feature_importance()
    if importance_df is not None:
        fig_imp, ax_imp = plt.subplots(figsize=(10, 4), facecolor='none')
        top_data = importance_df.head(7)
        sns.barplot(x='Importance', y='Feature', hue='Feature', data=top_data, palette='mako', ax=ax_imp, legend=False)
        ax_imp.set_title("Top 7 des facteurs influençant ce diagnostic", fontsize=10, weight='bold')
        st.pyplot(fig_imp)

    # Export PDF
    st.markdown("<br>", unsafe_allow_html=True)
    record = hm.get_analysis_by_id(analysis_id)
    if record:
        pdf_path = reporter.generate_patient_report(record)
        with open(pdf_path, "rb") as f:
            st.download_button(
                label="📥 TÉLÉCHARGER LE COMPTE-RENDU PDF (Format Expert)",
                data=f,
                file_name=os.path.basename(pdf_path),
                mime="application/pdf",
                use_container_width=True
            )

    if st.button("NOUVELLE ANALYSE POUR CE PATIENT"):
        st.rerun()

