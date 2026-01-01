📊 DASHBOARD COMPLET - Guide d'Utilisation
================================================

## 📁 Structure du Projet

```
projet_v6/
├── 1_data/              # Étape 1: Préparation des données
│   └── prepare_data.py
├── 2_graph/             # Étape 2: Construction des graphes
│   └── graph_builder.py
├── 3_gnn/               # Étape 3: Modèle GNN et propagation
│   └── gnn_model.py
├── 4_analysis/          # Étape 4: Analyse des chemins critiques
│   └── critical_paths.py
├── 5_dashboard/         # 🆕 Étape 5: Interface interactive
│   ├── app.py           # Application Dash principale
│   ├── start.py         # Script de démarrage
│   ├── generate_kpis.py # Génération des indicateurs
│   ├── export_visualizations.py
│   └── README.md
├── results/             # Résultats et données
│   ├── analysis_summary.csv     # Résumé 50 topologies
│   ├── critical_paths.json      # Chemins avec multi-métriques
│   ├── kpi_indicators.json      # Indicateurs clés
│   ├── kpi_report.txt           # Rapport textuel
│   └── visualizations/          # 4 graphiques PNG
│       ├── 01_complete_analysis.png
│       ├── 02_detailed_statistics.png
│       ├── 03_top10_topologies.png
│       └── 04_correlations_trends.png
├── data_v2/             # Données brutes (50 fichiers GraphML)
├── main.py              # Pipeline principal
└── RESULTATS_MODELE.txt # Rapport complet
```

## 🚀 Démarrage Rapide

### Option 1: Script Automatique (Recommandé)
```bash
cd projet_v6/5_dashboard
python start.py
```

### Option 2: Lancement Direct
```bash
cd projet_v6/5_dashboard
python app.py
```

Le dashboard s'ouvre automatiquement à **http://127.0.0.1:8050**

## 📊 Onglets Disponibles

### 1️⃣ Vue d'ensemble
- **Graphique Amplification**: Distribution de la différence GNN - Statique
- **Graphique Risques**: Box plot comparatif statique vs GNN
- **Graphique Nœuds vs Risque**: Scatter plot avec taille basée sur nombre de liens
- **KPI Cards**: 
  - 50 topologies analysées
  - 6.1% amplification moyenne
  - 0% saturation
  - ★★★★☆ score cohérence

### 2️⃣ Analyse Détaillée
- **Sélecteur de Topologie**: Choisir une topologie parmi 50
- **Indicateurs Topologie**: Nœuds, liens, risques, amplification
- **Chemins Critiques**: Top 3 chemins identifiés avec leurs risques
- **Graphique Chemins**: Bar chart comparant mean_risk vs max_risk

### 3️⃣ Statistiques
- **Box Plot Statistique**: Comparaison détaillée statique/GNN
- **Corrélation**: Scatter plot risque statique vs GNN
- **Histogramme Comparatif**: Overlay histogramme risques moyens

### 4️⃣ Rapports KPI
- **Overview**: Total topologies, nœuds, liens, chemins critiques
- **Amplification**: Moyenne, médiane, écart-type, plage
- **Risque Max GNN**: Distribution et intervalle
- **Qualité du Modèle**: Saturation, discrimination, stabilité

### 5️⃣ Visualisations (Static)
- 4 graphiques PNG haute résolution exportés
- Utilisables dans rapports et présentations

## 🎛️ Filtres Interactifs

### Sélectionner Topologie
- **Type**: Dropdown menu
- **Effet**: Met à jour tous les graphiques de détail
- **Valeur par défaut**: Aarnet

### Métrique de Chemin
- **Options**:
  - ✅ Mean Risk (RECOMMANDÉ) - Non biaisé par longueur
  - Max Risk (Bottleneck) - Maillon le plus faible
  - Sum Risk (Legacy) - Somme cumulative
  - Weighted Risk - Compromis paramétré
  - Product Risk - Modèle probabiliste
- **Effet**: Change la colonne affichée dans le tableau

### Nombre de Chemins
- **Range**: 1 à 10 chemins
- **Défaut**: 3
- **Effet**: Affiche top-k chemins critiques

## 📈 Données Disponibles

### analysis_summary.csv (52 lignes)
```
topology,n_nodes,n_edges,n_critical_paths,
max_static_risk,max_gnn_risk,
mean_static_risk,mean_gnn_risk,
avg_difference
```
- **Usage**: Comparaison globale 50 topologies
- **Format**: CSV standard (Excel compatible)

### critical_paths.json
```json
{
  "Aarnet": [
    {
      "path": [0, 3, 16, 14, 12, 15, 18],
      "mean_risk": 0.448,
      "max_risk": 0.745,
      "sum_risk": 3.137,
      "weighted_risk": 1.186,
      "product_risk": 0.988,
      "length": 7
    }
  ]
}
```
- **Usage**: Détails chemins critiques avec 5 métriques
- **Format**: JSON hierarchique

### kpi_indicators.json
- **Contenu**: Tous les KPIs structurés (JSON)
- **Usage**: Intégration dans autres systèmes
- **Sections**:
  - overview
  - amplification_metrics
  - max_gnn_risk
  - mean_gnn_risk
  - comparison_metrics
  - topology_sizes
  - top_amplifications
  - top_risks
  - model_quality

### kpi_report.txt
- **Format**: Texte structuré avec emojis
- **Sections**: 10 sections détaillées
- **Usage**: Lecture rapide, impression papier

## 🎨 Interface Design

