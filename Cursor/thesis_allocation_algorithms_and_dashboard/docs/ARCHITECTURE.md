# Thesis Allocation System - Architecture & Design

## Overview

The thesis allocation system is a professional-grade solver for optimally assigning students to thesis topics while respecting capacity constraints and student preferences.

## Architecture Principles

- **Modularity**: Clear separation of concerns with focused modules
- **Type Safety**: Full type hints throughout for IDE support and early error detection
- **Validation**: Comprehensive input validation with informative error messages
- **Extensibility**: Easy to add new algorithms or constraint types
- **Configuration**: Centralized, structured configuration management
- **Logging**: Consistent logging for debugging and monitoring

## Core Modules

### 1. **Entities** (`allocator/entities.py`)

Defines core domain models with validation methods:

- `Student`: Represents a student with preferences, tiers, bans, and **NEW** forced topic assignments
- `Topic`: Represents a thesis topic with capacity and coach info
- `Coach`: Represents a coach with total capacity
- `Department`: Represents a department with minimum student requirements
- `AssignmentRow`: Result of allocation for a single student

Each entity includes `.is_valid()` and utility methods for business logic.

### 2. **Configuration** (`allocator/config.py`)

Hierarchical, type-safe configuration system:

```python
AllocationConfig
├── PreferenceConfig      # Preference calculation parameters
├── CapacityConfig        # Constraint parameters
└── SolverConfig          # Solver algorithm selection
```

**Features:**
- JSON serialization/deserialization
- Built-in validation
- Merge CLI arguments with config files
- Type-safe parameters with defaults

### 3. **Data Repository** (`allocator/data_repository.py`)

Loads and normalizes input data:

- `students.csv`: Student preferences and constraints
- `capacities.csv`: Topic/coach/department capacities
- `overrides.csv` (optional): Manual cost overrides

**NEW**: Supports `forced_topic` column in students CSV

### 4. **Validation** (`allocator/validation.py`)

Comprehensive input validation:

- Entity-level validation (required fields, valid ranges)
- Cross-entity consistency (referential integrity)
- Helpful error messages with context
- Separation of errors vs warnings

```python
validator = InputValidator()
is_valid, results = validator.validate_all(students, topics, coaches, departments)
```

### 5. **Preference Model** (`allocator/preference_model.py`)

Computes edge costs (student → topic):

**Precedence:** Forced → Overrides → Tiers → Ranks → Unranked → Banned (no edge)

**NEW**: Forced assignments get cost of -10000 (highest priority)

```python
pref_model = PreferenceModel(topics, overrides, cfg)
costs = pref_model.compute_costs(students)  # Dict[(student, topic)] → int
```

### 6. **Allocation Models**

#### ILP Model (`allocator/allocation_model_ilp.py`)

Integer Linear Programming solver using PuLP:

```
min Σ cost[s,t]·x[s,t] + penalties
s.t.
  - Each student gets exactly one topic
  - Topic capacity constraints
  - Coach total capacity constraints
  - Department minimums (soft or hard)
```

#### Flow Model (`allocator/allocation_model_flow.py`)

Min-cost max-flow algorithm for scalability.

#### Hybrid Model

Combines both: ILP for quality, Flow for verification.

### 7. **Logging** (`allocator/logging_config.py`)

Structured logging with color support:

```python
logger = setup_logging(level=logging.INFO, log_file="run.log")
logger.info("Processing complete")
```

### 8. **Outputs** (`allocator/outputs.py`)

Generates results and reports:

- `allocation.csv`: Final assignments
- `summary.txt`: Statistics and diagnostics
- Sankey visualization (optional)

## Data Flow

```
Input CSVs
    ↓
DataRepository (load & normalize)
    ↓
InputValidator (comprehensive checks)
    ↓
Configuration (user + CLI args)
    ↓
PreferenceModel (compute costs)
    ↓
AllocationModel (ILP/Flow/Hybrid)
    ↓
Output CSVs + Reports
```

## New Features

### Forced Topic Assignments

Allow administrators to force a student to a specific topic:

```csv
student_id,plan_thesis,pref1,...,forced_topic
student01,Yes,topic12,...,topic05
```

**Behavior:**
- Takes absolute precedence over all preferences
- Validates that forced_topic ≠ banned_topic
- Reports with preference_rank = -1
- Cost = -10000 (ensures assignment)

### Configuration Management

**Option 1: CLI Arguments** (backward compatible)
```bash
python allocate.py --students ... --capacities ... \
  --algorithm flow --time-limit-sec 60
```

