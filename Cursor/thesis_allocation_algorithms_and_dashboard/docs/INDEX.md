# Thesis Allocation System - Documentation Index

Welcome! This guide helps you navigate the documentation and get started quickly.

## 📚 Documentation Overview

### For First-Time Users

1. **[README.md](README.md)** ← Start here!
   - Overview of features
   - Quick start (5 minutes)
   - Input/output file formats
   - Configuration reference

2. **[QUICK_EXAMPLES.md](QUICK_EXAMPLES.md)** ← Copy-paste ready
   - 20 common examples
   - From basic to advanced
   - Troubleshooting examples
   - Batch processing scripts

### For In-Depth Understanding

3. **[ARCHITECTURE.md](ARCHITECTURE.md)** ← System design
   - Module descriptions
   - Data flow
   - Design principles
   - Extension guide
   - Testing setup

4. **[USAGE_GUIDE.md](USAGE_GUIDE.md)** ← Detailed reference
   - Step-by-step tutorials
   - Configuration management
   - Advanced techniques
   - Real-world scenarios
   - Troubleshooting

### For What's New

5. **[RESTRUCTURING_SUMMARY.md](RESTRUCTURING_SUMMARY.md)** ← What changed?
   - Before/after comparison
   - New features explained
   - Code quality improvements
   - Migration guide
   - Best practices

### For Examples

6. **[config.example.json](config.example.json)** ← Configuration template
   - All available parameters
   - Default values
   - Reference for custom configs

7. **[data/input/students-forced-example.csv](data/input/students-forced-example.csv)**
   - Example CSV with forced assignments
   - Shows `forced_topic` column usage

## 🚀 Getting Started (5 Minutes)

### Step 1: Setup (1 min)
```bash
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Step 2: Basic Run (1 min)
```bash
python allocate.py \
  --students data/input/students.csv \
  --capacities data/input/capacities.csv \
  --out data/output/allocation.csv \
  --summary data/output/summary.txt
```

### Step 3: Check Results (1 min)
- Open `data/output/allocation.csv` in spreadsheet
- Review `data/output/summary.txt` for statistics

### Step 4: Explore Features (2 min)
```bash
# Validate data
python allocate.py --validate-only \
  --students data/input/students.csv \
  --capacities data/input/capacities.csv

# Export default config
python allocate.py --save-config config.json

# Quick test with faster algorithm
python allocate.py --algorithm flow \
  --students data/input/students.csv \
  --capacities data/input/capacities.csv \
  --out data/output/allocation.csv \
  --summary data/output/summary.txt
