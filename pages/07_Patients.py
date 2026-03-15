import streamlit as st
import pandas as pd
import os
import sys
from datetime import datetime, timezone

# Ensure root directory is in path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.styles import apply_custom_styles, render_premium_header, render_section_title, render_logo
from src.storage import HistoryManager
from src.database import get_db_session, Patient

# Configuration de la page
st.set_page_config(page_title="Patients - OncoAI PRO", layout="wide", page_icon="👥")
apply_custom_styles()
render_logo()

if 'user' not in st.session_state:
    st.warning("⚠️ Authentification requise pour accéder au répertoire patients.")
    st.stop()

render_premium_header(
    "Répertoire Patients", 
    "Gestion centralisée du cycle de vie patient et suivi oncologique.", 
    badge="Database Core v6.2"
)

hm = HistoryManager()
session_db = get_db_session()

# Session state for navigation
if 'selected_patient_id' not in st.session_state:
    st.session_state.selected_patient_id = None

# --- SIDEBAR: RECHERCHE & NAVIGATION ---
with st.sidebar:
    render_section_title("Moteur de Recherche")
    p_search = st.text_input("🔍 Rechercher un dossier", placeholder="Nom, Prénom ou HID...")
    
    # Bouton de création rapide
    if st.button("➕ NOUVEAU PATIENT", type="primary", use_container_width=True):
        st.session_state.selected_patient_id = "NEW"
        st.rerun()
    
    st.write("---")
    patients_df = hm.get_patients_df(search_query=p_search)
    
    if not patients_df.empty:
        for idx, row in patients_df.iterrows():
            # Styling for selection
            is_selected = st.session_state.selected_patient_id == row['id']
            btn_label = f"{row['Nom']} ({row['ID Clinique']})"
            
            if st.button(btn_label, key=f"p_{row['id']}", use_container_width=True, type="secondary" if not is_selected else "primary"):
                st.session_state.selected_patient_id = row['id']
                st.rerun()
    else:
        st.info("Aucun patient trouvé.")

# --- CONTENU PRINCIPAL ---

# CASE 1: INSCRIPTION NOUVEAU PATIENT
if st.session_state.selected_patient_id == "NEW":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    render_section_title("Enregistrement Nouvel Admis", "fa-solid fa-user-plus")
    
    with st.form("new_patient_form_pro"):
        c1, c2 = st.columns(2)
        with c1:
            n_hid = st.text_input("Identifiant HID (Unique)", placeholder="H-XXXXXX")
            n_first = st.text_input("Prénom")
            n_last = st.text_input("Nom de famille")
        with c2:
            n_email = st.text_input("Email de contact")
            n_phone = st.text_input("Numéro de téléphone")
            n_gender = st.selectbox("Sexe Biologique", ["Homme", "Femme"])
        
        n_addr = st.text_area("Adresse de résidence complète")
        
        st.markdown("<br>", unsafe_allow_html=True)
        if st.form_submit_button("VALIDER L'INSCRIPTION AU REGISTRE", use_container_width=True):
            if n_hid and n_first and n_last:
                existing = session_db.query(Patient).filter_by(clin_id=n_hid).first()
                if existing:
                    st.error(f"❌ Erreur : L'ID HID {n_hid} est déjà utilisé par un autre patient.")
                else:
                    new_p = Patient(
                        clin_id=n_hid, first_name=n_first, last_name=n_last,
                        email=n_email, phone=n_phone, address=n_addr,
                        gender=1 if n_gender == "Homme" else 2,
                        created_at=datetime.now(timezone.utc)
                    )
                    session_db.add(new_p)
                    session_db.commit()
                    st.success("✅ Patient inscrit avec succès dans le Core SQL.")
                    st.session_state.selected_patient_id = new_p.id
                    st.rerun()
            else: st.warning("⚠️ Les champs HID, Nom et Prénom sont obligatoires.")
    st.markdown("</div>", unsafe_allow_html=True)

