# 🎛️ Dashboard Configuration & Explanation Guide

## Overview

This guide explains every setting in the Streamlit dashboard and what each one does. All settings directly impact how the allocation algorithm works.

---

## ⚙️ Configuration Page

### Preference Settings
*How to value different preference levels (lower cost = higher priority)*

#### **Allow Unranked Topics** (Toggle)
- **ON** (Default): Students CAN be assigned to topics they didn't rank
- **OFF**: Students MUST get one of their ranked preferences or tier assignments
- **When to use OFF**: When you want to guarantee every student gets a preference they listed

#### **Tier 2 Cost** (Slider: 0-10, Default: 1)
- Penalty for assigning to a **Tier 2 preference**
- Lower value = more willing to use tier 2
- Example: 1 = almost as good as tier 1; 5 = quite undesirable
- **Use case**: Set higher if you want students to prefer ranked choices over tiers

#### **Tier 3 Cost** (Slider: 0-20, Default: 5)
- Penalty for assigning to a **Tier 3 preference**
- Lower value = more acceptable; higher value = avoid this tier
- **Use case**: Set very high if tier 3 is only for emergencies

#### **Unranked Cost** (Slider: 0-500, Default: 200)
- Penalty for assigning to a **topic the student never mentioned**
- Very high value (200+) = try hard to avoid this
- **Use case**: Default of 200 is good; increase if you really don't want unranked assignments

#### **Apply Top-2 Bias** (Toggle, Default: ON)
- **ON**: Strongly prefer 1st choice, then 2nd choice (exponential cost increase)
- **OFF**: All ranked preferences treated equally (linear cost increase)
- **When to use ON**: Most cases - students usually have strong preferences for top choices
- **When to use OFF**: When all preferences are equally important

---

### Capacity Settings
*How to handle when topics/coaches exceed capacity*

#### **Enable Topic Overflow** (Toggle, Default: ON)
- **ON**: Topics CAN exceed their capacity, but with penalty
- **OFF**: Hard limit - no topic can exceed capacity (may cause unassigned students)
- **When to use OFF**: Strict capacity requirements (e.g., lab equipment limits)

#### **Enable Coach Overflow** (Toggle, Default: ON)
- **ON**: Coaches CAN exceed their capacity, but with penalty
- **OFF**: Hard limit - no coach can exceed capacity (may cause unassigned students)
- **When to use OFF**: Coaches have strict maximum workload

#### **Department Min Mode** (Dropdown: "soft" | "hard")
- **soft** (Default): Try to meet department minimums, but not required
- **hard**: Strictly enforce department minimums (algorithm will always meet them)
- **When to use hard**: Department has strong minimums that must be honored

#### **Department Shortfall Penalty** (Slider: 0-5000, Default: 1000)
- Penalty for EACH STUDENT below the department minimum
- Higher = stricter enforcement
- **Impact**: Set higher to guarantee department minimums are met

#### **Topic Overflow Penalty** (Slider: 0-2000, Default: 800)
- Penalty for assigning beyond a topic's capacity
- Higher = stricter capacity enforcement
- **Impact**: Higher value prevents overallocation to popular topics

#### **Coach Overflow Penalty** (Slider: 0-2000, Default: 600)
- Penalty for assigning beyond a coach's capacity
- Higher = stricter enforcement
- **Impact**: Higher value prevents coaches from being overloaded

**💡 General Rule**: Higher penalties → stricter constraints → slower solving but fairer results

---

### Solver Settings
*Algorithm selection and optimization parameters*

#### **Algorithm** (Dropdown)

**ILP (Integer Linear Programming)**
- **Speed**: ⚡ Slow (10-120 seconds)
- **Quality**: 🎯🎯🎯 Optimal (guaranteed best solution)
- **Use when**: Final production run, critical decisions
- **Trade-off**: Longer wait, but perfect results

**Flow (Min-Cost Max-Flow)**
- **Speed**: ⚡⚡⚡ Fast (2-10 seconds)
- **Quality**: 🎯🎯 Near-optimal (usually good, but not always best)
- **Use when**: Testing configurations, quick previews, large datasets
- **Trade-off**: Faster, but may miss slightly better solutions

**Hybrid (ILP + Flow Verification)**
- **Speed**: ⚡⚡ Medium (10-120 seconds)
- **Quality**: 🎯🎯🎯 Verified optimal
- **Use when**: Important decisions where speed matters
- **Trade-off**: Balanced approach - good quality and reasonable speed

#### **Time Limit (Seconds)** (Slider: 0-600, Default: 60)
- Maximum time the solver can spend optimizing
- 0 = no limit (solver runs until done)
- Higher = better results but potentially longer wait
- **Recommendations**:
  - 10-30 sec: Quick test runs
  - 60 sec: Standard allocation
  - 300+ sec: Critical production runs

#### **Random Seed** (Number, Default: empty/random)
- Seed for reproducible results
- Same seed → exact same results (useful for reports)
- Leave empty for random allocation each time
- **Use case**: Set to 42 for documentation and demos

#### **Epsilon Suboptimal** (Slider: 0.0-1.0, Default: 0.0)
- Allow solutions within X% of optimal cost
- 0.0 = only truly optimal solutions
- 0.05 = accept 5% worse solutions (but faster)
- 0.1 = accept 10% worse solutions (much faster)
- **Example**: If optimal cost is 100, epsilon=0.05 accepts costs up to 105

---

## 🚀 Run Allocation Page

