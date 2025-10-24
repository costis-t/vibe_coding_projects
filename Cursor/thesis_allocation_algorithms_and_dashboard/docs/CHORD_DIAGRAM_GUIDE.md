# Chord Diagram Visualization Guide

## Overview

**Chord diagrams** provide an elegant, interactive way to visualize the thesis allocation flow. They show how students flow through topics to reach coaches in a circular, interconnected layout.

---

## What You Get

### 1. **chord_comparison.html** ⭐ Start Here
**Side-by-side comparison of all three algorithms**

Contains:
- ILP, Flow, and Hybrid chord diagrams together
- Legend explaining colors
- Statistics table comparing metrics
- All interactive

**Open in browser:** `file://chord_comparison.html`

### 2. Individual Chord Diagrams

- **chord_ilp.html** - ILP algorithm allocation
- **chord_flow.html** - Min-cost max-flow algorithm allocation  
- **chord_hybrid.html** - Hybrid algorithm allocation

Each is 58KB and loads in seconds.

---

## How to Read a Chord Diagram

### Layout

```
        Students (Blue)
       /      |      \
    (many chords showing assignments)
   /          |          \
Topics (Green) - Coaches (Purple)
```

### Elements

| Element | What It Represents |
|---------|-------------------|
| **Blue Ring** | 80 students (S01-S80) |
| **Green Ring** | 23 topics (T01-T23) |
| **Purple Ring** | 21 coaches (Coach01-Coach25) |
| **Chord (Line)** | Student→Topic connection |
| **Chord Width** | Number of students sharing connection |
| **Chord Color** | Satisfaction level |

### Colors

```
🔵 Blue   = 1st choice assignment (most satisfied)
🟠 Orange = 2nd choice assignment
🔴 Red    = Low preference assignment
⚪ Gray   = Other connections
```

### Interactions

**Hover Effects:**
- Hover over any chord → Highlights connection
- Shows tooltip: "StudentID → TopicID"
- Chord becomes darker and thicker

**Visual Feedback:**
- Arc becomes darker on hover
- Chord opacity increases
- Tooltip appears near cursor

---

## Key Observations

### What to Look For

1. **Chord Density**
   - Dense web = many equally-good alternatives
   - Sparse web = preferences are concentrated

2. **Color Distribution**
   - More blue = more 1st choices (happier students)
   - More red = more compromises (less happy)

3. **Coach Distribution**
   - How evenly students are spread across coaches
   - Thicker arcs = more loaded coaches
   - Thin arcs = underutilized coaches

4. **Pattern Differences**
   - Compare how ILP, Flow, and Hybrid patterns differ
   - ILP might show more balanced load
   - Flow might show more clustered assignments
   - Hybrid shows best trade-off

---

## Algorithm Comparison in Chord Diagrams

### ILP (Left)
```
Expected Pattern:
- Moderately distributed connections
- Mix of blue, orange, red chords
- Balanced coach loads
```

**Why:** ILP optimizes with penalty balancing. Some students get unranked to achieve fairness.

### Flow (Middle)
```
Expected Pattern:
- More structured, fewer chords
- Mostly blue connections (1st choices)
- Some coaches heavily loaded
```

**Why:** Flow directly minimizes preferences without penalty overhead. Results in more 1st choices but less balanced load.

### Hybrid (Right)
```
Expected Pattern:
- Very similar to Flow
- Mostly blue connections
- Hybrid picked Flow as better
```

**Why:** Hybrid ran both and selected the better result. In this case, Flow wins.

---

## Statistics Legend

### Metrics Shown

| Metric | What It Means | Ideal |
|--------|---------------|-------|
| **1st Choice %** | Students getting their 1st choice | Higher is better |
| **2nd Choice %** | Students getting their 2nd choice | Lower when 1st is high |
| **Unranked %** | Students with unranked assignments | Lower is better |
| **Capacity OK** | All coach capacities respected | ✓ Yes |
| **Gini Coefficient** | Fairness measure (0=fair, 1=unfair) | Lower is fairer |
| **Objective Value** | Optimization score (lower is better) | Lower |
| **Speed** | Algorithm runtime | Very Fast > Medium > Slow |
| **Uniqueness** | Is solution deterministic? | Unique > Non-unique |

---

## Usage Examples

### For Presentation/Thesis

