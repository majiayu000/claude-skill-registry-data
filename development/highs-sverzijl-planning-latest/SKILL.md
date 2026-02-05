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
- Extracting model information and solution data
- Modifying existing optimization models

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

- **Simplex methods:** Revised simplex (primal and dual) - Most robust for general LP
- **Interior point method:** Two implementations (IPX serial, HiPO parallel)
- **PDLP:** First-order primal-dual method (GPU-accelerated option available)
- **Branch-and-cut:** For MILP
- **Active set:** For QP

## Quick Reference

### 1. Basic Setup and Solve (Python)

Initialize HiGHS and solve a model from file:

```python
import highspy
import numpy as np
h = highspy.Highs()

# Read a model from MPS file
filename = 'model.mps'
status = h.readModel(filename)
print('Reading model file', filename, 'returns a status of', status)

# Solve the model
h.run()

# Get solution
solution = h.getSolution()
info = h.getInfo()
```

### 2. Building a Simple Model (Python Simplified Interface)

Build an optimization model programmatically:

```python
# Problem:
#   minimize    f  =  x0 +  x1
#   subject to              x1 <= 7
#               5 <=  x0 + 2x1 <= 15
#               6 <= 3x0 + 2x1
#               0 <= x0 <= 4; 1 <= x1

import highspy
h = highspy.Highs()

x0 = h.addVariable(lb = 0, ub = 4)
x1 = h.addVariable(lb = 1, ub = 7)

h.addConstr(5 <=   x0 + 2*x1 <= 15)
h.addConstr(6 <= 3*x0 + 2*x1)

h.minimize(x0 + x1)
```

### 3. Building a MILP Model (Julia C API)

Complete MILP example using Julia's C API wrapper:

```julia
using HiGHS

highs = Highs_create()
ret = Highs_setBoolOptionValue(highs, "log_to_console", false)
@assert ret == 0  # If ret != 0, something went wrong

# Add columns (variables)
Highs_addCol(highs, 1.0, 0.0, 4.0, 0, C_NULL, C_NULL)   # x is column 0
Highs_addCol(highs, 1.0, 1.0, Inf, 0, C_NULL, C_NULL)   # y is column 1

# Set y as integer variable
Highs_changeColIntegrality(highs, 1, kHighsVarTypeInteger)

# Set objective to minimize
Highs_changeObjectiveSense(highs, kHighsObjSenseMinimize)

# Solve
Highs_run(highs)
```

### 4. Using with Julia JuMP (High-Level Interface)

```julia
using JuMP
import HiGHS

model = Model(HiGHS.Optimizer)
set_optimizer_attribute(model, "presolve", "on")
set_optimizer_attribute(model, "time_limit", 60.0)

# Define your optimization model...
@variable(model, x >= 0)
@variable(model, y >= 0)
@objective(model, Min, x + y)
@constraint(model, 5 <= x + 2*y <= 15)

optimize!(model)
```

### 5. Extracting Solution Values Efficiently (Python)

**Important:** Direct array access is slow in Python. Convert to list first!

```python
import highspy
h = highspy.Highs()
h.readModel('model.mps')
h.run()

# Get solution object
solution = h.getSolution()

# SLOW: Accessing directly from solution.col_value
# for i in range(num_cols):
#     val = solution.col_value[i]  # Takes 0.04s

# FAST: Convert to list first
col_value = list(solution.col_value)
for i in range(num_cols):
    val = col_value[i]  # Takes 0.0001s (400x faster!)
```

### 6. Setting Options and Choosing Solver

```python
import highspy
h = highspy.Highs()

# Set common options
h.setOptionValue("presolve", "on")
h.setOptionValue("time_limit", 100.0)
h.setOptionValue("mip_rel_gap", 0.01)

# Choose specific solver
h.setOptionValue("solver", "simplex")  # or "ipm", "pdlp", "hipo"

# For GPU acceleration with PDLP
h.setOptionValue("solver", "pdlp")
h.setOptionValue("kkt_tolerance", 1e-4)  # Recommended for PDLP
```

### 7. Command Line Usage (Executable)

```bash
# Basic solve
$ bin/highs model.mps

# With options file
$ bin/highs --options_file=my_options.txt model.mps

# Write solution to file
$ bin/highs --solution_file=solution.txt model.mps

# See all command line options
$ bin/highs --help
```

