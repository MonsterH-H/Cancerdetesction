from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey, Text, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime, timezone
import hashlib
import os

# Base de données SQLite locale - Migration v6.1 (Timezone Aware)
DB_PATH = "data/cancer_risk_v6.db"
os.makedirs("data", exist_ok=True)

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(128), nullable=False)
    email = Column(String(100), unique=True)
    role = Column(String(20), default='Doctor') # Doctor, Admin, Supervisor, Auditor
    first_name = Column(String(50))
    last_name = Column(String(50))
    status = Column(String(20), default='Active') # Active, Suspended
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    last_login = Column(DateTime)

    def set_password(self, password):
        self.password_hash = hashlib.sha256(password.encode()).hexdigest()

    def check_password(self, password):
        return self.password_hash == hashlib.sha256(password.encode()).hexdigest()

class Patient(Base):
    __tablename__ = 'patients'
    id = Column(Integer, primary_key=True)
    clin_id = Column(String(50), unique=True, index=True, nullable=False)
    first_name = Column(String(100))
    last_name = Column(String(100))
    gender = Column(Integer) # 1: Male, 2: Female
    birth_date = Column(DateTime)
    phone = Column(String(20))
    email = Column(String(100))
    address = Column(Text)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    
    analyses = relationship("PatientAnalysis", back_populates="patient", cascade="all, delete-orphan")

class PatientAnalysis(Base):
    __tablename__ = 'analyses'
    id = Column(Integer, primary_key=True)
    doctor_id = Column(Integer, ForeignKey('users.id'))
    patient_id = Column(Integer, ForeignKey('patients.id')) # Relation to patient
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    
    # Analysis Metadata
    analysis_title = Column(String(100))
    analysis_status = Column(String(20), default='Completed') # Draft, Completed, Archived
    source_type = Column(String(20)) # Manual, Batch
    
    # Clinical Features (Flattened for this version, but linked to patient)
    age = Column(Integer)
    gender = Column(Integer) # 1: Male, 2: Female (Stored here for analysis consistency)
    air_pollution = Column(Integer); alcohol_use = Column(Integer); dust_allergy = Column(Integer)
    occupational_hazards = Column(Integer); genetic_risk = Column(Integer); chronic_lung_disease = Column(Integer)
    balanced_diet = Column(Integer); obesity = Column(Integer); smoking = Column(Integer)
    passive_smoker = Column(Integer); chest_pain = Column(Integer); coughing_of_blood = Column(Integer)
    fatigue = Column(Integer); weight_loss = Column(Integer); shortness_of_breath = Column(Integer)
    wheezing = Column(Integer); swallowing_difficulty = Column(Integer); clubbing_of_finger_nails = Column(Integer)
    frequent_cold = Column(Integer); dry_cough = Column(Integer); snoring = Column(Integer)
    
    # Results
    risk_level = Column(String(20))
    confidence_score = Column(Float)
    ai_interpretation = Column(Text)
    
    patient = relationship("Patient", back_populates="analyses")
    prediction_details = relationship("PredictionDetails", back_populates="analysis", uselist=False, cascade="all, delete-orphan")

class PredictionDetails(Base):
    __tablename__ = 'prediction_details'
    id = Column(Integer, primary_key=True)
    analysis_id = Column(Integer, ForeignKey('analyses.id'))
    prob_low = Column(Float)
    prob_medium = Column(Float)
    prob_high = Column(Float)
    model_version = Column(String(20), default="RF-v2.8")
    
    analysis = relationship("PatientAnalysis", back_populates="prediction_details")

class AuditLog(Base):
    __tablename__ = 'audit_logs'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    action = Column(String(100))
    details = Column(Text)
    ip_address = Column(String(45))
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))

# Engine & Session
engine = create_engine(f'sqlite:///{DB_PATH}')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

def get_db_session():
    return Session()

def init_enterprise_admin():
    session = get_db_session()
    if session.query(User).filter_by(username="admin").count() == 0:
        admin = User(
            username="admin", 
            role="Admin", 
            first_name="Système", 
            last_name="Admin",
            email="admin@oncoai.com",
            status="Active"
        )
        admin.set_password("admin123")
        session.add(admin)
        session.commit()
    session.close()

if __name__ == "__main__":
    init_enterprise_admin()
