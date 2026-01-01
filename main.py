"""
Script principal - Pipeline complet
Étape 1: Préparer les données (copier 50 topologies)
Étape 2: Construire graphes enrichis
Étape 3: Entraîner GNN et prédire risques
Étape 4: Analyser chemins critiques
"""
import sys
from pathlib import Path

BASE_DIR = Path(__file__).parent

print("=" * 60)
print("PROJET: Identification des Chemins Critiques dans un Réseau")
print("=" * 60)
print()

# Étape 1: Préparer les données
print(">>> ÉTAPE 1: Préparation des données <<<")
print()
sys.path.insert(0, str(BASE_DIR / "1_data"))
from prepare_data import copy_topologies

copy_topologies(n_topologies=50)

# Étape 2: Construire les graphes
print(">>> ÉTAPE 2: Construction des graphes enrichis <<<")
print()
sys.path.insert(0, str(BASE_DIR / "2_graph"))
from graph_builder import GraphBuilder

builder = GraphBuilder()
graphs = builder.build_all_graphs()
builder.save_graphs()
builder.get_summary()

# Étape 3: GNN
print(">>> ÉTAPE 3: Entraînement GNN <<<")
print()
sys.path.insert(0, str(BASE_DIR / "3_gnn"))
from gnn_model import GNNTrainer

trainer = GNNTrainer()
trainer.train_on_graphs(graphs, epochs=5)
graphs = trainer.predict_risks(graphs)

import pickle
RESULTS_DIR = BASE_DIR / "results"
with open(RESULTS_DIR / "graphs_with_gnn.pkl", 'wb') as f:
    pickle.dump(graphs, f)

# Étape 4: Analyse
print(">>> ÉTAPE 4: Analyse des chemins critiques <<<")
print()
sys.path.insert(0, str(BASE_DIR / "4_analysis"))
from critical_paths import CriticalPathAnalyzer

analyzer = CriticalPathAnalyzer()
results_df = analyzer.analyze_all_graphs(graphs)

# Valider cohérence du modèle
analyzer.validate_model_coherence(results_df, graphs)

analyzer.export_results(results_df)
analyzer.plot_comparison(results_df)

print("=" * 60)
print("[✓] PIPELINE TERMINÉ AVEC SUCCÈS")
print("=" * 60)
print(f"\nRésultats disponibles dans: {RESULTS_DIR}")
print("  - analysis_summary.csv")
print("  - critical_paths.json")
print("  - analysis_plots.png")
print()
