

# CAHIER DES CHARGES COMPLET D’UNE APPLICATION DE PRÉDICTION DU NIVEAU DE RISQUE DE CANCER

---

# 1. Intitulé du projet

**Développement d’une application complète de prédiction, d’analyse, de suivi et de reporting du niveau de risque de cancer à partir de données patients**

---

# 2. Contexte du projet

Un modèle de machine learning de prédiction du niveau de risque de cancer a déjà été développé, validé et exporté.  
Le besoin actuel porte sur la création d’une **application complète**, exploitable par des utilisateurs métiers et techniques, permettant d’utiliser ce modèle dans un cadre opérationnel.

L’application doit permettre à un utilisateur :
- de saisir manuellement des informations patient,
- d’importer des données en lot,
- de lancer des prédictions,
- de consulter les résultats,
- d’interpréter les facteurs influents,
- de générer des rapports,
- de conserver un historique,
- de retrouver les analyses précédentes,
- de gérer les utilisateurs et les accès,
- d’assurer une traçabilité complète.

L’objectif est de disposer d’une **véritable application métier**, et non d’un simple notebook ou script d’inférence.

---

# 3. Objectif général

Concevoir une application web ou desktop professionnelle permettant :

- l’exploitation du modèle de prédiction déjà entraîné,
- la gestion des dossiers d’analyse,
- la saisie de données patients,
- la génération de prédictions du niveau de risque,
- la visualisation claire des résultats,
- l’édition de rapports,
- l’archivage des analyses,
- la consultation d’un historique,
- la supervision fonctionnelle et technique de l’application.

---

# 4. Objectifs spécifiques

L’application devra offrir les capacités suivantes :

1. **Créer une nouvelle analyse**
2. **Saisir les données d’un patient via formulaire**
3. **Importer des données depuis un fichier**
4. **Exécuter une prédiction individuelle ou en lot**
5. **Afficher le niveau de risque prédit**
6. **Afficher le score de probabilité par niveau**
7. **Afficher l’explication des résultats**
8. **Conserver l’analyse dans un historique**
9. **Permettre la recherche et la consultation d’analyses passées**
10. **Générer un rapport téléchargeable**
11. **Exporter les résultats**
12. **Afficher des tableaux de bord de synthèse**
13. **Permettre l’administration des comptes et paramètres**
14. **Journaliser les actions des utilisateurs**
15. **Garantir la sécurité et la confidentialité des données**

---

# 5. Nature de l’application

L’application visée est une **application métier complète** pouvant être déployée sous forme :

- d’application web responsive,
- ou d’application interne accessible via navigateur.

### Type recommandé :
**Application web sécurisée avec back-office d’administration**

### Stack possible :
- Frontend : React / Vue / Angular ou Streamlit avancé selon budget
- Backend : FastAPI / Django / Flask
- Base de données : PostgreSQL / MySQL / SQLite en prototype
- Stockage modèles : `.pkl` / `.onnx`
- Reporting : PDF / Excel / CSV
- Authentification : JWT / session sécurisée

---

# 6. Utilisateurs cibles

## 6.1 Utilisateurs métier
- médecins
- assistants médicaux
- personnel de saisie
- analystes de santé
- coordinateurs de programme de dépistage

## 6.2 Utilisateurs techniques
- administrateur applicatif
- data scientist
- administrateur système
- responsable qualité / audit

---

# 7. Profils utilisateurs

---

## 7.1 Administrateur
Peut :
- créer/modifier/supprimer des comptes,
- gérer les rôles,
- consulter tous les historiques,
- accéder aux statistiques globales,
- configurer l’application,
- gérer les exports,
- superviser les journaux.

## 7.2 Utilisateur métier
Peut :
- créer une analyse,
- remplir un formulaire patient,
- lancer une prédiction,
- voir les résultats,
- générer un rapport,
- consulter ses historiques,
- exporter ses données selon ses droits.

## 7.3 Superviseur / Responsable
Peut :
- consulter les analyses de son équipe,
- visualiser les rapports consolidés,
- suivre les statistiques d’activité.

