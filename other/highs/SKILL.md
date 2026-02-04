---
name: highs
description: High Performance Optimization Software for solving linear programming (LP), mixed integer linear programming (MILP), and quadratic programming (QP) problems
---

# HiGHS - High Performance Optimization Software

Comprehensive assistance with HiGHS development, generated from official documentation.

HiGHS is open-source software for defining, modifying, and solving large-scale sparse linear optimization models. It's freely available under MIT license with no third-party dependencies.

## When to Use This Skill

Use this skill when:
- Solving **linear programming (LP)** problems
- Solving **mixed integer linear programming (MILP)** problems
- Solving **quadratic programming (QP)** problems
- Implementing optimization solutions in C++, Python (highspy), Julia, C, C#, Fortran, or Rust
- Building or modifying optimization models programmatically
- Working with MPS or CPLEX LP file formats
- Optimizing performance with parallel solvers or GPU acceleration
- Setting solver options and tolerances
- Hot-starting from existing solutions or bases

## Problem Types Supported

HiGHS can solve problems of the form:

**Linear Programming (LP):**
```
minimize    c^T x
subject to  L ≤ Ax ≤ U
            l ≤ x ≤ u
```

**Mixed Integer Linear Programming (MILP):**
Same as LP, but some variables must take integer values.

**Quadratic Programming (QP):**
LP with additional objective term `½x^T Q x` where Q is positive semi-definite.
(Note: Cannot solve integer QP problems)

## Solvers Available

- **Simplex methods:** Revised simplex (primal and dual)
- **Interior point method:** For continuous LP and QP
- **PDLP:** First-order primal-dual method (GPU-accelerated option available)
- **Branch-and-cut:** For MILP
- **Active set:** For QP

## Quick Reference

### Common Patterns

#### 1. Basic Model Setup (Python with highspy)

```python
import highspy
h = highspy.Highs()

# Read model from file
h.readModel("model.mps")

# Solve
h.run()

# Get solution
solution = h.getSolution()
info = h.getInfo()
```

#### 2. Building a Model Programmatically

```python
import highspy
h = highspy.Highs()

# Add variables (one at a time)
h.addCol(cost=1.0, lower=0.0, upper=4.0, num_nz=0, index=None, value=None)  # x
h.addCol(cost=1.0, lower=1.0, upper=float('inf'), num_nz=0, index=None, value=None)  # y

# Set variable as integer
h.changeColIntegrality(1, highspy.HighsVarType.kInteger)

# Set objective sense
h.changeObjectiveSense(highspy.ObjSense.kMinimize)

# Solve
h.run()
```

#### 3. Using with Julia JuMP

```julia
using JuMP
import HiGHS

model = Model(HiGHS.Optimizer)
set_optimizer_attribute(model, "presolve", "on")
set_optimizer_attribute(model, "time_limit", 60.0)

# Define your optimization model...
optimize!(model)
```

#### 4. Setting Options

```python
h = highspy.Highs()

# Common options
h.setOptionValue("presolve", "on")
h.setOptionValue("time_limit", 100.0)
h.setOptionValue("mip_rel_gap", 0.01)
h.setOptionValue("solver", "ipm")  # interior point method

# For GPU acceleration with PDLP
h.setOptionValue("solver", "pdlp")
h.setOptionValue("kkt_tolerance", 1e-4)  # Recommended for PDLP
```

#### 5. Hot Starting

```python
# Set initial solution
h.setSolution(solution)

# Set initial basis
h.setBasis(basis)

# Run from warm start
h.run()
```

#### 6. Extracting Model Information

```python
# Get model dimensions
num_cols = h.getNumCols()
num_rows = h.getNumRows()
num_nz = h.getNumEntries()

# Get specific column/row data
col_data = h.getCol(col_index)
row_data = h.getRow(row_index)

# Get matrix coefficient
coeff = h.getCoeff(row_index, col_index)
```

#### 7. Modifying Models

```python
# Change objective coefficient
h.changeColCost(col_index, new_cost)

# Change bounds
h.changeColBounds(col_index, new_lower, new_upper)
h.changeRowBounds(row_index, new_lower, new_upper)

# Change matrix coefficient
h.changeCoeff(row_index, col_index, new_value)
```

## Reference Files

This skill includes comprehensive documentation in `references/`:

- **api.md** - Api documentation
- **getting_started.md** - Getting Started documentation
- **guide.md** - Guide documentation
- **options.md** - Options documentation
- **solvers.md** - Solvers documentation
- **terminology.md** - Terminology documentation

Use `view` to read specific reference files when detailed information is needed.

## Key Concepts

### Installation

**Via Package Managers:**
- **Python:** `pip install highspy` or `conda install highs`
- **Julia:** `using Pkg; Pkg.add("HiGHS")`
- **C#:** NuGet package available
- **Rust:** Available via cargo

**From Source:**
```bash
git clone https://github.com/ERGO-Code/HiGHS.git
cd HiGHS
cmake -S. -B build
cmake --build build --parallel
```

