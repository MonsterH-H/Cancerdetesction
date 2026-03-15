ADDENDUM AU CAHIER DES CHARGES
Exigences de réalisme, de persistance et de fonctionnement 100% connecté
1. Principe fondamental du projet
L’application doit être conçue comme une application métier réelle, destinée à fonctionner avec :

une base de données opérationnelle,
un backend applicatif,
un modèle réellement chargé,
des formulaires réellement persistés,
un historique réellement stocké,
des rapports générés à partir des vraies données enregistrées,
des résultats réellement issus du moteur de prédiction,
des écrans alimentés exclusivement par des données réelles provenant du système.
Aucune fonctionnalité ne doit reposer sur des données fictives, du mock, du hardcode, du texte de démonstration ou des simulations visuelles non connectées.

2. Exigence absolue : aucune simulation
2.1 Interdictions
Il est strictement interdit d’intégrer dans l’application finale :

des exemples de patients fictifs,
des listes statiques non reliées à la base,
des historiques simulés,
des tableaux remplis à la main,
des rapports générés avec du faux contenu,
des résultats prédictifs factices,
des dashboards affichant des chiffres simulés,
des statuts ou métriques calculés hors des données stockées,
des boutons non fonctionnels,
des exports “de démonstration”.
2.2 Obligation
Chaque donnée affichée dans l’interface doit provenir :

soit de la base de données,
soit d’un calcul temps réel sur des données stockées,
soit du modèle chargé réellement côté backend,
soit d’un fichier effectivement importé et validé.
3. Exigence de connexion intégrale à la base de données
3.1 Règle générale
Toutes les entités manipulées par l’application doivent être persistées en base de données.

Cela inclut obligatoirement :

utilisateurs,
rôles,
sessions ou traces de connexion,
dossiers d’analyse,
formulaires saisis,
données patient importées ou saisies,
résultats de prédiction,
probabilités retournées,
versions de modèles,
rapports générés,
exports effectués,
historiques,
logs techniques,
journaux métier,
erreurs fonctionnelles.
3.2 Aucune mémoire temporaire comme source métier
Les données ne doivent pas être conservées uniquement :

dans la session navigateur,
dans des variables mémoire,
dans un état frontend,
dans un cache non persisté,
si elles ont une valeur métier.
Toute donnée métier doit être enregistrée de manière durable.

4. Exigence de cohérence entre écrans et base
Chaque écran de l’application doit afficher exclusivement des données récupérées dynamiquement depuis la base ou calculées à partir d’elle.

Exemples obligatoires
Le tableau de bord doit lire le nombre réel d’analyses enregistrées.
L’historique doit afficher les vraies analyses persistées.
Le détail d’une analyse doit reprendre les vraies données saisies au moment de l’exécution.
Le rapport PDF doit être généré à partir des données stockées dans la base.
Le niveau de risque affiché doit être celui réellement calculé puis enregistré.
Le graphique de répartition des risques doit être calculé à partir des résultats réellement existants.
5. Exigence de persistance complète des formulaires
5.1 Formulaires obligatoirement persistés
Tout formulaire métier doit être relié à la base de données.

Cela concerne notamment :

formulaire de création d’analyse,
formulaire de saisie patient,
formulaire d’import,
formulaire d’administration,
formulaire de recherche enregistrée si prévu,
formulaire de génération de rapport.
5.2 Enregistrement des brouillons
Si le mode brouillon existe :

le brouillon doit être enregistré en base ;
il doit être récupérable ;
il doit conserver les valeurs déjà saisies ;
il doit avoir un statut spécifique.
5.3 Historisation des modifications
Si une donnée métier est modifiée après création :

la modification doit être tracée ;
l’auteur et la date doivent être conservés ;
idéalement un mécanisme de versionnage ou d’audit doit être prévu.
6. Exigence de prédiction réelle uniquement
6.1 Le moteur de prédiction doit être réellement intégré
Le résultat de prédiction ne doit jamais être simulé.

Chaque prédiction doit :