## 7.4 Auditeur
Peut :
- consulter les logs,
- vérifier les actions,
- contrôler les accès,
- vérifier la traçabilité.

---

# 8. Périmètre fonctionnel global

L’application doit être structurée autour des grands modules suivants :

1. **Authentification et gestion des utilisateurs**
2. **Accueil / tableau de bord**
3. **Création d’analyse**
4. **Formulaire de saisie patient**
5. **Import de données**
6. **Moteur de prédiction**
7. **Affichage détaillé des résultats**
8. **Interprétation / explication**
9. **Historique des analyses**
10. **Recherche et filtrage**
11. **Rapports et exports**
12. **Administration**
13. **Journalisation / audit**
14. **Paramétrage**
15. **Support et aide utilisateur**

---

# 9. Description détaillée des modules fonctionnels

---

## 9.1 Module Authentification et gestion des accès

### Objectif
Sécuriser l’accès à l’application et adapter les droits selon les profils.

### Fonctionnalités
- page de connexion,
- mot de passe sécurisé,
- réinitialisation mot de passe,
- déconnexion,
- gestion des sessions,
- gestion des rôles,
- contrôle des permissions,
- blocage après tentatives échouées,
- journalisation des connexions.

### Champs écran connexion
- email / identifiant
- mot de passe
- bouton “Se connecter”
- lien “Mot de passe oublié”

### Contraintes
- mot de passe chiffré
- session expirante
- accès interdit sans authentification

---

## 9.2 Module Tableau de bord

### Objectif
Offrir une vue synthétique de l’activité et des résultats récents.

### Fonctionnalités
Le tableau de bord doit afficher :
- nombre total d’analyses réalisées,
- nombre d’analyses du jour / semaine / mois,
- répartition des niveaux de risque prédits,
- dernières analyses effectuées,
- taux d’utilisation de l’application,
- indicateurs globaux,
- accès rapide aux actions principales.

### Widgets attendus
- carte “Analyses totales”
- carte “Nouvelles analyses”
- graphique en barres des niveaux Low / Medium / High
- tableau des dernières analyses
- raccourcis :
  - Nouvelle analyse
  - Importer un fichier
  - Voir historique
  - Générer rapport

---

## 9.3 Module Création d’une nouvelle analyse

### Objectif
Créer un dossier d’analyse avant de saisir ou importer les données.

### Fonctionnalités
- bouton “Nouvelle analyse”
- génération d’un identifiant unique d’analyse
- rattachement à un utilisateur
- date/heure de création
- statut de l’analyse :
  - brouillon
  - en cours
  - terminée
  - archivée

### Informations de dossier
- identifiant analyse
- nom du dossier
- description
- patient ou lot
- source des données :
  - saisie manuelle
  - import fichier
- auteur
- date de création

---

## 9.4 Module Formulaire de saisie patient

### Objectif
Permettre la saisie manuelle de toutes les caractéristiques nécessaires au modèle.

### Fonctionnalités
- formulaire structuré par sections,
- validation en temps réel,
- champs obligatoires,
- enregistrement brouillon,
- soumission pour prédiction.

### Exigence majeure
Le formulaire doit contenir **toutes les variables d’entrée du modèle** excepté `Patient Id` si non utilisé, avec contrôle de cohérence.

### Sections recommandées

#### A. Informations administratives
- identifiant dossier
- nom patient (optionnel/anonymisé selon politique)
- code patient interne
- sexe
- âge
- date de saisie
- opérateur

#### B. Données cliniques / variables du modèle
Toutes les colonnes nécessaires au modèle doivent être présentes sous forme de :
- champs numériques,
- listes déroulantes,
- boutons radio,
- cases à cocher,
- sélecteurs selon la nature des variables.

#### C. Contrôles de saisie
- bornes minimales / maximales,
- format numérique,
- liste de valeurs autorisées,
- messages d’erreur explicites.

#### D. Actions possibles
- Enregistrer brouillon
- Réinitialiser le formulaire
- Lancer la prédiction
- Enregistrer et quitter

### Validation du formulaire
Le système doit :
- vérifier la complétude,
- vérifier les plages plausibles,
- empêcher les types invalides,
- afficher les champs en erreur.

