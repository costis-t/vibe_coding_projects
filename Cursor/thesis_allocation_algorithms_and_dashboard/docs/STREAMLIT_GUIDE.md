# Streamlit Dashboard Guide - Thesis Allocation System

Interactive web-based interface for configuring, running, and analyzing thesis allocations.

## 🚀 Quick Start

### 1. Installation

```bash
cd /home/username/thesis_allocation/cursors_thesis_allocation
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -r requirements.txt
```

### 2. Launch Dashboard

```bash
streamlit run viz_streamlit_dashboard.py
```

The dashboard will open in your browser at `http://localhost:8501`

## 📋 Dashboard Features

### 🏠 Home Page
- Welcome and getting started information
- Quick start guide (5-step process)
- File management options
- Load default data or upload custom CSV files

### ⚙️ Configuration Page
**Preference Settings:**
- Allow Unranked Topics (toggle)
- Tier 2 Cost (slider: 0-10)
- Tier 3 Cost (slider: 0-20)
- Unranked Cost (slider: 0-500)
- Top-2 Bias (toggle)

**Capacity Settings:**
- Enable Topic Overflow (toggle)
- Enable Coach Overflow (toggle)
- Department Min Mode (soft/hard)
- Department Shortfall Penalty (slider: 0-5000)
- Topic Overflow Penalty (slider: 0-2000)
- Coach Overflow Penalty (slider: 0-2000)

**Solver Settings:**
- Algorithm Selection (ilp/flow/hybrid)
- Time Limit (0-600 seconds)
- Random Seed (optional, for reproducibility)
- Epsilon Suboptimal (0.0-1.0, for near-optimal solutions)

**Save Configuration:**
- Click "💾 Save Configuration" to export as JSON

### 📊 Results Analysis
**Upload Results:**
1. Upload allocation CSV file
2. Upload summary TXT file

**Visualizations:**
- **Key Metrics Dashboard:**
  - Total Students Assigned
  - Percentage with Ranked Choice
  - Optimal Cost
  - Assignment Status

- **Preference Satisfaction Chart** - Bar chart showing preference ranks
- **Department Distribution** - Pie chart of students per department
- **Topic Capacity Utilization** - Overlaid bar chart (used vs. total)

**Data Table:**
- Full allocation details
- Sortable and searchable
- Download as CSV button

### 🔍 Data Explorer
Browse input data before allocation:

**Students:**
- Total count
- Preview first 10 rows
- All columns visible

**Topics:**
- Total count
- Preview first 10 rows
- Capacity information

**Coaches:**
- Total count
- Coach capacities
- Deduplicates per coach

### 📈 Advanced Charts
**Cost Matrix Heatmap:**
- Interactive heatmap of student-topic assignments
- Color-coded by cost (red=high, green=low)
- Hover for exact values
- Sample of first 50 students

**Summary Statistics:**
- Cost Distribution histogram
- Preference Rank Distribution histogram
- Statistical summaries

## 📂 Typical Workflow

### 1. Configure Settings
```
Navigate to Configuration Page
  ↓
Set your preferred parameters (sliders, toggles)
  ↓
Click "Save Configuration"
  ↓
Configuration saved to config_streamlit.json
```

### 2. Prepare Data
```
Home Page → Upload Custom Data
  ↓
Or use default data
  ↓
Files ready for allocation
```

### 3. Run Allocation (CLI)
```bash
# Use the configuration saved from dashboard
python allocate.py \
  --config config_streamlit.json \
  --students data/input/students.csv \
  --capacities data/input/capacities.csv \
  --out data/output/allocation.csv \
  --summary data/output/summary.txt
```

### 4. Analyze Results
```
Navigate to Results Analysis
  ↓
Upload allocation.csv and summary.txt
  ↓
View metrics and charts
  ↓
Download results if needed
```

## 🎨 Visualization Types

### Preference Satisfaction Chart
- **Type**: Bar chart
- **X-axis**: Choice rank (1st, 2nd, 3rd, etc.)
- **Y-axis**: Number of students
- **Color**: Gradient (Viridis colormap)
- **Insight**: Shows preference coverage quality

### Department Distribution Chart
- **Type**: Pie chart
- **Segments**: Each department
- **Size**: Proportional to student count
- **Insight**: Department load balance

### Capacity Utilization Chart
- **Type**: Grouped bar chart
- **Groups**: Each topic
- **Bars**: Used (blue) vs. Total capacity (gray)
- **Insight**: Over/under-utilization

### Cost Matrix Heatmap
- **Type**: 2D heatmap
- **Rows**: Students (first 50)
- **Columns**: Topics
- **Color**: Cost value (red=high, green=low)
- **Insight**: Cost distribution patterns

### Cost Distribution Histogram
- **Type**: Histogram
- **X-axis**: Effective cost
- **Y-axis**: Frequency
- **Bins**: 30
- **Insight**: Cost spread

