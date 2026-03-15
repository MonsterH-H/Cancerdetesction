from fpdf import FPDF
from datetime import datetime
import os

class ReportGenerator:
    def __init__(self, output_dir="data/reports"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def generate_patient_report(self, analysis_record):
        """
        Génère un rapport PDF Premium v6.2 (Thème Teal) avec identité patient et avis IA Mistral.
        """
        pdf = FPDF()
        pdf.add_page()
        
        # --- HEADER ---
        pdf.set_font("Helvetica", 'B', 22)
        pdf.set_text_color(13, 148, 136) # Teal OncoAI PRO
        pdf.cell(0, 15, "ONCOAI PRO : DOSSIER CLINIQUE", ln=True, align='C')
        
        pdf.set_font("Helvetica", '', 9)
        pdf.set_text_color(100, 116, 139)
        report_id = f"REF-{analysis_record.id:06d}"
        date_str = analysis_record.timestamp.strftime('%d/%m/%Y %H:%M')
        pdf.cell(0, 10, f"Rapport: {report_id} | Date: {date_str}", ln=True, align='R')
        
        pdf.ln(5)
        pdf.set_draw_color(13, 148, 136)
        pdf.set_line_width(0.5)
        pdf.line(10, pdf.get_y(), 200, pdf.get_y())
        pdf.ln(10)

        # In V6, analysis_record.patient is available via joinedload
        p_obj = getattr(analysis_record, 'patient', None)
        if p_obj:
            p_name = f"{p_obj.first_name} {p_obj.last_name}"
            p_id = p_obj.clin_id
        else:
            p_name = "Patient Anonyme"
            p_id = "N/A"

        # --- SECTION 1: IDENTITE PATIENT ---
        pdf.set_font("Helvetica", 'B', 14)
        pdf.set_text_color(15, 23, 42)
        pdf.cell(0, 10, "1. IDENTIFICATION DU PATIENT", ln=True)
        
        pdf.set_font("Helvetica", '', 11)
        pdf.cell(45, 8, "Nom complet:", border=0)
        pdf.set_font("Helvetica", 'B', 11)
        pdf.cell(0, 8, p_name.upper(), ln=True)
        
        pdf.set_font("Helvetica", '', 11)
        pdf.cell(45, 8, "ID Clinique (HID):", border=0)
        pdf.cell(0, 8, p_id, ln=True)
        
        pdf.cell(45, 8, "Age / Sexe:", border=0)
        gender_str = 'Masculin' if analysis_record.gender == 1 else 'Féminin'
        pdf.cell(0, 8, f"{analysis_record.age} ans / {gender_str}", ln=True)
        
        pdf.ln(10)

        # --- SECTION 2: ÉVALUATION DU RISQUE ---
        pdf.set_font("Helvetica", 'B', 14)
        pdf.cell(0, 10, "2. ANALYSE PRÉDICTIVE (AI ENGINE)", ln=True)
        
        risk_map = {"Low": "FAIBLE", "Medium": "MODÉRÉ", "High": "ÉLEVÉ"}
        r_level = analysis_record.risk_level
        if isinstance(r_level, bytes): r_level = r_level.decode('utf-8')
        status = str(risk_map.get(r_level, r_level)).upper()
        
        if "ÉLEVÉ" in status: 
            pdf.set_fill_color(252, 165, 165) # Rouge clair
            pdf.set_text_color(153, 27, 27) # Rouge foncé
        elif "MODÉRÉ" in status:
            pdf.set_fill_color(253, 230, 138) # Jaune clair
            pdf.set_text_color(146, 64, 14) # Jaune foncé
        else:
            pdf.set_fill_color(204, 251, 241) # Teal très clair
            pdf.set_text_color(13, 148, 136) # Teal PRO
            
        pdf.set_font("Helvetica", 'B', 16)
        pdf.cell(0, 15, f"RÉSULTAT : RISQUE {status}", ln=True, align='C', fill=True)
        
        pdf.set_font("Helvetica", '', 10)
        pdf.set_text_color(100, 116, 139)
        conf = f"{analysis_record.confidence_score*100:.1f}%"
        pdf.cell(0, 8, f"Confiance Statistique du Modèle : {conf} (RF-v2.8)", ln=True, align='C')
        
        pdf.ln(10)

        # --- SECTION 3: INTERPRÉTATION MISTRAL ---
        pdf.set_font("Helvetica", 'B', 14)
        pdf.set_text_color(15, 23, 42)
        pdf.set_fill_color(248, 250, 252)
        pdf.cell(0, 10, "3. SYNTHÈSE CLINIQUE GÉNÉRATIVE (MISTRAL AI)", ln=True, fill=True)
        
        pdf.ln(4)
        pdf.set_font("Helvetica", '', 11)
        pdf.set_text_color(51, 65, 85)
        ai_text = analysis_record.ai_interpretation or "Aucune interprétation disponible."
        pdf.multi_cell(0, 7, ai_text)
        
        pdf.ln(10)

        # --- FOOTER ---
        pdf.set_y(-35)
        pdf.set_font("Helvetica", 'I', 8)
        pdf.set_text_color(148, 163, 184)
        pdf.line(10, pdf.get_y(), 200, pdf.get_y())
        pdf.ln(2)
        legal = (
            "Avis Légal : Ce rapport est une aide à la décision clinique générée par Intelligence Artificielle. "
            "Il n'est pas un diagnostic définitif et doit être interprété par un oncologue qualifié."
        )
        pdf.multi_cell(0, 4, legal, align='C')
        
        file_name = f"Rapport_{p_id}_{datetime.now().strftime('%Y%m%d%H%M')}.pdf"
        file_path = os.path.join(self.output_dir, file_name)
        pdf.output(file_path)
        return file_path