---

## 9.5 Module Import de données

### Objectif
Permettre l’import de plusieurs enregistrements à traiter en lot.

### Formats acceptés
- `.xlsx`
- `.csv`

### Fonctionnalités
- téléchargement d’un fichier,
- aperçu du contenu,
- validation des colonnes,
- mapping automatique ou manuel,
- détection des anomalies,
- import en masse,
- lancement de prédictions par lot,
- génération de fichier de sortie enrichi.

### Contrôles à effectuer
- colonnes obligatoires présentes,
- format conforme,
- types cohérents,
- valeurs manquantes,
- lignes invalides,
- doublons.

### Sorties attendues
- nombre de lignes importées
- nombre de lignes valides
- nombre de lignes rejetées
- rapport d’erreurs d’import
- prédictions lot par lot

---

## 9.6 Module Moteur de prédiction

### Objectif
Exécuter le modèle déjà entraîné sur des données entrantes.

### Fonctionnalités
- chargement du modèle en production,
- application automatique du pipeline associé,
- prédiction unitaire,
- prédiction par lot,
- calcul des probabilités,
- retour du niveau de risque.

### Résultat attendu
Pour chaque patient :
- classe prédite :
  - Low
  - Medium
  - High
- score de confiance / probabilité
- date de prédiction
- version du modèle utilisé

### Contraintes
- temps de réponse rapide,
- résultat traçable,
- cohérence avec le pipeline entraîné.

---

## 9.7 Module Résultats d’analyse

### Objectif
Présenter clairement les résultats au professionnel utilisateur.

### Données affichées
- résumé patient / dossier,
- date de l’analyse,
- niveau de risque prédit,
- score de probabilité par classe,
- statut de l’analyse,
- observations complémentaires.

### Restitution visuelle attendue
- badge coloré :
  - vert = Low
  - orange = Medium
  - rouge = High
- graphique des probabilités,
- bloc “résultat principal” mis en avant,
- résumé lisible.

### Exemple de rendu
- Niveau prédit : **High**
- Confiance :
  - Low = 8%
  - Medium = 24%
  - High = 68%

### Actions disponibles
- enregistrer le résultat,
- générer un rapport,
- exporter,
- revenir au formulaire,
- comparer avec analyses précédentes.

---

## 9.8 Module Explication / Interprétabilité

### Objectif
Aider l’utilisateur à comprendre les facteurs ayant influencé la prédiction.

### Fonctionnalités
- affichage des variables les plus influentes,
- importance globale des variables,
- si possible explication locale du cas courant,
- synthèse interprétative lisible.

### Restitutions
- top variables contributives,
- graphique d’importance,
- message explicatif :
  - “Le risque élevé est principalement influencé par les variables X, Y et Z.”

### Attention
L’application ne doit pas afficher une certitude médicale abusive.  
Elle doit préciser que :
- le résultat est une **aide à la décision**,
- la décision finale appartient au professionnel de santé.

---

## 9.9 Module Historique des analyses

### Objectif
Conserver et consulter toutes les analyses réalisées.

### Fonctionnalités
- liste paginée des analyses,
- consultation par utilisateur,
- consultation globale selon rôle,
- recherche multicritère,
- tri,
- filtrage,
- accès au détail d’une analyse.

### Informations par ligne
- ID analyse
- date
- utilisateur
- patient / code patient
- type d’analyse
- niveau prédit
- statut
- version du modèle
- actions

### Filtres attendus
- date début / date fin
- utilisateur
- niveau de risque
- statut
- source (manuel / import)
- patient / identifiant dossier

### Actions sur l’historique
- consulter
- exporter
- archiver
- supprimer selon droits
- dupliquer une analyse
- régénérer un rapport

---

## 9.10 Module Recherche avancée

### Objectif
Retrouver rapidement une analyse ou un patient.

### Fonctionnalités
- barre de recherche rapide,
- recherche avancée multicritère,
- recherche plein texte sur commentaires et identifiants,
- filtres enregistrables.

