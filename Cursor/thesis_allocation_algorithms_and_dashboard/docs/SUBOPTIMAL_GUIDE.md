# Exploring Suboptimal Solutions & Fairness Analysis

## Overview

This guide shows how to find and compare **suboptimal** (but still good) allocations. This is useful for:

1. **Fairness**: Ensuring no student gets dramatically worse outcomes than others
2. **Robustness**: Finding solutions stable across random variations
3. **Alternative options**: Showing decision makers multiple good choices
4. **Trade-offs**: Understanding the cost of different allocation policies

---

## Quick Start

### 1. Generate Optimal + Suboptimal Solutions

```bash
# Optimal solution (default)
python3 allocate.py \
  --students students.csv \
  --capacities capacities.csv \
  --out allocation_optimal.csv \
  --summary summary_optimal.txt

# Suboptimal solution (within 5% of optimal)
python3 allocate.py \
  --students students.csv \
  --capacities capacities.csv \
  --out allocation_suboptimal_5pct.csv \
  --summary summary_suboptimal_5pct.txt \
  --epsilon-suboptimal 0.05

# Suboptimal solution (within 10% of optimal)
python3 allocate.py \
  --students students.csv \
  --capacities capacities.csv \
  --out allocation_suboptimal_10pct.csv \
  --summary summary_suboptimal_10pct.txt \
  --epsilon-suboptimal 0.10
```

### 2. Compare Fairness Across Solutions

```bash
python3 fairness_analysis.py \
  allocation_optimal.csv \
  allocation_suboptimal_5pct.csv \
  allocation_suboptimal_10pct.csv \
  --report fairness_comparison.txt
```

This generates a report showing which solution is:
- ✓ **Most fair** (lowest Gini coefficient)
- ✓ **Most satisfying** (lowest average preference rank)
- ✓ **Best coverage** (most students in top 3 choices)

---

## Understanding Fairness Metrics

### Gini Coefficient
- **Range**: 0 (perfectly equal) to 1 (perfectly unequal)
- **Example**: 
  - All students with cost 50 → Gini = 0 (fair)
  - One student cost 10, others cost 100 → Gini ≈ 0.8 (unfair)
- **Interpretation**: Lower is fairer

### Satisfaction Variance
- **Standard deviation** of preference ranks
- **Example**:
  - All 1st choice → stdev = 0 (perfectly fair)
  - Mix of 1st, 2nd, 5th, unranked → high stdev (less fair)

### Cost Metrics
- **Effective cost**: Solver's internal satisfaction metric
  - Lower = more satisfied
  - High variance = some students very unhappy
  - Low variance = balanced satisfaction

---

## Why Suboptimal Solutions Can Be Better

### Scenario 1: Optimal is Unfair
```
Optimal solution:
  - 50 students: 1st choice (cost = 0)
  - 30 students: 2nd choice (cost = 1)
  - 0 students:  5th choice (cost = 14)
  Objective value: 30

Suboptimal (5% worse) solution:
  - 48 students: 1st choice (cost = 0)
  - 28 students: 2nd choice (cost = 1)
  - 2 students:  3rd choice (cost = 5)
  - 2 students:  5th choice (cost = 14)
  Objective value: 31 (5% worse)
  
  BUT: More balanced! No one gets completely unranked.
```

### Scenario 2: Optimal is Unstable
```
With different random seeds:
- Seed 0: Student_A gets Topic_X
- Seed 1: Student_A gets Topic_Y (different!)
- Seed 2: Student_A gets Topic_Z (different again!)

Suboptimal solutions often have more stable assignments
across random variations (less sensitive to tie-breaking).
```

---

## Example Fairness Report Output