1. **Show chord_comparison.html** to your supervisor
   - Impressive visual
   - Professional appearance
   - Easy to understand
   - Tells the complete story

2. **Print as PNG** (Mac: Screenshot, Windows: Snipping Tool)
   - Insert into thesis/report
   - Shows all three algorithms at once
   - Beautiful visual aid

### For Decision Making

1. Open **chord_ilp.html** in one tab
2. Open **chord_flow.html** in another tab
3. Open **chord_hybrid.html** in a third tab
4. Compare side-by-side
5. Notice pattern differences
6. Decide which algorithm fits your requirements

### For Data Analysis

1. Hover over specific students
2. See which topic they got
3. Verify assignments
4. Check fairness visually
5. Identify outliers

---

## Technical Details

### How It Works

1. **Python Script** (`viz_chord_diagram.py`)
   - Reads allocation.csv
   - Builds chord matrix (students × topics × coaches)
   - Generates HTML with embedded D3.js code

2. **Visualization** (D3.js)
   - D3 chord layout algorithm
   - Circular arrangement
   - Interactive ribbons
   - Real-time hover detection

3. **Output**
   - Self-contained HTML file
   - No external dependencies needed
   - Works in any modern browser
   - 58KB file size

### Browser Requirements

- Modern browser (Chrome, Firefox, Safari, Edge)
- JavaScript enabled
- No internet connection needed (all D3.js embedded)

---

## Creating Your Own

### Generate Chord Diagrams

```bash
# For any allocation file
python3 viz_chord_diagram.py \
  --allocation allocation.csv \
  --output my_chord.html

# Or use the batch script
for algo in ilp flow hybrid; do
  python3 allocate.py ... --algorithm $algo --out alloc_$algo.csv
  python3 viz_chord_diagram.py --allocation alloc_$algo.csv \
    --output chord_$algo.html
done
```

### Customize Comparison Page

Edit `viz_chord_comparison.html` to:
- Add your own statistics
- Change colors/styling
- Add narrative text
- Include algorithm descriptions

---

## Troubleshooting

### Chord Diagram Won't Load

**Problem:** Blank page
**Solution:** 
- Ensure chord_ilp.html, chord_flow.html, chord_hybrid.html exist in same directory
- Check browser console for errors (F12)
- Try in different browser

### Slow Loading

**Problem:** Takes >5 seconds to load
**Solution:**
- Normal for first load (D3.js library loading)
- Subsequent loads are instant (browser cache)
- Try refreshing page

### Can't See Labels

**Problem:** Student/Coach/Topic names too small
**Solution:**
- Zoom in (Ctrl/Cmd +)
- Hover over nodes to see names in tooltip
- Check individual chord_*.html files (larger view)

---

## Advanced Usage

### Creating a Dashboard

```bash
# Combine with Streamlit
streamlit run dashboard.py
```

Include tabs:
- Chord Diagrams
- Statistics
- Individual allocations
- Filter by coach

### Exporting for Reports

```bash
# Mac
screencapture -l$(osascript -e 'id of window 1 of app "Chrome"') chord.png

# Windows - Use Snipping Tool or:
# Open in Chrome → Print → Save as PDF

# Linux
import -window root chord.png
```

---

## FAQ

**Q: Why is the diagram circular?**
A: Circular layout shows connections elegantly without edge overlap. D3's chord algorithm optimizes for clarity.

**Q: Can I interact with the PDF version?**
A: No, interactivity requires HTML/JavaScript. Export as HTML for full interactivity.

**Q: How many students can I visualize?**
A: Tested up to 500+ students. Performance depends on browser. >1000 students might be slow.

**Q: Can I add my own data?**
A: Yes! Run `viz_chord_diagram.py` on any allocation.csv file.

---

## Next Steps

1. **View the diagrams**
   - Open chord_comparison.html in your browser
   - Explore each algorithm's visualization
   - Notice the differences

2. **Make a decision**
   - Which algorithm's pattern looks best?
   - Which matches your fairness criteria?
   - Use statistics table to compare

3. **Present results**
   - Screenshot for thesis/report
   - Show comparison page to supervisor
   - Discuss algorithm trade-offs

---

**Generated:** October 23, 2025  
**Format:** Interactive D3.js Chord Diagrams  
**File Size:** ~58KB each  
**Browser:** Chrome, Firefox, Safari, Edge  