```

## 🎯 Common Tasks

### I want to...

**Understand what this tool does**
→ Read [README.md](README.md) section "Overview"

**Get started quickly**
→ Read [README.md](README.md) section "Quick Start"
→ Copy example from [QUICK_EXAMPLES.md](QUICK_EXAMPLES.md) #1

**Use forced topic assignments**
→ Read [README.md](README.md) section "With Forced Assignments"
→ Copy example from [QUICK_EXAMPLES.md](QUICK_EXAMPLES.md) #8
→ Use [data/input/students-forced-example.csv](data/input/students-forced-example.csv) as template

**Configure parameters**
→ Read [USAGE_GUIDE.md](USAGE_GUIDE.md) section "Configuration Management"
→ Export config: `python allocate.py --save-config config.json`
→ Edit `config.json` and use: `python allocate.py --config config.json ...`

**Find a specific example**
→ Browse [QUICK_EXAMPLES.md](QUICK_EXAMPLES.md) (20 examples)

**Understand the system design**
→ Read [ARCHITECTURE.md](ARCHITECTURE.md)

**Troubleshoot an issue**
→ Read [USAGE_GUIDE.md](USAGE_GUIDE.md) section "Troubleshooting"
→ Try validation: `python allocate.py --validate-only ...`
→ Enable logging: `python allocate.py --log-level DEBUG --log-file debug.log ...`

**Learn what's new after restructuring**
→ Read [RESTRUCTURING_SUMMARY.md](RESTRUCTURING_SUMMARY.md)

**Compare algorithms**
→ Read [QUICK_EXAMPLES.md](QUICK_EXAMPLES.md) #13

**Set up batch processing**
→ Read [QUICK_EXAMPLES.md](QUICK_EXAMPLES.md) #15

**See all command options**
→ Run `python allocate.py --help`

## 📊 Key Concepts

### Input Files

- **students.csv**: Student preferences and constraints
  - Required: student_id, plan_thesis, pref1..pref5
  - Optional: tier1, tier2, tier3, banned, **forced_topic**

- **capacities.csv**: Topic/coach/department capacities
  - Required: topic_id, coach_id, maximum students per topic, maximum students per coach, department_id
  - Optional: Desired minimum by department

- **overrides.csv** (optional): Manual cost assignments
  - Columns: student_id, topic_id, cost

### Output Files

- **allocation.csv**: Final assignments with details
- **summary.txt**: Statistics and diagnostics
- **\*.html** (optional): Sankey visualization

### Configuration

Three ways to configure:

1. **CLI Arguments** (simple, backward-compatible)
   ```bash
   python allocate.py --algorithm flow --time-limit-sec 60 ...
   ```

2. **Config File** (recommended for complex setups)
   ```bash
   python allocate.py --config config.json ...
   ```

3. **Combined** (config + CLI overrides)
   ```bash
   python allocate.py --config config.json --algorithm flow ...
   ```

### Algorithms

- **ILP**: Optimal solution (slow)
- **Flow**: Near-optimal, fast (recommended for large datasets)
- **Hybrid**: ILP + Flow verification (recommended for critical runs)

## 🔧 Tools & Commands

### Help & Info
```bash
python allocate.py --help              # Show all options
python allocate.py --save-config c.json # Export config template
```

### Validation
```bash
python allocate.py --validate-only ...  # Check inputs without solving
python allocate.py --no-validate ...    # Skip validation (for trusted data)
```

### Algorithms
```bash
python allocate.py --algorithm ilp ...    # Optimal
python allocate.py --algorithm flow ...   # Fast
python allocate.py --algorithm hybrid ... # Balanced
```

### Debugging
```bash
python allocate.py --log-level DEBUG --log-file debug.log ... # Full trace
python allocate.py --validate-only ... # Check input data
```

### Visualization
```bash
python allocate.py --sankey output.html ...  # Generate diagram
```

## 📖 Documentation Map

```
INDEX.md (you are here)
│
├─ README.md
│  └─ Quick start & overview
│
├─ QUICK_EXAMPLES.md
│  └─ 20 copy-paste ready examples
│
├─ ARCHITECTURE.md
│  └─ System design & extension guide
│
├─ USAGE_GUIDE.md
│  └─ Detailed tutorials & troubleshooting
│
├─ RESTRUCTURING_SUMMARY.md
│  └─ What changed & migration guide
│
├─ allocator/
│  ├─ entities.py          # Domain models
│  ├─ config.py            # Configuration system
│  ├─ validation.py        # Input validation
│  ├─ data_repository.py   # Data loading
│  ├─ preference_model.py  # Cost computation
│  ├─ allocation_model_ilp.py      # ILP solver
│  ├─ allocation_model_flow.py     # Flow solver
│  ├─ logging_config.py    # Logging setup
│  ├─ outputs.py           # Result output
│  └─ viz_sankey.py        # Visualization
│
├─ config.example.json      # Configuration template
├─ data/input/              # Input data directory
│  └─ students-forced-example.csv  # Example with forced assignments
└─ data/output/             # Output directory
```

## ⚡ Quick Command Reference

```bash
# Basic
python allocate.py --students ... --capacities ... --out ... --summary ...

# Fast test
python allocate.py --algorithm flow --students ... --capacities ... --out ... --summary ...