### Champs de recherche
- code patient
- ID analyse
- nom / pseudo patient
- date
- niveau prédit
- auteur
- statut
- modèle utilisé

---

## 9.11 Module Rapports

### Objectif
Produire des documents exploitables, imprimables ou transmissibles.

### Types de rapports

#### Rapport individuel patient/analyse
Contient :
- informations du dossier,
- données saisies,
- résultat de prédiction,
- probabilités,
- explication synthétique,
- date,
- utilisateur,
- version du modèle,
- mention légale.

#### Rapport consolidé
Contient :
- nombre d’analyses,
- répartition des niveaux de risque,
- tendances par période,
- export activité.

### Formats d’export
- PDF
- Excel
- CSV
- éventuellement impression directe

### Actions possibles
- visualiser avant téléchargement
- générer automatiquement
- télécharger
- envoyer par email si autorisé

---

## 9.12 Module Exports

### Objectif
Permettre l’extraction des résultats à des fins d’analyse ou d’archivage.

### Exports attendus
- résultats d’analyse unitaires
- résultats en lot
- historique filtré
- statistiques globales
- rapports PDF

### Contraintes
- droits d’export gérés par rôle,
- traçabilité des exports,
- anonymisation possible.

---

## 9.13 Module Administration

### Objectif
Permettre la supervision et le paramétrage de l’application.

### Fonctionnalités
- gestion des utilisateurs,
- gestion des rôles,
- activation/désactivation de comptes,
- paramétrage des seuils ou messages,
- gestion des modèles déployés,
- consultation des logs,
- supervision des imports,
- paramétrage des exports,
- gestion des mentions légales.

### Gestion des modèles
L’administrateur doit pouvoir voir :
- version active du modèle,
- date de déploiement,
- type de modèle,
- métriques de référence,
- fichier associé,
- possibilité de changer de version si prévu.

---

## 9.14 Module Journalisation / Audit

### Objectif
Garantir une traçabilité complète.

### Actions à journaliser
- connexion / déconnexion,
- création d’analyse,
- modification de formulaire,
- lancement de prédiction,
- génération de rapport,
- export de données,
- suppression,
- changement de paramètres,
- changement de modèle,
- erreurs techniques.

### Données de log
- date / heure
- utilisateur
- action
- ressource concernée
- résultat de l’action
- adresse IP si web

---

## 9.15 Module Notifications

### Fonctionnalités possibles
- succès de prédiction,
- erreur de saisie,
- import terminé,
- rapport généré,
- session expirée,
- alerte si prédiction de risque élevé,
- notification admin en cas d’erreur système.

---

# 10. Parcours utilisateur

---

## 10.1 Parcours prédiction unitaire
1. Connexion
2. Accès tableau de bord
3. Nouvelle analyse
4. Remplissage formulaire patient
5. Validation du formulaire
6. Lancement de la prédiction
7. Affichage du niveau de risque
8. Consultation de l’explication
9. Enregistrement de l’analyse
10. Génération du rapport
11. Consultation ultérieure dans l’historique

---

## 10.2 Parcours import en lot
1. Connexion
2. Accès module import
3. Upload du fichier
4. Validation des colonnes
5. Aperçu des données
6. Correction ou rejet des lignes invalides
7. Lancement de l’analyse lot
8. Visualisation des résultats
9. Export du fichier enrichi
10. Archivage dans l’historique

---

## 10.3 Parcours consultation historique
1. Connexion
2. Ouverture historique
3. Filtrage par période ou niveau
4. Sélection d’une analyse
5. Consultation détails
6. Téléchargement du rapport
7. Export ou archivage

---

# 11. Écrans de l’application

---

## 11.1 Écran Connexion
Contient :
- identifiant
- mot de passe
- bouton connexion
- lien mot de passe oublié

## 11.2 Écran Accueil / Dashboard
Contient :
- KPI
- dernières analyses
- graphiques de synthèse
- raccourcis d’actions

## 11.3 Écran Nouvelle analyse
Contient :
- création dossier
- choix saisie manuelle / import

## 11.4 Écran Formulaire patient
Contient :
- sections de saisie
- validation
- boutons d’action

