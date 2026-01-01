"""
Étape 1 : Construire le graphe enrichi
- Charger topologies graphml
- Ajouter features aux nœuds (charge, centralité)
- Ajouter features aux liens (latence, bande passante, utilisation)
- Sauvegarder en format PyG/DGL
"""
import networkx as nx
import numpy as np
import pandas as pd
import pickle
import os
from pathlib import Path
from tqdm import tqdm

BASE_DIR = Path(__file__).parent.parent
TOPOLOGIES_DIR = BASE_DIR / "1_data" / "topologies"
SYNTHETIC_DIR = BASE_DIR / "1_data" / "synthetic_data"
RESULTS_DIR = BASE_DIR / "results"

class GraphBuilder:
    def __init__(self):
        self.graphs = {}
        self.node_features = {}
        self.edge_features = {}
    
    def load_topology(self, filepath):
        """Charger un fichier graphml"""
        try:
            G = nx.read_graphml(filepath)
            # Convertir en simple graphe si multigraphe
            if isinstance(G, nx.MultiGraph):
                G = nx.Graph(G)
            elif isinstance(G, nx.MultiDiGraph):
                G = nx.DiGraph(G)
            return G
        except Exception as e:
            print(f"[!] Erreur chargement {filepath.name}: {e}")
            return None
    
    def add_node_features(self, G):
        """Ajouter features aux nœuds"""
        n_nodes = len(G.nodes())
        
        # Charge du nœud (0-100)
        node_load = {node: np.random.uniform(10, 100) for node in G.nodes()}
        
        # Centralité (0-1)
        centrality = nx.degree_centrality(G)
        
        for node in G.nodes():
            G.nodes[node]['load'] = node_load[node]
            G.nodes[node]['centrality'] = centrality[node]
        
        return G
    
    def add_edge_features(self, G):
        """Ajouter features aux liens"""
        for u, v in G.edges():
            # Latence (ms): 1-50
            G[u][v]['latency'] = np.random.uniform(1, 50)
            
            # Bande passante (Gbps): 1-100
            G[u][v]['bandwidth'] = np.random.uniform(1, 100)
            
            # Utilisation (%): 10-90
            G[u][v]['utilization'] = np.random.uniform(10, 90)
        
        return G
    
    def compute_link_risk(self, G):
        """Scorer les risques des liens (simple)"""
        for u, v in G.edges():
            latency = G[u][v]['latency']
            utilization = G[u][v]['utilization']
            bandwidth = G[u][v]['bandwidth']
            
            # Risk = (latence élevée) + (utilisation élevée) - (bande passante haute)
            risk = (latency / 50) * 0.3 + (utilization / 100) * 0.5 - (bandwidth / 100) * 0.2
            G[u][v]['risk_score'] = max(0, risk)
        
        return G
    
    def build_all_graphs(self):
        """Construire tous les graphes"""
        graphml_files = sorted(TOPOLOGIES_DIR.glob("*.graphml"))
        
        print(f"[*] Chargement de {len(graphml_files)} graphes...")
        
        for filepath in tqdm(graphml_files, desc="Graphes"):
            G = self.load_topology(filepath)
            if G is None or len(G.nodes()) == 0:
                continue
            
            G = self.add_node_features(G)
            G = self.add_edge_features(G)
            G = self.compute_link_risk(G)
            
            self.graphs[filepath.stem] = G
        
        print(f"[✓] {len(self.graphs)} graphes chargés et enrichis\n")
        return self.graphs
    
    def save_graphs(self):
        """Sauvegarder les graphes"""
        output_path = RESULTS_DIR / "graphs.pkl"
        os.makedirs(RESULTS_DIR, exist_ok=True)
        
        with open(output_path, 'wb') as f:
            pickle.dump(self.graphs, f)
        
        print(f"[✓] Graphes sauvegardés: {output_path}\n")
    
    def get_summary(self):
        """Résumé des graphes"""
        print("[*] Résumé des graphes:")
        for name, G in list(self.graphs.items())[:5]:  # Afficher les 5 premiers
            n_nodes = len(G.nodes())
            n_edges = len(G.edges())
            avg_risk = np.mean([G[u][v]['risk_score'] for u, v in G.edges()]) if n_edges > 0 else 0
            print(f"    {name}: {n_nodes} nœuds, {n_edges} liens, risque moyen={avg_risk:.3f}")
        print()

if __name__ == "__main__":
    import os
    builder = GraphBuilder()
    builder.build_all_graphs()
    builder.save_graphs()
    builder.get_summary()