### Preference Rank Distribution Histogram
- **Type**: Histogram
- **X-axis**: Preference rank (-1, 0-2, 10-14, 999)
- **Y-axis**: Frequency
- **Bins**: 20
- **Insight**: Preference satisfaction spread

## 💡 Tips & Tricks

### 1. Session State
Streamlit tracks state within a session. Settings are preserved while navigating pages within the same session.

### 2. File Uploading
- Upload CSVs directly in the dashboard
- No need to save files locally
- Reusable across pages

### 3. Configuration Export
Saved configurations can be:
- Used with CLI tool
- Shared with team members
- Version controlled in git
- Modified manually as JSON

### 4. Data Exploration
Use Data Explorer to:
- Preview files before allocation
- Identify data quality issues
- Verify topic/coach counts
- Check column names

### 5. Performance
- Large datasets (1000+ students) may be slow
- Use flow algorithm for faster preview
- Use time limits to cap solver execution

## 🔧 Configuration Examples

### Conservative (High Quality, Slow)
```
Algorithm: hybrid
Time Limit: 600 seconds
Epsilon: 0.0
Dept Min Mode: hard
```

### Balanced (Good Speed, Good Quality)
```
Algorithm: flow
Time Limit: 30 seconds
Epsilon: 0.05
Dept Min Mode: soft
```

### Fast (Quick Preview)
```
Algorithm: flow
Time Limit: 10 seconds
Epsilon: 0.1
Dept Min Mode: soft
```

## 📊 Interpreting Results

### Key Metrics
- **Total Students Assigned**: Should equal input count (or close to it)
- **Got Ranked Choice %**: Percentage getting preferences (higher is better)
- **Optimal Cost**: Lower is better (objective value)
- **Assignment Status**: "✓ All Assigned" is ideal

### Capacity Utilization
- **Full bars**: Good utilization
- **Short bars**: Underutilization
- **Overflow**: Some students beyond capacity (if enabled)

### Preference Satisfaction
- **High 1st choice**: Students happy
- **Low ranks**: Students got low preferences
- **Unranked**: Students in unranked topics

### Department Distribution
- **Even slices**: Fair distribution
- **Imbalanced**: Some departments underutilized

## 🐛 Troubleshooting

### Dashboard won't start
```bash
# Check Streamlit installation
streamlit --version

# Try again with verbose output
streamlit run viz_streamlit_dashboard.py --logger.level=debug
```

### Charts not appearing
- Check file upload format (must be CSV or TXT)
- Verify column names match expected format
- Try uploading allocation results from CLI first

### Slow performance
- Use flow algorithm instead of ILP
- Reduce time limit
- Upload smaller datasets first
- Restart dashboard and clear cache

### Configuration not saving
- Check file write permissions
- Verify output directory exists
- Try manual JSON edit as alternative

## 📞 Support

### Documentation
- README.md - System overview
- ARCHITECTURE.md - System design
- QUICK_EXAMPLES.md - Command examples
- config.example.json - Config reference

### Debugging
Enable debug logging in configuration:
```
See logs in browser console (F12)
Check terminal output for error messages
```

### Common Issues
**"Module not found" errors**
→ Install missing dependencies: `pip install -r requirements.txt`

**Charts display empty**
→ Upload both allocation.csv AND summary.txt files

**Configuration won't save**
→ Check directory permissions, create data/output if missing

**Slow allocation**
→ Use "flow" algorithm, set lower time limit, or use smaller dataset

## 🚀 Advanced Usage

### Multi-session Comparison
1. Configure and run allocation A
2. Download results
3. Reconfigure for allocation B
4. Download results
5. Compare side-by-side (excel or separate browser tabs)

### Batch Analysis
1. Run multiple allocations via CLI
2. Upload results sequentially to dashboard
3. Create comparison spreadsheet

### Parameter Tuning
1. Start with default config
2. Adjust one parameter at a time
3. Observe impact in visualizations
4. Save final configuration

## 📈 Next Steps

After analyzing results:
1. **Export results**: Download allocation CSV
2. **Share findings**: Screenshot charts
3. **Iterate**: Try different configurations
4. **Finalize**: Save best configuration for production use
5. **Document**: Note parameter choices and outcomes

## 🎯 Best Practices

✓ **Always validate first**: Use CLI --validate-only before running
✓ **Test with small data**: Try flow algorithm on subset first
✓ **Save configurations**: Document decision parameters
✓ **Check constraints**: Review capacities before allocation
✓ **Analyze thoroughly**: Study visualizations, not just numbers
✓ **Keep backups**: Save results from successful runs
✓ **Version control**: Track config and result changes

---

**Version**: Professional Edition with Streamlit Dashboard
**Last Updated**: 2024