### File Formats Supported

- `.mps` - MPS format (industry standard)
- `.lp` - CPLEX LP format
- `.gz` - Compressed files (gzip)

### Data Structures

**Key Classes:**
- `HighsLp` - Linear programming model data
- `HighsModel` - General optimization model
- `HighsSparseMatrix` - Sparse matrix representation
- `HighsHessian` - Quadratic objective Hessian
- `HighsSolution` - Solution data
- `HighsBasis` - Basis status information
- `HighsInfo` - Solver statistics and info

**Important Enums:**
- `HighsModelStatus` - Model status (optimal, infeasible, unbounded, etc.)
- `HighsVarType` - Variable types (continuous, integer, semi-continuous, etc.)
- `ObjSense` - Objective sense (minimize, maximize)

### Tolerances and Accuracy

HiGHS uses absolute tolerances by default (default: 1e-7):
- **Primal feasibility tolerance** - How close to feasible
- **Dual feasibility tolerance** - Dual constraint violations
- **Optimality tolerance** - KKT condition satisfaction

**Important:** PDLP uses **relative** tolerances. For PDLP, increase `kkt_tolerance` to 1e-4 for faster convergence.

### GPU Acceleration

PDLP solver can run on NVIDIA GPUs (Linux/Windows only):
- Requires CUDA Toolkit and matching NVIDIA driver
- Must build HiGHS locally with CMake
- Set solver to "pdlp" and adjust tolerances

### Callbacks

HiGHS supports callbacks for:
- Logging custom output
- Implementing custom termination criteria
- Monitoring solver progress
- Extracting intermediate solutions

## Working with This Skill

### For Beginners
1. Start with `references/getting_started.md` for installation and basic concepts
2. Review problem formulations in `references/terminology.md`
3. Try basic examples from `references/api.md`

### For Specific Features
- **Building models:** `references/guide.md` (Basic features section)
- **API reference:** `references/api.md` (C++, Python, Julia interfaces)
- **Solver options:** `references/options.md`
- **Advanced topics:** `references/guide.md` (GPU, hot start, presolve)
- **Performance tuning:** `references/solvers.md`

### For Code Examples
- Python examples in `references/api.md` (Python section)
- Julia examples in `references/api.md` (Julia section)
- C++ examples in `references/api.md` (C++ section)

## Performance Benchmarks

HiGHS is competitive with commercial solvers. See:
- Mittelmann LP benchmarks (feasibility and optimality)
- Mittelmann MILP benchmarks

## Common Use Cases

1. **Supply chain optimization** - Minimize costs while meeting constraints
2. **Resource allocation** - Optimize resource distribution
3. **Production planning** - Maximize output or minimize waste
4. **Portfolio optimization** - Balance risk and return (QP)
5. **Network flow problems** - Transportation, routing
6. **Scheduling** - Job shop, employee scheduling (MILP)
7. **Cutting stock problems** - Minimize material waste

## Resources

### references/
Organized documentation extracted from official sources. These files contain:
- Detailed explanations
- Code examples with language annotations
- Links to original documentation
- Table of contents for quick navigation

### scripts/
Add helper scripts here for common automation tasks.

### assets/
Add templates, boilerplate, or example projects here.

## Citing HiGHS

If you use HiGHS in an academic context, please cite:

**Parallelizing the dual revised simplex method**
Q. Huangfu and J. A. J. Hall, *Mathematical Programming Computation*, 10 (1), 119-142, 2018.
DOI: [10.1007/s12532-017-0130-5](https://link.springer.com/article/10.1007/s12532-017-0130-5)

## Troubleshooting

### Model Status Not Optimal
- Check `HighsInfo` for infeasibility/unboundedness indicators
- Review constraint feasibility and objective bounds
- Try different solvers (simplex, IPM, PDLP)

### PDLP Reports Optimal But HiGHS Says Not Optimal
- PDLP uses relative tolerances vs absolute
- Increase `kkt_tolerance` to 1e-4
- Check `HighsInfo` for actual infeasibility values
- Consider if the solution is "good enough" for your use case

### Slow Performance
- Enable presolve: `setOptionValue("presolve", "on")`
- Try parallel mode for large problems
- Adjust time limits and MIP gap tolerances
- Consider GPU acceleration for very large LPs (PDLP)

### Memory Issues with Large Models
- Use sparse matrix representations
- Pass models via `passModel()` rather than building incrementally
- Consider model compression techniques

## Additional Resources

- **GitHub:** https://github.com/ERGO-Code/HiGHS
- **Documentation:** https://ergo-code.github.io/HiGHS/dev/
- **Contact:** highsopt@gmail.com

## Notes

- This skill was automatically generated from official HiGHS documentation
- Reference files preserve structure and examples from source docs
- Code examples include language detection for syntax highlighting
- All references link back to original documentation

## Updating

To refresh this skill with updated documentation:
1. Re-run the scraper: `python3 cli/doc_scraper.py --config configs/highs.json`
2. The skill will be rebuilt with the latest information
