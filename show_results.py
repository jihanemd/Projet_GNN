import json

data = json.load(open('results/critical_paths.json'))
print("\n" + "=" * 80)
print("AARNET - TOP 3 CHEMINS CRITIQUES AVEC NOUVELLES MÉTRIQUES")
print("=" * 80)
for i, p in enumerate(data['Aarnet'], 1):
    path_str = "->".join(map(str, p['path'][:5]))
    if len(p['path']) > 5:
        path_str += f"->...{p['path'][-1]}"
    print(f"\nChemin {i}:")
    print(f"  Chemin: {path_str}")
    print(f"  Longueur: {p['length']} liens")
    print(f"  Métriques:")
    print(f"    • Mean Risk (RECOMMANDÉ): {p['mean_risk']:.3f}")
    print(f"    • Max Risk (bottleneck): {p['max_risk']:.3f}")
    print(f"    • Sum Risk (legacy): {p['sum_risk']:.3f}")
    print(f"    • Weighted Risk: {p['weighted_risk']:.3f}")
    print(f"    • Product Risk: {p['product_risk']:.3f}")

print("\n" + "=" * 80)
print("AI3 - TOP CHEMIN CRITIQUE")
print("=" * 80)
for i, p in enumerate(data['Ai3'], 1):
    path_str = "->".join(map(str, p['path']))
    print(f"\nChemin {i}:")
    print(f"  Chemin: {path_str}")
    print(f"  Longueur: {p['length']} liens")
    print(f"  Métriques:")
    print(f"    • Mean Risk: {p['mean_risk']:.3f}")
    print(f"    • Max Risk: {p['max_risk']:.3f}")
    print(f"    • Sum Risk: {p['sum_risk']:.3f}")

print("\n" + "=" * 80)
print("RÉSUMÉ STATISTIQUE - 50 TOPOLOGIES")
print("=" * 80)
import csv
with open('results/analysis_summary.csv') as f:
    reader = csv.DictReader(f)
    rows = list(reader)
    mean_diffs = [float(r['avg_difference']) for r in rows]
    max_gnn = [float(r['max_gnn_risk']) for r in rows]
    mean_gnn = [float(r['mean_gnn_risk']) for r in rows]
    
    import statistics
    print(f"\n  Amplification moyenne (avg_difference):")
    print(f"    • Min: {min(mean_diffs):.4f}")
    print(f"    • Moy: {statistics.mean(mean_diffs):.4f}")
    print(f"    • Max: {max(mean_diffs):.4f}")
    print(f"    • StdDev: {statistics.stdev(mean_diffs):.4f}")
    
    print(f"\n  Max GNN Risk across topologies:")
    print(f"    • Min: {min(max_gnn):.3f}")
    print(f"    • Moy: {statistics.mean(max_gnn):.3f}")
    print(f"    • Max: {max(max_gnn):.3f}")
    
    print(f"\n  Mean GNN Risk across topologies:")
    print(f"    • Min: {min(mean_gnn):.3f}")
    print(f"    • Moy: {statistics.mean(mean_gnn):.3f}")
    print(f"    • Max: {max(mean_gnn):.3f}")

print("\n✅ Pipeline complet avec validation et multi-métriques executé avec succès!")
print()
