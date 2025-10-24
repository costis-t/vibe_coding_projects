# 🎓 Streamlit Dashboard - Quick Start

Get beautiful interactive visualizations running in 2 minutes!

## ⚡ Super Quick Start

### Option 1: Using the Launcher Script (Easiest)
```bash
cd /path/to/thesis_allocation/cursors_thesis_allocation
./run_dashboard.sh
```

### Option 2: Manual Commands
```bash
cd /path/to/thesis_allocation/cursors_thesis_allocation
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
streamlit run viz_streamlit_dashboard.py
```

**Result**: Browser opens to `http://localhost:8501` 🎉

## 📊 What You Get

### 5 Interactive Pages

**🏠 Home**
- Welcome screen
- Quick start guide
- Load sample data
- Upload custom files

**⚙️ Configuration**
- 15+ interactive sliders and toggles
- Real-time parameter adjustment
- Save configuration as JSON
- Export to use with CLI

**📊 Results Analysis**
- Upload allocation results
- View 4 key metrics
- 3 beautiful charts:
  - Preference satisfaction
  - Department distribution  
  - Capacity utilization
- Interactive data table
- Download results

**🔍 Data Explorer**
- Browse student data
- View topic information
- See coach details
- Check data quality

**📈 Advanced Charts**
- Cost matrix heatmap
- Cost distribution histogram
- Preference rank distribution
- Statistical summaries

## 🎯 Typical Usage

### Workflow 1: Configure & Visualize
```
1. Go to ⚙️ Configuration
2. Adjust sliders to your preferences
3. Click "💾 Save Configuration"
4. Use saved config with CLI:
   
   python allocate.py --config config_streamlit.json \
     --students data/input/students.csv \
     --capacities data/input/capacities.csv \
     --out data/output/allocation.csv \
     --summary data/output/summary.txt

5. Go to 📊 Results Analysis
6. Upload allocation.csv and summary.txt
7. View beautiful visualizations!
```

### Workflow 2: Explore Data
```
1. Go to 🔍 Data Explorer
2. Upload your students.csv and capacities.csv
3. Browse data before allocation
4. Verify counts and columns
5. Ready to run allocation
```

### Workflow 3: Compare Results
```
1. Run allocation A (save results)
2. Upload results to dashboard
3. Screenshot/download charts
4. Reconfigure and run allocation B
5. Upload and compare side-by-side
```

## 🎨 Interactive Features

### Sliders
- Adjust costs in real-time
- Set time limits
- Control penalties

### Toggles
- Enable/disable features
- Adjust modes
- Quick experiments

### File Upload
- Drag & drop support
- Multiple formats (CSV, TXT)
- Real-time preview

### Charts
- Hover for details
- Zoom & pan
- Download as PNG
- Interactive legend

### Data Table
- Sort by column
- Search/filter
- Copy data
- Download as CSV

## 💡 Example Scenarios

### Scenario 1: Test Different Algorithms
```
⚙️ Configuration:
  - Set Algorithm to "flow"
  - Set Time Limit to 30 seconds
  - Save and run CLI command

Then:
  - ⚙️ Configuration
  - Change Algorithm to "hybrid"  
  - Set Time Limit to 120 seconds
  - Save and run again

Then:
  - 📊 Results Analysis
  - Upload flow results
  - Screenshot
  - Upload hybrid results
  - Compare charts
```

### Scenario 2: Parameter Tuning
```
1. Go to ⚙️ Configuration
2. Start with defaults
3. Adjust Tier 2 Cost slider
4. Save and run allocation
5. View results in 📊 Results Analysis
6. Note the impact
7. Try different value
8. Repeat until satisfied
```

### Scenario 3: Quality Check
```
1. Go to 🔍 Data Explorer
2. Upload students.csv
3. Note: Total students = ?
4. Upload capacities.csv
5. Note: Total topics = ?
6. Note: Total coaches = ?
7. Run allocation
8. Check 📊 Results Analysis
9. Verify all students assigned
```

