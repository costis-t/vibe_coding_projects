# Quick Examples - Thesis Allocation System

Copy-paste ready examples for common tasks.

## 1. Basic Allocation (No Config)

```bash
python allocate.py \
  --students data/input/students.csv \
  --capacities data/input/capacities.csv \
  --out data/output/allocation.csv \
  --summary data/output/summary.txt
```

## 2. Quick Test (Fast Algorithm)

```bash
python allocate.py \
  --algorithm flow \
  --students data/input/students.csv \
  --capacities data/input/capacities.csv \
  --out data/output/allocation.csv \
  --summary data/output/summary.txt
```

## 3. Validate Input Data Only

```bash
python allocate.py --validate-only \
  --students data/input/students.csv \
  --capacities data/input/capacities.csv
```

## 4. Generate Default Configuration

```bash
python allocate.py --save-config config.json
cat config.json
```

## 5. Use Configuration File

```bash
# Edit config.json first, then:
python allocate.py \
  --config config.json \
  --students data/input/students.csv \
  --capacities data/input/capacities.csv \
  --out data/output/allocation.csv \
  --summary data/output/summary.txt
```

## 6. Optimal Allocation with Verification

```bash
python allocate.py \
  --algorithm hybrid \
  --time-limit-sec 120 \
  --students data/input/students.csv \
  --capacities data/input/capacities.csv \
  --out data/output/allocation.csv \
  --summary data/output/summary.txt
```

## 7. Debug Mode with Logging

```bash
python allocate.py \
  --log-level DEBUG \
  --log-file logs/allocation.log \
  --students data/input/students.csv \
  --capacities data/input/capacities.csv \
  --out data/output/allocation.csv \
  --summary data/output/summary.txt

# Then check logs
tail logs/allocation.log
```

## 8. With Forced Topic Assignments

First, prepare CSV with `forced_topic` column:

```csv
student_id,plan_thesis,pref1,pref2,pref3,forced_topic
student01,Yes,topic12,topic04,topic02,topic10
student02,Yes,topic28,topic21,topic09,
```

Then run:

```bash
python allocate.py \
  --students data/input/students-special.csv \
  --capacities data/input/capacities.csv \
  --out data/output/allocation.csv \
  --summary data/output/summary.txt
```

## 9. With Visualization

```bash
python allocate.py \
  --students data/input/students.csv \
  --capacities data/input/capacities.csv \
  --out data/output/allocation.csv \
  --summary data/output/summary.txt \
  --sankey data/output/sankey.html

# Open sankey.html in browser
open data/output/sankey.html
```

## 10. Config + CLI Override

```bash
# Use config as base, override specific parameters
python allocate.py \
  --config config.json \
  --algorithm flow \
  --time-limit-sec 30 \
  --students data/input/students.csv \
  --capacities data/input/capacities.csv \
  --out data/output/allocation.csv \
  --summary data/output/summary.txt
```

## 11. Hard Department Minimums

```bash
python allocate.py \
  --dept-min-mode hard \
  --students data/input/students.csv \
  --capacities data/input/capacities.csv \
  --out data/output/allocation.csv \
  --summary data/output/summary.txt
```

## 12. Allow Near-Optimal Solutions (Faster)

```bash
python allocate.py \
  --epsilon-suboptimal 0.05 \
  --students data/input/students.csv \
  --capacities data/input/capacities.csv \
  --out data/output/allocation.csv \
  --summary data/output/summary.txt
```

## 13. Compare Algorithms

```bash
# Run ILP
echo "Running ILP..."
python allocate.py \
  --algorithm ilp \
  --time-limit-sec 120 \
  --students data/input/students.csv \
  --capacities data/input/capacities.csv \
  --out data/output/allocation_ilp.csv \
  --summary data/output/summary_ilp.txt

# Run Flow
echo "Running Flow..."
python allocate.py \
  --algorithm flow \
  --students data/input/students.csv \
  --capacities data/input/capacities.csv \
  --out data/output/allocation_flow.csv \
  --summary data/output/summary_flow.txt

# Compare results
echo "Differences:"
diff data/output/allocation_ilp.csv data/output/allocation_flow.csv | head -20
```

