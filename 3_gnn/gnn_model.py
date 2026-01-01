"""
Étape 2 : GNN simple pour scorer les risques
- Propager l'information dans le graphe
- Prédire le score de risque par lien
"""
import numpy as np
import pickle
import networkx as nx
from pathlib import Path
from tqdm import tqdm

BASE_DIR = Path(__file__).parent.parent
RESULTS_DIR = BASE_DIR / "results"

class SimpleGNN:
    """Propagation de risque dans le graphe - AVEC RECALIBRATION AUTOMATIQUE"""
    def __init__(self, iterations=3, charge_weight=0.03, centrality_weight=0.02):
        self.iterations = iterations
        self.charge_weight = charge_weight  # Réduit: 0.15 → 0.03
        self.centrality_weight = centrality_weight  # Réduit: 0.1 → 0.02
    
    def propagate_risk(self, G):
        """Propager le risque des nœuds chargés aux liens adjacents"""
        # Initialiser les risques GNN = risque statique
        for u, v in G.edges():
            G[u][v]['gnn_risk'] = G[u][v]['risk_score']
        
        # Propager à partir des nœuds chargés
        for iteration in range(self.iterations):
            updates = {}
            
            for u, v in G.edges():
                current_risk = G[u][v]['gnn_risk']
                
                # Impact du nœud source
                charge_u = G.nodes[u]['load'] / 100
                centrality_u = G.nodes[u]['centrality']
                impact_u = charge_u * self.charge_weight + centrality_u * self.centrality_weight
                
                # Impact du nœud cible
                charge_v = G.nodes[v]['load'] / 100
                centrality_v = G.nodes[v]['centrality']
                impact_v = charge_v * self.charge_weight + centrality_v * self.centrality_weight
                
                # Propagation (moyenne des impacts)
                propagated_risk = current_risk + (impact_u + impact_v) / 2
                updates[(u, v)] = max(0, min(1, propagated_risk))
            
            # Appliquer les mises à jour
            for (u, v), risk in updates.items():
                G[u][v]['gnn_risk'] = risk
        
        return G
    
    def analyze_risk_distribution(self, G):
        """Analyser la distribution des risques"""
        static_risks = [G[u][v]['risk_score'] for u, v in G.edges()]
        gnn_risks = [G[u][v]['gnn_risk'] for u, v in G.edges()]
        
        if len(static_risks) == 0:
            return None
        
        # Vérifier saturation
        saturated = sum(1 for r in gnn_risks if r > 0.95) / len(gnn_risks)
        
        return {
            'static_min': min(static_risks),
            'static_max': max(static_risks),
            'static_mean': np.mean(static_risks),
            'static_std': np.std(static_risks),
            'gnn_min': min(gnn_risks),
            'gnn_max': max(gnn_risks),
            'gnn_mean': np.mean(gnn_risks),
            'gnn_std': np.std(gnn_risks),
            'saturation_rate': saturated
        }
    
    def train_on_graphs(self, graphs, epochs=5):
        """Entraîner (ici = propagation)"""
        print(f"[*] Propagation de risque ({len(graphs)} graphes, {self.iterations} iterations)...")
        print(f"    Coefficients: charge={self.charge_weight}, centrality={self.centrality_weight}")
        
        saturation_rates = []
        
        for name, G in tqdm(graphs.items(), desc="Propagation"):
            if len(G.edges()) == 0:
                continue
            self.propagate_risk(G)
            stats = self.analyze_risk_distribution(G)
            if stats:
                saturation_rates.append(stats['saturation_rate'])
        
        # Vérifier saturation globale
        if saturation_rates:
            mean_saturation = np.mean(saturation_rates)
            print(f"\n[📊] Saturation moyenne: {mean_saturation*100:.1f}%")
            
            if mean_saturation > 0.5:
                print(f"    ⚠️  DÉTECTÉ: Saturation > 50%")
                print(f"    → Recalibrage automatique en cours...")
                self.charge_weight = max(0.005, self.charge_weight / 2)
                self.centrality_weight = max(0.005, self.centrality_weight / 2)
                print(f"    → Nouveaux coefficients: charge={self.charge_weight}, centrality={self.centrality_weight}")
                
                # Relancer propagation
                for name, G in tqdm(graphs.items(), desc="Repropagation", leave=False):
                    if len(G.edges()) == 0:
                        continue
                    self.propagate_risk(G)
                
                print(f"[✓] Recalibrage complété\n")
            else:
                print(f"    ✓  Bonne discrimination entre liens\n")
        
        print("[✓] Propagation terminée\n")
    
    def predict_risks(self, graphs):
        """Retourner les graphes avec risques propagés"""
        return graphs

class GNNTrainer:
    def __init__(self):
        self.gnn = SimpleGNN(iterations=3)
    
    def train_on_graphs(self, graphs, epochs=10):
        """Wrapper pour entraînement"""
        self.gnn.train_on_graphs(graphs, epochs=epochs)
    
    def predict_risks(self, graphs):
        """Wrapper pour prédictions"""
        return self.gnn.predict_risks(graphs)

if __name__ == "__main__":
    # Charger les graphes
    graphs_path = RESULTS_DIR / "graphs.pkl"
    with open(graphs_path, 'rb') as f:
        graphs = pickle.load(f)
    
    # Entraîner et prédire
    trainer = GNNTrainer()
    trainer.train_on_graphs(graphs, epochs=5)
    graphs = trainer.predict_risks(graphs)
    
    # Sauvegarder
    with open(RESULTS_DIR / "graphs_with_gnn.pkl", 'wb') as f:
        pickle.dump(graphs, f)
    
    print("[✓] Graphes avec prédictions GNN sauvegardés")
