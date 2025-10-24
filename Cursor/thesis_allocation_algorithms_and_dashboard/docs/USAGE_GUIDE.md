# Usage Guide - Thesis Allocation Solver

## Table of Contents

1. [Basic Usage](#basic-usage)
2. [Forced Topic Assignments](#forced-topic-assignments)
3. [Configuration Management](#configuration-management)
4. [Advanced Techniques](#advanced-techniques)
5. [Troubleshooting](#troubleshooting)
6. [Real-World Scenarios](#real-world-scenarios)

## Basic Usage

### Step 1: Prepare Input Data

Ensure you have three CSV files:

**students.csv** - Student preferences
```csv
student_id,plan_thesis,pref1,pref2,pref3,pref4,pref5
s001,Yes,t01,t02,t03,t04,t05
s002,Yes,t05,t04,t03,t02,t01
```

**capacities.csv** - Topic and coach capacities
```csv
topic_id,coach_id,maximum students per topic,maximum students per coach,department_id,Desired minimum by department
t01,coach_a,4,12,dept_cs,5
t02,coach_a,3,12,dept_cs,5
```

### Step 2: Run Basic Allocation

```bash
python allocate.py \
  --students data/input/students.csv \
  --capacities data/input/capacities.csv \
  --out data/output/allocation.csv \
  --summary data/output/summary.txt
```

### Step 3: Review Results

Check `allocation.csv` for assignments and `summary.txt` for statistics.

## Forced Topic Assignments

Forced assignments allow administrators to lock specific students to topics.

### Adding Forced Topics

Add a `forced_topic` column to `students.csv`:

```csv
student_id,plan_thesis,pref1,pref2,pref3,pref4,pref5,forced_topic
s001,Yes,t01,t02,t03,t04,t05,t10
s002,Yes,t05,t04,t03,t02,t01,
s003,Yes,t02,t03,t04,t05,t06,t05
```

In this example:
- `s001` will be forced to `t10` regardless of preferences
- `s002` has no forced topic (empty field)
- `s003` will be forced to `t05` 

### Running with Forced Assignments

```bash
python allocate.py \
  --students data/input/students-forced.csv \
  --capacities data/input/capacities.csv \
  --out data/output/allocation.csv \
  --summary data/output/summary.txt
```

### Validation

The system will validate that:
- Forced topics exist in capacities.csv
- Forced topics are not in the banned list
- Capacity constraints are still respected

## Configuration Management

### Option 1: Command-Line Arguments (Simple)

```bash
python allocate.py \
  --students data/input/students.csv \
  --capacities data/input/capacities.csv \
  --algorithm flow \
  --time-limit-sec 60 \
  --out data/output/allocation.csv \
  --summary data/output/summary.txt
```

### Option 2: Configuration File (Recommended)

#### Create Default Configuration

```bash
python allocate.py --save-config config.json
```

This generates:
```json
{
  "preference": {
    "allow_unranked": true,
    "tier2_cost": 1,
    "tier3_cost": 5,
    "unranked_cost": 200,
    "top2_bias": true
  },
  "capacity": {
    "enable_topic_overflow": true,
    "enable_coach_overflow": true,
    "dept_min_mode": "soft",
    "P_dept_shortfall": 1000,
    "P_topic": 800,
    "P_coach": 600
  },
  "solver": {
    "algorithm": "ilp",
    "time_limit_sec": null,
    "random_seed": null,
    "epsilon_suboptimal": null
  }
}
```

#### Customize Configuration

Edit `config.json`:
```json
{
  "preference": {
    "allow_unranked": false,
    "tier2_cost": 2,
    "tier3_cost": 10,
    "unranked_cost": 500,
    "top2_bias": true
  },
  "capacity": {
    "enable_topic_overflow": false,
    "enable_coach_overflow": true,
    "dept_min_mode": "hard",
    "P_dept_shortfall": 5000,
    "P_topic": 1000,
    "P_coach": 800
  },
  "solver": {
    "algorithm": "hybrid",
    "time_limit_sec": 120,
    "random_seed": 42,
    "epsilon_suboptimal": 0.05
  }
}
```

#### Use Configuration File

```bash
python allocate.py \
  --config config.json \
  --students data/input/students.csv \
  --capacities data/input/capacities.csv \
  --out data/output/allocation.csv \
  --summary data/output/summary.txt
```

### Option 3: Merge Config File + CLI Arguments

Config file provides defaults, CLI arguments override:

```bash
python allocate.py \
  --config config.json \
  --algorithm flow \
  --time-limit-sec 30 \
  --students data/input/students.csv \
  --capacities data/input/capacities.csv \
  --out data/output/allocation.csv \
  --summary data/output/summary.txt
```

This uses settings from `config.json` but overrides:
- `solver.algorithm` to "flow"
- `solver.time_limit_sec` to 30

## Advanced Techniques

### 1. Input Validation Only

Validate inputs without solving:

```bash
python allocate.py --validate-only \
  --students data/input/students.csv \
  --capacities data/input/capacities.csv
```

Output:
```
INFO: Thesis Allocation Solver Started
INFO: Loaded 100 students, 30 topics, 10 coaches, 3 departments
INFO: Validating input data...
INFO: ✓ All validations passed
```

### 2. Skip Validation (for Trusted Data)

```bash
python allocate.py --no-validate \
  --students data/input/students.csv \
  --capacities data/input/capacities.csv \
  --out data/output/allocation.csv \
  --summary data/output/summary.txt
```

### 3. Algorithm Selection

#### Fast Flow Algorithm

```bash
python allocate.py --algorithm flow \
  --students data/input/students.csv \
  --capacities data/input/capacities.csv \
  --out data/output/allocation.csv \
  --summary data/output/summary.txt
```

**Pros**: Fast (milliseconds to seconds)
**Cons**: May be suboptimal

#### Optimal ILP Algorithm

```bash
python allocate.py --algorithm ilp \
  --students data/input/students.csv \
  --capacities data/input/capacities.csv \
  --out data/output/allocation.csv \
  --summary data/output/summary.txt
```

**Pros**: Guaranteed optimal solution
**Cons**: Slower (seconds to minutes)

#### Hybrid Algorithm (Recommended)

```bash
python allocate.py --algorithm hybrid \
  --students data/input/students.csv \
  --capacities data/input/capacities.csv \
  --out data/output/allocation.csv \
  --summary data/output/summary.txt
```

**Behavior**: Solves with ILP, then verifies with Flow, uses best result
**Pros**: Combines quality of both methods
**Cons**: Slowest overall

### 4. Solver Timeout & Near-Optimal Solutions

#### Set Time Limit

```bash
python allocate.py --time-limit-sec 60 \
  --students data/input/students.csv \
  --capacities data/input/capacities.csv \
  --out data/output/allocation.csv \
  --summary data/output/summary.txt
```

#### Allow Near-Optimal Solutions

Accept solutions within 5% of optimal:

```bash
python allocate.py --epsilon-suboptimal 0.05 \
  --students data/input/students.csv \
  --capacities data/input/capacities.csv \
  --out data/output/allocation.csv \
  --summary data/output/summary.txt
```

### 5. Reproducibility

Use random seed:

```bash
python allocate.py --random-seed 42 \
  --students data/input/students.csv \
  --capacities data/input/capacities.csv \
  --out data/output/allocation.csv \
  --summary data/output/summary.txt
```

### 6. Debug Logging

```bash
python allocate.py \
  --log-level DEBUG \
  --log-file logs/allocation.log \
  --students data/input/students.csv \
  --capacities data/input/capacities.csv \
  --out data/output/allocation.csv \
  --summary data/output/summary.txt
```

Check `logs/allocation.log` for detailed execution trace.

### 7. Visualizations

Generate Sankey diagram:

```bash
python allocate.py \
  --students data/input/students.csv \
  --capacities data/input/capacities.csv \
  --out data/output/allocation.csv \
  --summary data/output/summary.txt \
  --sankey data/output/sankey.html
```

Open `sankey.html` in a browser to visualize student → topic → department flows.

## Troubleshooting

### Issue: "Unassignable students" Warning

Students with no valid topic assignment options.

**Causes:**
1. All preferred topics are banned
2. All preferred topics have no capacity
3. All preferences conflict with forced assignments

**Solutions:**
```bash
# Check validation for details
python allocate.py --validate-only \
  --students data/input/students.csv \
  --capacities data/input/capacities.csv

# Review banned topics
# - Remove from banned list
# - Add new topic to preferences

# Increase capacities
# - Edit capacities.csv
# - Increase topic and coach caps
```

### Issue: Solver Timeout

ILP solver takes too long.

**Solutions:**
```bash
# Option 1: Use faster algorithm
python allocate.py --algorithm flow ...

# Option 2: Set time limit
python allocate.py --time-limit-sec 30 ...

# Option 3: Allow near-optimal solutions
python allocate.py --epsilon-suboptimal 0.1 ...

# Option 4: Use hybrid (intelligent choice between ILP and flow)
python allocate.py --algorithm hybrid --time-limit-sec 120 ...
```

### Issue: Validation Errors

Input data has issues.

**Solutions:**
```bash
# Run validation to see errors
python allocate.py --validate-only \
  --students data/input/students.csv \
  --capacities data/input/capacities.csv

# Fix issues:
# - Check topic_id references match
# - Verify student_id format
# - Ensure capacities are positive
# - Check for duplicate topics
```

### Issue: Unexpected Results

Allocation quality is poor.

**Solutions:**
```bash
# 1. Check preference configuration
python allocate.py --save-config debug_config.json
# Review preference costs are reasonable

# 2. Enable top2 bias
# - Ensure top2_bias is true in config

# 3. Adjust penalty weights
# - Increase P_topic, P_coach for stricter capacity enforcement
# - Increase P_dept_shortfall for stricter department minimums

# 4. Use better algorithm
python allocate.py --algorithm ilp ...
```

## Real-World Scenarios

### Scenario 1: Quick Test Run

You want to test configuration without waiting:

```bash
python allocate.py \
  --algorithm flow \
  --students data/input/students.csv \
  --capacities data/input/capacities.csv \
  --out data/output/test_allocation.csv \
  --summary data/output/test_summary.txt
```

### Scenario 2: Production Run with Verification

You need optimal solution with verification:

```bash
python allocate.py \
  --algorithm hybrid \
  --time-limit-sec 300 \
  --random-seed 2024 \
  --students data/input/students.csv \
  --capacities data/input/capacities.csv \
  --out data/output/allocation.csv \
  --summary data/output/summary.txt \
  --log-level INFO \
  --log-file logs/allocation.log
```

### Scenario 3: Accommodate Special Requests

Some students have special requirements (forced topics):

```csv
student_id,plan_thesis,pref1,pref2,pref3,forced_topic
s001,Yes,t01,t02,t03,t_special_001
s002,Yes,t04,t05,t06,
s003,Yes,t07,t08,t09,t_special_002
```

```bash
python allocate.py \
  --students data/input/students-special.csv \
  --capacities data/input/capacities.csv \
  --out data/output/allocation.csv \
  --summary data/output/summary.txt
```

### Scenario 4: Enforce Hard Department Minimums

```bash
python allocate.py \
  --config config.json \
  --dept-min-mode hard \
  --students data/input/students.csv \
  --capacities data/input/capacities.csv \
  --out data/output/allocation.csv \
  --summary data/output/summary.txt
```

### Scenario 5: Multiple Runs with Different Settings

Compare results from different algorithms:

```bash
# ILP (optimal)
python allocate.py --algorithm ilp --time-limit-sec 120 \
  --students data/input/students.csv \
  --capacities data/input/capacities.csv \
  --out data/output/allocation_ilp.csv \
  --summary data/output/summary_ilp.txt

# Flow (fast)
python allocate.py --algorithm flow \
  --students data/input/students.csv \
  --capacities data/input/capacities.csv \
  --out data/output/allocation_flow.csv \
  --summary data/output/summary_flow.txt

# Compare outputs
diff data/output/allocation_ilp.csv data/output/allocation_flow.csv
```

### Scenario 6: Debug with Verbose Logging

Something unexpected happened, need details:

```bash
python allocate.py \
  --log-level DEBUG \
  --log-file logs/debug.log \
  --validate-only \
  --students data/input/students.csv \
  --capacities data/input/capacities.csv

# Then review logs/debug.log for detailed trace
tail -f logs/debug.log
```

## Best Practices

1. **Always validate first**: Use `--validate-only` on new datasets
2. **Start with flow**: Use `--algorithm flow` for quick feedback
3. **Use config files**: More maintainable than long command lines
4. **Enable logging**: Helps with debugging issues
5. **Test new constraints**: Use `--validate-only` before full solve
6. **Keep backups**: Save working configurations and outputs
7. **Document parameters**: Comment in config.json why values were chosen
8. **Monitor performance**: Log runtimes to track algorithm efficiency

## Getting Help

```bash
# Show all available options
python allocate.py --help

# Validate configuration
python allocate.py --save-config test_config.json
cat test_config.json

# Check version (if available)
python allocate.py --version
```

## See Also

- `ARCHITECTURE.md` - System design and module documentation
- `README.md` - Overview and quick reference
- `config.example.json` - Example configuration file
- `data/input/students-forced-example.csv` - Example with forced assignments
