"""
Exportation de visualisations enrichies
Création de figures professionnelles pour rapports
"""
import pandas as pd
import json
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from pathlib import Path

# Configuration
BASE_DIR = Path(__file__).parent.parent
RESULTS_DIR = BASE_DIR / "results"
VIZ_DIR = RESULTS_DIR / "visualizations"
VIZ_DIR.mkdir(exist_ok=True)

# Charger les données
results_df = pd.read_csv(RESULTS_DIR / "analysis_summary.csv")
with open(RESULTS_DIR / "critical_paths.json") as f:
    critical_paths = json.load(f)

# Style
sns.set_style("whitegrid")
plt.rcParams['figure.facecolor'] = '#f8f9fa'
plt.rcParams['font.size'] = 10

print("[*] Génération des visualisations...")

# Figure 1: Comparaison complète statique vs GNN
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('Analyse Complète: Risque Statique vs Risque GNN (50 Topologies)', 
             fontsize=16, fontweight='bold', y=1.00)

# 1.1 Scatter plot avec amplification
ax = axes[0, 0]
scatter = ax.scatter(results_df['mean_static_risk'], 
                     results_df['mean_gnn_risk'],
                     c=results_df['avg_difference'],
                     s=results_df['n_nodes']*5,
                     cmap='RdYlGn_r',
                     alpha=0.6,
                     edgecolors='black',
                     linewidth=0.5)
ax.plot([0, 1], [0, 1], 'r--', linewidth=2, label='Pas d\'amplification')
ax.set_xlabel('Risque Statique Moyen', fontsize=11, fontweight='bold')
ax.set_ylabel('Risque GNN Moyen', fontsize=11, fontweight='bold')
ax.set_title('Scatter: Taille = nb nœuds, Couleur = Amplification')
ax.legend(fontsize=9)
ax.grid(True, alpha=0.3)
cbar = plt.colorbar(scatter, ax=ax)
cbar.set_label('Amplification', fontsize=10)

# 1.2 Distribution amplification
ax = axes[0, 1]
ax.hist(results_df['avg_difference'], bins=15, color='#2ecc71', alpha=0.7, edgecolor='black')
ax.axvline(results_df['avg_difference'].mean(), color='red', linestyle='--', 
          linewidth=2, label=f'Moyenne: {results_df["avg_difference"].mean():.4f}')
ax.axvline(results_df['avg_difference'].median(), color='blue', linestyle='--',
          linewidth=2, label=f'Médiane: {results_df["avg_difference"].median():.4f}')
ax.set_xlabel('Amplification (GNN - Statique)', fontsize=11, fontweight='bold')
ax.set_ylabel('Nombre de topologies', fontsize=11, fontweight='bold')
ax.set_title('Distribution de l\'Amplification')
ax.legend(fontsize=9)
ax.grid(True, alpha=0.3, axis='y')

# 1.3 Box plot comparaison
ax = axes[1, 0]
data_box = [results_df['mean_static_risk'], results_df['mean_gnn_risk']]
bp = ax.boxplot(data_box, labels=['Statique', 'GNN'], patch_artist=True)
for patch, color in zip(bp['boxes'], ['#3498db', '#e74c3c']):
    patch.set_facecolor(color)
ax.set_ylabel('Risque Moyen', fontsize=11, fontweight='bold')
ax.set_title('Comparaison Statique vs GNN')
ax.grid(True, alpha=0.3, axis='y')

# 1.4 Relation taille vs amplification
ax = axes[1, 1]
ax.scatter(results_df['n_nodes'], results_df['avg_difference'], 
          color='#9b59b6', s=100, alpha=0.6, edgecolors='black', linewidth=0.5)
z = np.polyfit(results_df['n_nodes'], results_df['avg_difference'], 2)
p = np.poly1d(z)
x_line = np.linspace(results_df['n_nodes'].min(), results_df['n_nodes'].max(), 100)
ax.plot(x_line, p(x_line), 'r--', linewidth=2, label='Tendance (polynomial)')
ax.set_xlabel('Nombre de Nœuds', fontsize=11, fontweight='bold')
ax.set_ylabel('Amplification', fontsize=11, fontweight='bold')
ax.set_title('Amplification vs Taille de Topologie')
ax.legend(fontsize=9)
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig(VIZ_DIR / "01_complete_analysis.png", dpi=300, bbox_inches='tight')
print("[✓] Figure 1: Analyse complète")

