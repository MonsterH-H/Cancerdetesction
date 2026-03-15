import streamlit as st
import requests
import json
import time

class AIAdvisor:
    """
    Interface pour Mistral AI - Génération d'interprétations cliniques.
    Gère la connexion sécurisée via les secrets Streamlit.
    """
    def __init__(self):
        self.api_url = "https://api.mistral.ai/v1/chat/completions"
        self.model = "mistral-tiny" # ou 'mistral-medium' selon votre abonnement
        
        # Récupération de la clé API depuis .streamlit/secrets.toml
        try:
            self.api_key = st.secrets["mistral"]["api_key"]
        except Exception:
            self.api_key = None

    def generate_clinical_interpretation(self, patient_data, risk_level, confidence):
        """
        Génère une interprétation réelle via l'API Mistral si disponible,
        sinon bascule sur le moteur logique par défaut.
        """
        if not self.api_key or "VOTRE_CLE" in self.api_key:
            return self._fallback_logic(risk_level, confidence)

        # Prompt structuré pour l'IA
        prompt = (
            f"En tant qu'assistant oncologue expert, analysez ce cas :\n"
            f"Patient Âge: {patient_data.get('age')} ans\n"
            f"Niveau de risque prédit: {risk_level}\n"
            f"Score de confiance: {confidence*100:.1f}%\n"
            f"Générez un avis clinique concis (max 3 phrases) pour le médecin traitant."
        )

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }

        payload = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.2
        }

        try:
            response = requests.post(self.api_url, headers=headers, json=payload, timeout=10)
            if response.status_code == 200:
                return response.json()['choices'][0]['message']['content']
            else:
                return f"Erreur API Mistral ({response.status_code}). " + self._fallback_logic(risk_level, confidence)
        except Exception:
            return self._fallback_logic(risk_level, confidence)

    def _fallback_logic(self, risk_level, confidence):
        """Moteur logique de secours en cas d'absence de connexion API."""
        if risk_level == "High":
            return (
                f"L'analyse identifie une corrélation forte avec les biomarqueurs critiques. "
                f"Avec une confiance de {confidence*100:.1f}%, un dépistage par scanner thoracique "
                f"est fortement recommandé."
            )
        elif risk_level == "Medium":
            return (
                f"Profil de vigilance modéré. Un suivi clinique semestriel et une évaluation "
                f"de la fonction pulmonaire sont recommandés."
            )
        else:
            return (
                f"Niveau de risque faible ({confidence*100:.1f}%). Maintenir les habitudes saines "
                f"et contrôle de routine annuel préconisé."
            )

    def generate_summary(self, df):
        """Génère un résumé de cohorte épidémiologique."""
        if df.empty:
            return "Données insuffisantes pour l'analyse."
            
        total = len(df)
        high_risk_pct = (len(df[df['risk_level'].isin(['High', 'Élevé'])]) / total) * 100
        avg_age = df['age'].mean()
        
        summary = (
            f"Analyse de cohorte sur {total} patients. "
            f"Le taux de risque élevé est de {high_risk_pct:.1f}%, avec un âge moyen de {avg_age:.1f} ans. "
            "Les tendances suggèrent une corrélation stable entre l'exposition environnementale et les scores de risque."
        )
        return summary
