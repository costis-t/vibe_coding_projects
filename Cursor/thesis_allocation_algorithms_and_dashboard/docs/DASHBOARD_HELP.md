# 🎓 Dashboard Help Center

## Quick Navigation

### New to the dashboard?
👉 Start here: **[CONFIGURATION_GUIDE.md](CONFIGURATION_GUIDE.md)**

### Want to get started immediately?
👉 See: **[DASHBOARD_QUICK_START.md](DASHBOARD_QUICK_START.md)**

### How to run an allocation?
👉 Check: **[RUN_ALLOCATION_GUIDE.md](RUN_ALLOCATION_GUIDE.md)**

---

## 📚 What Each Configuration Setting Does

### Preference Settings (How students are matched to choices)

| Setting | What It Does | Default | Range | Advice |
|---------|-------------|---------|-------|--------|
| **Allow Unranked Topics** | Can assign to topics students never listed? | ✓ ON | ON/OFF | OFF if you want to respect preferences |
| **Tier 2 Cost** | Penalty for Tier 2 (medium preference) | 1 | 0-10 | Higher = less willing to use tier 2 |
| **Tier 3 Cost** | Penalty for Tier 3 (lower preference) | 5 | 0-20 | Higher = avoid tier 3 |
| **Unranked Cost** | Penalty for unlisted topics | 200 | 0-500 | HIGH = really avoid (200-300 is good) |
| **Top-2 Bias** | Strongly prefer 1st & 2nd choices? | ✓ ON | ON/OFF | Keep ON (students care about order) |

**Key Insight**: All costs are penalties - LOWER is better, so students prefer items with lower costs.

---

### Capacity Settings (Respecting limits)

| Setting | What It Does | Default | Range | Advice |
|---------|-------------|---------|-------|--------|
| **Enable Topic Overflow** | Can exceed topic capacity with penalty? | ✓ ON | ON/OFF | OFF = hard cap (may leave students unassigned) |
| **Enable Coach Overflow** | Can exceed coach workload with penalty? | ✓ ON | ON/OFF | OFF = hard cap on coach workload |
| **Department Min Mode** | Enforce department minimums? | soft | soft/hard | hard = force strict minimums |
| **Dept Shortfall Penalty** | Punishment per missing student | 1000 | 0-5000 | Higher = stricter enforcement |
| **Topic Overflow Penalty** | Punishment per student over topic cap | 800 | 0-2000 | Higher = prevent popular topics overfilling |
| **Coach Overflow Penalty** | Punishment per student over coach cap | 600 | 0-2000 | Higher = prevent coach overload |

**Key Insight**: Penalties are applied PER VIOLATION. Higher penalty = algorithm tries harder to avoid violating that constraint.

---

### Solver Settings (Algorithm choice)

| Setting | Options | Default | What Each Does |
|---------|---------|---------|-----------------|
| **Algorithm** | ilp / flow / hybrid | — | **ILP**: Optimal (slow, 10-120s) **Flow**: Fast (2-10s, near-optimal) **Hybrid**: Both (balanced) |
| **Time Limit** | 0-600 sec | 60 | Max time solver can spend. 0=no limit |
| **Random Seed** | Number or empty | empty | Same seed = same results (for reproducibility) |
| **Epsilon Suboptimal** | 0.0-1.0 | 0.0 | Allow solutions X% worse than optimal (makes it faster) |

**Algorithm Comparison**:
```
┌─────────┬────────────────┬─────────────────┬──────────────┐
│ Method  │ Speed          │ Quality         │ Use When     │
├─────────┼────────────────┼─────────────────┼──────────────┤
│ ILP     │ ⚡ Slow         │ 🎯🎯🎯 Perfect   │ Final run    │
│ Flow    │ ⚡⚡⚡ Fast    │ 🎯🎯 Very Good | Testing      │
│ Hybrid  │ ⚡⚡ Medium   │ 🎯🎯🎯 Perfect   │ Balanced     │
└─────────┴────────────────┴─────────────────┴──────────────┘
```

---

## 📊 Understanding Results

### Key Metrics in Results Display

**Students Assigned**: Total students who got an assignment
- ✅ All students = Success
- ⚠️ < 100% = Some students unassigned (check constraints)

**Optimal Cost**: How good the solution is
- ✅ Lower is better (means students are happier)
- This number tells you the total "unhappiness" across all assignments

**Got Choice %**: Percentage who got a ranked preference
- ✅ 80%+ = Good!
- ⚠️ 50-80% = Constraints limiting choices
- ❌ <50% = Capacity or minimum constraints very tight

**Status**: All assigned vs. some unassigned
- ✓ Success = Everyone got something
- ⚠ Partial = Not everyone could be assigned

---

### Preference Rank Explained

In results table, you'll see a "preference_rank" column:

```
Rank -1  = FORCED by admin (this student MUST get this topic)
Rank 0-2 = TIER preference (Tier 1, Tier 2, Tier 3)
Rank 10-14 = RANKED preference (the student listed this: 1st, 2nd, 3rd, etc.)
Rank 999 = UNRANKED (the student never mentioned this topic)
```

