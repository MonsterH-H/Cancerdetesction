# 🧬 OncoAI PRO | Enterprise Cancer Risk Suite

OncoAI PRO is a professional-grade clinical intelligence platform designed for predicting cancer risk levels using advanced machine learning. It features a robust multi-page Streamlit interface, a persistent SQL backend, and automated medical reporting.

## 🏗️ Project Architecture

The project follows a modular "Enterprise Standard" architecture:

- **`app.py`**: Main entry point, handling authentication and the central dashboard.
- **`pages/`**: Functional modules for the application:
  - `01_Diagnostic.py`: Individual patient analysis and ML inference.
  - `02_Importation.py`: Batch processing of clinical data (Excel/CSV).
  - `03_Exploration.py`: Data analytics and clinical correlation visualization.
  - `04_Registre.py`: Full history of analyses and audit logs.
  - `05_Console.py`: Administrative tools and system settings.
  - `07_Patients.py`: Patient directory management.
- **`src/`**: Core business logic:
  - `database.py`: SQLAlchemy models (Users, Patients, Analyses, AuditLogs). Uses SQLite (`data/cancer_risk_v6.db`).
  - `engine.py`: AI inference engine (Random Forest v2.8) loading `models/cancer_risk_model.pkl`.
  - `reporting.py`: PDF report generation using `fpdf2`.
  - `analytics.py`: Statistical analysis on raw clinical datasets.
  - `styles.py`: Custom CSS and premium UI components.
- **`models/`**: Serialization of the Random Forest model.
- **`data/`**: Persistent storage for databases, CSV logs, raw Excel datasets, and generated PDF reports.

## 🛠️ Key Technologies

- **Frontend**: Streamlit (Premium Custom UI).
- **Backend**: Python 3.12+, SQLAlchemy (SQLite).
- **AI/ML**: Scikit-learn (Random Forest), Joblib.
- **Reporting**: FPDF2, Mistral AI (for generative clinical synthesis).
- **Data Analysis**: Pandas, Matplotlib, Seaborn.

## 🚀 Building and Running

### Prerequisites
- Python 3.9+ (3.12 recommended).
- Virtual environment (recommended).

### Setup
1. **Install Dependencies**:
   ```powershell
   pip install -r requirements.txt
   ```
2. **Initialize Database**:
   The database and default admin account are automatically initialized on the first run. Default credentials: `admin` / `admin123`.

### Running the App
```powershell
streamlit run app.py
```

## ⚖️ Development Conventions

- **Persistence**: "No Simulation" mandate. All data displayed must be fetched from the database or the ML engine.
- **Clinical Features**: The system rigorously expects 23 specific clinical features (Age, Gender, Air Pollution, Alcohol use, etc.).
- **Security**: Audit logs (`AuditLog` table) must record all critical actions (Auth, Predictions, Exports).
- **Timezone Awareness**: All timestamps must be UTC-based (implemented in v6.1).
- **Modularity**: Business logic must reside in `src/`, while UI logic remains in `app.py` or `pages/`.

## 📂 Key Files
- `data/cancer_risk_v6.db`: The primary production database.
- `models/cancer_risk_model.pkl`: The core ML model file.
- `data/raw/cancer patient data sets.xlsx`: Source dataset for clinical exploration.
- `src/database.py`: Defines the relational schema.
- `src/engine.py`: Defines the prediction pipeline.
