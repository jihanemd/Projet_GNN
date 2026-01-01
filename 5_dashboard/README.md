# 📊 Dashboard Interactif - Chemins Critiques

## Vue d'ensemble

Le dashboard permet d'explorer interactivement les résultats de l'analyse des chemins critiques sur 50 topologies réseau.

## Fonctionnalités

### 1. **Indicateurs Clés (KPIs)**
- Amplification moyenne GNN-Statique
- Risque maximum et moyen
- Nombre de topologies et liens analysés
- Statistiques en temps réel

### 2. **Graphiques Interactifs**
- **Scatter Plot**: Comparaison Statique vs GNN (taille = nb nœuds)
- **Histogramme**: Distribution des amplifications/risques
- **Bar Chart**: Détails par topologie sélectionnée
- **Tableau**: Chemins critiques avec multi-métriques

### 3. **Filtres Dynamiques**
- Sélection de topologie
- Choix de métrique (mean/max/sum/weighted/product)
- Nombre de chemins à afficher

### 4. **Visualisations Statiques (PNG)**
- Analyse complète (4 sous-graphes)
- Statistiques détaillées
- Top 10 topologies
- Corrélations et tendances

### 5. **Indicateurs (JSON + TXT)**
- Métriques au format JSON pour intégration
- Rapport textuel formaté

## Installation

```bash
# Dépendances requises
pip install dash plotly pandas matplotlib seaborn numpy

# OU directement
cd projet_v6
pip install -r requirements_dashboard.txt
```

## Utilisation

### Lancer le dashboard complet (recommandé)
```bash
python 5_dashboard/start.py
```

Cela va:
1. Générer les KPIs
2. Créer les visualisations statiques
3. Lancer le dashboard interactif sur http://127.0.0.1:8050

### Lancer uniquement le dashboard
```bash
python 5_dashboard/app.py
```

### Générer les visualisations seul
```bash
python 5_dashboard/export_visualizations.py
```

### Générer les KPIs seul
```bash
python 5_dashboard/generate_kpis.py
```

## Structure des fichiers

```
5_dashboard/
├── app.py                     # Application Dash principale
├── export_visualizations.py   # Générateur de graphiques statiques
├── generate_kpis.py          # Générateur d'indicateurs clés
├── start.py                  # Script de démarrage complet
└── README.md                 # Cette documentation

results/
├── analysis_summary.csv           # Données 50 topologies
├── critical_paths.json            # Chemins critiques (5 métriques)
├── kpi_indicators.json            # KPIs structurés
├── kpi_report.txt                 # Rapport texte
└── visualizations/
    ├── 01_complete_analysis.png
    ├── 02_detailed_statistics.png
    ├── 03_top10_topologies.png
    └── 04_correlations_trends.png
```

## Guide d'utilisation du dashboard

### Page 1: Vue d'ensemble
- **KPIs en haut**: Métriques globales principales
- **Filtres**: Sélectionnez topologie et métrique
- **Scatter**: Explorez la distribution des risques

### Page 2: Analyse détaillée
- **Histogramme**: Distribution des métriques
- **Bar Chart**: Comparaison topologie vs globale
- **Tableau**: Chemins critiques triés

### Conseils d'exploration

1. **Identifier les topologies critiques**:
   - Filtrez par métrique "Mean Risk"
   - Les couleurs rouges = haute criticité

2. **Comparer longueur vs risque**:
   - Tableau "Chemins Critiques"
   - Comparez colonnes "Longueur" vs "Métrique Choisie"

3. **Analyser les tendances**:
   - Scatter plot montre corrélation taille-risque
   - Ligne rouge = pas d'amplification (référence)

## Métriques disponibles

### Pour les chemins:
- **mean_risk**: Risque moyen (NON biaisé par longueur) ✅ **RECOMMANDÉ**
- **max_risk**: Risque maximum (bottleneck)
- **sum_risk**: Somme des risques (biais longueur)
- **weighted_risk**: Somme pondérée par √longueur
- **product_risk**: Modèle probabiliste

### Pour les topologies:
- **Amplification**: Différence GNN - Statique
- **Max GNN Risk**: Risque maximum dans la topologie
- **Mean GNN Risk**: Risque moyen de tous les liens

## Performance

- **Temps de chargement**: < 2 secondes
- **Responsivité**: < 100ms par interaction
- **Mémoire**: ~150 MB (données + visualisations)

## Dépannage

### Le dashboard ne démarre pas
```bash
# Vérifiez les dépendances
pip list | grep dash

# Réinstallez si nécessaire
pip install --upgrade dash plotly
```

### Erreur "Port 8050 already in use"
```bash
# Lancez sur un port différent (dans app.py):
app.run_server(debug=True, port=8051)
```

### Graphiques vides
```bash
# Vérifiez que analysis_summary.csv existe
ls results/analysis_summary.csv

# Relancez le pipeline principal
python main.py
```

## Export des données

Tous les fichiers générés peuvent être exportés:

```python
# Charger les KPIs
import json
with open('results/kpi_indicators.json') as f:
    kpis = json.load(f)

# Charger les chemins
with open('results/critical_paths.json') as f:
    paths = json.load(f)

# Charger les résumés
import pandas as pd
df = pd.read_csv('results/analysis_summary.csv')
```

## Personnalisation

### Modifier les couleurs
Éditer les variables `COLOR_*` dans `app.py`:
```python
COLOR_STATIC = '#1f77b4'
COLOR_GNN = '#ff7f0e'
COLOR_GOOD = '#2ecc71'
```

### Ajouter de nouveaux graphiques
Ajouter un `dcc.Graph()` dans le `app.layout` et son callback `@app.callback()`

### Changer le port par défaut
Dans `start.py` ou `app.py`:
```python
app.run_server(port=8080)  # Au lieu de 8050
```

## Support

Pour plus d'informations:
- Voir `RESULTATS_MODELE.txt` pour la méthodologie
- Voir `critical_paths.json` pour les données brutes
- Voir `kpi_report.txt` pour le rapport détaillé

---

**Version**: 2.0 - Multi-Métriques  
**Dernière mise à jour**: 01/01/2026
