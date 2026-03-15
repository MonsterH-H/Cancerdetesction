import os
import sys
import hashlib
import time
from datetime import datetime, timedelta, timezone
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import func, desc

# Configuration du chemin racine
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from src.styles import apply_custom_styles, render_premium_header, render_logo, render_section_title
from src.database import get_db_session, PatientAnalysis, User, AuditLog, Patient, init_enterprise_admin

# Initialisation de la base de données (Premier run)
init_enterprise_admin()

# Configuration de la page
st.set_page_config(
    page_title="OncoAI PRO | Enterprise Suite",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

apply_custom_styles()

def generate_session_token(username):
    """Génère un token de session simulé pour l'aspect 'Concret/Enterprise'"""
    return hashlib.sha256(f"{username}{time.time()}".encode()).hexdigest()[:16].upper()

# --- AUTHENTICATION FLOW ---
if "user" not in st.session_state:
    st.markdown("""
        <div style='display: flex; justify-content: center; align-items: center; min-height: 80vh;'>
            <div class='card' style='width: 480px; padding: 45px; border-top: 8px solid #0d9488;'>
    """, unsafe_allow_html=True)

    render_logo(sidebar=False)

    st.markdown(
        "<p style='text-align:center; color:#64748b; margin-top:-0.5rem; margin-bottom:2rem; font-weight:500;'>Identification de l'opérateur de santé</p>",
        unsafe_allow_html=True
    )

    with st.container():
        username = st.text_input("Identifiant", placeholder="Username")
        password = st.text_input("Mot de passe", type="password", placeholder="••••••••")
        
        remember_me = st.checkbox("Rester connecté (Session persistante)")

        st.markdown("<br>", unsafe_allow_html=True)
        login_btn = st.button("ACCÈS SÉCURISÉ", width='stretch')

    if login_btn:
        session_db = get_db_session()
        try:
            user_rec = session_db.query(User).filter_by(username=username).first()
            if user_rec and user_rec.check_password(password):
                if user_rec.status != "Active":
                    st.error("Ce compte est actuellement suspendu.")
                else:
                    st.session_state.user = {
                        "id": user_rec.id,
                        "name": f"{user_rec.first_name or ''} {user_rec.last_name or user_rec.username}".strip(),
                        "role": user_rec.role,
                        "token": generate_session_token(username)
                    }
                    now_utc = datetime.now(timezone.utc)
                    user_rec.last_login = now_utc
                    
                    log = AuditLog(
                        user_id=user_rec.id, 
                        action="AUTH_SUCCESS", 
                        details=f"Token: {st.session_state.user['token']}", 
                        timestamp=now_utc
                    )
                    session_db.add(log)
                    session_db.commit()
                    st.rerun()
            else:
                st.error("Identifiants de sécurité non valides.")
        except Exception as e:
            st.error(f"Erreur de connexion au Core SQL : {e}")
        finally:
            session_db.close()

    st.markdown("</div></div>", unsafe_allow_html=True)
    st.stop()

# --- MAIN DASHBOARD INTERFACE ---
user = st.session_state.user
render_logo() # Logo SVG PRO

session_db = get_db_session()
try:
    now = datetime.now(timezone.utc)
    last_24h = now - timedelta(hours=24)

    # Statistiques Réelles
    total_count = session_db.query(func.count(PatientAnalysis.id)).scalar() or 0
    total_patients = session_db.query(func.count(Patient.id)).scalar() or 0
    today_count = session_db.query(func.count(PatientAnalysis.id)).filter(PatientAnalysis.timestamp >= last_24h).scalar() or 0
    high_risk = session_db.query(func.count(PatientAnalysis.id)).filter(PatientAnalysis.risk_level.in_(["High", "Élevé"])).scalar() or 0

    risk_counts = session_db.query(PatientAnalysis.risk_level, func.count(PatientAnalysis.id)).group_by(PatientAnalysis.risk_level).all()
    
    # Recent Activities (Analyses + Patient enrollment)
    recent_analyses = (
        session_db.query(PatientAnalysis, Patient.last_name)
        .join(Patient)
        .order_by(desc(PatientAnalysis.timestamp))
        .limit(5)
        .all()
    )
    
    recent_logs = (
        session_db.query(AuditLog, User.username)
        .outerjoin(User, AuditLog.user_id == User.id)
        .order_by(AuditLog.timestamp.desc())
        .limit(5)
        .all()
    )
except Exception as e:
    st.error(f"Erreur de synchronisation Dashboard : {e}")
    total_count = total_patients = today_count = high_risk = 0
    risk_counts = []
    recent_analyses = []
    recent_logs = []

# Sidebar Info
with st.sidebar:
    st.markdown(f"""
        <div style='padding: 1.5rem 0; border-bottom: 1px solid #e2e8f0; margin-bottom: 1.5rem; text-align:center;'>
            <div style='font-size: 1.1rem; font-weight: 700; color:#0f172a;'>{user['name']}</div>
            <div style='margin-top: 8px;'><span class='premium-badge'>{user['role']}</span></div>
            <div style='margin-top: 15px; font-size: 0.7rem; color: #94a3b8; font-family: monospace;'>TOKEN: {user['token']}</div>
        </div>
    """, unsafe_allow_html=True)

    if st.button("DÉCONNEXION SÉCURISÉE", width='stretch'):
        st.session_state.pop("user", None)
        st.rerun()

render_premium_header(
    "Tableau de Bord Clinical", 
    "Surveillance temps réel des indicateurs épidémiologiques et de l'activité.",
    icon_class="fa-solid fa-house-medical",
    badge="PRO v6.3 ONLINE"
)

# KPI Row
k1, k2, k3, k4 = st.columns(4)
k1.metric("Analyses Clôturées", total_count)
k2.metric("Base Patients", total_patients)
k3.metric("Activité (24h)", today_count)
k4.metric("Alertes Critiques", high_risk, delta_color="inverse")

st.markdown("---")

col_l, col_r = st.columns([2, 1])

with col_l:
    st.markdown(f"""
        <div class="card">
            <h3 style="margin-bottom: 0.5rem;">Statut du Système</h3>
            <p style="font-size:1rem; color:#475569;">
                Connecté au Core SQL OncoAI v6.1 (Timezone Aware). Moteur d'inférence Random Forest v2.8 opérationnel.
            </p>
        </div>
    """, unsafe_allow_html=True)

    # RECENT ANALYSES
    render_section_title("Activités Cliniques Récentes", "fa-solid fa-clock-rotate-left")
    if recent_analyses:
        for record, p_name in recent_analyses:
            risk_color = "#dc2626" if record.risk_level == "High" else ("#d97706" if record.risk_level == "Medium" else "#0d9488")
            st.markdown(f"""
                <div style='background:#ffffff; border:1px solid #e2e8f0; border-radius:12px; padding:1.2rem; margin-bottom:0.75rem; border-left: 6px solid {risk_color};'>
                    <div style='display:flex; justify-content:space-between; align-items:center;'>
                        <div>
                            <span style='font-weight:700; color:#0f172a;'>{record.analysis_title}</span> 
                            <span style='color:#64748b; margin-left:10px;'>&mdash; Patient : {p_name}</span>
                        </div>
                        <div style='background:{risk_color}; color:white; padding:4px 10px; border-radius:8px; font-size:0.75rem; font-weight:800;'>{str(record.risk_level).upper()}</div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.info("Aucune analyse récente.")

    # CHART
    st.subheader("📊 Répartition Étiologique des Risques")
    if risk_counts:
        df_counts = pd.DataFrame(risk_counts, columns=["Risk", "Count"])
        fig, ax = plt.subplots(figsize=(7, 4), facecolor="none")
        colors = {"High": "#dc2626", "Medium": "#d97706", "Low": "#0d9488", "Élevé": "#dc2626", "Modéré": "#d97706", "Faible": "#0d9488"}
        c_list = [colors.get(x, "#cbd5e1") for x in df_counts["Risk"]]
        
        wedges, texts, autotexts = ax.pie(df_counts["Count"], labels=df_counts["Risk"], autopct="%1.1f%%", colors=c_list, startangle=140, pctdistance=0.82, textprops={'color':"#0f172a", 'weight':'bold'})
        plt.setp(autotexts, size=10, weight="bold", color="white")
        centre_circle = plt.Circle((0, 0), 0.70, fc="white")
        ax.add_artist(centre_circle)
        ax.axis("equal")
        st.pyplot(fig)

with col_r:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("⚡ Accès Rapide")
    if st.button("🔬 NOUVELLE ANALYSE", width='stretch'): st.switch_page("pages/01_Diagnostic.py")
    if st.button("👥 RÉPERTOIRE PATIENTS", width='stretch'): st.switch_page("pages/07_Patients.py")
    if st.button("🗄️ HISTORIQUE CLINIQUE", width='stretch'): st.switch_page("pages/04_Registre.py")
    
    if user["role"] == "Admin":
        st.markdown("<hr style='border: 0.5px solid #f1f5f9; margin: 15px 0;'>", unsafe_allow_html=True)
        if st.button("⚙️ CONSOLE D'ADMINISTRATION", width='stretch'): st.switch_page("pages/05_Console.py")
    st.markdown("</div>", unsafe_allow_html=True)

    # AUDIT LOGS IN SIDE
    st.subheader("🛡️ Journal de Sécurité")
    if recent_logs:
        for log, username in recent_logs:
            display_user = username if username else "Système"
            st.markdown(f"""
                <div style='background:#f8fafc; border:1px solid #e2e8f0; border-radius:10px; padding:0.8rem; margin-bottom:0.5rem;'>
                    <div style='font-size:0.85rem; font-weight:700; color:#0d9488;'>{display_user}</div>
                    <div style='font-size:0.8rem; color:#64748b;'>{log.action}</div>
                    <div style='font-size:0.7rem; color:#94a3b8;'>{log.timestamp.strftime("%H:%M:%S")}</div>
                </div>
            """, unsafe_allow_html=True)

    # Session Status Card
    st.markdown(f"""
        <div class='card' style='background: #f8fafc; border: 1px dashed #cbd5e1; margin-top:20px;'>
            <h4 style='margin-top:0;'>État de Session</h4>
            <div style='display:flex; justify-content:space-between; font-size:0.85rem;'>
                <span>Status</span>
                <span style='color:#10b981; font-weight:700;'>EN LIGNE</span>
            </div>
            <div style='display:flex; justify-content:space-between; font-size:0.85rem; margin-top:5px;'>
                <span>Expert</span>
                <span>{user['name']}</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

session_db.close()
