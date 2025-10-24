# 🚀 Run Allocation from Dashboard - Complete Guide

## Overview

**YES! You can now run allocations directly from the dashboard!** 🎉

No more switching between CLI and browser - everything is integrated in the Streamlit dashboard.

## What's New

A new **"🚀 Run Allocation"** page has been added to the dashboard that allows you to:

✅ Upload input files directly  
✅ Configure algorithm settings  
✅ Run the allocation with live progress  
✅ View results immediately  
✅ Download results in one click  

## How to Use

### Step 1: Launch the Dashboard

```bash
./run_dashboard.sh
```

### Step 2: Go to "🚀 Run Allocation" Page

Click the **"🚀 Run Allocation"** option in the sidebar.

### Step 3: Upload Input Files

**Left side - Input Files:**
- Upload **Students CSV** (required)
- Upload **Capacities CSV** (required)
- Upload **Overrides CSV** (optional)

**Right side - Algorithm Settings:**
- Select **Algorithm**: ilp, flow, or hybrid
- Set **Time Limit**: 0-600 seconds
- (Optional) Set **Random Seed** for reproducibility

### Step 4: View Validation

After uploading files, you'll see:
- ✓ Number of students
- ✓ Number of topics/capacities
- ✓ Column names (preview)

### Step 5: Click "▶️ Run Allocation"

Press the blue **"▶️ Run Allocation"** button to start.

### Step 6: Watch Progress

Live status messages show:
- 📂 Loading data...
- ✓ Loaded X students, Y topics
- 🔍 Validating data...
- ✓ Validation passed
- 🎯 Building preference model...
- 🔨 Building MODEL model...
- ⚡ Solving...
- ✅ Allocation complete!

### Step 7: View Results

Immediately see:
- **Key Metrics Dashboard** (4 metrics)
- **Allocation Details Table** (sortable, searchable)
- **Download Buttons** (CSV & TXT)

### Step 8: Download or Go to Visualization

**Option A:** Download results directly
- 📥 Download Allocation CSV
- 📥 Download Summary TXT

**Option B:** View visualizations
- Click "📊 Results Analysis" in sidebar
- Charts auto-populate from last allocation
- View preference satisfaction, department distribution, capacity utilization

## Features

### Live Progress Tracking

Real-time status updates as allocation runs:
```
📂 Loading data...
✓ Loaded 80 students, 29 topics
🔍 Validating data...
✓ Validation passed
🎯 Building preference model...
🔨 Building ILP model...
⚡ Solving...
✅ Allocation complete!
```

### Key Metrics Display

Immediately after completion:
- **Students Assigned**: Total count
- **Optimal Cost**: Objective value
- **Got Choice %**: Percentage with ranked preference
- **Status**: Success/Partial

### Results Table

Interactive table showing:
- Student ID
- Assigned Topic
- Assigned Coach
- Department
- Preference Rank
- Effective Cost

Table features:
- Sort by column (click header)
- Search within table
- Copy rows
- Download as CSV

### One-Click Download

Get results instantly:
- **Allocation CSV**: Ready for spreadsheet analysis
- **Summary TXT**: Diagnostic report

## Example Workflows

### Workflow 1: Run & View Charts

```
1. Go to "🚀 Run Allocation"
2. Upload students.csv and capacities.csv
3. Select algorithm: "flow"
4. Set time limit: 30 seconds
5. Click "▶️ Run Allocation"
6. Wait for completion
7. View results in table
8. Click "📊 Results Analysis" to see charts
9. Explore visualizations
```

**Time:** ~2 minutes total ✨

### Workflow 2: Compare Algorithms

```
1. Run allocation with "flow" algorithm
2. Download results → allocation_flow.csv
3. Configure for "ilp" algorithm
4. Run allocation again
5. Download results → allocation_ilp.csv
6. Compare the two CSVs in Excel
```

### Workflow 3: Validate Before CLI Run

```
1. Go to "🚀 Run Allocation"
2. Upload your CSV files
3. Click "▶️ Run Allocation" with "flow" algorithm
4. See results immediately
5. If satisfied, run production allocation via CLI with "ilp"
```

## Algorithm Options

### Flow (Fast)
- **Speed**: ⚡⚡⚡ (2-10 seconds)
- **Quality**: 🎯🎯 (near-optimal)
- **Best for**: Quick testing, previews

### ILP (Optimal)
- **Speed**: ⚡ (10-120 seconds)
- **Quality**: 🎯🎯🎯 (optimal)
- **Best for**: Production allocations, final results