récupérer les données d’entrée réelles du formulaire ou du fichier importé ;
les transmettre au pipeline du modèle réellement chargé ;
récupérer la classe prédite réelle ;
récupérer les probabilités réelles si disponibles ;
stocker le résultat en base ;
afficher ce résultat dans l’interface.
6.2 Données minimales à enregistrer pour chaque prédiction
identifiant analyse
identifiant dossier
données d’entrée
date/heure d’exécution
modèle utilisé
version du modèle
classe prédite
probabilité par classe
utilisateur initiateur
statut de succès/échec
message d’erreur si applicable
7. Exigence de reporting réel
7.1 Rapports générés uniquement à partir de données réelles
Tous les rapports doivent être produits dynamiquement depuis :

les données saisies ou importées,
les résultats enregistrés,
les métadonnées réelles du système,
la version du modèle effectivement utilisée.
7.2 Contenu interdit dans les rapports
données fictives,
exemples préremplis,
nom patient générique non lié à la base,
résultats “exemple”,
commentaires statiques mensongers.
7.3 Contenu obligatoire
Chaque rapport doit contenir au minimum :

identifiant unique du rapport,
identifiant de l’analyse liée,
date de génération,
utilisateur générateur,
données réelles du dossier,
résultat réel de prédiction,
version réelle du modèle,
mention de non-substitution au jugement médical,
empreinte ou référence du rapport généré.
8. Exigence de tableau de bord réel
8.1 Les KPI doivent être calculés en base
Les indicateurs affichés dans le dashboard doivent être construits à partir de requêtes réelles sur la base de données.

Exemples
nombre total d’analyses = COUNT en base
nombre d’analyses du jour = filtre date
taux de risque élevé = proportion des analyses avec classe “High”
dernières analyses = tri réel par date
analyses par utilisateur = agrégation réelle
8.2 Aucune carte statique
Il est interdit d’afficher :

“125 analyses” en dur,
“12 nouveaux cas” codé à la main,
graphiques alimentés par des tableaux statiques.
9. Exigence d’historique réel et complet
9.1 Historique non simulé
Le module historique doit être totalement alimenté par la base de données.

9.2 Chaque événement important doit créer une trace réelle
Au minimum :

création d’analyse
modification
soumission
prédiction
génération de rapport
export
archivage
suppression
connexion
9.3 Consultation historique
L’utilisateur doit pouvoir :

retrouver une analyse existante,
ouvrir son détail réel,
voir ses données réelles,
voir son résultat réel,
télécharger son rapport réel.
10. Exigence d’intégrité des données
10.1 Cohérence transactionnelle
Les opérations critiques doivent être transactionnelles.

Exemple :

si une analyse est lancée,
alors les données d’entrée, le résultat, le log et l’état de l’analyse doivent être cohérents ;
en cas d’erreur, rollback ou état d’erreur maîtrisé.
10.2 Contraintes base de données
La base doit prévoir :

clés primaires,
clés étrangères,
contraintes d’unicité,
contrôles de nullité,
contraintes de type,
index sur les champs de recherche,
horodatage de création et modification.
11. Exigence d’architecture concrète
L’application doit reposer sur une architecture réelle et exploitable, par exemple :

Backend
API REST ou backend MVC
gestion des règles métier
connexion au modèle
connexion à la base
génération de rapports
journalisation
Base de données
PostgreSQL recommandé
schéma relationnel propre
tables normalisées
gestion des audits
Frontend
interface reliée au backend par API
récupération dynamique des données
formulaires connectés
pages synchronisées avec la base
Stockage documentaire
rapports PDF réellement générés et référencés
stockage fichier avec chemin persisté en base
12. Exigence de suppression du “fake UX”
L’interface ne doit pas contenir d’éléments purement décoratifs simulant un comportement.

Interdits
faux boutons “Télécharger” sans backend
faux badge “Analyse réussie” sans persistance
faux indicateur de progression non lié au traitement
faux historique UI-only
cartes remplies avec données d’exemple
Exigence
Tout composant cliquable doit produire une action réelle, contrôlée et persistée si nécessaire.

13. Exigence d’exactitude des données affichées
Les données affichées à l’écran doivent toujours refléter l’état réel de la base au moment de la consultation.

Cela implique :