**Example options file (my_options.txt):**
```
solver = pdlp
kkt_tolerance = 1e-4
presolve = on
time_limit = 300
```

### 8. C API - Adding Variables and Constraints

```c
// Add a single column (variable)
Highs_addCol(highs, cost, lower, upper, num_new_nz, index, value)

// Add multiple columns
Highs_addCols(highs, num_new_col, costs, lower, upper, num_new_nz,
              starts, index, value)

// Change coefficient in constraint matrix
Highs_changeCoeff(highs, row, col, new_value)

// Change variable bounds
Highs_changeColBounds(highs, col, new_lower, new_upper)

// Change objective coefficient
Highs_changeColCost(highs, col, new_cost)

// Set variable as integer
Highs_changeColIntegrality(highs, col, kHighsVarTypeInteger)
```

### 9. Building from Source

```bash
# Clone repository
git clone https://github.com/ERGO-Code/HiGHS.git

# Build with CMake
cd HiGHS
cmake -S. -B build
cmake --build build --parallel

# For C# support
cmake -S. -Bbuild -DCSHARP=ON
```

### 10. Installation via Package Managers

```bash
# Python
$ pip install highspy

# Julia
julia> using Pkg
julia> Pkg.add("HiGHS")

# C# (NuGet)
$ dotnet add package Highs.Native --version 1.12.0

# Linux (install dependencies for HiPO)
$ sudo apt update
$ sudo apt install libopenblas-dev
```

## Reference Files

This skill includes comprehensive documentation in `references/`:

### api.md (15 pages)
Complete API reference for all language interfaces:
- **C++ interface:** Building from source, class-based API
- **Python (highspy):** Installation, examples, efficient value extraction
- **Julia:** JuMP integration, C API wrapper
- **C API:** Complete function reference for all operations
- **C#:** NuGet package, build instructions
- **Data structures:** HighsLp, HighsModel, HighsSparseMatrix, HighsHessian
- **Enums:** Model status, variable types, solver options

### getting_started.md (3 pages)
- Overview of HiGHS capabilities (LP, MILP, QP)
- Installation methods (source, package managers, binaries)
- File format support (MPS, LP, gzip)
- Executable usage and command-line options
- Citation information

### guide.md (4 pages)
Advanced features and usage patterns:
- **Basic features:** Defining models, solving, extracting results
- **Further features:** Model modification, hot starting, presolve
- **GPU acceleration:** PDLP solver setup with CUDA
- **Feasibility and optimality:** Understanding tolerances (absolute vs relative)

### options.md (2 pages)
- Complete list of HiGHS options
- How to set options (file, command line, API)
- Important options: presolve, solver, parallel, time_limit, tolerances

### solvers.md (1 page)
- Detailed solver descriptions (simplex, IPM, PDLP)
- When to use each solver
- Performance characteristics
- Academic references

### terminology.md (1 page)
- Optimization terminology explained
- Bounds, constraints, feasible region
- Sparse matrices
- Primal and dual values
- Basic solutions and sensitivity

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
- `HighsModel` - General optimization model (includes QP)
- `HighsSparseMatrix` - Sparse matrix representation
- `HighsHessian` - Quadratic objective Hessian
- `HighsSolution` - Solution data (primal/dual values)
- `HighsBasis` - Basis status information
- `HighsInfo` - Solver statistics and convergence info

**Important Enums:**
- `HighsModelStatus` - Model status (optimal, infeasible, unbounded, etc.)
- `HighsVarType` - Variable types (continuous, integer, semi-continuous, etc.)
- `ObjSense` - Objective sense (minimize, maximize)
- `HighsStatus` - Return status from API calls

### Tolerances and Accuracy

HiGHS uses **absolute tolerances** by default (default: 1e-7):
- **Primal feasibility tolerance** - How close constraints must be satisfied
- **Dual feasibility tolerance** - Dual constraint violations
- **Optimality tolerance** - KKT condition satisfaction

**Important:** PDLP uses **relative** tolerances. For PDLP, increase `kkt_tolerance` to 1e-4 for faster convergence with acceptable accuracy.

### GPU Acceleration

