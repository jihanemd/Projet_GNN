"""
Dashboard moderne et interactif - Analyse des Chemins Critiques
Visualisations avancées, métriques temps réel, sélecteur topologie
"""
import dash
from dash import dcc, html, Input, Output, callback
import plotly.graph_objs as go
import plotly.express as px
import pandas as pd
import json
from pathlib import Path
import numpy as np
import sys

# Configuration
BASE_DIR = Path(__file__).parent.parent
RESULTS_DIR = BASE_DIR / "results"
ANALYSIS_DIR = BASE_DIR / "4_analysis"

# Ajouter le répertoire analysis au path pour importer le module
sys.path.insert(0, str(ANALYSIS_DIR))

# Importer le générateur de carte des chemins à risque
try:
    from critical_paths_map_generator import get_critical_paths_figures
    CRITICAL_PATHS_MAP_AVAILABLE = True
    print("[*] Module critical_paths_map_generator importé avec succès")
except ImportError as e:
    CRITICAL_PATHS_MAP_AVAILABLE = False
    print(f"[!] Avertissement: {e}")

# Charger les données
print("[*] Chargement des données...")
results_df = pd.read_csv(RESULTS_DIR / "analysis_summary.csv")
with open(RESULTS_DIR / "critical_paths.json") as f:
    critical_paths = json.load(f)

# Charger les figures de la carte si disponibles
if CRITICAL_PATHS_MAP_AVAILABLE:
    try:
        critical_paths_figures = get_critical_paths_figures()
        print("[✓] Figures de la carte des chemins chargées")
    except Exception as e:
        print(f"[!] Erreur lors du chargement des figures: {e}")
        CRITICAL_PATHS_MAP_AVAILABLE = False

print(f"[✓] {len(results_df)} topologies chargées")

# Initialiser l'application
app = dash.Dash(__name__, suppress_callback_exceptions=True)
app.title = "Dashboard Avancé - Chemins Critiques"

# Palette de couleurs moderne
COLORS = {
    'primary': '#1e88e5',      # Bleu moderne
    'secondary': '#26a69a',    # Teal
    'success': '#43a047',      # Vert
    'warning': '#ffa726',      # Orange
    'danger': '#ef5350',       # Rouge
    'info': '#5c6bc0',         # Indigo
    'light': '#eceff1',        # Gris clair
    'dark': '#263238',         # Gris foncé
    'bg': '#f5f7fa',          # Fond principal
}