### Hybrid (Balanced)
- **Speed**: ⚡⚡ (5-120 seconds)
- **Quality**: 🎯🎯🎯 (verified optimal)
- **Best for**: Critical decisions, verification

## Tips & Tricks

### 1. Quick Preview
- Use "flow" algorithm
- Set time limit to 10-30 seconds
- See results in seconds
- Good for testing configurations

### 2. Production Run
- Use "ilp" algorithm
- Set time limit to 300 seconds
- Wait for optimal solution
- Download for final use

### 3. Debug Data Issues
- Upload files to "🚀 Run Allocation"
- Dashboard validates automatically
- Error messages show issues clearly
- Fix and re-upload

### 4. Reproducible Results
- Set **Random Seed** (e.g., 42)
- Same seed = same results
- Useful for reports and documentation

### 5. Batch Allocations
- Run allocation A, download results
- Change input files
- Run allocation B, download results
- Compare side-by-side

## What Happens Behind the Scenes

1. **File Upload** → Files held in memory
2. **Validation** → Input data checked
3. **Data Loading** → DataRepository processes files
4. **Solver Setup** → Preference model built
5. **Optimization** → ILP/Flow solves
6. **Results** → Displayed immediately
7. **Download** → Ready for export

All in **your browser**, **no CLI needed**! ✨

## Error Handling

### File Format Issues

**Error**: "Column names not recognized"
- **Solution**: Check CSV headers match expected format
- **Fix**: Use sample CSV from data/input as template

### Validation Failures

**Error**: "Validation failed: Topic references non-existent coach"
- **Solution**: Fix data issues in CSV
- **Fix**: Review error messages, update CSV, re-upload

### Solver Issues

**Error**: "No solution found"
- **Solution**: Constraints too strict or data issue
- **Fix**: Relax constraints or fix data

All errors show **detailed messages** to help debugging! 🔍

## Comparison: Dashboard vs CLI

| Feature | Dashboard | CLI |
|---------|-----------|-----|
| Run allocation | ✅ Yes | ✅ Yes |
| Visualizations | ✅ Yes | ❌ Separate |
| Configuration | ✅ Web UI | ✅ CLI args |
| Results download | ✅ One-click | ✅ Manual |
| Speed | Similar | Similar |
| Learning curve | ⭐⭐ Easy | ⭐⭐⭐ Moderate |
| Batch processing | ⭐⭐ Good | ⭐⭐⭐ Better |

## Performance Tips

### For Fast Results
- Use "flow" algorithm
- Set time limit: 10-30 seconds
- Allocations run in seconds

### For Better Results
- Use "ilp" algorithm
- Set time limit: 60-300 seconds
- Better solution quality

### For Large Datasets
- Use "flow" for preview (fast)
- Use "hybrid" for verification
- Consider smaller subsets first

## Keyboard Shortcuts

While in dashboard:
- `r` - Rerun script
- `c` - Clear cache
- `q` - Quit

## Troubleshooting

### Dashboard won't show Run Allocation page

**Solution**: Restart dashboard
```bash
Ctrl+C
./run_dashboard.sh
```

### Files don't upload

**Solution**: Check file format
- Must be CSV files
- Must have correct headers
- Try smaller test file first

### Allocation runs very slow

**Solution**: Change algorithm
```
Try: algorithm = "flow"
Set: time_limit = 30 seconds
```

### Results don't appear

**Solution**: Check error messages
- Scroll down to see errors
- Fix data issues
- Verify CSV format

## Next Steps

After running allocation in dashboard:

1. **View Results Table** - Explore allocation details
2. **Go to Results Analysis** - See visualizations
3. **Download Results** - Get CSV for analysis
4. **Try Different Settings** - Run again with new config
5. **Share with Team** - Download and share results

## FAQ

**Q: Is dashboard allocation as good as CLI?**
A: Yes! Same algorithm, same solver, same results.

**Q: Can I run large datasets?**
A: Yes, but use "flow" algorithm for fast preview first.

**Q: What if allocation fails?**
A: Error messages show exactly what's wrong. Fix data and retry.

**Q: Can I save configs from dashboard?**
A: Yes! Go to ⚙️ Configuration page and save as JSON.

**Q: Can I run multiple allocations?**
A: Yes! Each run saves results, no conflicts.

---

**Happy Allocating from the Dashboard! 🎓📊✨**