## 14. Production Run (All Features)

```bash
python allocate.py \
  --config config.json \
  --algorithm hybrid \
  --time-limit-sec 300 \
  --random-seed 2024 \
  --students data/input/students.csv \
  --capacities data/input/capacities.csv \
  --overrides data/input/overrides.csv \
  --out data/output/allocation.csv \
  --summary data/output/summary.txt \
  --sankey data/output/allocation_sankey.html \
  --log-level INFO \
  --log-file logs/allocation.log
```

## 15. Batch Processing Multiple Datasets

```bash
#!/bin/bash

for dataset in dataset1 dataset2 dataset3; do
  echo "Processing $dataset..."
  python allocate.py \
    --students data/input/${dataset}_students.csv \
    --capacities data/input/capacities.csv \
    --out data/output/${dataset}_allocation.csv \
    --summary data/output/${dataset}_summary.txt \
    --log-file logs/${dataset}_allocation.log
done
```

## 16. Troubleshooting - Check Validation First

```bash
# When something goes wrong, validate first
python allocate.py --validate-only \
  --students data/input/students.csv \
  --capacities data/input/capacities.csv

# If validation passes but results are wrong, add debug logging
python allocate.py \
  --log-level DEBUG \
  --log-file logs/debug.log \
  --students data/input/students.csv \
  --capacities data/input/capacities.csv \
  --out data/output/allocation.csv \
  --summary data/output/summary.txt
```

## 17. Reproducible Results

```bash
# Same seed = same results
python allocate.py \
  --random-seed 42 \
  --algorithm flow \
  --students data/input/students.csv \
  --capacities data/input/capacities.csv \
  --out data/output/allocation.csv \
  --summary data/output/summary.txt
```

## 18. Check Help and Version

```bash
# Show all options
python allocate.py --help

# Check current config structure
python allocate.py --save-config test_config.json
cat test_config.json
```

## 19. Disable Validation for Known Good Data

```bash
# Skip validation if data is trusted and validated separately
python allocate.py \
  --no-validate \
  --students data/input/students.csv \
  --capacities data/input/capacities.csv \
  --out data/output/allocation.csv \
  --summary data/output/summary.txt
```

## 20. Strict Constraints (No Overflow)

```bash
python allocate.py \
  --enable-topic-overflow false \
  --enable-coach-overflow false \
  --students data/input/students.csv \
  --capacities data/input/capacities.csv \
  --out data/output/allocation.csv \
  --summary data/output/summary.txt
```

## Common Aliases

Add to your shell profile (`.bashrc`, `.zshrc`):

```bash
# Quick run with defaults
alias alloc-run="python /path/to/allocate.py"

# Fast test run
alias alloc-test="python /path/to/allocate.py --algorithm flow"

# Validate and run
alias alloc-validate="python /path/to/allocate.py --validate-only"

# With full logging
alias alloc-debug="python /path/to/allocate.py --log-level DEBUG --log-file logs/debug.log"
```

Then use:
```bash
alloc-run --students data/input/students.csv --capacities data/input/capacities.csv --out data/output/allocation.csv --summary data/output/summary.txt
```

## Notes

- All examples assume you're in the project root directory
- Data files are in `data/input/`
- Output files go to `data/output/`
- Logs go to `logs/` (auto-created)
- Config files can be JSON format
- Forced topic assignments require `forced_topic` column in students.csv

## Common Issues

### Students not assigned?
```bash
# Check if they have admissible topics
python allocate.py --validate-only --students ... --capacities ...
```

### Solver too slow?
```bash
# Use faster algorithm
python allocate.py --algorithm flow ...

# Or set time limit
python allocate.py --time-limit-sec 30 ...
```

### Wrong results?
```bash
# Enable debug logging to see what's happening
python allocate.py --log-level DEBUG --log-file debug.log ...
```

### Want to change parameters?
```bash
# Generate config file to edit
python allocate.py --save-config config.json
# Edit config.json
python allocate.py --config config.json ...
```

## See Also

- `README.md` - Quick reference
- `USAGE_GUIDE.md` - Detailed guide
- `ARCHITECTURE.md` - System design
