# 🌐 Analyse des Chemins Critiques dans les Réseaux Internet

**Dashboard Interactif | Identification des Chemins Vulnérables | Analyse GNN**

---

## 📋 Table des Matières

- [Vue d'Ensemble](#vue-densemble)
- [Démarrage Rapide](#démarrage-rapide)
- [Caractéristiques](#caractéristiques)
- [Architecture du Projet](#architecture-du-projet)
- [Installation](#installation)
- [Utilisation](#utilisation)
- [Documentation](#documentation)
- [Résultats](#résultats)

---

## 🎯 Vue d'Ensemble

Ce projet fournit une **plateforme complète d'analyse** pour identifier les **chemins critiques** dans les réseaux Internet. Il utilise une approche combinant:

- 📊 **Analyse Statique** : Évaluation basée sur les propriétés topologiques
- 🧠 **Graph Neural Networks (GNN)** : Apprentissage profond sur les graphes
- 📈 **Métriques Multi-Perspectives** : 5 approches différentes pour évaluer le risque

### Données
- **50 topologies** Internet réelles (Abilene, Arpanet, Garr, etc.)
- **1,290 nœuds** analysés
- **1,642 liens** étudiés
- **120+ chemins critiques** identifiés

---

## 🚀 Démarrage Rapide

### Option 1: Lancer le Dashboard Complet

```bash
cd 5_dashboard
python start.py
```

**Cela va:**
1. ✅ Générer les KPI et rapports
2. ✅ Exporter les visualisations PNG
3. ✅ Lancer le dashboard interactif

### Option 2: Lancer Uniquement le Dashboard

```bash
cd 5_dashboard
python app.py
```

### Option 3: Générer les Données Seules

```bash
# Générer les KPIs
cd 5_dashboard
python generate_kpis.py

# Exporter les visualisations
python export_visualizations.py
```

### 📍 Accès au Dashboard

```
🌐 URL: http://127.0.0.1:8050
```

---

## ✨ Caractéristiques

### 📊 Dashboard Interactif (3 Onglets)

#### **Tab 1: Vue Générale**
- 📈 **Scatter Plot** : Risque Statique vs GNN avec amplification
- 📊 **Histogramme** : Distribution de l'amplification
- 🔍 **Graphique Détaillé** : Comparaison pour topologie sélectionnée

#### **Tab 2: Chemins Critiques**
- 🔴 **Tableau Dynamique** : Top K chemins avec code couleur
- 📋 **5 Métriques** : Mean, Max, Sum, Weighted, Product Risk
- 🎯 **Sélection Interactive** : Filtrer par topologie et métrique

#### **Tab 3: Distributions**
- 📦 **Box Plot** : Distribution de l'amplification
- 🎻 **Violin Plots** : Comparaison Mean vs Max Risk
- 🔥 **Heatmap** : Corrélation entre métriques

### 🎨 4 KPI Cards

```
📊 Amplification Moyenne    ⚠️  Max GNN Risk
   0.0613 ± 0.0095           0.655

📈 Mean GNN Risk           🎯 Topologies Analysées
   0.357                       50 (1,290 nœuds | 1,642 liens)
```

### 🎛️ Filtres Dynamiques

- 🌐 **Sélecteur Topologie** : 50 options avec recherche
- 📊 **Sélecteur Métrique** : 5 approches différentes
- 🔝 **Top K Slider** : Ajuster de 1 à 10 chemins

---

## 🏗️ Architecture du Projet

```
projet_v6/
├── 📁 1_data/                    # Données brutes
│   └── *.graphml                 # 50 fichiers de topologies
│
├── 📁 2_graph/                   # Construction des graphes
│   ├── graph_builder.py
│   └── graph_loader.py
│
├── 📁 3_gnn/                      # Modèle Graph Neural Network
│   └── gnn_model.py
│
├── 📁 4_analysis/                 # Analyse des chemins critiques
│   ├── critical_paths.py
│   └── path_analyzer.py
│
├── 📁 5_dashboard/                # Dashboard Interactif
│   ├── app.py                     # Application Dash (379 lignes)
│   ├── generate_kpis.py           # Génération des KPIs (223 lignes)
│   ├── export_visualizations.py   # Export PNG (150+ lignes)
│   └── start.py                   # Script de démarrage
│
├── 📁 results/                    # Résultats générés
│   ├── analysis_summary.csv       # 50 topologies × 9 métriques
│   ├── critical_paths.json        # 120+ chemins avec 5 métriques
│   ├── kpi_indicators.json        # Indicateurs machine-readable
│   ├── kpi_report.txt             # Rapport texte formaté
│   └── visualizations/
│       ├── 01_complete_analysis.png
│       ├── 02_detailed_statistics.png
│       ├── 03_top10_topologies.png
│       └── 04_correlations_trends.png
│
├── main.py                        # Pipeline complet
├── RESULTATS_MODELE.txt          # Rapport complet (500+ lignes)
├── README.md                      # Ce fichier
├── INDEX.md                       # Référence complète
└── PROJECT_SUMMARY.md             # Résumé du projet
```

---

## 💻 Installation

### Prérequis

- Python 3.8+
- pip ou conda
- 100MB d'espace disque

### Étapes

```bash
# 1. Cloner/Naviguer vers le projet
cd projet_v6

# 2. Créer un environnement virtuel
python -m venv .venv

# 3. Activer l'environnement
# Windows:
.\.venv\Scripts\Activate.ps1
# Linux/Mac:
source .venv/bin/activate

# 4. Installer les dépendances
pip install dash plotly pandas numpy networkx scikit-learn matplotlib seaborn

# 5. Lancer le pipeline complet
python main.py

# 6. Ouvrir le dashboard
cd 5_dashboard && python app.py
```

---

## 📖 Utilisation

### Via le Dashboard Web

1. **Ouvrir** : http://127.0.0.1:8050
2. **Sélectionner une topologie** : 📍 Dropdown avec 50 options
3. **Choisir une métrique** : 📊 Risque Mean (recommandé)
4. **Ajuster Top K** : 🔝 Slider 1-10 chemins
5. **Explorer les onglets** : 📊 Vue Générale | 🔴 Chemins | 📈 Distributions

### Via Python Script

```python
import pandas as pd
import json

# Charger les résultats
results_df = pd.read_csv('results/analysis_summary.csv')
with open('results/critical_paths.json') as f:
    critical_paths = json.load(f)

# Explorer les données
print(f"Topologies: {len(results_df)}")
print(f"Amplification moyenne: {results_df['avg_difference'].mean():.4f}")

# Accéder aux chemins pour une topologie
topology = 'Abilene'
paths = critical_paths[topology]
print(f"Chemins critiques ({topology}): {len(paths)}")
```

### Via CSV/JSON

```bash
# Consulter les résultats
cat results/analysis_summary.csv          # Tableau récapitulatif
cat results/critical_paths.json           # Chemins détaillés
cat results/kpi_report.txt                # Rapport formaté
```

---

## 📊 Résultats Principaux

### Amplification GNN

| Métrique | Valeur |
|----------|--------|
| **Moyenne** | 0.0613 (6.1%) |
| **Médiane** | 0.0596 |
| **Écart-type** | 0.0095 |
| **Min** | 0.0462 |
| **Max** | 0.0897 |

### Risques GNN

| Catégorie | Mean Risk | Max Risk |
|-----------|-----------|----------|
| **Moyenne** | 0.357 | 0.655 |
| **Min** | 0.285 | 0.411 |
| **Max** | 0.453 | 0.795 |

### Qualité du Modèle

| Aspect | Score |
|--------|-------|
| **Saturation** | 0% ✅ |
| **Discrimination** | Excellente |
| **Stabilité** | ⭐⭐⭐⭐ |
| **Score Global** | ★★★★☆ (4/5) |

---

## 📐 Métriques de Chemin Critiques

Le projet calcule **5 métriques différentes** pour chaque chemin:

### 1. **Mean Risk** ✨ (Recommandé)
- Moyenne des risques des nœuds
- Permet la comparaison équitable
- Meilleure discrimination

### 2. **Max Risk** 🚫 (Goulot d'étranglement)
- Risque maximum du chemin
- Identifie le point faible

### 3. **Sum Risk** ∑ (Héritage)
- Somme de tous les risques
- Favorise les longs chemins

### 4. **Weighted Risk** ⚖️
- Moyenne pondérée (√n)
- Équilibre longueur vs risque

### 5. **Product Risk** 📉
- Approche probabiliste
- Hypothèse d'indépendance

---

## 🔧 Configuration

### Paramètres GNN

Éditer `3_gnn/gnn_model.py`:

```python
# Coefficients de normalisation
STATIC_COEFF = 0.4
GNN_COEFF = 0.6
AMPLIFICATION_COEFF = 0.0
```

### Port Dashboard

Éditer `5_dashboard/app.py`:

```python
app.run(debug=False, host='127.0.0.1', port=8050)  # Changer le port ici
```

---

## 📚 Documentation Complète

| Document | Description |
|----------|-------------|
| **README.md** | Ce fichier - Guide de démarrage |
| **INDEX.md** | Référence complète du projet |
| **PROJECT_SUMMARY.md** | Résumé des résultats |
| **RESULTATS_MODELE.txt** | Rapport détaillé (500+ lignes) |
| **DASHBOARD_GUIDE.md** | Guide utilisation dashboard |

---

## 🎨 Design & Interface

### Palette de Couleurs

```
🔵 Bleu Primaire    : #1e88e5
🟢 Succès (Vert)    : #43a047
🟠 Avertissement    : #ffa726
🔴 Danger (Rouge)   : #ef5350
🟦 Secondaire (Teal): #26a69a
```

### Typographie

- **Font**: Segoe UI, sans-serif
- **Thème**: Modern, Responsive
- **Animations**: Smooth transitions

---

## 🚀 Améliorations Futures

- [ ] Support du machine learning en temps réel
- [ ] Export des résultats en PDF
- [ ] Intégration SNMP/NetFlow
- [ ] Authentification utilisateur
- [ ] Déploiement cloud (AWS/Azure)
- [ ] API REST pour intégrations tierces

---

## 📞 Support

Pour toute question ou problème:

1. Consultez **INDEX.md** pour la référence complète
2. Vérifiez **PROJECT_SUMMARY.md** pour les résultats
3. Lisez **DASHBOARD_GUIDE.md** pour l'utilisation du dashboard

---

## 📄 Licence

Ce projet est fourni à titre d'exemple éducatif.

---

## 👨‍💻 Auteur

**Projet de Virtualisation & Analyse de Réseaux**  
Analyse des Chemins Critiques | Graph Neural Networks | Dashboard Interactif

---

## 📊 Statistiques du Projet

```
📈 Métriques:
   • 50 topologies Internet
   • 1,290 nœuds
   • 1,642 liens
   • 120+ chemins critiques
   
💻 Code:
   • 4 modules Python
   • 5 fichiers dashboard
   • 1,550+ lignes de documentation
   • 1,000+ lignes de code Python
   
📊 Visualisations:
   • 7 graphiques interactifs
   • 4 PNG haute résolution
   • 10 sections KPI
   • 5 métriques par chemin
```

---

**🎯 Prêt à démarrer? Lancez le dashboard:** 

```bash
python 5_dashboard/app.py
```

**Alors accédez à:** http://127.0.0.1:8050

---

*Dashboard Interactif - Analyse Avancée des Chemins Critiques dans les Réseaux*