### Couleurs
- **Primary**: #3498db (Bleu) - Données principales
- **Success**: #27ae60 (Vert) - Bon (amplification contrôlée)
- **Warning**: #f39c12 (Orange) - À surveiller
- **Danger**: #e74c3c (Rouge) - Critique
- **Secondary**: #95a5a6 (Gris) - Données statiques

### Layout Responsive
- **Desktop**: Grille 4 colonnes pour KPI cards
- **Tablet**: Ajustement automatique
- **Mobile**: Stacking vertical

### Interactivité
- ✅ Hover sur points: Affiche détails topologie
- ✅ Sélectionneur: Mise à jour dynamique
- ✅ Curseur: Smooth animation
- ✅ Export: Click droit pour sauvegarder PNG

## 📊 Génération des Artefacts

### KPIs (generate_kpis.py)
```bash
python generate_kpis.py
```
- **Entrées**: analysis_summary.csv, critical_paths.json
- **Sorties**: 
  - kpi_indicators.json (machine-readable)
  - kpi_report.txt (human-readable)
- **Temps**: ~2 secondes

### Visualisations (export_visualizations.py)
```bash
python export_visualizations.py
```
- **Entrées**: analysis_summary.csv
- **Sorties**: 4 fichiers PNG haute résolution
- **Temps**: ~3 secondes
- **Résolution**: 1200x800 pixels chacun

## 🔧 Configuration

### Port du Dashboard
Par défaut: **8050**
Pour changer: Éditer `app.py` ligne 370
```python
app.run(debug=False, host='127.0.0.1', port=YOUR_PORT)
```

### Dossiers des Résultats
Par défaut: `../results/`
Implicite depuis `5_dashboard/`

### Nombre de Chemins Affichés
Par défaut: Top 3
Modifiable via slider dans interface (1-10)

## 🚨 Troubleshooting

### Port 8050 déjà utilisé
```bash
# Windows
netstat -ano | findstr :8050
taskkill /PID YOUR_PID /F
```

### Module non trouvé (dash, plotly, seaborn)
```bash
pip install dash plotly pandas seaborn
```

### Navigateur n'ouvre pas automatiquement
- Accédez manuellement à http://127.0.0.1:8050
- Assurez-vous d'avoir un navigateur par défaut configuré

### Images PNG non visibles
- Vérifier que `results/visualizations/` existe
- Réexécuter `python export_visualizations.py`

## 📈 Métriques Expliquées

### Mean Risk (RECOMMANDÉ)
- **Définition**: Moyenne des risques des liens du chemin
- **Avantage**: Comparable entre chemins de longueurs différentes
- **Cas d'usage**: Priorisation, comparaisons équitables
- **Formule**: Σ risk_i / n_liens

### Max Risk (Bottleneck)
- **Définition**: Risque maximum du chemin
- **Avantage**: Identifie le point critique
- **Cas d'usage**: Maintenance du lien le plus critique
- **Formule**: max(risk_i)

### Sum Risk (Legacy)
- **Définition**: Somme cumulative des risques
- **Avantage**: Probabilité cumulative
- **Cas d'usage**: Risque total du chemin
- **Formule**: Σ risk_i

### Weighted Risk
- **Définition**: Somme / √longueur
- **Avantage**: Compromis entre somme et moyenne
- **Cas d'usage**: Quand longueur importe partiellement

### Product Risk
- **Définition**: 1 - Π(1 - risk_i) (fiabilité)
- **Avantage**: Modèle probabiliste rigoureux
- **Cas d'usage**: Analyse de disponibilité

## 📱 Accès à Distance

Pour accéder au dashboard depuis autre machine:
```python
# Dans app.py
app.run(debug=False, host='0.0.0.0', port=8050)
```
Puis accédez à: `http://YOUR_IP:8050`

**Attention**: Utilisez un firewall ou VPN en production!

## 📄 Export & Intégration

### Télécharger Données CSV
- Clic droit sur graphique → Download plot as PNG
- CSV disponible dans `results/analysis_summary.csv`

### Intégrer dans Rapport
- Copier/coller images PNG depuis visualisations
- JSON importable dans d'autres outils
- Texte rapport lisible dans documents

### API Externe
- JSON accessible via requête HTTP
- Possibilité d'ajouter routes REST
- Extensible avec webhooks

## 🎓 Cas d'Utilisation

### 1. Priorisation Maintenance
1. Aller à "Analyse Détaillée"
2. Sélectionner topologie critique (AsnetAm, Airtel)
3. Vérifier top 3 chemins
4. Prioriser maintenance sur max_risk liens

### 2. Validation Modèle
1. Aller à "Statistiques"
2. Vérifier corrélation statique/GNN (y=x)
3. Observer amplification moderate (6.1%)
4. Confirmer pas de saturation (0%)

### 3. Présentation Exécutive
1. Afficher "Vue d'ensemble"
2. Souligner 4 KPI cards
3. Montrer stabilité (distribution tight)
4. Inclure graphiques "Visualisations"

### 4. Analyse Comparative
1. Comparer 2 topologies
2. Vérifier si corrélation linéaire
3. Identifier outliers
4. Analyser facteurs de risque

## 🔐 Sécurité

- Dashboard en localhost (127.0.0.1) par défaut
- Pas d'authentification requise
- Données synthétiques (pas sensibles)
- En production: Utiliser SSL/TLS + Auth

## 📞 Support

Pour problèmes ou améliorations:
1. Vérifier troubleshooting ci-dessus
2. Consulter logs dans terminal
3. Vérifier fichiers résultats existent
4. Réexécuter pipeline complet si nécessaire

---

**Version**: 2.0 - Multi-Métriques avec Validation
**Date**: Janvier 2026
**Dernière mise à jour**: 01/01/2026