# Validate
python allocate.py --validate-only --students ... --capacities ...

# With config
python allocate.py --config config.json --students ... --capacities ... --out ... --summary ...

# Debug
python allocate.py --log-level DEBUG --log-file logs/debug.log --students ... --capacities ... --out ... --summary ...

# With forced assignments
python allocate.py --students students-forced.csv --capacities ... --out ... --summary ...

# Export config
python allocate.py --save-config config.json
```

## 🎓 Learning Path

**Beginner**
1. Read [README.md](README.md) intro
2. Try [QUICK_EXAMPLES.md](QUICK_EXAMPLES.md) #1-#3
3. Run: `python allocate.py --help`

**Intermediate**
1. Read [USAGE_GUIDE.md](USAGE_GUIDE.md) "Configuration Management"
2. Generate and edit `config.json`
3. Try [QUICK_EXAMPLES.md](QUICK_EXAMPLES.md) #4-#10

**Advanced**
1. Read [ARCHITECTURE.md](ARCHITECTURE.md)
2. Try [QUICK_EXAMPLES.md](QUICK_EXAMPLES.md) #11-#20
3. Explore modifying code in `allocator/`

## 🐛 Debugging Guide

### Problem: "Unassignable students"
**Solution**: 
1. Read [USAGE_GUIDE.md](USAGE_GUIDE.md) section "Issue: Unassignable students"
2. Run: `python allocate.py --validate-only ...`

### Problem: Solver too slow
**Solution**:
1. Read [QUICK_EXAMPLES.md](QUICK_EXAMPLES.md) #2
2. Try: `python allocate.py --algorithm flow ...`

### Problem: Validation errors
**Solution**:
1. Run: `python allocate.py --validate-only ...` to see details
2. Check [USAGE_GUIDE.md](USAGE_GUIDE.md) section "Issue: Validation errors"

### Problem: Unexpected results
**Solution**:
1. Enable logging: `python allocate.py --log-level DEBUG --log-file debug.log ...`
2. Review [RESTRUCTURING_SUMMARY.md](RESTRUCTURING_SUMMARY.md) for how things work

## 📞 Support Resources

### Within Documentation
- **Question about usage?** → [USAGE_GUIDE.md](USAGE_GUIDE.md)
- **Looking for example?** → [QUICK_EXAMPLES.md](QUICK_EXAMPLES.md)
- **Need to debug?** → [USAGE_GUIDE.md](USAGE_GUIDE.md) "Troubleshooting"
- **System design question?** → [ARCHITECTURE.md](ARCHITECTURE.md)
- **What's new?** → [RESTRUCTURING_SUMMARY.md](RESTRUCTURING_SUMMARY.md)

### Quick Help
```bash
python allocate.py --help
```

## 📋 Checklist Before Running

- [ ] Python 3.8+ installed
- [ ] Virtual environment activated
- [ ] Dependencies installed: `pip install -r requirements.txt`
- [ ] `students.csv` prepared and checked
- [ ] `capacities.csv` prepared and checked
- [ ] Output directory exists: `data/output/`
- [ ] (Optional) `config.json` configured
- [ ] (Optional) `overrides.csv` if needed

## 🎯 Next Steps

1. **Beginner**: Start with [README.md](README.md)
2. **Ready to run**: Copy example from [QUICK_EXAMPLES.md](QUICK_EXAMPLES.md)
3. **Need details**: Consult [USAGE_GUIDE.md](USAGE_GUIDE.md)
4. **Want to extend**: Read [ARCHITECTURE.md](ARCHITECTURE.md)

---

**Last Updated**: 2024
**Version**: Professional Edition (Restructured)

For questions about specific features, use the search function in your editor or terminal:
```bash
grep -r "forced_topic" .           # Find forced topic documentation
grep -r "configuration" .           # Find config documentation
grep -r "algorithm" .              # Find algorithm documentation
```