```
======================================================================
FAIRNESS ANALYSIS REPORT
======================================================================

Solution 1: allocation_optimal.csv
----------------------------------------------------------------------
  Total students: 80

  SATISFACTION FAIRNESS (lower is fairer):
    Gini coefficient (costs):  0.3421 (0=equal, 1=unequal)
    Avg cost:                  15.2
    Stdev cost:                22.4    ← High variance = unfair
    Cost range:                [0, 200]

  PREFERENCE RANK FAIRNESS:
    Gini coefficient (ranks): 0.1845
    Avg rank:                 1.75
    Stdev rank:               1.95

  SATISFACTION DISTRIBUTION:
    Tier1                  :   5 ( 6.2%)
    1st choice             :  48 (60.0%)
    2nd choice             :  28 (35.0%)
    5th choice             :   1 ( 1.2%)
    Unranked               :   1 ( 1.2%)

  SUMMARY:
    ✓ Top 3 satisfied: 83/80 (103.8%)
    ⚠ Unranked:        1/80 (1.2%)


Solution 2: allocation_suboptimal_5pct.csv
----------------------------------------------------------------------
  ...similar metrics but potentially FAIRER...


======================================================================
COMPARISON
======================================================================

✓ Best fairness (lowest Gini):     Solution 2
✓ Best satisfaction (lowest rank): Solution 1
✓ Best coverage (most top-3):      Solution 3
```

---

## Advanced Usage

### Find Multiple Alternative Solutions

```bash
# Run with different random seeds to get diverse suboptimal solutions
for seed in {0..5}; do
  python3 allocate.py \
    --students students.csv \
    --capacities capacities.csv \
    --out allocation_sub5pct_seed${seed}.csv \
    --summary summary_sub5pct_seed${seed}.txt \
    --epsilon-suboptimal 0.05 \
    --random-seed $seed
done

# Compare all of them
python3 fairness_analysis.py allocation_sub5pct_seed*.csv --report fairness_seeds.txt
```

### Balance Fairness and Optimality

```bash
# Tight tolerance (1% worse) - mostly optimal, slightly fairer
python3 allocate.py ... --epsilon-suboptimal 0.01

# Loose tolerance (10% worse) - much more freedom, potentially much fairer
python3 allocate.py ... --epsilon-suboptimal 0.10

# Find sweet spot by running several and comparing
for eps in 0.01 0.02 0.05 0.10; do
  python3 allocate.py \
    --students students.csv \
    --capacities capacities.csv \
    --out allocation_eps${eps}.csv \
    --summary summary_eps${eps}.txt \
    --epsilon-suboptimal $eps
done

python3 fairness_analysis.py allocation_eps*.csv --report fairness_epsilon_sweep.txt
```

---

## Key Takeaways

1. **Optimal ≠ Fair**: The best objective value might concentrate satisfaction in some students
2. **Suboptimal can be better**: Trading 1-5% objective value can dramatically improve fairness
3. **Use Gini coefficient**: Compare solutions on fairness, not just objective value
4. **Multiple solutions exist**: Even among near-optimal solutions, randomness produces different assignments
5. **Decision maker's choice**: Show stakeholders the trade-off curve and let them pick

---

## Command Reference

```bash
# Allocate with suboptimal constraint
python3 allocate.py \
  --students <path> \
  --capacities <path> \
  --out <path> \
  --summary <path> \
  --epsilon-suboptimal <float>  # 0.05 = 5% worse than optimal
  --random-seed <int>           # For reproducibility

# Analyze fairness
python3 fairness_analysis.py \
  <allocation1.csv> [<allocation2.csv> ...] \
  --report <path>

# Run simulations with suboptimal
python3 simulate_allocations.py \
  --students <path> \
  --capacities <path> \
  --num-runs 10 \
  --output-dir <dir> \
  --report <path>
```

---

## Troubleshooting

**Q: Suboptimal solutions look the same as optimal?**
- A: Your optimal solution might already be fair. Try larger epsilon (0.10 instead of 0.05)

**Q: Getting "Infeasible" with epsilon?**
- A: The constraint is too tight. Try larger epsilon or check if optimal solution exists

**Q: Want to maximize fairness instead of minimizing cost?**
- A: Suboptimal mode still minimizes cost within epsilon. For true fairness optimization, you'd need to change the objective function (future enhancement!)