# CSS personnalisé
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <style>
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
                color: #333;
            }
            .metric-card {
                background: white;
                border-radius: 12px;
                padding: 20px;
                margin: 10px;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                border-left: 4px solid #1e88e5;
                transition: transform 0.3s, box-shadow 0.3s;
            }
            .metric-card:hover {
                transform: translateY(-5px);
                box-shadow: 0 8px 12px rgba(0,0,0,0.15);
            }
            .metric-title {
                color: #666;
                font-size: 12px;
                font-weight: 600;
                text-transform: uppercase;
                letter-spacing: 0.5px;
            }
            .metric-value {
                font-size: 32px;
                font-weight: bold;
                margin: 10px 0;
            }
            .metric-subtitle {
                color: #999;
                font-size: 12px;
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

# Layout
app.layout = html.Div([
    # Header avec gradient
    html.Div([
        html.Div([
            html.H1("🌐 Analyse Avancée des Chemins Critiques", 
                   style={'color': 'white', 'margin': '0 0 10px 0', 'fontSize': '36px'}),
            html.P("Identification des chemins vulnérables dans les réseaux Internet - Dashboard Interactif", 
                  style={'color': 'rgba(255,255,255,0.9)', 'margin': 0, 'fontSize': '16px'})
        ], style={'padding': '30px 40px'})
    ], style={
        'background': f'linear-gradient(135deg, {COLORS["primary"]} 0%, {COLORS["info"]} 100%)',
        'color': 'white',
        'marginBottom': '30px',
        'boxShadow': '0 4px 6px rgba(0,0,0,0.1)'
    }),

    # Indicateurs clés (KPIs)
    html.Div([
        html.Div([
            # Card 1: Amplification
            html.Div([
                html.Div([
                    html.Div("📊", style={'fontSize': '32px', 'marginBottom': '10px'}),
                    html.Div("Amplification Moyenne", className='metric-title'),
                    html.Div(f"{results_df['avg_difference'].mean():.4f}", 
                            className='metric-value', style={'color': COLORS['success']}),
                    html.Div(f"±{results_df['avg_difference'].std():.4f} (écart-type)", 
                            className='metric-subtitle')
                ])
            ], className='metric-card', style={'borderLeftColor': COLORS['success']}),
            
            # Card 2: Max GNN Risk
            html.Div([
                html.Div([
                    html.Div("⚠️", style={'fontSize': '32px', 'marginBottom': '10px'}),
                    html.Div("Max GNN Risk", className='metric-title'),
                    html.Div(f"{results_df['max_gnn_risk'].mean():.3f}", 
                            className='metric-value', style={'color': COLORS['danger']}),
                    html.Div(f"Intervalle: {results_df['max_gnn_risk'].min():.3f}-{results_df['max_gnn_risk'].max():.3f}", 
                            className='metric-subtitle')
                ])
            ], className='metric-card', style={'borderLeftColor': COLORS['danger']}),
            
            # Card 3: Mean GNN Risk
            html.Div([
                html.Div([
                    html.Div("📈", style={'fontSize': '32px', 'marginBottom': '10px'}),
                    html.Div("Mean GNN Risk", className='metric-title'),
                    html.Div(f"{results_df['mean_gnn_risk'].mean():.3f}", 
                            className='metric-value', style={'color': COLORS['warning']}),
                    html.Div(f"Intervalle: {results_df['mean_gnn_risk'].min():.3f}-{results_df['mean_gnn_risk'].max():.3f}", 
                            className='metric-subtitle')
                ])
            ], className='metric-card', style={'borderLeftColor': COLORS['warning']}),
            
            # Card 4: Topologies
            html.Div([
                html.Div([
                    html.Div("🎯", style={'fontSize': '32px', 'marginBottom': '10px'}),
                    html.Div("Topologies Analysées", className='metric-title'),
                    html.Div(f"{len(results_df)}", 
                            className='metric-value', style={'color': COLORS['primary']}),
                    html.Div(f"{results_df['n_nodes'].sum():,} nœuds | {results_df['n_edges'].sum():,} liens", 
                            className='metric-subtitle')
                ])
            ], className='metric-card', style={'borderLeftColor': COLORS['primary']}),
            
        ], style={
            'display': 'grid',
            'gridTemplateColumns': 'repeat(auto-fit, minmax(250px, 1fr))',
            'gap': '20px',
            'marginBottom': '30px'
        })
    ], style={'padding': '0 20px', 'maxWidth': '1400px', 'margin': '0 auto'}),

    # Contrôles et Filtres
    html.Div([
        html.Div([
            html.Div([
                html.Label("🌐 Sélectionner Topologie", style={'fontWeight': 'bold', 'color': COLORS['dark'], 'marginBottom': '10px', 'display': 'block'}),
                dcc.Dropdown(
                    id='topology-dropdown',
                    options=[{'label': f"📍 {t}", 'value': t} for t in sorted(results_df['topology'].unique())],
                    value=results_df['topology'].iloc[0],
                    style={'width': '100%'},
                    clearable=False,
                    searchable=True
                )
            ], style={'marginBottom': '20px'}),
            
            html.Div([
                html.Label("📊 Sélectionner Métrique", style={'fontWeight': 'bold', 'color': COLORS['dark'], 'marginBottom': '10px', 'display': 'block'}),
                dcc.Dropdown(
                    id='metric-dropdown',
                    options=[
                        {'label': '✨ Mean Risk (Recommandé)', 'value': 'mean_risk'},
                        {'label': '🚫 Max Risk (Goulot)', 'value': 'max_risk'},
                        {'label': '∑ Sum Risk (Héritage)', 'value': 'sum_risk'},
                        {'label': '⚖️ Weighted Risk', 'value': 'weighted_risk'},
                        {'label': '📉 Product Risk', 'value': 'product_risk'}
                    ],
                    value='mean_risk',
                    style={'width': '100%'},
                    clearable=False
                )
            ], style={'marginBottom': '20px'}),
            
            html.Div([
                html.Label("🔝 Top K Chemins Critiques", style={'fontWeight': 'bold', 'color': COLORS['dark'], 'marginBottom': '10px', 'display': 'block'}),
                dcc.Slider(
                    id='topk-slider',
                    min=1, max=10, step=1, value=5,
                    marks={i: str(i) for i in range(1, 11)},
                    tooltip={"placement": "bottom", "always_visible": True}
                )
            ], style={'marginTop': '20px'})
        ], style={
            'background': 'white',
            'padding': '25px',
            'borderRadius': '12px',
            'boxShadow': '0 2px 8px rgba(0,0,0,0.08)',
            'marginBottom': '30px',
            'maxWidth': '1400px',
            'margin': '0 auto 30px'
        })
    ], style={'padding': '0 20px'}),

    # Onglets pour différentes visualisations
    html.Div([
        dcc.Tabs(id='tabs', value='tab-1', children=[
            # TAB 1: Vue générale
            dcc.Tab(label='📊 Vue Générale', value='tab-1', children=[
                html.Div([
                    html.Div([
                        dcc.Graph(id='scatter-plot')
                    ], style={'width': '48%', 'display': 'inline-block', 'paddingRight': '2%'}),
                    
                    html.Div([
                        dcc.Graph(id='histogram-plot')
                    ], style={'width': '48%', 'display': 'inline-block', 'paddingLeft': '2%'})
                ]),
                
                html.Div([
                    dcc.Graph(id='topology-detail')
                ], style={'marginTop': '20px'})
            ], style={'padding': '20px'}),
            
            # TAB 2: Chemins Critiques
            dcc.Tab(label='🔴 Chemins Critiques', value='tab-2', children=[
                html.Div([
                    html.Div([
                        html.H3("📋 Top Chemins Critiques", style={'color': COLORS['dark']}),
                        html.Div(id='critical-paths-table')
                    ], style={
                        'background': 'white',
                        'padding': '25px',
                        'borderRadius': '12px',
                        'boxShadow': '0 2px 8px rgba(0,0,0,0.08)'
                    })
                ], style={'padding': '20px'})
            ]),
            
            # TAB 3: Distributions
            dcc.Tab(label='📈 Distributions', value='tab-3', children=[
                html.Div([
                    html.Div([
                        dcc.Graph(id='amplitude-distribution')
                    ], style={'width': '48%', 'display': 'inline-block', 'paddingRight': '2%'}),
                    
                    html.Div([
                        dcc.Graph(id='risk-distribution')
                    ], style={'width': '48%', 'display': 'inline-block', 'paddingLeft': '2%'})
                ], style={'marginTop': '20px'}),
                
                html.Div([
                    dcc.Graph(id='correlation-plot')
                ], style={'marginTop': '20px'})
            ], style={'padding': '20px'}),
            
            # TAB 4: Carte des Chemins à Risque
            dcc.Tab(label='🗺️ Carte des Chemins', value='tab-4', children=[
                html.Div([
                    html.Div([
                        html.H3("📊 Carte Interactive des Chemins à Risque", 
                               style={'color': '#263238', 'marginBottom': '20px'}),
                        html.P("Visualisation complète des chemins critiques identifiés par le modèle GNN.",
                              style={'color': '#666', 'marginBottom': '20px'}),
                    ], style={
                        'background': 'white',
                        'padding': '20px',
                        'borderRadius': '12px',
                        'boxShadow': '0 2px 8px rgba(0,0,0,0.08)',
                        'marginBottom': '20px'
                    }),
                    
                    # Grille des stats de la carte
                    html.Div([
                        html.Div([
                            html.Div([
                                html.Div("🔴", style={'fontSize': '24px', 'marginBottom': '5px'}),
                                html.Div("Chemins Critiques", style={'fontSize': '12px', 'color': '#666'}),
                                html.Div(id='map-critical-count', style={
                                    'fontSize': '24px', 
                                    'fontWeight': 'bold', 
                                    'color': '#d32f2f',
                                    'marginTop': '8px'
                                })
                            ], style={
                                'background': 'white',
                                'padding': '20px',
                                'borderRadius': '8px',
                                'textAlign': 'center',
                                'borderLeft': '4px solid #d32f2f'
                            })
                        ], style={'flex': '1', 'marginRight': '10px'}),
                        
                        html.Div([
                            html.Div([
                                html.Div("🟡", style={'fontSize': '24px', 'marginBottom': '5px'}),
                                html.Div("Chemins Modérés", style={'fontSize': '12px', 'color': '#666'}),
                                html.Div(id='map-moderate-count', style={
                                    'fontSize': '24px', 
                                    'fontWeight': 'bold', 
                                    'color': '#ff9800',
                                    'marginTop': '8px'
                                })
                            ], style={
                                'background': 'white',
                                'padding': '20px',
                                'borderRadius': '8px',
                                'textAlign': 'center',
                                'borderLeft': '4px solid #ff9800'
                            })
                        ], style={'flex': '1', 'marginRight': '10px', 'marginLeft': '10px'}),
                        
                        html.Div([
                            html.Div([
                                html.Div("🟢", style={'fontSize': '24px', 'marginBottom': '5px'}),
                                html.Div("Chemins Stables", style={'fontSize': '12px', 'color': '#666'}),
                                html.Div(id='map-stable-count', style={
                                    'fontSize': '24px', 
                                    'fontWeight': 'bold', 
                                    'color': '#388e3c',
                                    'marginTop': '8px'
                                })
                            ], style={
                                'background': 'white',
                                'padding': '20px',
                                'borderRadius': '8px',
                                'textAlign': 'center',
                                'borderLeft': '4px solid #388e3c'
                            })
                        ], style={'flex': '1', 'marginLeft': '10px'})
                    ], style={
                        'display': 'flex',
                        'justifyContent': 'space-between',
                        'marginBottom': '20px'
                    }),
                    
                    # Graphiques de la carte
                    html.Div([
                        html.Div([
                            dcc.Graph(id='map-distribution', style={'marginBottom': '20px'})
                        ], style={'width': '48%', 'display': 'inline-block', 'paddingRight': '2%'}),
                        
                        html.Div([
                            dcc.Graph(id='map-categories', style={'marginBottom': '20px'})
                        ], style={'width': '48%', 'display': 'inline-block', 'paddingLeft': '2%'})
                    ]),
                    
                    html.Div([
                        dcc.Graph(id='map-comparison')
                    ], style={'marginTop': '20px'}),
                    
                    # Lien vers la page complète
                    html.Div([
                        html.Div([
                            html.H4("📄 Rapport Complet", style={'color': '#263238', 'marginTop': '0'}),
                            html.P("Accédez au rapport HTML complet avec toutes les visualisations interactives et les données détaillées.",
                                  style={'color': '#666'}),
                            html.A([
                                html.Button("📂 Ouvrir results/critical_paths_map.html", 
                                          style={
                                              'padding': '12px 25px',
                                              'backgroundColor': '#1e88e5',
                                              'color': 'white',
                                              'border': 'none',
                                              'borderRadius': '6px',
                                              'cursor': 'pointer',
                                              'fontSize': '14px',
                                              'fontWeight': 'bold',
                                              'transition': 'all 0.3s'
                                          })
                            ], href='/results/critical_paths_map.html', target='_blank',
                            style={'textDecoration': 'none'})
                        ], style={
                            'background': 'white',
                            'padding': '20px',
                            'borderRadius': '12px',
                            'boxShadow': '0 2px 8px rgba(0,0,0,0.08)',
                            'marginTop': '20px'
                        })
                    ])
                ], style={'padding': '20px'})
            ])
        ], style={
            'background': 'white',
            'borderRadius': '12px',
            'boxShadow': '0 2px 8px rgba(0,0,0,0.08)',
            'maxWidth': '1400px',
            'margin': '0 auto'
        })
    ], style={'padding': '0 20px', 'marginBottom': '30px'}),

    # Footer
    html.Div([
        html.Div([
            html.P("🚀 Dashboard Interactif - Analyse Avancée des Chemins Critiques dans les Réseaux | Topologies Internet | 50 Topologies | 120+ Chemins Critiques", 
                  style={'textAlign': 'center', 'color': '#666', 'margin': '0'})
        ], style={'padding': '20px', 'textAlign': 'center', 'color': '#999', 'fontSize': '12px'})
    ], style={'marginTop': '50px'})

], style={
    'fontFamily': '"Segoe UI", Tahoma, Geneva, Verdana, sans-serif',
    'padding': '20px',
    'backgroundColor': COLORS['bg']
})

# ============================================================================
# CALLBACKS - Mises à jour dynamiques
# ============================================================================

@callback(
    Output('scatter-plot', 'figure'),
    Input('topology-dropdown', 'value')
)
def update_scatter(topology):
    """Scatter plot: Risque Statique vs GNN avec amplification"""
    fig = go.Figure()
    
    # Points pour chaque topologie
    fig.add_trace(go.Scatter(
        x=results_df['mean_static_risk'],
        y=results_df['mean_gnn_risk'],
        mode='markers',
        marker=dict(
            size=np.sqrt(results_df['n_nodes']) * 1.5,
            color=results_df['avg_difference'],
            colorscale='Turbo',
            showscale=True,
            colorbar=dict(
                title="Amplification<br>%",
                thickness=15,
                len=0.7
            ),
            line=dict(width=2, color='white'),
            opacity=0.7
        ),
        text=[f"<b>{t}</b><br>Nœuds: {n}<br>Statique: {s:.3f}<br>GNN: {g:.3f}<br>Amplif: {a:.4f}" 
              for t, n, s, g, a in zip(
                  results_df['topology'], 
                  results_df['n_nodes'],
                  results_df['mean_static_risk'],
                  results_df['mean_gnn_risk'],
                  results_df['avg_difference']
              )],
        hovertemplate='%{text}<extra></extra>',
        name='Topologies'
    ))
    
    # Ligne y=x (pas d'amplification)
    max_val = max(results_df['mean_static_risk'].max(), results_df['mean_gnn_risk'].max())
    fig.add_trace(go.Scatter(
        x=[0, max_val], y=[0, max_val],
        mode='lines',
        line=dict(color='rgba(255,0,0,0.5)', dash='dash', width=3),
        name='Pas d\'amplification',
        hoverinfo='skip'
    ))
    
    # Highlight topologie sélectionnée
    selected = results_df[results_df['topology'] == topology]
    if not selected.empty:
        fig.add_trace(go.Scatter(
            x=selected['mean_static_risk'],
            y=selected['mean_gnn_risk'],
            mode='markers+text',
            marker=dict(size=20, color=COLORS['danger'], symbol='star'),
            text=[topology],
            textposition='top center',
            hovertemplate='<b>★ Sélectionnée ★</b><br>' + topology,
            name='Topologie sélectionnée'
        ))
    
    fig.update_layout(
        title='<b>Analyse Risque: Statique vs GNN</b><br><sub>Taille = Nombre de nœuds | Couleur = Amplification</sub>',
        xaxis_title='Risque Statique Moyen',
        yaxis_title='Risque GNN Moyen',
        height=500,
        template='plotly_white',
        font=dict(family='Segoe UI', size=12),
        hovermode='closest',
        plot_bgcolor='rgba(240,240,240,0.5)',
        paper_bgcolor='white',
        margin=dict(l=60, r=100, t=100, b=60)
    )
    
    return fig

@callback(
    Output('histogram-plot', 'figure'),
    Input('topology-dropdown', 'value')
)
def update_histogram(topology):
    """Histogramme: Distribution de l'amplification"""
    fig = go.Figure()
    
    fig.add_trace(go.Histogram(
        x=results_df['avg_difference'],
        nbinsx=20,
        name='Amplification',
        marker=dict(color=COLORS['primary'], opacity=0.8, line=dict(color='white', width=2)),
        hovertemplate='Intervalle: %{x:.4f}<br>Nombre: %{y}<extra></extra>'
    ))
    
    # Ajouter ligne verticale pour la topologie sélectionnée
    selected = results_df[results_df['topology'] == topology]
    if not selected.empty:
        selected_amp = selected['avg_difference'].values[0]
        fig.add_vline(
            x=selected_amp, 
            line_dash='dash', 
            line_color=COLORS['danger'],
            annotation_text=f'<b>{topology}</b><br>{selected_amp:.4f}',
            annotation_position='top right'
        )
    
    fig.update_layout(
        title='<b>Distribution de l\'Amplification</b><br><sub>Amplification = (GNN - Statique) / Statique</sub>',
        xaxis_title='Amplification (%)',
        yaxis_title='Nombre de Topologies',
        height=500,
        template='plotly_white',
        font=dict(family='Segoe UI', size=12),
        plot_bgcolor='rgba(240,240,240,0.5)',
        paper_bgcolor='white',
        margin=dict(l=60, r=60, t=100, b=60),
        showlegend=False
    )
    
    return fig

@callback(
    Output('topology-detail', 'figure'),
    Input('topology-dropdown', 'value')
)
def update_detail(topology):
    """Graphique détaillé: Comparaison risques pour topologie sélectionnée"""
    selected = results_df[results_df['topology'] == topology]
    if selected.empty:
        return go.Figure().add_annotation(text="Topologie non trouvée")
    
    top_data = selected.iloc[0]
    
    fig = go.Figure()
    
    # Comparaison statistique
    categories = ['Min', 'Moyenne', 'Max']
    
    fig.add_trace(go.Bar(
        name='Risque Statique',
        x=categories,
        y=[
            results_df['mean_static_risk'].min(),
            top_data['mean_static_risk'],
            results_df['max_static_risk'].max()
        ],
        marker=dict(color=COLORS['secondary']),
        text=[f"{v:.3f}" for v in [
            results_df['mean_static_risk'].min(),
            top_data['mean_static_risk'],
            results_df['max_static_risk'].max()
        ]],
        textposition='outside',
        hovertemplate='<b>Risque Statique</b><br>%{x}<br>Valeur: %{y:.3f}<extra></extra>'
    ))
    
    fig.add_trace(go.Bar(
        name='Risque GNN',
        x=categories,
        y=[
            results_df['mean_gnn_risk'].min(),
            top_data['mean_gnn_risk'],
            results_df['max_gnn_risk'].max()
        ],
        marker=dict(color=COLORS['danger']),
        text=[f"{v:.3f}" for v in [
            results_df['mean_gnn_risk'].min(),
            top_data['mean_gnn_risk'],
            results_df['max_gnn_risk'].max()
        ]],
        textposition='outside',
        hovertemplate='<b>Risque GNN</b><br>%{x}<br>Valeur: %{y:.3f}<extra></extra>'
    ))
    
    fig.update_layout(
        title=f'<b>Détails Topologie: {topology}</b><br><sub>{int(top_data["n_nodes"])} nœuds • {int(top_data["n_edges"])} liens • Amplif: {top_data["avg_difference"]:.4f}</sub>',
        xaxis_title='Catégorie',
        yaxis_title='Risque',
        barmode='group',
        height=500,
        template='plotly_white',
        font=dict(family='Segoe UI', size=12),
        plot_bgcolor='rgba(240,240,240,0.5)',
        paper_bgcolor='white',
        margin=dict(l=60, r=60, t=120, b=60),
        hovermode='x unified'
    )
    
    return fig

@callback(
    Output('amplitude-distribution', 'figure'),
    Input('topology-dropdown', 'value')
)
def update_amplitude_dist(topology):
    """Distribution des amplifications en box plot"""
    fig = go.Figure()
    
    fig.add_trace(go.Box(
        y=results_df['avg_difference'],
        name='Amplification',
        marker=dict(color=COLORS['success']),
        boxmean='sd',
        hovertemplate='Amplif: %{y:.4f}<extra></extra>'
    ))
    
    fig.update_layout(
        title='<b>Distribution de l\'Amplification</b><br><sub>Box plot avec moyenne et écart-type</sub>',
        yaxis_title='Amplification (%)',
        height=450,
        template='plotly_white',
        font=dict(family='Segoe UI', size=12),
        showlegend=False,
        plot_bgcolor='rgba(240,240,240,0.5)',
        paper_bgcolor='white',
        margin=dict(l=60, r=60, t=100, b=60)
    )
    
    return fig

@callback(
    Output('risk-distribution', 'figure'),
    Input('topology-dropdown', 'value')
)
def update_risk_dist(topology):
    """Distribution des risques GNN"""
    fig = go.Figure()
    
    fig.add_trace(go.Violin(
        y=results_df['mean_gnn_risk'],
        name='Mean GNN Risk',
        side='negative',
        marker=dict(color=COLORS['warning']),
        hovertemplate='Risk: %{y:.3f}<extra></extra>'
    ))
    
    fig.add_trace(go.Violin(
        y=results_df['max_gnn_risk'],
        name='Max GNN Risk',
        side='positive',
        marker=dict(color=COLORS['danger']),
        hovertemplate='Risk: %{y:.3f}<extra></extra>'
    ))
    
    fig.update_layout(
        title='<b>Distribution des Risques GNN</b><br><sub>Violin plot: Mean vs Max</sub>',
        yaxis_title='Risque GNN',
        height=450,
        template='plotly_white',
        font=dict(family='Segoe UI', size=12),
        plot_bgcolor='rgba(240,240,240,0.5)',
        paper_bgcolor='white',
        margin=dict(l=60, r=60, t=100, b=60),
        hovermode='closest'
    )
    
    return fig

@callback(
    Output('correlation-plot', 'figure'),
    Input('topology-dropdown', 'value')
)
def update_correlation(topology):
    """Corrélation entre métriques"""
    cols_numeric = ['n_nodes', 'n_edges', 'mean_static_risk', 'mean_gnn_risk', 'avg_difference']
    corr_matrix = results_df[cols_numeric].corr()
    
    fig = go.Figure(data=go.Heatmap(
        z=corr_matrix.values,
        x=['Nœuds', 'Liens', 'Risk Statique', 'Risk GNN', 'Amplification'],
        y=['Nœuds', 'Liens', 'Risk Statique', 'Risk GNN', 'Amplification'],
        colorscale='RdBu',
        zmid=0,
        text=np.round(corr_matrix.values, 2),
        texttemplate='%{text:.2f}',
        textfont={"size": 12},
        hovertemplate='%{x} vs %{y}<br>Corrélation: %{z:.3f}<extra></extra>'
    ))
    
    fig.update_layout(
        title='<b>Matrice de Corrélation</b><br><sub>Relations entre les métriques principales</sub>',
        height=450,
        template='plotly_white',
        font=dict(family='Segoe UI', size=12),
        paper_bgcolor='white',
        margin=dict(l=120, r=60, t=100, b=120)
    )
    
    return fig

# ==================== CALLBACKS CARTE DES CHEMINS À RISQUE ====================

@callback(
    [Output('map-distribution', 'figure'),
     Output('map-comparison', 'figure'),
     Output('map-categories', 'figure'),
     Output('map-critical-count', 'children'),
     Output('map-moderate-count', 'children'),
     Output('map-stable-count', 'children')],
    Input('tabs', 'value')
)
def update_critical_paths_map(selected_tab):
    """Met à jour les graphiques de la carte des chemins à risque"""
    if selected_tab != 'tab-4' or not CRITICAL_PATHS_MAP_AVAILABLE:
        # Retourner des graphiques vides si l'onglet n'est pas sélectionné
        empty_fig = go.Figure()
        empty_fig.add_annotation(text="Données non disponibles", showarrow=False)
        return (empty_fig, empty_fig, empty_fig, "N/A", "N/A", "N/A")
    
    try:
        figs = critical_paths_figures
        
        # Compter les chemins par catégorie
        all_paths = []
        for topology, paths in critical_paths.items():
            all_paths.extend(paths)
        
        critical_count = sum(1 for p in all_paths if p.get('mean_risk', 0) > 0.5)
        moderate_count = sum(1 for p in all_paths if 0.3 <= p.get('mean_risk', 0) <= 0.5)
        stable_count = sum(1 for p in all_paths if p.get('mean_risk', 0) < 0.3)
        
        return (
            figs['distribution'],
            figs['comparison'],
            figs['categories'],
            str(critical_count),
            str(moderate_count),
            str(stable_count)
        )
    except Exception as e:
        print(f"[!] Erreur lors du chargement de la carte: {e}")
        empty_fig = go.Figure()
        empty_fig.add_annotation(text=f"Erreur: {str(e)}", showarrow=False)
        return (empty_fig, empty_fig, empty_fig, "Erreur", "Erreur", "Erreur")

# ==================== FIN CALLBACKS CARTE DES CHEMINS À RISQUE ====================

@callback(
    Output('critical-paths-table', 'children'),
    [Input('topology-dropdown', 'value'),
     Input('metric-dropdown', 'value'),
     Input('topk-slider', 'value')]
)
def update_critical_paths(topology, metric, top_k):
    """Tableau des chemins critiques avec styling"""
    if topology not in critical_paths:
        return html.Div([
            html.P(f"⚠️ Aucun chemin trouvé pour {topology}", 
                  style={'color': COLORS['warning'], 'fontSize': '16px', 'textAlign': 'center'})
        ])
    
    paths = critical_paths[topology][:top_k]
    
    rows = []
    for i, path_data in enumerate(paths, 1):
        path = path_data['path']
        # Afficher le chemin COMPLET en une seule ligne ou multiple selon la longueur
        path_str = " → ".join(map(str, path))
        
        metric_value = path_data.get(metric, path_data.get('mean_risk', 0))
        max_risk = path_data.get('max_risk', 0)
        
        # Couleur basée sur le risque
        if metric_value > 0.5:
            color = COLORS['danger']
        elif metric_value > 0.3:
            color = COLORS['warning']
        else:
            color = COLORS['success']
        
        rows.append(
            html.Tr([
                html.Td(f"#{i:02d}", style={
                    'fontWeight': 'bold',
                    'textAlign': 'center',
                    'color': 'white',
                    'backgroundColor': COLORS['primary'],
                    'padding': '12px',
                    'borderRadius': '6px',
                    'minWidth': '50px'
                }),
                html.Td([
                    html.Div(f"Chemin {i}: {len(path)} nœuds", 
                            style={'fontWeight': 'bold', 'marginBottom': '8px', 'color': '#333'}),
                    html.Code(path_str, style={
                        'fontFamily': 'monospace',
                        'fontSize': '12px',
                        'padding': '10px',
                        'backgroundColor': '#f5f5f5',
                        'borderRadius': '4px',
                        'display': 'block',
                        'wordBreak': 'break-all',
                        'whiteSpace': 'pre-wrap',
                        'color': '#333',
                        'border': '1px solid #ddd'
                    })
                ], style={
                    'padding': '12px',
                    'color': '#333'
                }),
                html.Td(f"{path_data['length']}", style={
                    'textAlign': 'center',
                    'padding': '12px',
                    'color': '#666',
                    'fontWeight': '500'
                }),
                html.Td(f"{metric_value:.4f}", style={
                    'textAlign': 'center',
                    'color': 'white',
                    'backgroundColor': color,
                    'padding': '12px',
                    'borderRadius': '6px',
                    'fontWeight': 'bold'
                }),
                html.Td(f"{max_risk:.4f}", style={
                    'textAlign': 'center',
                    'padding': '12px',
                    'color': COLORS['danger'],
                    'fontWeight': '500'
                }),
            ], style={
                'borderBottom': f'1px solid {COLORS["light"]}'
            })
        )
    
    table = html.Table([
        html.Thead(
            html.Tr([
                html.Th("#", style={
                    'textAlign': 'center',
                    'padding': '14px',
                    'backgroundColor': COLORS['dark'],
                    'color': 'white',
                    'fontWeight': 'bold',
                    'borderRadius': '6px 0 0 0'
                }),
                html.Th("Chemin", style={
                    'padding': '14px',
                    'backgroundColor': COLORS['dark'],
                    'color': 'white',
                    'fontWeight': 'bold'
                }),
                html.Th("Longueur", style={
                    'textAlign': 'center',
                    'padding': '14px',
                    'backgroundColor': COLORS['dark'],
                    'color': 'white',
                    'fontWeight': 'bold'
                }),
                html.Th("Métrique", style={
                    'textAlign': 'center',
                    'padding': '14px',
                    'backgroundColor': COLORS['dark'],
                    'color': 'white',
                    'fontWeight': 'bold'
                }),
                html.Th("Max Risk", style={
                    'textAlign': 'center',
                    'padding': '14px',
                    'backgroundColor': COLORS['dark'],
                    'color': 'white',
                    'fontWeight': 'bold',
                    'borderRadius': '0 6px 0 0'
                }),
            ])
        ),
        html.Tbody(rows)
    ], style={
        'width': '100%',
        'borderCollapse': 'collapse',
        'marginTop': '15px',
        'backgroundColor': 'white',
        'borderRadius': '8px',
        'overflow': 'hidden'
    })
    
    return table

if __name__ == '__main__':
    print("\n" + "="*70)
    print("🚀 DASHBOARD INTERACTIF - DÉMARRAGE")
    print("="*70)
    print(f"[✓] {len(results_df)} topologies chargées")
    print(f"[✓] {len(critical_paths)} analyses de chemins critiques disponibles")
    print("[*] Accessible à: http://127.0.0.1:8050")
    print("[*] Appuyez sur Ctrl+C pour arrêter")
    print("="*70 + "\n")
    
    app.run(debug=False, host='127.0.0.1', port=8050, dev_tools_ui=False)