### Input Files
- **Students CSV** (Required): Your student preferences
- **Capacities CSV** (Required): Topic capacities and coach limits
- **Overrides CSV** (Optional): Manual adjustments to costs

### Algorithm Settings
Same as Configuration page, but specific to this run

### Validation Section
Shows:
- Number of students loaded
- Number of topics/capacities
- Column previews

### Results Display
After clicking "▶️ Run Allocation":

#### **Key Metrics**
- **Students Assigned**: Total count of allocated students
- **Optimal Cost**: Overall solution quality (lower = better)
- **Got Choice %**: Percentage of students who got a ranked preference
- **Status**: ✓ Success (all assigned) or ⚠ Partial (some unassigned)

#### **Allocation Details Table**
Shows each student's assignment:
- **student**: Student ID
- **assigned_topic**: Topic they got
- **assigned_coach**: Coach of that topic
- **department_id**: Department of that coach
- **preference_rank**: How they ranked this topic (-1=forced, 0-2=tier, 10-14=ranked, 999=unranked)
- **effective_cost**: Algorithm's cost for this assignment

#### **Download Options**
- 📥 **Allocation CSV**: Individual file, open in Excel
- 📥 **Summary TXT**: Text report with diagnostics
- 📦 **Download Both (ZIP)**: Both files compressed

---

## 📊 Results Analysis Page

### Upload Allocation Results
Upload previously generated allocation files to visualize

### Key Metrics Dashboard
Quick stats shown first:
- Total students assigned
- Percentage who got a ranked choice
- Optimal cost value
- Success/partial status

### Visualizations

#### **Preference Satisfaction Chart** (Bar Chart)
Shows how many students got each ranked choice level:
- **1st choice**: Green peak shows preference satisfaction
- **2nd choice**: Secondary bar
- **3rd-5th choice**: Lower bars show fallback assignments
- **What to look for**: Want tall left bars (students got top choices)

#### **Department Distribution** (Pie Chart)
Shows student count across departments:
- **What to look for**: Even distribution = fair allocation
- **What to worry about**: One slice much larger = imbalance

#### **Topic Capacity Utilization** (Overlaid Bars)
For each topic, shows:
- **Blue bar**: Actual students assigned
- **Gray bar**: Topic capacity
- **What to look for**: Blue bars near gray = efficient use
- **What to worry about**: Many short blue bars = wasted capacity

---

## 🔍 Data Explorer Page

### Students Section
Shows:
- Total number of students
- Sample of student records (first 10)
- Available columns

### Topics Section
Shows:
- Total topics available
- Sample of topic records
- Capacity information

### Coaches Section
Shows:
- Unique coaches
- Coach load capacities
- Department assignments

**Use this to**: Verify data quality before allocation

---

## 📈 Advanced Charts Page

### Cost Matrix Heatmap
Visualization showing:
- **Rows**: Students (first 50 sample)
- **Columns**: Topics
- **Colors**: Green (low cost) to Red (high cost)
- **What it shows**: Which student-topic pairs are attractive vs unattractive

### Cost Distribution Histogram
Shows how costs are spread:
- **Left skew**: Good! Most students got low-cost assignments
- **Right skew**: Bad! Many high-cost assignments

### Preference Rank Distribution
Shows spread of preference achievement:
- **Peak at left**: Good! Students got highly-ranked choices
- **Spread across**: Concerning! Wide variety of satisfaction levels

---

## 🎯 Quick Reference

### Best Configuration for Different Goals

**Goal: Maximize Student Satisfaction**
```
- Top2Bias: ON
- Allow Unranked: OFF
- Tier2 Cost: 1
- Algorithm: ILP (optimal)
- Time Limit: 300 sec
```

**Goal: Fast Results with Good Quality**
```
- Algorithm: Hybrid (ILP + Flow)
- Time Limit: 60 sec
- Epsilon: 0 (optimal only)
```

**Goal: Quick Testing**
```
- Algorithm: Flow
- Time Limit: 30 sec
- Epsilon: 0.1 (allow 10% suboptimal)
```

**Goal: Respect Capacity Limits Strictly**
```
- Topic Overflow: OFF
- Coach Overflow: OFF
- Dept Min Mode: hard
- Algorithm: ILP
```

---

## 📚 Key Concepts

### Preference Rank
- **-1**: Forced assignment (admin lock)
- **0-2**: Tier preference (Tier 1, 2, or 3)
- **10-14**: Ranked preference (pref1 through pref5, +9 offset)
- **999**: Unranked (not listed anywhere)

### Cost System
- **Lower cost = better assignment** (algorithm minimizes)
- **Negative cost**: Very high priority
- **Positive cost**: Lower priority
- **High penalty**: Constraint violation (discouraged but possible)

### Overflow
- Allows exceeding capacity with a **penalty cost**
- Useful when you'd rather exceed capacity than leave students unassigned
- Can be toggled OFF for hard limits

---

## 🆘 Troubleshooting

### "Why did student X not get their 1st choice?"
- Their 1st choice might be full/overcapacity
- Other constraints conflict (department min, coach cap, etc.)
- Algorithm optimizes globally, not locally

### "Why are some students unassigned?"
- All their preferences might be banned/full
- Department minimums conflicting
- Capacity constraints too tight
- Try: Enabling overflow or relaxing dept_min_mode to "soft"

### "Results are too slow"
- Reduce `time_limit_sec`
- Use `flow` algorithm instead of `ilp`
- Increase `epsilon` to allow suboptimal solutions

---

**Need help?** Check the "Run Allocation" page - each setting has a tooltip (hover over "?" icon) with additional details!
