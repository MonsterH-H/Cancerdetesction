import streamlit as st
import pandas as pd
import os
import sys
from datetime import datetime, timedelta

# Ensure root directory is in path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.styles import apply_custom_styles, render_premium_header, render_section_title, render_logo
from src.storage import HistoryManager
from src.reporting import ReportGenerator

# Configuration de la page
st.set_page_config(page_title="Registre - OncoAI PRO", layout="wide", page_icon="🗄️")
apply_custom_styles()
render_logo()

if 'user' not in st.session_state:
    st.warning("Authentification requise pour consulter les archives cliniques.")
    st.stop()

render_premium_header(
    "Registre National", 
    "Archive centrale des diagnostics, journal d'exportation et traçabilité.", 
    icon_class="fa-solid fa-box-archive", 
    badge="Archive Sécurisée"
)

hm = HistoryManager()
reporter = ReportGenerator()

# --- FILTRES AVANCÉS ---
with st.container():
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    f1, f2, f3 = st.columns([2, 1, 1])
    
    with f1:
        search_q = st.text_input("Recherche textuelle (Patient, ID, Titre)", placeholder="Ex: Jean Dupont ou H-123456")
    
    with f2:
        risk_filter = st.selectbox("Niveau de Risque", ["Tous", "High", "Medium", "Low"])
        
    with f3:
        period_filter = st.selectbox("Période", ["Tout", "Dernières 24h", "7 derniers jours", "30 derniers jours"])
    
    st.markdown("</div>", unsafe_allow_html=True)

# Récupération des données
df = hm.get_history_df(search_query=search_q)

# Application des filtres supplémentaires en local sur le DF pour plus de réactivité
if not df.empty:
    if risk_filter != "Tous":
        # Mapping possible labels
        risk_map_rev = {"High": ["High", "Élevé"], "Medium": ["Medium", "Modéré"], "Low": ["Low", "Faible"]}
        df = df[df['Risque'].isin(risk_map_rev[risk_filter])]
        
    if period_filter != "Tout":
        now = datetime.now()
        if period_filter == "Dernières 24h":
            cutoff = now - timedelta(days=1)
        elif period_filter == "7 derniers jours":
            cutoff = now - timedelta(days=7)
        else:
            cutoff = now - timedelta(days=30)
        
        # Ensure 'Date' is datetime for comparison
        df['Date'] = pd.to_datetime(df['Date'])
        # Handle timezone-aware vs naive
        if df['Date'].dt.tz is not None:
             import pytz
             cutoff = cutoff.replace(tzinfo=pytz.UTC)
        df = df[df['Date'] >= cutoff]

# Affichage du Registre
if not df.empty:
    st.write(f"📁 **{len(df)} dossiers correspondants à vos critères**")
    
    # Custom display for dataframe
    st.dataframe(
        df, 
        column_config={
            "id": st.column_config.NumberColumn("Ref", format="#%d"),
            "Date": st.column_config.DatetimeColumn("Horodatage", format="DD/MM/YYYY HH:mm"),
            "Risque": st.column_config.TextColumn("Verdict IA"),
        },
        width='stretch', 
        hide_index=True
    )
    
    render_section_title("Modules d'Intervention & Export", "fa-solid fa-gears")
    
    col_sel, col_act = st.columns([1, 2])
    
    with col_sel:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        available_ids = df['id'].tolist()
        sid = st.selectbox("Sélectionner un ID Dossier", available_ids)
        st.markdown("</div>", unsafe_allow_html=True)
        
    with col_act:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        a1, a2 = st.columns(2)
        
        with a1:
            if st.button("📄 GÉNÉRER RAPPORT PDF", use_container_width=True):
                record = hm.get_analysis_by_id(sid)
                if record:
                    path = reporter.generate_patient_report(record)
                    with open(path, "rb") as f:
                        st.download_button(
                            label="⬇️ TÉLÉCHARGER LE PDF", 
                            data=f, 
                            file_name=os.path.basename(path), 
                            mime="application/pdf",
                            use_container_width=True
                        )
        
        with a2:
            if st.session_state.user['role'] == 'Admin':
                if st.toggle(f"🔓 Débloquer Suppression #{sid}"):
                    if st.button("🔥 EFFACER DÉFINITIVEMENT", type="primary", use_container_width=True):
                        if hm.delete_analysis(sid, st.session_state.user['id']):
                            st.success(f"Dossier #{sid} supprimé.")
                            st.rerun()
            else:
                st.info("⚠️ Droits d'édition limités.")
        st.markdown("</div>", unsafe_allow_html=True)

    # Bulk Export
    st.markdown("<br>", unsafe_allow_html=True)
    exp_l, exp_r = st.columns(2)
    with exp_l:
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("📤 EXPORTER LE REGISTRE (CSV)", csv, "oncoai_registre_export.csv", "text/csv", use_container_width=True)
    with exp_r:
        json_data = df.to_json(orient='records').encode('utf-8')
        st.download_button("📤 EXPORTER LE REGISTRE (JSON)", json_data, "oncoai_registre_export.json", "application/json", use_container_width=True)

else:
    st.info("Aucun dossier trouvé dans le registre avec les filtres actuels.")