PDLP solver can run on NVIDIA GPUs (Linux/Windows only):
- Requires CUDA Toolkit and matching NVIDIA driver
- Must build HiGHS locally with CMake
- Set solver to "pdlp" and adjust tolerances
- Verify CUDA: `nvcc --version`

**Health Warning:** PDLP may not achieve same accuracy as simplex/IPM. Check `HighsInfo` for actual feasibility values.

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
3. Try **Quick Reference Example 2** (simple Python model)
4. Learn file-based solving with **Quick Reference Example 1**

### For Intermediate Users
- **Building models:** See examples in `references/api.md` (Python section)
- **Solver options:** Read `references/options.md` for tuning
- **Model modification:** Check `references/guide.md` (Further features)
- **Hot starting:** Use previous solutions to speed up solving

### For Advanced Users
- **API reference:** `references/api.md` for language-specific details
- **Performance tuning:** `references/solvers.md` - choose optimal solver
- **GPU acceleration:** `references/guide.md` (GPU section)
- **Tolerances:** `references/guide.md` (Feasibility and optimality)

### For Code Examples
- **Python:** `references/api.md` (Python section) - Complete highspy examples
- **Julia:** `references/api.md` (Julia section) - JuMP and C API
- **C++:** `references/api.md` (C++ section) - Native library
- **C API:** `references/api.md` (C section) - Low-level interface

## Performance Benchmarks

HiGHS is competitive with commercial solvers. See:
- [Mittelmann LP benchmarks](http://plato.asu.edu/ftp/lpopt.html) (feasibility and optimality)
- [Mittelmann MILP benchmarks](http://plato.asu.edu/ftp/milp.html)

## Common Use Cases

1. **Supply chain optimization** - Minimize costs while meeting constraints
2. **Resource allocation** - Optimize resource distribution
3. **Production planning** - Maximize output or minimize waste
4. **Portfolio optimization** - Balance risk and return (QP)
5. **Network flow problems** - Transportation, routing
6. **Scheduling** - Job shop, employee scheduling (MILP)
7. **Cutting stock problems** - Minimize material waste
8. **Energy systems** - Power generation and distribution

## Resources

### references/
Organized documentation extracted from official sources. These files contain:
- Detailed explanations of all features
- Code examples with language annotations
- Links to original documentation
- Table of contents for quick navigation

### scripts/
Add helper scripts here for common automation tasks (e.g., batch solving, result analysis).

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
- Verify model data is correct (no NaN, Inf values)

### PDLP Reports Optimal But HiGHS Says Not Optimal
- PDLP uses relative tolerances vs absolute
- Increase `kkt_tolerance` to 1e-4 (recommended)
- Check `HighsInfo` for actual infeasibility values
- Consider if the solution is "good enough" for your use case

### Slow Performance
- Enable presolve: `setOptionValue("presolve", "on")`
- Try parallel mode for large problems
- Adjust time limits and MIP gap tolerances
- Consider GPU acceleration for very large LPs (PDLP)
- Try different solver: simplex vs IPM vs PDLP

### Memory Issues with Large Models
- Use sparse matrix representations
- Pass models via `passModel()` rather than building incrementally
- Consider model compression techniques
- Use compressed input files (.mps.gz)

### Python Performance Issues
- **Critical:** Convert solution arrays to lists before iteration (see Example 5)
- Use numpy arrays when appropriate
- Avoid repeated API calls in loops

### Can't Read LP/MPS File
- Check file format (lpsolve format NOT supported)
- Try compressed version (.gz works, .zip does not)
- Verify file path is correct

## Additional Resources

- **GitHub:** https://github.com/ERGO-Code/HiGHS
- **Documentation:** https://ergo-code.github.io/HiGHS/dev/
- **Contact:** highsopt@gmail.com
- **Issues:** File bugs at GitHub Issues

## Notes

- This skill was automatically generated from official HiGHS documentation (v1.10.0+)
- Reference files preserve structure and examples from source docs
- Code examples include language detection for syntax highlighting
- All references link back to original documentation
- Examples tested with HiGHS v1.10.0 and later

## Updating

To refresh this skill with updated documentation:
1. Re-run the scraper: `python3 cli/doc_scraper.py --config configs/highs.json`
2. The skill will be rebuilt with the latest information
