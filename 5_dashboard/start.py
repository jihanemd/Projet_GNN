"""
Script de démarrage complet
Génère visualisations, KPIs, et lance le dashboard
"""
import subprocess
import sys
from pathlib import Path
import webbrowser
import time

BASE_DIR = Path(__file__).parent.parent

print("\n" + "="*80)
print("🚀 DÉMARRAGE DU SYSTÈME COMPLET - DASHBOARD INTERACTIF")
print("="*80 + "\n")

# Étape 1: Générer les KPIs
print("[1/3] Génération des indicateurs clés (KPIs)...")
print("-" * 80)
result = subprocess.run([sys.executable, "generate_kpis.py"], cwd=BASE_DIR / "5_dashboard")
if result.returncode != 0:
    print("❌ Erreur lors de la génération des KPIs")
    sys.exit(1)

# Étape 2: Exporter les visualisations
print("\n[2/3] Création des visualisations statiques...")
print("-" * 80)
result = subprocess.run([sys.executable, "export_visualizations.py"], cwd=BASE_DIR / "5_dashboard")
if result.returncode != 0:
    print("❌ Erreur lors de l'export des visualisations")
    sys.exit(1)

# Étape 3: Lancer le dashboard
print("\n[3/3] Lancement du dashboard interactif...")
print("-" * 80)
print("\n📊 Le dashboard démarre...")
time.sleep(2)

# Ouvrir le navigateur
print("\n✨ Ouverture du navigateur à http://127.0.0.1:8050...\n")
time.sleep(1)

try:
    webbrowser.open('http://127.0.0.1:8050', new=2)
except:
    pass

# Lancer Dash
try:
    from app import app
    print("="*80)
    print("🌐 DASHBOARD EN LIGNE")
    print("="*80)
    print("\n  URL: http://127.0.0.1:8050")
    print("\n  Appuyez sur Ctrl+C pour arrêter\n")
    print("="*80 + "\n")
    
    app.run(debug=False, host='127.0.0.1', port=8050)
except Exception as e:
    print(f"❌ Erreur lors du démarrage du dashboard: {e}")
    print("\n💡 Assurez-vous d'avoir installé dash:")
    print("   pip install dash plotly pandas")
    sys.exit(1)
