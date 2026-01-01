#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test des imports et de la charge du dashboard
"""
import sys
from pathlib import Path

BASE_DIR = Path(__file__).parent
ANALYSIS_DIR = BASE_DIR / "4_analysis"

print("[TEST] Vérification des imports...")

# Test 1: Import du module critical_paths_map_generator
sys.path.insert(0, str(ANALYSIS_DIR))
try:
    from critical_paths_map_generator import get_critical_paths_figures, CriticalPathsMapGenerator
    print("[OK] Module critical_paths_map_generator importé")
except ImportError as e:
    print(f"[ERREUR] Impossible d'importer critical_paths_map_generator: {e}")
    sys.exit(1)

# Test 2: Vérifier les données
print("\n[TEST] Vérification des données...")
try:
    generator = CriticalPathsMapGenerator()
    print(f"[OK] {len(generator.critical_paths_data)} topologies chargées")
    print(f"[OK] {len(generator.graphs)} graphes chargés")
except Exception as e:
    print(f"[ERREUR] Impossible de charger les données: {e}")
    sys.exit(1)

# Test 3: Vérifier les figures
print("\n[TEST] Création des figures...")
try:
    figs = get_critical_paths_figures()
    print(f"[OK] Figure distribution: {type(figs['distribution'])}")
    print(f"[OK] Figure comparison: {type(figs['comparison'])}")
    print(f"[OK] Figure categories: {type(figs['categories'])}")
    print(f"[OK] DataFrame paths: {len(figs['paths_df'])} chemins")
except Exception as e:
    print(f"[ERREUR] Impossible de créer les figures: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n[SUCCESS] Tous les tests sont passés!")
print("\nLe module critical_paths_map_generator est prêt pour l'intégration au dashboard.")