rechargement après action,
messages de confirmation réels,
gestion d’erreur réelle,
synchronisation entre backend et interface,
pas de divergence entre vue et persistance.
14. Exigence d’import réel
Le module d’import doit :

stocker le fichier importé ou son empreinte,
enregistrer le lot en base,
enregistrer chaque ligne traitée,
enregistrer le statut de chaque ligne,
enregistrer les erreurs réelles de validation,
produire un résultat de traitement consultable,
lier chaque ligne importée à une prédiction réelle si elle est analysée.
Aucun import ne doit être “accepté visuellement” sans traitement réel côté backend.

15. Exigence de traçabilité complète
Chaque action majeure doit laisser une trace exploitable.

Traces obligatoires
qui a fait l’action
quand
sur quelle entité
avec quel résultat
depuis quelle interface / module si possible
quelle version du modèle était utilisée
Cette exigence vaut pour :

création
lecture sensible
modification
suppression
export
connexion
prédiction
génération rapport
16. Exigence de versionnement réel du modèle
Le système doit stocker en base la référence du modèle réellement utilisé pour chaque prédiction.

Données minimales
id modèle
nom du modèle
version
date de déploiement
format du fichier
chemin ou référence
statut actif/inactif
Règle
Une prédiction déjà réalisée doit rester liée à la version exacte du modèle qui l’a produite.

17. Exigence de production et non de démonstration
Le projet doit être pensé comme un produit réellement exploitable et non comme une preuve de concept.

Cela implique :

composants finalisés,
workflows réels,
données persistées,
erreurs gérées,
architecture claire,
base de données structurée,
droits utilisateurs réels,
vraie traçabilité,
vraie logique d’exploitation.
18. Exigence de concret dans le cahier des charges
Le cahier des charges doit être interprété de la manière suivante :

chaque écran correspond à une vraie page ou vue ;
chaque bouton correspond à une vraie action backend ;
chaque tableau lit de vraies données ;
chaque métrique est calculée ;
chaque rapport est généré ;
chaque historique est persisté ;
chaque formulaire est stocké ;
chaque prédiction est exécutée réellement ;
chaque export produit un vrai fichier.
19. Formulation à intégrer dans le cahier des charges officiel
Tu peux intégrer cette clause telle quelle dans le document final :

Clause de fonctionnement réel et de persistance intégrale
L’application devra être développée sans recours à des contenus simulés, fictifs, statiques ou non connectés.
Toute donnée affichée, modifiée, exportée, historisée ou exploitée dans l’application devra provenir d’une source réelle : base de données, moteur de prédiction intégré, fichier importé et validé, ou calcul métier effectué sur des données persistées.
Aucun écran, tableau, indicateur, historique, rapport, résultat ou formulaire ne devra être implémenté sous forme de démonstration visuelle non reliée au système d’information.
Toute fonctionnalité décrite dans ce cahier des charges devra être concrètement opérationnelle, connectée au backend et à la base de données, persistée si nécessaire, et exploitable dans un contexte réel d’utilisation.

20. Complément à ajouter aux critères d’acceptation
L’application ne pourra être validée que si :

aucun écran n’utilise de données factices ;
tous les formulaires enregistrent réellement en base ;
toutes les listes sont alimentées dynamiquement ;
les résultats sont issus du vrai modèle chargé ;
les rapports sont générés à partir des vraies données stockées ;
les exports correspondent aux données réellement filtrées ;
les dashboards sont calculés à partir de la base ;
l’historique est réellement persistant ;
les actions sont journalisées ;
les données restent cohérentes d’un écran à l’autre.
Si tu veux, je peux maintenant te faire la version finale fusionnée, c’est-à-dire :

un cahier des charges complet professionnel unique, déjà réécrit avec :
modules de vraie app,
formulaires,
historique,
rapports,
dashboard,
administration,
sécurité,
base de données,
et la clause “aucune simulation / tout connecté à la BD” intégrée partout.
Si tu veux, je peux te livrer ça sous forme :

1. Document final propre et structuré
2. SRS professionnel complet
3. CDC fonctionnel + technique
4. avec schéma de base de données
5. avec user stories et critères d’acceptation