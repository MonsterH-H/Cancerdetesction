import streamlit as st
import pandas as pd
import os
import sys
import time
import io

# Ensure root directory is in path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.styles import apply_custom_styles, render_premium_header, render_section_title, render_logo
from src.engine import PredictionEngine
from src.storage import HistoryManager
from src.ai_advisor import AIAdvisor

# Configuration de la page
st.set_page_config(page_title="Import - OncoAI PRO", layout="wide", page_icon="📥")
apply_custom_styles()
render_logo()

if 'user' not in st.session_state:
    st.warning("⚠️ Authentification requise pour le traitement de masse.")
    st.stop()

render_premium_header(
    "Importation Massive", 
    "Inférence en lot et archivage automatique de données structurées.", 
    icon_class="fa-solid fa-file-excel", 
    badge="Batch Engine v6.3"
)

engine = PredictionEngine()
hm = HistoryManager()
ai_advisor = AIAdvisor()

# --- MODULE D'UPLOAD & TEMPLATE ---
with st.container():
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    c_up, c_tmp = st.columns([2, 1])
    
    with c_up:
        st.write("### 📂 Source de données")
        uploaded_file = st.file_uploader("Sélectionner un fichier (CSV ou XLSX)", type=["csv", "xlsx"])
    
    with c_tmp:
        st.write("### 📄 Modèle Standard")
        st.write("Téléchargez le format requis pour une importation sans erreur.")
        
        # Create Template
        template_df = pd.DataFrame(columns=[
            "ID", "Surname", "Name", "Age", "Gender", "Air Pollution", "Alcohol use", 
            "Dust Allergy", "OccuPational Hazards", "Genetic Risk", "chronic Lung Disease", 
            "Balanced Diet", "Obesity", "Smoking", "Passive Smoker", "Chest Pain", 
            "Coughing of Blood", "Fatigue", "Weight Loss", "Shortness of Breath", 
            "Wheezing", "Swallowing Difficulty", "Clubbing of Finger Nails", 
            "Frequent Cold", "Dry Cough", "Snoring"
        ])
        # Add example row
        template_df.loc[0] = ["H-000001", "Dupont", "Jean", 45, 1, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]
        
        buffer = io.BytesIO()
        template_df.to_excel(buffer, index=False)
        st.download_button(
            label="📥 TÉLÉCHARGER LE MODÈLE XLSX",
            data=buffer.getvalue(),
            file_name="OncoAI_Import_Template.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )

    st.markdown("</div>", unsafe_allow_html=True)

if uploaded_file is not None:
    try:
        # Chargement des données
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
            
        render_section_title("Validation des Données Source", "fa-solid fa-vial-circle-check")
        
        # Mapping logic
        feature_names = engine.get_feature_names()
        # Look for columns matching feature names
        found_features = [c for c in df.columns if c in feature_names]
        
        if len(found_features) < 23:
            st.warning(f"⚠️ Format incomplet : seulement {len(found_features)}/23 biomarqueurs identifiés par nom de colonne.")
            st.write("L'application tentera d'utiliser les premières colonnes numériques disponibles.")
        else:
            st.success(f"✅ Mapping optimal : les 23 biomarqueurs ont été identifiés.")

        st.dataframe(df.head(10), use_container_width=True)
        
        col_m1, col_m2 = st.columns(2)
        with col_m1:
            batch_ref = st.text_input("Référence du Lot Clinique", value=f"LOT-{time.strftime('%Y%m%d-%H%M')}")
        with col_m2:
            st.info(f"Total de lignes détectées : **{len(df)}**")
        
        if st.button("🚀 LANCER L'INFÉRENCE ET L'ARCHIVAGE", use_container_width=True, type="primary"):
            progress_bar = st.progress(0, text="Initialisation du lot...")
            
            results = []
            error_count = 0
            
            for index, row in df.iterrows():
                try:
                    # Robust Feature Extraction
                    features = []
                    if len(found_features) >= 23:
                        # Use mapped columns
                        features = [float(row[fn]) for fn in feature_names]
                    else:
                        # Fallback: take first 23 numeric values
                        num_vals = []
                        for v in row.values:
                            try:
                                fv = float(v)
                                if not pd.isna(fv): num_vals.append(fv)
                            except: continue
                        if len(num_vals) >= 23:
                            features = num_vals[:23]
                    
                    if len(features) >= 23:
                        # Inférence
                        pred, probs = engine.predict(features)
                        conf = float(max(probs)) if probs is not None else 0.0
                        
                        # Mapping Labels
                        if not isinstance(pred, str):
                            mapping = {0: "High", 1: "Low", 2: "Medium"}
                            pred = mapping.get(pred, str(pred))
                            
                        # Interpretation IA
                        interp = ai_advisor.generate_clinical_interpretation({"age": features[0]}, pred, conf)
                        
                        # Patient Info Mapping
                        p_info = {
                            "name": str(row.get('Name', row.get('Firstname', 'Patient'))),
                            "surname": str(row.get('Surname', row.get('Lastname', f'Import_{index}'))),
                            "clin_id": str(row.get('ID', row.get('HID', f'H-BATCH-{index:03d}'))),
                            "gender": int(features[1])
                        }
                        
                        # Save to Database
                        hm.save_prediction_full(
                            st.session_state.user['id'], 
                            p_info, 
                            features, 
                            pred, 
                            probs, 
                            interp, 
                            {"title": batch_ref, "source": "Batch Import"}
                        )
                        
                        results.append({
                            "HID": p_info['clin_id'],
                            "Patient": f"{p_info['surname']} {p_info['name']}",
                            "Risque": pred,
                            "Confiance": f"{conf*100:.1f}%"
                        })
                    else:
                        error_count += 1
                except Exception:
                    error_count += 1
                    continue
                
                # Update progress
                progress = (index + 1) / len(df)
                progress_bar.progress(progress, text=f"Traitement : {index+1}/{len(df)}")

            st.success(f"✅ Importation terminée : {len(results)} dossiers créés. ({error_count} erreurs)")
            
            if results:
                render_section_title("Résumé de l'Opération", "fa-solid fa-square-poll-vertical")
                res_df = pd.DataFrame(results)
                st.dataframe(res_df, use_container_width=True, hide_index=True)
                
                # Stats
                c1, c2, c3 = st.columns(3)
                c1.metric("Total Importé", len(results))
                high_p = len(res_df[res_df['Risque'].isin(['High', 'Élevé'])])
                c2.metric("Risques Élevés", high_p, delta=f"{(high_p/len(results))*100:.1f}%", delta_color="inverse")
                c3.metric("Lignes Rejetées", error_count)

    except Exception as e:
        st.error(f"❌ Erreur lors de la lecture du fichier : {e}")
else:
    st.info("💡 Prêt pour l'importation. Utilisez le modèle standard pour garantir l'intégrité des données.")
