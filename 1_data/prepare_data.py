"""
Étape 1 : Préparer les données
- Copier 50 topologies du dossier data_v2
- Générer données synthétiques (charges, latences)
"""
import os
import shutil
import numpy as np
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "1_data"
TOPOLOGIES_DIR = DATA_DIR / "topologies"
SYNTHETIC_DIR = DATA_DIR / "synthetic_data"
SOURCE_DATA = Path("c:/Users/dell/Documents/AI/S3/virtualisation/projet_v6/data_v2")

def copy_topologies(n_topologies=50):
    """Copier les 50 premiers fichiers graphml"""
    print(f"[*] Copie des {n_topologies} topologies...")
    
    graphml_files = sorted([f for f in SOURCE_DATA.glob("*.graphml")])[:n_topologies]
    
    for graphml in graphml_files:
        shutil.copy(graphml, TOPOLOGIES_DIR / graphml.name)
        print(f"    ✓ {graphml.name}")
    
    print(f"[✓] {len(graphml_files)} topologies copiées\n")

def generate_synthetic_data(n_topologies=50):
    """Générer données synthétiques pour chaque topologie"""
    print(f"[*] Génération données synthétiques...")
    
    # On créera les données réelles dans graph_builder.py après avoir chargé les graphes
    # Ici on fait juste une structure
    
    print("[✓] Données synthétiques prêtes à être générées\n")

if __name__ == "__main__":
    os.makedirs(TOPOLOGIES_DIR, exist_ok=True)
    os.makedirs(SYNTHETIC_DIR, exist_ok=True)
    
    copy_topologies(n_topologies=50)
    generate_synthetic_data()
    
    print("[✓] Préparation des données terminée")