# CASE 2: PROFIL PATIENT DÉTAILLÉ
elif st.session_state.selected_patient_id:
    profile = hm.get_patient_profile(st.session_state.selected_patient_id)
    if profile:
        patient = profile['patient']
        history = profile['history']
        
        tab_info, tab_history, tab_edit = st.tabs(["📋 Profil Clinique", "📊 Historique & Évolution", "⚙️ Paramètres"])
        
        with tab_info:
            col_l, col_r = st.columns([1, 2])
            with col_l:
                st.markdown(f"""
                    <div class='card' style='border-top: 5px solid #0d9488; text-align:center;'>
                        <div style='font-size:4rem; margin-bottom:15px;'>👤</div>
                        <h2 style="margin:0;">{patient.last_name.upper()}</h2>
                        <h4 style="margin:5px 0; color:#64748b;">{patient.first_name}</h4>
                        <span class="premium-badge">HID: {patient.clin_id}</span>
                        <hr style='border:0.5px solid #f1f5f9; margin:20px 0;'>
                        <div style='text-align:left; font-size:0.9rem;'>
                            <p><b>Sexe</b> : {'Homme' if patient.gender == 1 else 'Femme'}</p>
                            <p><b>Admission</b> : {patient.created_at.strftime('%d/%m/%Y')}</p>
                            <p><b>Email</b> : {patient.email or 'N/A'}</p>
                            <p><b>Tel</b> : {patient.phone or 'N/A'}</p>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
                
                if st.button("🎯 NOUVEAU DIAGNOSTIC", use_container_width=True, type="primary"):
                    st.session_state.analysis_meta = {
                        "title": f"Suivi - {patient.last_name}",
                        "source": "Examen Clinique",
                        "p_id": patient.clin_id,
                        "is_new": False,
                        "p_name": patient.first_name,
                        "p_surname": patient.last_name,
                        "p_gender": patient.gender
                    }
                    st.session_state.analysis_started = True
                    st.switch_page("pages/01_Diagnostic.py")

            with col_r:
                st.markdown("<div class='card'>", unsafe_allow_html=True)
                render_section_title("Résumé Médical & Alertes")
                if history:
                    last = history[0]
                    risk_color = "#dc2626" if last.risk_level == "High" else ("#d97706" if last.risk_level == "Medium" else "#0d9488")
                    st.markdown(f"""
                        <div style='padding:20px; border-radius:12px; background:#f8fafc; border-left:8px solid {risk_color};'>
                            <h4 style='margin:0; color:#64748b;'>DERNIER ÉTAT DE RISQUE</h4>
                            <h2 style='margin:10px 0; color:{risk_color} !important;'>{str(last.risk_level).upper()}</h2>
                            <p style='margin:0; font-size:0.9rem;'>Date de l'analyse : {last.timestamp.strftime('%d/%m/%Y %H:%M')}</p>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    st.markdown("<br>", unsafe_allow_html=True)
                    st.write("**Dernière Interprétation IA :**")
                    st.write(f"_{last.ai_interpretation}_")
                else:
                    st.info("Aucun historique d'analyse pour ce patient. Cliquez sur 'Nouveau Diagnostic' pour commencer.")
                st.markdown("</div>", unsafe_allow_html=True)

        with tab_history:
            render_section_title("Chronologie Clinique")
            if history:
                for a in history:
                    with st.expander(f"Analyse: {a.analysis_title} | {a.timestamp.strftime('%d/%m/%Y')} | {a.risk_level}"):
                        st.write(f"**ID Dossier** : #{a.id} | **Score Confiance** : {a.confidence_score*100:.1f}%")
                        st.write(f"**Source** : {a.source_type}")
                        st.info(f"**Avis IA** : {a.ai_interpretation}")
                
                if len(history) > 1:
                    render_section_title("Évolution du Risque")
                    risk_map = {"Low": 1, "Medium": 2, "High": 3, "Faible": 1, "Modéré": 2, "Élevé": 3}
                    evol_df = pd.DataFrame([{"Date": a.timestamp, "Niveau": risk_map.get(a.risk_level, 0)} for a in reversed(history)])
                    st.line_chart(evol_df.set_index("Date"))
            else:
                st.info("Historique vide.")

        with tab_edit:
            render_section_title("Mise à jour des coordonnées")
            with st.form("edit_p_form"):
                e_first = st.text_input("Prénom", value=patient.first_name)
                e_last = st.text_input("Nom", value=patient.last_name)
                e_email = st.text_input("Email", value=patient.email or "")
                e_phone = st.text_input("Téléphone", value=patient.phone or "")
                e_addr = st.text_area("Adresse", value=patient.address or "")
                
                if st.form_submit_button("ENREGISTRER LES MODIFICATIONS"):
                    patient.first_name = e_first
                    patient.last_name = e_last
                    patient.email = e_email
                    patient.phone = e_phone
                    patient.address = e_addr
                    session_db.commit()
                    st.success("✅ Coordonnées mises à jour.")
                    st.rerun()
            
            st.markdown("<br><br>", unsafe_allow_html=True)
            render_section_title("Zone Critique", "fa-solid fa-triangle-exclamation")
            if st.toggle(f"⚠️ Activer la suppression du dossier {patient.clin_id}"):
                if st.button("CONFIRMER LA SUPPRESSION DÉFINITIVE", type="primary"):
                    session_db.delete(patient)
                    session_db.commit()
                    st.success("Dossier supprimé.")
                    st.session_state.selected_patient_id = None
                    st.rerun()
    else:
        st.error("Dossier introuvable.")

else:
    # Vue par défaut
    st.markdown("""
        <div style='height:40vh; display:flex; flex-direction:column; justify-content:center; align-items:center; color:#94a3b8;'>
            <div style='font-size:5rem;'>🔍</div>
            <h3>Sélectionnez un patient dans la barre latérale</h3>
            <p>Ou utilisez le bouton "Nouveau Patient" pour une inscription.</p>
        </div>
    """, unsafe_allow_html=True)

session_db.close()