# Figure 2: Statistiques détaillées
fig, axes = plt.subplots(1, 3, figsize=(15, 5))
fig.suptitle('Statistiques Détaillées sur les 50 Topologies', 
             fontsize=14, fontweight='bold')

# 2.1 Max risk distribution
ax = axes[0]
ax.hist(results_df['max_gnn_risk'], bins=15, color='#e74c3c', alpha=0.7, edgecolor='black')
ax.axvline(results_df['max_gnn_risk'].mean(), color='darkred', linestyle='--', linewidth=2)
ax.set_xlabel('Max GNN Risk', fontsize=11, fontweight='bold')
ax.set_ylabel('Fréquence', fontsize=11, fontweight='bold')
ax.set_title(f'Max Risk\nMoy: {results_df["max_gnn_risk"].mean():.3f}')
ax.grid(True, alpha=0.3, axis='y')

# 2.2 Mean risk distribution
ax = axes[1]
ax.hist(results_df['mean_gnn_risk'], bins=15, color='#f39c12', alpha=0.7, edgecolor='black')
ax.axvline(results_df['mean_gnn_risk'].mean(), color='darkorange', linestyle='--', linewidth=2)
ax.set_xlabel('Mean GNN Risk', fontsize=11, fontweight='bold')
ax.set_ylabel('Fréquence', fontsize=11, fontweight='bold')
ax.set_title(f'Mean Risk\nMoy: {results_df["mean_gnn_risk"].mean():.3f}')
ax.grid(True, alpha=0.3, axis='y')

# 2.3 Nombre de liens distribution
ax = axes[2]
ax.hist(results_df['n_edges'], bins=15, color='#3498db', alpha=0.7, edgecolor='black')
ax.axvline(results_df['n_edges'].mean(), color='darkblue', linestyle='--', linewidth=2)
ax.set_xlabel('Nombre de Liens', fontsize=11, fontweight='bold')
ax.set_ylabel('Nombre de topologies', fontsize=11, fontweight='bold')
ax.set_title(f'Distribution Nombre de Liens\nMoy: {results_df["n_edges"].mean():.1f}')
ax.grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.savefig(VIZ_DIR / "02_detailed_statistics.png", dpi=300, bbox_inches='tight')
print("[✓] Figure 2: Statistiques détaillées")

# Figure 3: Top 10 topologies
fig, axes = plt.subplots(1, 2, figsize=(14, 6))
fig.suptitle('Top 10 Topologies (par amplification et max risk)', 
             fontsize=14, fontweight='bold')

# 3.1 Top 10 amplification
ax = axes[0]
top10_amp = results_df.nlargest(10, 'avg_difference')
bars = ax.barh(range(len(top10_amp)), top10_amp['avg_difference'], color='#2ecc71', edgecolor='black')
ax.set_yticks(range(len(top10_amp)))
ax.set_yticklabels(top10_amp['topology'])
ax.set_xlabel('Amplification', fontsize=11, fontweight='bold')
ax.set_title('Top 10: Amplification GNN-Statique')
ax.grid(True, alpha=0.3, axis='x')
# Ajouter valeurs
for i, (idx, row) in enumerate(top10_amp.iterrows()):
    ax.text(row['avg_difference'] + 0.001, i, f"{row['avg_difference']:.4f}", 
           va='center', fontsize=9)

# 3.2 Top 10 max risk
ax = axes[1]
top10_risk = results_df.nlargest(10, 'max_gnn_risk')
bars = ax.barh(range(len(top10_risk)), top10_risk['max_gnn_risk'], color='#e74c3c', edgecolor='black')
ax.set_yticks(range(len(top10_risk)))
ax.set_yticklabels(top10_risk['topology'])
ax.set_xlabel('Max GNN Risk', fontsize=11, fontweight='bold')
ax.set_title('Top 10: Risque GNN Maximum')
ax.grid(True, alpha=0.3, axis='x')
# Ajouter valeurs
for i, (idx, row) in enumerate(top10_risk.iterrows()):
    ax.text(row['max_gnn_risk'] + 0.01, i, f"{row['max_gnn_risk']:.3f}", 
           va='center', fontsize=9)

