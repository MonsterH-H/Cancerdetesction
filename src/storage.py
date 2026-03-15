from src.database import get_db_session, PatientAnalysis, PredictionDetails, AuditLog, User, Patient
import pandas as pd
from datetime import datetime
from sqlalchemy import or_
from sqlalchemy.orm import joinedload

class HistoryManager:
    def __init__(self):
        pass

    def get_or_create_patient(self, session, info):
        """
        Récupère ou crée un patient basé sur son ID clinique.
        """
        patient = session.query(Patient).filter_by(clin_id=info['clin_id']).first()
        if not patient:
            patient = Patient(
                clin_id=info['clin_id'],
                first_name=info.get('name'),
                last_name=info.get('surname'),
                gender=info.get('gender')
            )
            session.add(patient)
            session.flush()
        return patient

    def save_prediction_full(self, user_id, patient_info, features, prediction, probs, ai_comment=None, metadata=None):
        """
        Sauvegarde complète v6 conforme Patient Centralized.
        """
        session = get_db_session()
        try:
            metadata = metadata or {}
            
            # 1. Get/Create Patient
            patient = self.get_or_create_patient(session, patient_info)
            
            # 2. Create Analysis Record
            analysis = PatientAnalysis(
                doctor_id=user_id,
                patient_id=patient.id,
                analysis_title=metadata.get('title', f"Analyse {datetime.now().strftime('%Y%m%d%H%M')}"),
                analysis_status='Completed',
                source_type=metadata.get('source', 'Manual'),
                age=features[0],
                gender=features[1],
                air_pollution=features[2], alcohol_use=features[3],
                dust_allergy=features[4], occupational_hazards=features[5],
                genetic_risk=features[6], chronic_lung_disease=features[7],
                balanced_diet=features[8], obesity=features[9],
                smoking=features[10], passive_smoker=features[11],
                chest_pain=features[12], coughing_of_blood=features[13],
                fatigue=features[14], weight_loss=features[15],
                shortness_of_breath=features[16], wheezing=features[17],
                swallowing_difficulty=features[18], clubbing_of_finger_nails=features[19],
                frequent_cold=features[20], dry_cough=features[21],
                snoring=features[22],
                risk_level=prediction,
                confidence_score=max(probs) if (probs is not None and len(probs) > 0) else 0.0,
                ai_interpretation=ai_comment
            )
            session.add(analysis)
            session.flush()

            # 3. Create Prediction Details
            if probs is not None:
                details = PredictionDetails(
                    analysis_id=analysis.id,
                    prob_low=probs[0] if len(probs)>0 else 0,
                    prob_medium=probs[1] if len(probs)>1 else 0,
                    prob_high=probs[2] if len(probs)>2 else 0
                )
                session.add(details)

            # 4. Audit Log
            log = AuditLog(
                user_id=user_id,
                action="PREDICTION_CREATED",
                details=f"Dossier {analysis.id} - Patient ID: {patient.clin_id}"
            )
            session.add(log)
            
            session.commit()
            return analysis.id
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def delete_analysis(self, analysis_id, user_id):
        session = get_db_session()
        try:
            analysis = session.query(PatientAnalysis).filter_by(id=analysis_id).first()
            if analysis:
                session.delete(analysis)
                log = AuditLog(user_id=user_id, action="DELETE_RECORD", details=f"Analyse ID: {analysis_id}")
                session.add(log)
                session.commit()
                return True
            return False
        finally:
            session.close()

    def get_history_df(self, search_query=None):
        session = get_db_session()
        try:
            query = session.query(PatientAnalysis, User.username, Patient).join(User).join(Patient)
            if search_query:
                s = f"%{search_query}%"
                query = query.filter(or_(
                    Patient.first_name.like(s),
                    Patient.last_name.like(s),
                    Patient.clin_id.like(s),
                    PatientAnalysis.analysis_title.like(s)
                ))
            
            data = []
            for record, username, patient in query.all():
                risk_map = {"Low": "Faible", "Medium": "Modéré", "High": "Élevé"}
                data.append({
                    "id": record.id,
                    "Titre": record.analysis_title,
                    "Patient": f"{patient.first_name or ''} {patient.last_name or ''}".strip(),
                    "ID Clinique": patient.clin_id,
                    "Date": record.timestamp,
                    "Risque": risk_map.get(record.risk_level, record.risk_level),
                    "Expert": username,
                    "Source": record.source_type
                })
            
            df = pd.DataFrame(data)
            if not df.empty:
                return df.sort_values(by="Date", ascending=False)
            else:
                return pd.DataFrame(columns=["id", "Titre", "Patient", "ID Clinique", "Date", "Risque", "Expert", "Source"])
        finally:
            session.close()

    def get_patients_df(self, search_query=None):
        session = get_db_session()
        try:
            query = session.query(Patient)
            if search_query:
                s = f"%{search_query}%"
                query = query.filter(or_(
                    Patient.first_name.like(s),
                    Patient.last_name.like(s),
                    Patient.clin_id.like(s)
                ))
            
            data = []
            for p in query.all():
                analysis_count = session.query(PatientAnalysis).filter_by(patient_id=p.id).count()
                last_risk = session.query(PatientAnalysis.risk_level).filter_by(patient_id=p.id).order_by(PatientAnalysis.timestamp.desc()).first()
                data.append({
                    "id": p.id,
                    "ID Clinique": p.clin_id,
                    "Nom": f"{p.first_name} {p.last_name}",
                    "Analyses": analysis_count,
                    "Dernier Risque": last_risk[0] if last_risk else "N/A",
                    "Inscrit le": p.created_at
                })
            return pd.DataFrame(data)
        finally:
            session.close()

    def get_patient_profile(self, patient_id):
        session = get_db_session()
        try:
            patient = session.query(Patient).filter_by(id=patient_id).first()
            if not patient: return None
            
            analyses = session.query(PatientAnalysis).options(joinedload(PatientAnalysis.patient)).filter_by(patient_id=patient.id).order_by(PatientAnalysis.timestamp.desc()).all()
            return {
                "patient": patient,
                "history": analyses
            }
        finally:
            session.close()

    def get_analysis_by_id(self, analysis_id):
        session = get_db_session()
        try:
            return session.query(PatientAnalysis).options(joinedload(PatientAnalysis.patient)).filter_by(id=analysis_id).first()
        finally:
            session.close()

