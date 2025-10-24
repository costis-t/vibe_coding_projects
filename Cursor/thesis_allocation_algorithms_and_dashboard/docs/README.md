# Thesis Topic Allocator - Professional Edition (rofl)

Optimally assigns each student to **exactly one** thesis topic while maximizing preference satisfaction and respecting:
- Per-topic capacities
- Per-coach total capacities
- Per-department desired minimums (soft/hard)
- Individual tiers/ranks/bans/overrides
- **NEW**: Forced topic assignments

## Key Features

- ✅ **Multiple Algorithms**: ILP (optimal), Flow (fast), Hybrid (verified)
- ✅ **Forced Assignments**: Lock students to specific topics
- ✅ **Configuration Management**: JSON-based config files
- ✅ **Input Validation**: Comprehensive checks with clear error messages
- ✅ **Structured Logging**: Debug-friendly logging with color output
- ✅ **Type-Safe**: Full type hints for IDE support
- ✅ **Modular Architecture**: Clean separation of concerns
- ✅ **Visualizations**: Sankey diagrams for flow analysis

## Quick Start

### 1. Setup

```bash
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Basic Allocation

```bash
python allocate.py \
  --students data/input/students.csv \
  --capacities data/input/capacities.csv \
  --out data/output/allocation.csv \
  --summary data/output/summary.txt
```

### 3. With Forced Assignments

Add a `forced_topic` column to `students.csv`:

```csv
student_id,plan_thesis,pref1,pref2,pref3,pref4,pref5,tier1,tier2,tier3,banned,forced_topic
student01,Yes,topic12,topic04,topic02,topic22,topic01,,,,,topic05
student02,Yes,topic28,topic21,topic09,topic24,topic14,,,,,
```

Then run normally:

```bash
python allocate.py \
  --students data/input/students.csv \
  --capacities data/input/capacities.csv \
  --out data/output/allocation.csv \
  --summary data/output/summary.txt
```

Students with `forced_topic` will be assigned to that topic regardless of other preferences.

## Advanced Usage

### Configuration File

Create a configuration file:

```bash
# Export default configuration
python allocate.py --save-config config.json
```

Edit `config.json` and use it:

```bash
python allocate.py \
  --config config.json \
  --students data/input/students.csv \
  --capacities data/input/capacities.csv \
  --out data/output/allocation.csv \
  --summary data/output/summary.txt
```

### Algorithm Selection

```bash
# Fast min-cost flow algorithm
python allocate.py --algorithm flow \
  --students data/input/students.csv \
  --capacities data/input/capacities.csv \
  --out data/output/allocation.csv \
  --summary data/output/summary.txt

# Hybrid: ILP with flow verification
python allocate.py --algorithm hybrid --time-limit-sec 120 \
  --students data/input/students.csv \
  --capacities data/input/capacities.csv \
  --out data/output/allocation.csv \
  --summary data/output/summary.txt
```

### Input Validation

```bash
# Validate inputs without solving
python allocate.py --validate-only \
  --students data/input/students.csv \
  --capacities data/input/capacities.csv

# Skip validation for trusted inputs
python allocate.py --no-validate \
  --students data/input/students.csv \
  --capacities data/input/capacities.csv \
  --out data/output/allocation.csv \
  --summary data/output/summary.txt
```

### Debugging & Logging

```bash
# Verbose logging with file output
python allocate.py --log-level DEBUG --log-file allocation.log \
  --students data/input/students.csv \
  --capacities data/input/capacities.csv \
  --out data/output/allocation.csv \
  --summary data/output/summary.txt
```

### Visualizations

```bash
# Generate Sankey diagram
python allocate.py \
  --students data/input/students.csv \
  --capacities data/input/capacities.csv \
  --out data/output/allocation.csv \
  --summary data/output/summary.txt \
  --sankey data/output/allocation_sankey.html
