#!/usr/bin/env python3
import csv
import argparse
try:
    import plotly.graph_objects as go
except ImportError:
    print("Error: plotly not installed. Run: pip install plotly")
    exit(1)

def load_allocation(path):
    rows = []
    with open(path, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)
    return rows

def create_sankey_html(rows, output_path="sankey_enhanced.html"):
    students = []
    topics = []
    coaches = []
    departments = []
    
    for row in rows:
        s = row["student"]
        t = row["assigned_topic"]
        c = row["assigned_coach"]
        d = row["department_id"]
        if s not in students: students.append(s)
        if t not in topics: topics.append(t)
        if c not in coaches: coaches.append(c)
        if d not in departments: departments.append(d)
    
    students.sort()
    topics.sort()
    coaches.sort()
    departments.sort()
    
    # Create labels with icons
    labels = (
        [f"👤 {s}" for s in students] + 
        [f"📚 {t}" for t in topics] + 
        [f"👨‍🏫 {c}" for c in coaches] + 
        [f"🏛️ {d}" for d in departments]
    )
    
    source, target, value, color, hovertext = [], [], [], [], []
    
    # Preference rank colors with labels
    rank_colors = {
        -1: "rgba(255, 0, 0, 0.7)",       # Red: Forced assignment
        0: "rgba(46, 204, 113, 0.7)",     # Green: Tier 1 (best)
        1: "rgba(52, 152, 219, 0.7)",     # Blue: Tier 2
        2: "rgba(155, 89, 182, 0.7)",     # Purple: Tier 3
        10: "rgba(52, 152, 219, 0.7)",    # Blue: 1st ranked choice
        11: "rgba(241, 196, 15, 0.7)",    # Yellow: 2nd choice
        12: "rgba(230, 126, 34, 0.7)",    # Orange: 3rd choice
        13: "rgba(231, 76, 60, 0.7)",     # Red: 4th choice
        14: "rgba(192, 57, 43, 0.7)",     # Dark red: 5th choice
        999: "rgba(149, 165, 166, 0.7)",  # Gray: Unranked
    }
    
    rank_labels = {
        -1: "Forced",
        0: "Tier 1",
        1: "Tier 2",
        2: "Tier 3",
        10: "1st Choice",
        11: "2nd Choice",
        12: "3rd Choice",
        13: "4th Choice",
        14: "5th Choice",
        999: "Unranked",
    }
    
    for row in rows:
        s, t, c, d = row["student"], row["assigned_topic"], row["assigned_coach"], row["department_id"]
        rank = int(row["preference_rank"])
        
        s_idx = students.index(s)
        t_idx = len(students) + topics.index(t)
        c_idx = len(students) + len(topics) + coaches.index(c)
        d_idx = len(students) + len(topics) + len(coaches) + departments.index(d)
        
        # Student → Topic (colored by preference rank, with rank label in hover)
        source.append(s_idx)
        target.append(t_idx)
        value.append(1)
        rank_label = rank_labels.get(rank, "Unknown")
        color.append(rank_colors.get(rank, "rgba(200, 200, 200, 0.7)"))
        hovertext.append(f"{s} → {t}<br>Preference: {rank_label} (Rank: {rank})")
        
        # Topic → Coach (neutral gray)
        source.append(t_idx)
        target.append(c_idx)
        value.append(1)
        color.append("rgba(200, 200, 200, 0.5)")
        hovertext.append(f"{t} → {c}")
        
        # Coach → Department (neutral gray)
        source.append(c_idx)
        target.append(d_idx)
        value.append(1)
        color.append("rgba(200, 200, 200, 0.5)")
        hovertext.append(f"{c} → {d}")
    
    fig = go.Figure(data=[go.Sankey(
        node=dict(
            pad=20, 
            thickness=20, 
            line=dict(color="#333", width=1), 
            label=labels,
            color=[
                "rgba(52, 152, 219, 0.8)" if "👤" in l else 
                "rgba(46, 204, 113, 0.8)" if "📚" in l else 
                "rgba(241, 196, 15, 0.8)" if "👨‍🏫" in l else 
                "rgba(155, 89, 182, 0.8)" 
                for l in labels
            ],
        ),
        link=dict(
            source=source, 
            target=target, 
            value=value, 
            color=color,
            customdata=hovertext,
            hovertemplate='%{customdata}<extra></extra>'
        ),
        arrangement="snap",
    )])
    
    fig.update_layout(
        title={
            "text": "Thesis Allocation - Sankey Diagram (Student → Topic → Coach → Department)", 
            "x": 0.5, 
            "xanchor": "center", 
            "font": {"size": 24, "color": "#333"}
        },
        font=dict(size=11, family="Arial"), 
        plot_bgcolor="rgba(240, 240, 240, 1)", 
        paper_bgcolor="white", 
        height=950,
        margin=dict(l=50, r=50, t=80, b=220), 
        hovermode="closest",
    )
    
    # Enhanced annotation with preference legend at BOTTOM
    fig.add_annotation(
        text=(
            "<b>Column Legend:</b> <b>👤 Students (Blue)</b> → <b>📚 Topics (Green)</b> → <b>👨‍🏫 Coaches (Yellow)</b> → <b>🏛️ Departments (Purple)</b><br><br>"
            "<b>Preference Colors (Student→Topic flow):</b> "
            "<span style='color:rgb(46, 204, 113)'>■</span> Tier 1 or 1st Choice (Green)  |  "
            "<span style='color:rgb(52, 152, 219)'>■</span> Tier 2/Ranked (Blue)  |  "
            "<span style='color:rgb(155, 89, 182)'>■</span> Tier 3 (Purple)  |  "
            "<span style='color:rgb(241, 196, 15)'>■</span> 2nd Choice (Yellow)  |  "
            "<span style='color:rgb(230, 126, 34)'>■</span> 3rd Choice (Orange)  |  "
            "<span style='color:rgb(231, 76, 60)'>■</span> 4th Choice (Red)  |  "
            "<span style='color:rgb(192, 57, 43)'>■</span> 5th Choice (Dark Red)  |  "
            "<span style='color:rgb(149, 165, 166)'>■</span> Unranked (Gray)"
        ),
        xref="paper", 
        yref="paper", 
        x=0.5, 
        y=-0.15, 
        showarrow=False, 
        font=dict(size=10, color="#333"), 
        xanchor="center",
        align="center",
    )
    
    fig.write_html(output_path, auto_open=False)
    return output_path

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create enhanced Sankey diagram")
    parser.add_argument("--allocation", required=True, help="Path to allocation.csv")
    parser.add_argument("--output", default="sankey_enhanced.html", help="Output HTML path")
    args = parser.parse_args()
    
    print(f"Loading allocation from {args.allocation}...")
    rows = load_allocation(args.allocation)
    print(f"Creating Sankey diagram...")
    output_path = create_sankey_html(rows, args.output)
    print(f"✓ Sankey diagram created: {output_path}")
