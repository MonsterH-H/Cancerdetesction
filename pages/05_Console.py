import streamlit as st
import pandas as pd
import os
import sys
from datetime import datetime, timezone

# Ensure root directory is in path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.styles import apply_custom_styles, render_premium_header, render_section_title, render_logo
from src.database import get_db_session, User, AuditLog
from src.engine import PredictionEngine

# Configuration de la page
st.set_page_config(page_title="Console Admin - OncoAI PRO", layout="wide", page_icon="⚙️")
apply_custom_styles()
render_logo()

# Sécurité : Accès Admin uniquement
if 'user' not in st.session_state or st.session_state.user['role'] != 'Admin':
    st.error("⛔ ACCÈS REFUSÉ : Cette zone est réservée aux administrateurs système.")
    if st.button("Retour au Tableau de Bord"):
        st.switch_page("app.py")
    st.stop()

render_premium_header(
    "Console d'Administration", 
    "Supervision des accès, journalisation de sécurité et maintenance du Core.", 
    icon_class="fa-solid fa-shield-halved", 
    badge="ADMIN ROOT"
)

session = get_db_session()
engine = PredictionEngine()

# Navigation par onglets
tab_users, tab_audit, tab_model, tab_sys = st.tabs([
    "👥 Utilisateurs", "🛡️ Audit Trail", "🧠 Modèles IA", "🔧 Maintenance"
])

# --- ONGLET 1 : UTILISATEURS ---
with tab_users:
    render_section_title("Opérateurs & Experts", "fa-solid fa-users-gear")
    
    users = session.query(User).all()
    user_data = []
    for u in users:
        user_data.append({
            "ID": u.id,
            "Identifiant": u.username,
            "Nom": f"{u.first_name or ''} {u.last_name or ''}",
            "Email": u.email,
            "Rôle": u.role,
            "Statut": u.status,
            "Dernier Accès": u.last_login.strftime('%d/%m/%Y %H:%M') if u.last_login else "Jamais"
        })
    
    st.dataframe(pd.DataFrame(user_data), use_container_width=True, hide_index=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    with st.expander("➕ AJOUTER UN NOUVEL OPÉRATEUR"):
        with st.form("new_user_form"):
            c1, c2, c3 = st.columns(3)
            with c1:
                new_un = st.text_input("Identifiant (Username)")
                new_pw = st.text_input("Mot de passe", type="password")
            with c2:
                new_fn = st.text_input("Prénom")
                new_ln = st.text_input("Nom")
            with c3:
                new_em = st.text_input("Email")
                new_rl = st.selectbox("Rôle Système", ["Doctor", "Admin", "Supervisor", "Auditor"])
            
            if st.form_submit_button("CRÉER LE COMPTE UTILISATEUR", use_container_width=True):
                if new_un and new_pw:
                    exists = session.query(User).filter_by(username=new_un).first()
                    if exists: st.error(f"L'identifiant '{new_un}' est déjà utilisé.")
                    else:
                        u = User(username=new_un, first_name=new_fn, last_name=new_ln, email=new_em, role=new_rl, status="Active")
                        u.set_password(new_pw)
                        session.add(u)
                        session.commit()
                        st.success(f"Compte pour {new_un} créé avec succès.")
                        st.rerun()

# --- ONGLET 2 : AUDIT LOGS ---
with tab_audit:
    render_section_title("Journal de Sécurité", "fa-solid fa-fingerprint")
    logs = (session.query(AuditLog, User.username).outerjoin(User).order_by(AuditLog.timestamp.desc()).limit(100).all())
    audit_data = [{"Horodatage": l.timestamp.strftime("%d/%m/%Y %H:%M:%S"), "Utilisateur": u or "Système", "Action": l.action, "Détails": l.details} for l, u in logs]
    st.dataframe(pd.DataFrame(audit_data), use_container_width=True, hide_index=True)

# --- ONGLET 3 : MODÈLES IA ---
with tab_model:
    render_section_title("Gestion des Modèles d'Inférence", "fa-solid fa-brain")
    
    col_m1, col_m2 = st.columns(2)
    with col_m1:
        st.markdown(f"""
            <div class='card'>
                <h4>Modèle Actif</h4>
                <h2 style='color:#0d9488;'>Random Forest v2.8</h2>
                <p><b>Fichier</b> : <code>models/cancer_risk_model.pkl</code></p>
                <p><b>Pipeline</b> : Scikit-Learn 1.3.0 Compatible</p>
                <p><b>Features requis</b> : 23 variables biomédicales</p>
                <hr>
                <p><b>Précision (Validation)</b> : 98.4%</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col_m2:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.write("#### 📤 Déployer une nouvelle version")
        uploaded_model = st.file_uploader("Charger un fichier .pkl", type=["pkl"])
        if uploaded_model:
            st.warning("⚠️ Le remplacement du modèle affectera tous les diagnostics futurs.")
            if st.button("CONFIRMER LE DÉPLOIEMENT", use_container_width=True):
                with open("models/cancer_risk_model.pkl", "wb") as f:
                    f.write(uploaded_model.getbuffer())
                st.success("✅ Nouveau modèle déployé avec succès. Redémarrage du moteur...")
                time.sleep(1)
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

# --- ONGLET 4 : MAINTENANCE ---
with tab_sys:
    render_section_title("Paramètres du Core", "fa-solid fa-microchip")
    if st.button("Nettoyer les rapports PDF temporaires", use_container_width=True):
        import glob
        files = glob.glob("data/reports/*.pdf")
        for f in files: os.remove(f)
        st.success(f"Nettoyage effectué : {len(files)} fichiers supprimés.")

session.close()