**What students prefer** (in order):
1. Their own rankings (10-14) - especially 1st choice (10)
2. Their tier preferences (0-2) - especially Tier 1 (0)
3. Anything else (999)

---

## 🔧 Configuration Recipes

### "I want maximum student happiness"
```
Preference Settings:
  ✓ Allow Unranked: OFF (force ranked if possible)
  • Tier 2 Cost: 2 (slightly dislike tier 2)
  • Tier 3 Cost: 10 (really avoid tier 3)
  • Unranked Cost: 500 (hate unranked)
  ✓ Top-2 Bias: ON (prefer top choices)

Solver:
  • Algorithm: ILP (optimal)
  • Time Limit: 300 seconds
  • Epsilon: 0 (no suboptimal)
```

### "I need fast results, good enough quality"
```
Solver:
  • Algorithm: Hybrid (balanced)
  • Time Limit: 60 seconds
  • Epsilon: 0 (optimal)

Capacity:
  • Enable Topic Overflow: ON (flexibility)
  • Enable Coach Overflow: ON (flexibility)
```

### "Quick testing of different configs"
```
Solver:
  • Algorithm: Flow (fastest)
  • Time Limit: 30 seconds
  • Epsilon: 0.1 (allow 10% worse)
```

### "Strict capacity limits (e.g., lab limits)"
```
Capacity:
  • Enable Topic Overflow: OFF (hard cap)
  • Enable Coach Overflow: OFF (hard cap)

Solver:
  • Algorithm: ILP (optimal with hard limits)
  • Time Limit: 300 seconds
```

---

## 🆘 Troubleshooting

### "Students are getting unranked topics!"
**Try these**:
1. Increase `Unranked Cost` (make it 400-500)
2. Set `Allow Unranked: OFF` (force ranked if possible)
3. Check if there's a capacity problem:
   - Increase `enable_topic_overflow`
   - Increase `enable_coach_overflow`

### "Not everyone is assigned!"
**Probably**: Constraints are too tight
1. Enable overflow: `enable_topic_overflow: ON`
2. Use `dept_min_mode: "soft"` (don't force mins)
3. Try `Algorithm: ILP` with higher time limit
4. Check if departments have conflicting minimums

### "Results taking too long"
**Speed it up**:
1. Use `Algorithm: Flow` instead of `ILP`
2. Reduce `Time Limit` (30 seconds instead of 60)
3. Increase `Epsilon` (e.g., 0.05 allows 5% suboptimal)
4. Check your CSV sizes (if huge, Flow is better)

### "I want reproducible results for reporting"
**Set a Random Seed**:
1. Open Configuration page
2. Set `Random Seed: 42` (any number)
3. Same seed always gives same results
4. Great for documentation and presentations

---

## 📈 Reading the Visualizations

### Preference Satisfaction Chart
```
█████ ← Want tall here (1st choice)
███   ← Second choice acceptable
█     ← Trying to avoid
█     ← Last resort
```
**Good** = Most bars on the left (students got early choices)
**Bad** = Many bars on the right (students got late choices)

### Department Pie Chart
```
Shows: [Dept A: 30%] [Dept B: 25%] [Dept C: 45%]
```
**Good** = Similar sizes (roughly equal distribution)
**Bad** = One huge slice (imbalanced across departments)

### Topic Capacity Utilization
```
Topic 1: ████ (4/5 capacity)  ✓ Good use
Topic 2: █ (1/5 capacity)     ⚠ Wasted space
Topic 3: ██████ (6/5 capacity) ✓ Using overflow
```
**Good** = Blue bars mostly full
**Bad** = Many nearly-empty topics

---

## 🎯 Common Workflows

### Workflow 1: Standard Allocation
1. Go to **🚀 Run Allocation**
2. Upload `students.csv` and `capacities.csv`
3. Leave algorithm as default (hybrid, 60 sec)
4. Click **▶️ Run Allocation**
5. Download results as ZIP
6. Send to stakeholders ✅

### Workflow 2: Testing Different Settings
1. Go to **⚙️ Configuration**
2. Adjust settings
3. Go to **🚀 Run Allocation**
4. Re-upload same files
5. Click **▶️ Run Allocation**
6. Compare metrics
7. Repeat with different settings

### Workflow 3: Detailed Analysis
1. Complete allocation in **🚀 Run Allocation**
2. Go to **📊 Results Analysis**
3. Upload allocation results (auto-populated)
4. Examine charts for:
   - Preference satisfaction (happy students?)
   - Department balance (fair distribution?)
   - Capacity usage (efficient?)
5. If unhappy, go back to step 1 with different settings

---

## 📞 Getting More Help

| Question | Where to Look |
|----------|---------------|
| "What does this setting do?" | Hover over it in dashboard (tooltip) |
| "How do I configure for [goal]?" | CONFIGURATION_GUIDE.md → Quick Reference |
| "How to read this chart?" | CONFIGURATION_GUIDE.md → Visualizations |
| "Dashboard won't start" | DASHBOARD_QUICK_START.md → Troubleshooting |
| "Command-line usage?" | README.md |
| "Technical architecture?" | ARCHITECTURE.md |

---

**Happy allocating! 🎓**
