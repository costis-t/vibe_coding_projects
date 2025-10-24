#!/usr/bin/env python3
"""
Network Flow Visualization for Min-Cost Max-Flow Algorithm.
Shows the actual network structure used by the flow solver.
"""
import csv
import argparse
from collections import defaultdict
try:
    import networkx as nx
    import plotly.graph_objects as go
    import numpy as np
except ImportError:
    print("Error: networkx or plotly not installed. Run: pip install networkx plotly")
    exit(1)

def load_allocation(path):
    rows = []
    with open(path, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)
    return rows

def create_network_visualization(rows, output_path="network_flow.html"):
    """Create interactive network flow visualization."""
    
    # Collect unique entities
    students = list({row["student"] for row in rows})
    topics = list({row["assigned_topic"] for row in rows})
    coaches = list({row["assigned_coach"] for row in rows})
    departments = list({row["department_id"] for row in rows})
    
    students.sort()
    topics.sort()
    coaches.sort()
    departments.sort()
    
    # Build flow graph
    G = nx.DiGraph()
    
    # Add nodes with attributes
    for s in students:
        G.add_node(f"S_{s}", node_type="student", label=f"👤 {s}", color="rgba(52, 152, 219, 0.8)")
    
    for t in topics:
        G.add_node(f"T_{t}", node_type="topic", label=f"📚 {t}", color="rgba(46, 204, 113, 0.8)")
    
    for c in coaches:
        G.add_node(f"C_{c}", node_type="coach", label=f"🏛️ {c}", color="rgba(155, 89, 182, 0.8)")
    
    for d in departments:
        G.add_node(f"D_{d}", node_type="dept", label=f"🏢 {d}", color="rgba(241, 196, 15, 0.8)")
    
    # Add source and sink
    G.add_node("SOURCE", node_type="source", label="SOURCE", color="rgba(39, 174, 96, 0.9)")
    G.add_node("SINK", node_type="sink", label="SINK", color="rgba(230, 126, 34, 0.9)")
    
    # Add edges with flow information
    flow_by_edge = defaultdict(int)
    satisfaction_by_edge = defaultdict(list)
    
    for row in rows:
        s = row["student"]
        t = row["assigned_topic"]
        c = row["assigned_coach"]
        d = row["department_id"]
        rank = int(row["preference_rank"])
        
        # Source → Student
        edge_key = (f"SOURCE", f"S_{s}")
        flow_by_edge[edge_key] += 1
        
        # Student → Topic
        edge_key = (f"S_{s}", f"T_{t}")
        flow_by_edge[edge_key] += 1
        satisfaction_by_edge[edge_key].append(rank)
        
        # Topic → Coach
        edge_key = (f"T_{t}", f"C_{c}")
        flow_by_edge[edge_key] += 1
        
        # Coach → Department
        edge_key = (f"C_{c}", f"D_{d}")
        flow_by_edge[edge_key] += 1
        
        # Department → Sink
        edge_key = (f"D_{d}", "SINK")
        flow_by_edge[edge_key] += 1
    
    # Add edges to graph
    rank_colors = {
        0: "rgba(46, 204, 113, 0.6)", 1: "rgba(52, 152, 219, 0.6)", 2: "rgba(155, 89, 182, 0.6)",
        10: "rgba(52, 152, 219, 0.6)", 11: "rgba(241, 196, 15, 0.6)", 12: "rgba(230, 126, 34, 0.6)",
        13: "rgba(231, 76, 60, 0.6)", 14: "rgba(192, 57, 43, 0.6)", 999: "rgba(149, 165, 166, 0.6)",
    }
    
    for (source, target), flow in flow_by_edge.items():
        if source in G and target in G:
            # Determine edge color based on satisfaction
            if (source, target) in satisfaction_by_edge:
                avg_rank = sum(satisfaction_by_edge[(source, target)]) / len(satisfaction_by_edge[(source, target)])
                color = rank_colors.get(int(avg_rank), "rgba(200, 200, 200, 0.6)")
            else:
                color = "rgba(200, 200, 200, 0.6)"
            
            G.add_edge(source, target, flow=flow, color=color, width=max(1, flow * 0.5))
    
    # Use spring layout for better visualization
    pos = nx.spring_layout(G, k=3, iterations=50, seed=42)
    
    # Extract coordinates
    x_nodes = [pos[node][0] for node in G.nodes()]
    y_nodes = [pos[node][1] for node in G.nodes()]
    node_colors = [G.nodes[node].get('color', 'rgba(100, 100, 100, 0.8)') for node in G.nodes()]
    node_labels = [G.nodes[node].get('label', node) for node in G.nodes()]
    
    # Edge traces
    edge_traces = []
    for (source, target) in G.edges():
        x = [pos[source][0], pos[target][0]]
        y = [pos[source][1], pos[target][1]]
        flow = G[source][target].get('flow', 0)
        color = G[source][target].get('color', 'rgba(200, 200, 200, 0.5)')
        width = G[source][target].get('width', 1)
        
        edge_trace = go.Scatter(
            x=x, y=y,
            mode='lines',
            line=dict(width=width, color=color),
            hoverinfo='text',
            text=f"{source} → {target}<br>Flow: {flow}",
            showlegend=False
        )
        edge_traces.append(edge_trace)
    
    # Node trace
    node_trace = go.Scatter(
        x=x_nodes, y=y_nodes,
        mode='markers+text',
        marker=dict(size=15, color=node_colors, line=dict(width=2, color="white")),
        text=node_labels,
        textposition="top center",
        hoverinfo='text',
        hovertext=[f"{label}" for label in node_labels],
        showlegend=False
    )
    
    # Create figure
    fig = go.Figure(data=edge_traces + [node_trace])
    
    fig.update_layout(
        title={
            "text": "Min-Cost Max-Flow Network Visualization",
            "x": 0.5, "xanchor": "center",
            "font": {"size": 24, "color": "#333"}
        },
        showlegend=False,
        hovermode='closest',
        margin=dict(b=0, l=0, r=0, t=50),
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        plot_bgcolor='rgba(240, 240, 240, 1)',
        paper_bgcolor='white',
        height=800,
    )
    
    fig.add_annotation(
        text="<b>Network Flow Structure:</b> SOURCE → Students → Topics → Coaches → Departments → SINK<br>" +
             "<i>Edge thickness represents flow volume | Colors show satisfaction level</i>",
        xref="paper", yref="paper", x=0.5, y=1.05,
        showarrow=False, font=dict(size=11, color="#666"), xanchor="center",
    )
    
    fig.write_html(output_path, auto_open=False)
    return output_path

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create network flow visualization")
    parser.add_argument("--allocation", required=True, help="Path to allocation.csv")
    parser.add_argument("--output", default="network_flow.html", help="Output HTML path")
    args = parser.parse_args()
    
    print(f"Loading allocation from {args.allocation}...")
    rows = load_allocation(args.allocation)
    
    print(f"Building network graph...")
    output_path = create_network_visualization(rows, args.output)
    
    print(f"✓ Network visualization created: {output_path}")
    print(f"\nOpen in browser: file://{output_path}")
