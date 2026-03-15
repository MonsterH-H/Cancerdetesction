import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import os

class AnalyticsManager:
    def __init__(self, data_path='data/raw/cancer patient data sets.xlsx'):
        self.data_path = data_path
        self.df = self._load_data()

    def _load_data(self):
        paths = [self.data_path, 'data/raw/cancer patient data sets.xlsx', 'cancer patient data sets.xlsx']
        for path in paths:
            if os.path.exists(path):
                return pd.read_excel(path)
        return None

    def get_summary_stats(self):
        if self.df is None: return None
        stats = {
            "total_patients": len(self.df),
            "avg_age": round(self.df['Age'].mean(), 1),
            "high_risk_count": len(self.df[self.df['Level'] == 'High']),
            "smokers_percentage": round((self.df['Smoking'] > 5).sum() / len(self.df) * 100, 1)
        }
        return stats

    def plot_risk_by_age(self):
        if self.df is None: return None
        fig, ax = plt.subplots(figsize=(10, 5))
        sns.kdeplot(data=self.df, x='Age', hue='Level', fill=True, palette='viridis', ax=ax)
        ax.set_title("Distribution de l'Âge par Niveau de Risque")
        return fig

    def plot_correlation_matrix(self):
        if self.df is None: return None
        # Select numeric columns
        numeric_cols = self.df.select_dtypes(include=['number']).columns
        corr = self.df[numeric_cols].corr()
        
        fig, ax = plt.subplots(figsize=(12, 10))
        sns.heatmap(corr, annot=False, cmap='coolwarm', ax=ax)
        ax.set_title("Matrice de Corrélation Clinique")
        return fig

    def plot_feature_distribution(self, feature_name):
        if self.df is None or feature_name not in self.df.columns: return None
        fig, ax = plt.subplots(figsize=(8, 4))
        sns.countplot(data=self.df, x=feature_name, hue='Level', palette='magma', ax=ax)
        ax.set_title(f"Impact de: {feature_name}")
        return fig