## 11.5 Écran Résultat
Contient :
- prédiction
- probabilités
- interprétation
- actions export / rapport

## 11.6 Écran Historique
Contient :
- tableau de résultats
- filtres
- pagination
- actions

## 11.7 Écran Rapport
Contient :
- aperçu rapport
- téléchargement

## 11.8 Écran Administration
Contient :
- comptes utilisateurs
- rôles
- logs
- modèle actif
- paramètres

---

# 12. Données manipulées par l’application

---

## 12.1 Entité Utilisateur
- id
- nom
- prénom
- email
- rôle
- mot de passe hashé
- statut
- date création
- dernière connexion

## 12.2 Entité Analyse
- id analyse
- id utilisateur
- date création
- date traitement
- statut
- type analyse
- source
- modèle utilisé
- résultat principal
- commentaire

## 12.3 Entité Patient / Dossier
- id dossier
- code patient
- données d’entrée du modèle
- métadonnées

## 12.4 Entité Résultat
- id résultat
- id analyse
- classe prédite
- probabilité low
- probabilité medium
- probabilité high
- explication
- date de prédiction

## 12.5 Entité Rapport
- id rapport
- id analyse
- format
- date génération
- chemin fichier

## 12.6 Entité Log
- id log
- utilisateur
- action
- date
- détail
- statut

---

# 13. Exigences UI/UX

L’application doit être :
- claire,
- professionnelle,
- simple à utiliser,
- responsive,
- lisible par des non-techniciens.

### Exigences ergonomiques
- navigation latérale ou menu clair,
- boutons d’action visibles,
- formulaires bien découpés,
- messages de validation compréhensibles,
- couleurs cohérentes pour les niveaux de risque,
- accessibilité minimale (contraste, tailles de police).

---

# 14. Exigences non fonctionnelles

---

## 14.1 Performance
- chargement des pages rapide,
- prédiction unitaire < 3 secondes idéalement,
- import lot optimisé,
- historique paginé.

## 14.2 Sécurité
- authentification obligatoire,
- mots de passe hashés,
- gestion des permissions,
- chiffrement des échanges si web,
- protection contre accès non autorisés,
- journalisation.

## 14.3 Disponibilité
- application stable,
- reprise après erreur,
- sauvegarde des données.

## 14.4 Confidentialité
- respect de la confidentialité patient,
- possibilité d’anonymisation,
- accès limité selon rôle.

## 14.5 Maintenabilité
- architecture modulaire,
- code documenté,
- séparation front/back,
- configuration centralisée.

## 14.6 Scalabilité
- possibilité d’ajouter de nouveaux modèles,
- possibilité d’ajouter de nouveaux rapports,
- possibilité d’ajouter de nouveaux champs ou workflows.

---

# 15. Règles métier

1. Toute prédiction doit être associée à une analyse enregistrée.
2. Une analyse peut être en brouillon avant validation.
3. Une prédiction ne peut être lancée que si tous les champs requis sont valides.
4. Les résultats doivent toujours être historisés.
5. Le rapport doit mentionner la version du modèle.
6. Les exports doivent être réservés aux profils autorisés.
7. Une analyse archivée ne peut plus être modifiée sauf droit admin.
8. Le résultat affiché est une aide à la décision et non un diagnostic définitif.
9. Les actions sensibles doivent être journalisées.
10. Les données d’entrée doivent rester cohérentes avec le schéma du modèle.

---

# 16. Mentions et avertissements applicatifs

L’application doit intégrer des mentions visibles indiquant que :
- la prédiction est issue d’un modèle statistique / machine learning,
- elle constitue une aide à l’évaluation du risque,
- elle ne remplace pas une décision médicale,
- l’interprétation finale revient au professionnel compétent.

---

# 17. Critères d’acceptation fonctionnels

L’application sera acceptée si :

- un utilisateur peut se connecter ;
- il peut créer une analyse ;
- il peut remplir un formulaire complet ;
- il peut lancer une prédiction ;
- le niveau de risque s’affiche clairement ;
- l’analyse est enregistrée dans l’historique ;
- il peut rechercher une ancienne analyse ;
- il peut générer un rapport PDF ;
- il peut exporter les résultats ;
- un administrateur peut gérer les utilisateurs ;
- les actions sont tracées.