**Option 2: JSON Config File**
```bash
# Export default config
python allocate.py --save-config config.json

# Use config
python allocate.py --config config.json --students ...
```

**Option 3: Merge Config + CLI**
```bash
python allocate.py --config config.json \
  --algorithm hybrid --time-limit-sec 120
```

### Input Validation

Comprehensive validation catches errors early:

```bash
# Validate only, don't solve
python allocate.py --students ... --validate-only

# Skip validation (for trusted inputs)
python allocate.py --students ... --no-validate
```

### Enhanced Logging

```bash
# Log level control
python allocate.py --log-level DEBUG --log-file allocation.log

# Automatic colored output + file logging
```

## Usage Examples

### Basic Allocation
```bash
python allocate.py \
  --students data/students.csv \
  --capacities data/capacities.csv \
  --out output/allocation.csv \
  --summary output/summary.txt
```

### With Forced Assignments
Create `students.csv` with `forced_topic` column:
```csv
student_id,plan_thesis,pref1,pref2,pref3,forced_topic
s001,Yes,t01,t02,t03,t05
s002,Yes,t04,t05,t06,
```

### Advanced Configuration
```bash
# Create config template
python allocate.py --save-config my_config.json

# Edit my_config.json with custom parameters

# Run with config
python allocate.py --config my_config.json \
  --students data/students.csv \
  --capacities data/capacities.csv \
  --out output/allocation.csv \
  --summary output/summary.txt
```

### Hybrid Algorithm with Flow Verification
```bash
python allocate.py \
  --students data/students.csv \
  --capacities data/capacities.csv \
  --algorithm hybrid \
  --time-limit-sec 120 \
  --out output/allocation.csv \
  --summary output/summary.txt
```

### With Comprehensive Logging
```bash
python allocate.py \
  --students data/students.csv \
  --capacities data/capacities.csv \
  --out output/allocation.csv \
  --summary output/summary.txt \
  --log-level DEBUG \
  --log-file logs/allocation.log
```

## Configuration Reference

See `config.py` for all parameters:

### Preference Configuration
- `allow_unranked` (bool): Allow unranked topics
- `tier2_cost` (int): Cost for tier 2 preferences
- `tier3_cost` (int): Cost for tier 3 preferences
- `unranked_cost` (int): Cost for unranked topics
- `top2_bias` (bool): Bias towards top 2 preferences

### Capacity Configuration
- `enable_topic_overflow` (bool): Allow topic overcapacity
- `enable_coach_overflow` (bool): Allow coach overcapacity
- `dept_min_mode` (str): "soft" or "hard" department minimums
- `P_dept_shortfall` (int): Penalty for department shortfall
- `P_topic` (int): Penalty for topic overflow
- `P_coach` (int): Penalty for coach overflow

### Solver Configuration
- `algorithm` (str): "ilp", "flow", or "hybrid"
- `time_limit_sec` (int): Solver timeout
- `random_seed` (int): Reproducibility seed
- `epsilon_suboptimal` (float): Allow near-optimal solutions

## Extending the System

### Adding a New Constraint

1. **Define entity property** in `entities.py`
2. **Load from CSV** in `data_repository.py`
3. **Validate** in `validation.py`
4. **Add to models** in allocation models
5. **Report results** in `outputs.py`

### Adding a New Algorithm

1. **Create** `allocator/allocation_model_myalgorithm.py`
2. **Implement** same interface as `AllocationModelILP`
3. **Register** in `allocate.py` CLI
4. **Test** with existing test suite

## Testing

Create unit tests in `tests/`:

```python
from allocator.config import AllocationConfig
from allocator.validation import InputValidator
from allocator.entities import Student, Topic

def test_forced_topic_validation():
    student = Student(
        student="s1",
        plan=True,
        tiers={},
        ranks=[],
        banned={"t1"},
        forced_topic="t1"  # Invalid!
    )
    assert not student.is_valid()
```

## Performance Characteristics

- **ILP**: Optimal, slower (seconds to minutes)
- **Flow**: Near-optimal, faster (milliseconds to seconds)
- **Hybrid**: Combines both for verification

Typical performance with 1000 students, 50 topics:
- ILP: 10-60 seconds
- Flow: 0.5-5 seconds
- Hybrid: 10-65 seconds

## Future Enhancements

- [ ] Database backend for large-scale deployments
- [ ] Web UI for interactive configuration
- [ ] Real-time constraint modification
- [ ] Multi-year sequential allocations
- [ ] Constraint relaxation analysis
- [ ] Parallel algorithm execution
- [ ] ML-based preference prediction