## 📈 Interpreting Charts

### Preference Satisfaction Bar Chart
- **X-axis**: 1st choice, 2nd choice, 3rd choice, etc.
- **Height**: Number of students
- **Goal**: Tall left bars (most got preferences)
- **Action**: If low, relax constraints

### Department Distribution Pie Chart
- **Slices**: Each department
- **Size**: Student count
- **Goal**: Even distribution
- **Action**: If imbalanced, adjust dept_min_mode

### Capacity Utilization Bar Chart
- **Pairs**: Used (blue) vs. Total (gray)
- **Goal**: Blue bars near gray (well utilized)
- **Action**: If many empty, consider fewer topics

### Cost Matrix Heatmap
- **Color**: Red=high cost, Green=low cost
- **Goal**: Mostly green (low costs)
- **Action**: If red, students got poor matches

### Cost Distribution Histogram
- **Shape**: Distribution of effective costs
- **Goal**: Left-skewed (most low costs)
- **Action**: High average = poor allocation

## 🔧 Configuration Presets

### Fast Preview (2-5 seconds)
```
Algorithm: flow
Time Limit: 10 seconds
Epsilon: 0.1
Dept Min: soft
```

### Balanced (30-60 seconds)
```
Algorithm: hybrid
Time Limit: 60 seconds
Epsilon: 0.05
Dept Min: soft
```

### Production (high quality, slow)
```
Algorithm: ilp
Time Limit: 300 seconds
Epsilon: 0.0
Dept Min: hard
```

## 🚀 Pro Tips

### 1. Use Keyboard Shortcuts
- `r` - Rerun script
- `c` - Clear cache
- `q` - Quit

### 2. Session Management
- Each browser tab = separate session
- Settings preserved while navigating
- Refresh page to reset

### 3. File Management
- Upload same files multiple times (no conflicts)
- Files not saved (temporary upload)
- Download results for persistence

### 4. Performance Optimization
- Use "flow" for testing
- Use "ilp" for final allocation
- Set reasonable time limits
- Work with smaller samples first

### 5. Configuration Sharing
- Save config to JSON
- Share config file with team
- Use same config for reproducibility
- Version control configs in git

## 🐛 Troubleshooting

### Dashboard won't start
```bash
# Check dependencies
pip install -r requirements.txt

# Check Python version (3.8+)
python --version

# Try direct run
streamlit run viz_streamlit_dashboard.py --logger.level=debug
```

### Charts appear blank
```
→ Upload both allocation.csv AND summary.txt
→ Check file format (exact columns needed)
→ Try re-uploading files
```

### Configuration won't save
```
→ Check folder exists: data/output
→ Create if missing: mkdir -p data/output
→ Check write permissions
```

### Dashboard running slowly
```
→ Close other browser tabs
→ Use flow algorithm (not ilp)
→ Set lower time limit
→ Reduce data size
```

## 📚 Full Documentation

For detailed information, see:
- **STREAMLIT_GUIDE.md** - Complete feature guide
- **README.md** - System overview
- **QUICK_EXAMPLES.md** - More examples

## 🎉 You're Ready!

```
✓ Streamlit installed
✓ Dashboard ready
✓ Sample data available
✓ All visualizations working

Next step: Run `./run_dashboard.sh` and explore!
```

## 📞 Need Help?

```bash
# Show all command options
python allocate.py --help

# Validate input data
python allocate.py --validate-only \
  --students data/input/students.csv \
  --capacities data/input/capacities.csv

# Run with logging
python allocate.py \
  --students data/input/students.csv \
  --capacities data/input/capacities.csv \
  --out data/output/allocation.csv \
  --summary data/output/summary.txt \
  --log-level DEBUG \
  --log-file debug.log
```

---

**Happy Allocating! 🎓📊✨**