---

# 18. Livrables attendus

## Livrables applicatifs
- application fonctionnelle
- base de données
- intégration du modèle
- système de rapports
- module historique
- module administration

## Livrables documentaires
- cahier des charges
- documentation utilisateur
- documentation technique
- guide d’installation
- manuel d’administration
- plan de tests

## Livrables techniques
- code source frontend/backend
- scripts de déploiement
- fichier de configuration
- structure base de données

---

# 19. Backlog fonctionnel synthétique

### Epic 1 : Authentification
- US01 connexion utilisateur
- US02 gestion mot de passe
- US03 gestion rôles

### Epic 2 : Analyse individuelle
- US04 créer une analyse
- US05 saisir les données patient
- US06 enregistrer brouillon
- US07 lancer prédiction
- US08 afficher résultat

### Epic 3 : Analyse en lot
- US09 importer fichier
- US10 contrôler le fichier
- US11 analyser en lot
- US12 exporter résultats lot

### Epic 4 : Historique
- US13 consulter historique
- US14 filtrer historique
- US15 voir détail analyse

### Epic 5 : Rapports
- US16 générer PDF
- US17 exporter CSV/Excel
- US18 imprimer rapport

### Epic 6 : Administration
- US19 gérer utilisateurs
- US20 gérer paramètres
- US21 consulter logs
- US22 gérer version modèle

---

# 20. Recommandation d’architecture réelle

Pour une vraie app professionnelle, je recommande :

## Frontend
- React ou Vue.js

## Backend
- FastAPI

## Base de données
- PostgreSQL

## Moteur ML
- service Python séparé ou intégré backend

## Reporting
- génération PDF côté backend

## Sécurité
- JWT + RBAC (role-based access control)

## Déploiement
- Docker + Nginx + serveur cloud ou local

---

# 21. Modules visibles dans le menu principal

Le menu principal de l’application pourrait contenir :

- Accueil
- Nouvelle analyse
- Formulaire patient
- Import en lot
- Résultats
- Historique
- Rapports
- Exports
- Tableau de bord
- Administration
- Journal d’activité
- Paramètres
- Aide

---

# 22. Exemple de structure des pages

```text
Accueil
 ├── KPI
 ├── Activité récente
 └── Actions rapides

Analyses
 ├── Nouvelle analyse
 ├── Saisie manuelle
 ├── Import lot
 └── Résultats

Historique
 ├── Liste
 ├── Recherche avancée
 └── Détail analyse

Rapports
 ├── Rapport individuel
 ├── Rapport consolidé
 └── Exports

Administration
 ├── Utilisateurs
 ├── Rôles
 ├── Logs
 ├── Modèle actif
 └── Paramètres
```

---

# 23. Conclusion

Cette application doit être conçue comme une **véritable plateforme métier de prédiction du risque de cancer**, et non comme un simple outil de démonstration.

Elle devra intégrer :

- un **formulaire complet**,
- un **moteur de prédiction opérationnel**,
- un **historique détaillé**,
- des **rapports téléchargeables**,
- des **exports**,
- une **administration**,
- des **tableaux de bord**,
- une **traçabilité complète**,
- et une **expérience utilisateur professionnelle**.

---

Si tu veux, je peux maintenant te faire la **suite directement**, au choix :

### 1. le **cahier des charges ultra professionnel en version formelle client**
### 2. les **fonctionnalités détaillées écran par écran**
### 3. les **User Stories complètes avec critères d’acceptation**
### 4. le **schéma de base de données complet**
### 5. l’**arborescence complète de l’application**
### 6. le **wireframe textuel de toutes les pages**
### 7. le **document SRS complet** comme pour un vrai projet logiciel
### 8. le **prompt complet pour générer l’app avec une IA ou un développeur**

Je te conseille la suite suivante :  
**“fais-moi maintenant le cahier des charges fonctionnel détaillé écran par écran + schéma base de données + user stories”**  
et je te le fais complet.