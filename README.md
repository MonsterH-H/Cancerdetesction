# 🏥 Cancer Risk AI | Guide d'Installation & Utilisation

Bienvenue dans le guide officiel de la plateforme **Cancer Risk AI**. Ce document détaille les étapes concrètes pour configurer l'environnement, installer les dépendances et exploiter toute la puissance du modèle de diagnostic.

---

## 🏛️ Architecture du Projet

Le projet suit une structure modulaire de grade professionnel (Enterprise Standard) :

| Dossier / Fichier | Rôle |
| :--- | :--- |
| `app.py` | Point d'entrée principal (Landing Page & Navigation) |
| `pages/` | Modules d'interface (Analytics & Diagnosis) |
| `src/` | Logique métier (IA Engine, Data Analytics, Storage, Styles) |
| `models/` | Conteneur du modèle de Machine Learning (`.pkl`) |
| `data/raw/` | Données sources (`.xlsx`) |
| `data/prediction_history.csv` | Journal d'audit et historique des prédictions |
| `assets/` | Ressources visuelles et Identité de marque |

---

## 🛠️ Installation & Configuration

### 1. Prérequis
- Python 3.9 ou supérieur installé.
- Navigateur moderne (Chrome, Firefox, Safari).

### 2. Création de l'Environnement (Recommandé)
Ouvrez votre terminal dans le dossier du projet et exécutez :

```powershell
# Création de l'environnement virtuel
python -m venv venv

# Activation de l'environnement (Windows)
.\venv\Scripts\activate
```

### 3. Installation des Dépendances
Installez l'ensemble des bibliothèques nécessaires au moteur IA et à l'interface premium :

```powershell
pip install -r requirements.txt
```

---

## 📊 Configuration des Données

Pour que l'application soit 100% fonctionnelle et connectée, assurez-vous que les fichiers suivants sont présents :

1.  **Modèle IA** : Déplacez `cancer_risk_model.pkl` vers le dossier `models/`.
2.  **Dataset** : Déplacez `cancer patient data sets.xlsx` vers le dossier `data/raw/`.

---

## 🚀 Lancement de l'Application

Une fois l'environnement prêt, lancez la plateforme avec la commande suivante :

```powershell
streamlit run app.py
```

L'application s'ouvrira automatiquement dans votre navigateur à l'adresse : `http://localhost:8501`

---

## 📖 Guide d'Utilisation

### 📉 Analytics Engine
- **Exploration** : Visualisez les statistiques réelles de votre cohorte de patients.
- **Interprétabilité** : Consultez l'importance réelle des variables (Features) extraites du modèle.
- **Exports** : Filtrez et exportez vos données cliniques en format CSV.

### 🎯 AI Diagnosis
- **Saisie Multimodale** : Remplissez les 23 paramètres cliniques (âge, symptômes, environnement).
- **Inférence** : Cliquez sur "PROCESS CLINICAL DATA" pour obtenir un score de risque et un niveau de confiance.
- **Audit Log** : Chaque diagnostic est automatiquement sauvegardé dans l'historique pour un suivi longitudinal.

---

## 💡 Résolution de Problèmes

| Problème | Solution |
| :--- | :--- |
| **Modèle non trouvé** | Vérifiez que le fichier `.pkl` est bien dans `models/` avec le nom correct. |
| **Erreur de chargement Excel** | Assurez-vous que les fichiers ne sont pas ouverts dans Excel lors du lancement. |
| **Icônes manquantes** | Une connexion internet est requise pour le chargement de FontAwesome. |

---

> [!IMPORTANT]
> **Cancer Risk AI** est un outil de recherche et d'aide à la décision. Les résultats doivent systématiquement être interprétés par un professionnel de santé qualifié.

---
© 2024 Clinical Intelligence Platform - Premium Edition