plt.tight_layout()
plt.savefig(VIZ_DIR / "03_top10_topologies.png", dpi=300, bbox_inches='tight')
print("[✓] Figure 3: Top 10 topologies")

# Figure 4: Corrélation et tendances
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('Corrélations et Tendances', fontsize=14, fontweight='bold')

# 4.1 Corrélation Pearson
ax = axes[0, 0]
corr_matrix = results_df[['n_nodes', 'n_edges', 'max_gnn_risk', 'mean_gnn_risk', 'avg_difference']].corr()
sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='coolwarm', center=0, ax=ax, 
           cbar_kws={'label': 'Corrélation'}, vmin=-1, vmax=1)
ax.set_title('Matrice de Corrélation')

# 4.2 Nombre de nœuds vs max risk
ax = axes[0, 1]
ax.scatter(results_df['n_nodes'], results_df['max_gnn_risk'], 
          color='#e74c3c', s=100, alpha=0.6, edgecolors='black', linewidth=0.5)
z = np.polyfit(results_df['n_nodes'], results_df['max_gnn_risk'], 1)
p = np.poly1d(z)
x_line = np.linspace(results_df['n_nodes'].min(), results_df['n_nodes'].max(), 100)
ax.plot(x_line, p(x_line), 'r--', linewidth=2)
corr_val = results_df['n_nodes'].corr(results_df['max_gnn_risk'])
ax.set_xlabel('Nombre de Nœuds', fontsize=11, fontweight='bold')
ax.set_ylabel('Max GNN Risk', fontsize=11, fontweight='bold')
ax.set_title(f'Nœuds vs Max Risk (r={corr_val:.3f})')
ax.grid(True, alpha=0.3)

# 4.3 Nombre de liens vs mean risk
ax = axes[1, 0]
ax.scatter(results_df['n_edges'], results_df['mean_gnn_risk'], 
          color='#f39c12', s=100, alpha=0.6, edgecolors='black', linewidth=0.5)
z = np.polyfit(results_df['n_edges'], results_df['mean_gnn_risk'], 1)
p = np.poly1d(z)
x_line = np.linspace(results_df['n_edges'].min(), results_df['n_edges'].max(), 100)
ax.plot(x_line, p(x_line), 'r--', linewidth=2)
corr_val = results_df['n_edges'].corr(results_df['mean_gnn_risk'])
ax.set_xlabel('Nombre de Liens', fontsize=11, fontweight='bold')
ax.set_ylabel('Mean GNN Risk', fontsize=11, fontweight='bold')
ax.set_title(f'Liens vs Mean Risk (r={corr_val:.3f})')
ax.grid(True, alpha=0.3)

# 4.4 Densité vs amplification
ax = axes[1, 1]
results_df['density'] = 2 * results_df['n_edges'] / (results_df['n_nodes'] * (results_df['n_nodes'] - 1))
ax.scatter(results_df['density'], results_df['avg_difference'], 
          color='#9b59b6', s=100, alpha=0.6, edgecolors='black', linewidth=0.5)
z = np.polyfit(results_df['density'], results_df['avg_difference'], 1)
p = np.poly1d(z)
x_line = np.linspace(results_df['density'].min(), results_df['density'].max(), 100)
ax.plot(x_line, p(x_line), 'r--', linewidth=2)
corr_val = results_df['density'].corr(results_df['avg_difference'])
ax.set_xlabel('Densité du Graphe', fontsize=11, fontweight='bold')
ax.set_ylabel('Amplification', fontsize=11, fontweight='bold')
ax.set_title(f'Densité vs Amplification (r={corr_val:.3f})')
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig(VIZ_DIR / "04_correlations_trends.png", dpi=300, bbox_inches='tight')
print("[✓] Figure 4: Corrélations et tendances")

print(f"\n[✓] Visualisations sauvegardées dans: {VIZ_DIR}")
print(f"    ├── 01_complete_analysis.png")
print(f"    ├── 02_detailed_statistics.png")
print(f"    ├── 03_top10_topologies.png")
print(f"    └── 04_correlations_trends.png")