```

## Input Files

### students.csv

Required columns:
- `student_id`: Unique identifier
- `plan_thesis`: "Yes" or "No"
- `pref1..pref5`: Topic preferences (ranked)

Optional columns:
- `tier1`: `|`-separated tier 1 topics
- `tier2`: `|`-separated tier 2 topics
- `tier3`: `|`-separated tier 3 topics
- `banned`: `|`-separated banned topics
- `forced_topic`: Force assignment to specific topic (**NEW**)

Example:
```csv
student_id,plan_thesis,pref1,pref2,pref3,pref4,pref5,tier1,tier2,tier3,banned,forced_topic
s001,Yes,t01,t02,t03,t04,t05,,,,,t10
s002,Yes,t05,t04,t03,t02,t01,,,,,
s003,Yes,t10,t11,t12,t13,t14,t10|t11,t15,,,
```

### capacities.csv

Required columns (flexible naming):
- `topic_id`: Topic identifier
- `coach_id`: Coach identifier
- `maximum students per topic`: Topic capacity
- `maximum students per coach`: Coach total capacity
- `department_id`: Department identifier
- `Desired minimum by department`: Soft lower bound

Example:
```csv
topic_id,coach_id,maximum students per topic,maximum students per coach,department_id,Desired minimum by department
topic01,coach_a,4,12,dept_cs,5
topic02,coach_a,3,12,dept_cs,5
topic03,coach_b,5,10,dept_eng,3
```

### overrides.csv (optional)

Manual cost overrides for specific student-topic pairs:

```csv
student_id,topic_id,cost
s001,t05,0
s002,t10,500
```

## Configuration Options

### Preference Settings

- `allow_unranked` (bool, default=true): Allow assigning to unranked topics
- `tier2_cost` (int, default=1): Cost for tier 2 preferences
- `tier3_cost` (int, default=5): Cost for tier 3 preferences
- `unranked_cost` (int, default=200): Cost for unranked topics
- `top2_bias` (bool, default=true): Prioritize top 2 preferences

### Capacity Settings

- `enable_topic_overflow` (bool, default=true): Allow exceeding topic capacity
- `enable_coach_overflow` (bool, default=true): Allow exceeding coach capacity
- `dept_min_mode` (str, "soft"/"hard", default="soft"): Enforce department minimums
- `P_dept_shortfall` (int, default=1000): Penalty for unmet department minimum
- `P_topic` (int, default=800): Penalty for topic overflow
- `P_coach` (int, default=600): Penalty for coach overflow

### Solver Settings

- `algorithm` (str, "ilp"/"flow"/"hybrid", default="ilp"): Optimization algorithm
- `time_limit_sec` (int, optional): Solver timeout in seconds
- `random_seed` (int, optional): Seed for reproducibility
- `epsilon_suboptimal` (float, optional): Allow near-optimal solutions (e.g., 0.05 for 5%)

## Output Files

### allocation.csv

Final student-topic assignments with details:
- `student_id`
- `assigned_topic`
- `assigned_coach`
- `department_id`
- `preference_rank`: -1 (forced), 0-2 (tier), 10-14 (ranked), 999 (unranked)
- `effective_cost`
- `via_topic_overflow`: 1 if topic exceeded capacity
- `via_coach_overflow`: 1 if coach exceeded capacity
- `forced`: 1 if forced assignment

### summary.txt

Statistics and diagnostics:
- Total students assigned
- Preference satisfaction metrics
- Capacity utilization
- Department minimum satisfaction
- Unassigned students (if any)
- Algorithm and timing information

## Architecture

See `ARCHITECTURE.md` for detailed system design, module overview, and extension guide.

## CLI Help

```bash
python allocate.py --help
```

## Examples

### Scenario: Prefer ILP but fallback to flow if timeout

```bash
# Try ILP with 60-second limit
python allocate.py --algorithm ilp --time-limit-sec 60 \
  --students data/input/students.csv \
  --capacities data/input/capacities.csv \
  --out data/output/allocation_ilp.csv \
  --summary data/output/summary_ilp.txt || \
# Fallback to flow if ILP times out
python allocate.py --algorithm flow \
  --students data/input/students.csv \
  --capacities data/input/capacities.csv \
  --out data/output/allocation.csv \
  --summary data/output/summary.txt
```

### Scenario: Validate and test configuration

```bash
# Validate only
python allocate.py --validate-only \
  --students data/input/students.csv \
  --capacities data/input/capacities.csv

# Test with small time limit
python allocate.py --algorithm hybrid --time-limit-sec 10 \
  --students data/input/students.csv \
  --capacities data/input/capacities.csv \
  --out data/output/test_allocation.csv \
  --summary data/output/test_summary.txt
```

## Troubleshooting

### "Unassignable students" warning

Students with no admissible topics (all banned, or preferences conflict with capacities):

1. Review `banned` column
2. Check preference coverage vs. available topics
3. Verify capacities are not too restrictive

### Validation errors

Run with `--validate-only` to check input data:

```bash
python allocate.py --validate-only \
  --students data/input/students.csv \
  --capacities data/input/capacities.csv
```

### Performance issues

- Use `--algorithm flow` for speed (sacrifices optimality slightly)
- Add `--time-limit-sec 30` to limit solver time
- Reduce topic count or increase capacities
- Use `--epsilon-suboptimal 0.05` to allow 5% suboptimal solutions

## Development

Create unit tests in `tests/`:

```python
pytest tests/
```

See ARCHITECTURE.md for extension guide.

## Requirements

- Python 3.8+
- PuLP >= 2.7.0
- Pandas >= 2.0.0
- NetworkX
- Plotly >= 5.20.0 (for visualizations)

## License

See LICENSE file

## Support

For issues or questions, refer to ARCHITECTURE.md or create an issue.
