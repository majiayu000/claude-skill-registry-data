---
name: pyomo
description: Expert in Pyomo mathematical optimization modeling in Python - use for optimization problems, linear/nonlinear programming, constraint programming, and dynamic optimization
---

# Pyomo Skill

Expert guidance for Python Optimization Modeling Objects (Pyomo), covering model formulation, solver integration, dynamic optimization with differential equations, and advanced analysis techniques.

## When to Use This Skill

Activate this skill when:
- **Building optimization models** - Linear programming (LP), mixed-integer programming (MIP), nonlinear programming (NLP), or MINLP problems
- **Formulating constraints and objectives** - Creating variables, parameters, constraints, and objective functions
- **Working with dynamic systems** - Differential algebraic equations (DAE), continuous-time optimization, ODE simulation
- **Solving optimization problems** - Integrating with solvers like GLPK, IPOPT, Gurobi, CPLEX
- **Analyzing model structure** - Community detection, model interrogation, accessing variable/dual values
- **Parameter estimation** - Data reconciliation, sensitivity analysis
- **Advanced features** - Generalized disjunctive programming (GDP), stochastic programming, decomposition methods

## Quick Reference

### Example 1: Simple Concrete Model (Beginner)

Create and solve a basic optimization model:

```python
import pyomo.environ as pyo

# Create a concrete model
model = pyo.ConcreteModel()

# Define variables
model.x = pyo.Var([1, 2, 3, 4], domain=pyo.Binary)

# Define objective: maximize sum of variables
model.obj = pyo.Objective(expr=sum(model.x[i] for i in model.x), sense=pyo.maximize)

# Add a constraint
model.con = pyo.Constraint(expr=sum(model.x[i] for i in model.x) <= 3)

# Solve
solver = pyo.SolverFactory('glpk')
results = solver.solve(model)

# Access solution
print(f"Objective value: {pyo.value(model.obj)}")
for i in model.x:
    print(f"x[{i}] = {pyo.value(model.x[i])}")
```

### Example 2: Accessing Variable Values After Solving

Get optimal values from solved models:

```python
import pyomo.environ as pyo

# After solving a model...
# Access a single variable value
opt_value = pyo.value(model.quant)

# Access indexed variable
opt_value_indexed = pyo.value(model.x[2])

# Iterate through all variables
for v in model.component_objects(pyo.Var, active=True):
    print(f"Variable: {v}")
    for index in v:
        print(f"  {v[index].name} = {pyo.value(v[index])}")
```

### Example 3: Dynamic Optimization with DAE (Intermediate)

Define and discretize a differential equation model:

```python
import pyomo.environ as pyo
from pyomo.dae import ContinuousSet, DerivativeVar

# Create model
model = pyo.ConcreteModel()

# Time domain
model.t = ContinuousSet(bounds=(0, 5))

# State variables
model.x = pyo.Var(model.t)
model.y = pyo.Var(model.t)

# Derivatives
model.dxdt = DerivativeVar(model.x, wrt=model.t)
model.dydt = DerivativeVar(model.y, wrt=model.t)

# Initial conditions
model.x[0].fix(1.0)
model.y[0].fix(0.0)

# Define ODE
def _ode_x(m, t):
    if t == 0:
        return pyo.Constraint.Skip
    return m.dxdt[t] == -m.x[t] + m.y[t]

def _ode_y(m, t):
    if t == 0:
        return pyo.Constraint.Skip
    return m.dydt[t] == m.x[t]

model.ode_x = pyo.Constraint(model.t, rule=_ode_x)
model.ode_y = pyo.Constraint(model.t, rule=_ode_y)

# Discretize using collocation
discretizer = pyo.TransformationFactory('dae.collocation')
discretizer.apply_to(model, nfe=20, ncp=3, scheme='LAGRANGE-RADAU')

# Solve
solver = pyo.SolverFactory('ipopt')
results = solver.solve(model)
```

### Example 4: Simulating Dynamic Systems

Simulate ODEs using the pyomo.DAE Simulator:

```python
import pyomo.environ as pyo
from pyomo.dae import ContinuousSet, DerivativeVar, Simulator

# Define model
m = pyo.ConcreteModel()
m.t = ContinuousSet(bounds=(0.0, 10.0))

# Parameters and variables
m.b = pyo.Param(initialize=0.25)
m.c = pyo.Param(initialize=5.0)
m.omega = pyo.Var(m.t)
m.theta = pyo.Var(m.t)
m.domegadt = DerivativeVar(m.omega, wrt=m.t)
m.dthetadt = DerivativeVar(m.theta, wrt=m.t)

# Initial conditions
m.omega[0].fix(0.0)
m.theta[0].fix(3.14 - 0.1)

# Differential equations
def _diffeq1(m, t):
    return m.domegadt[t] == -m.b * m.omega[t] - m.c * pyo.sin(m.theta[t])

def _diffeq2(m, t):
    return m.dthetadt[t] == m.omega[t]

m.diffeq1 = pyo.Constraint(m.t, rule=_diffeq1)
m.diffeq2 = pyo.Constraint(m.t, rule=_diffeq2)

# Simulate
sim = Simulator(m, package='scipy')
tsim, profiles = sim.simulate(numpoints=100, integrator='vode')
```

### Example 5: Combining Multiple Discretization Methods

Apply different discretization schemes to different continuous domains:

```python
import pyomo.environ as pyo
from pyomo.dae import ContinuousSet

# Create model with two time/space dimensions
model = pyo.ConcreteModel()
model.t1 = ContinuousSet(bounds=(0, 10))
model.t2 = ContinuousSet(bounds=(0, 5))

# ... define variables and constraints ...

# Apply finite difference to t1
disc_fe = pyo.TransformationFactory('dae.finite_difference')
disc_fe.apply_to(model, wrt=model.t1, nfe=10)

# Apply collocation to t2
disc_col = pyo.TransformationFactory('dae.collocation')
disc_col.apply_to(model, wrt=model.t2, nfe=10, ncp=5)
```

### Example 6: Pyomo Configuration System

Configure solver options and model settings:

```python
from pyomo.common.config import ConfigDict, ConfigValue

# Create configuration dictionary
config = ConfigDict()

config.declare('filename', ConfigValue(
    default=None,
    domain=str,
    description="Input file name"
))

config.declare("iteration_limit", ConfigValue(
    default=30,
    domain=int,
    description="Maximum iterations"
))

# Use configuration
config['filename'] = 'data.csv'
config.iteration_limit = 50  # Attribute access with underscores

print(config.iteration_limit)  # Output: 50
```

### Example 7: Repeated Solves and Model Manipulation

Iteratively solve models with changing constraints:

```python
import pyomo.environ as pyo

# Create solver
solver = pyo.SolverFactory('glpk')

# Create base model
model = pyo.AbstractModel()
model.x = pyo.Var([1, 2, 3, 4], domain=pyo.Binary)
model.obj = pyo.Objective(expr=sum(model.x[i] for i in [1, 2, 3, 4]), sense=pyo.maximize)
model.c_list = pyo.ConstraintList()

# Create instance
instance = model.create_instance()

# Solve multiple times with different constraints
for iteration in range(5):
    # Solve current model
    result = solver.solve(instance)

    # Get current solution
    current_x = [pyo.value(instance.x[i]) for i in [1, 2, 3, 4]]

    # Add constraint to exclude this solution
    instance.c_list.add(sum(instance.x[i] for i in [1, 2, 3, 4]) != sum(current_x))
```

### Example 8: Accessing Dual Values and Slacks

Extract sensitivity information from solved models:

```python
import pyomo.environ as pyo

# Solve model and load results
model = pyo.ConcreteModel()
# ... define model ...
solver = pyo.SolverFactory('ipopt')
results = solver.solve(model)

# Load dual values
model.dual = pyo.Suffix(direction=pyo.Suffix.IMPORT)
results = solver.solve(model)

# Access duals
for c in model.component_objects(pyo.Constraint, active=True):
    print(f"Constraint: {c}")
    for index in c:
        print(f"  Dual for {c[index].name}: {model.dual[c[index]]}")
```

### Example 9: Community Detection for Model Analysis

Analyze model structure and identify subproblems:

```python
from pyomo.contrib.community_detection.detection import detect_communities
import pyomo.environ as pyo

# Create a model
model = pyo.ConcreteModel()
model.x1 = pyo.Var(initialize=-3)
model.x2 = pyo.Var(initialize=-1)
model.x3 = pyo.Var(initialize=-3)
model.x4 = pyo.Var(initialize=-1)

model.c1 = pyo.Constraint(expr=model.x1 + model.x2 <= 0)
model.c2 = pyo.Constraint(expr=model.x1 - 3 * model.x2 <= 0)
model.c3 = pyo.Constraint(expr=model.x2 + model.x3 + 4 * model.x4 ** 2 == 0)
model.c4 = pyo.Constraint(expr=model.x3 + model.x4 <= 0)
model.c5 = pyo.Constraint(expr=model.x3 ** 2 + model.x4 ** 2 - 10 == 0)

# Detect communities (subproblems)
community_map = detect_communities(
    model,
    type_of_community_map='constraint',
    random_seed=42
)

# Print communities
print(community_map)
# Output: {0: (['c1', 'c2'], ['x1', 'x2']), 1: (['c3', 'c4', 'c5'], ['x3', 'x4'])}
```

### Example 10: Fixing Variables and Re-solving

Fix integer variables and resolve optimization:

```python
import pyomo.environ as pyo

# After solving a model with integer variables
for v in model.component_data_objects(pyo.Var):
    if v.is_integer():
        v.fix(round(pyo.value(v)))

# Re-solve with fixed integers
solver.solve(model)

# Unfix later if needed
for v in model.component_data_objects(pyo.Var):
    if v.is_integer():
        v.unfix()
```

## Key Concepts

### Model Types
- **ConcreteModel**: All data specified during model construction (immediate instantiation)
- **AbstractModel**: Data supplied later through data files or dictionaries (delayed instantiation)

### Core Components
- **Var**: Decision variables (continuous, integer, binary)
- **Param**: Fixed parameter values/input data
- **Objective**: Function to minimize or maximize
- **Constraint**: Restrictions on variable values (equality, inequality)
- **Set**: Index sets for variables and constraints
- **ContinuousSet**: Bounded continuous domains for differential equations

### Advanced Components (pyomo.dae)
- **DerivativeVar**: Represents derivatives in differential equations
- **Integral**: Integral expressions over continuous domains
- **Simulator**: ODE/DAE simulation using SciPy or CasADi

### Discretization Methods
- **Finite Difference**: FORWARD, BACKWARD, CENTRAL schemes
- **Collocation**: LAGRANGE-RADAU, LAGRANGE-LEGENDRE with orthogonal polynomials

### Solvers
- **Open-source**: GLPK, IPOPT, CBC
- **Commercial**: Gurobi, CPLEX, BARON
- **Specialized**: SciPy integrators, CasADi for DAE

## Reference Files

Comprehensive documentation organized by topic in `references/`:

- **tutorials.md** (Recommended starting point) - Step-by-step guides and examples
- **modeling.md** - Model formulation, variables, constraints, objectives
- **api.md** - Complete API reference for all Pyomo modules
- **howto.md** - Practical guides for common tasks (interrogating models, manipulation, abstract models)
- **explanation.md** - Deep dives into DAE modeling, configuration system, network modeling
- **solvers.md** - Solver integration and configuration
- **reference.md** - Mathematical foundations and formulation details
- **index.html.md** - Documentation overview and navigation

Use the `view` command to read specific reference files for detailed information.

## Working with This Skill

### For Beginners
1. Start with **Example 1** to understand basic model structure
2. Review `tutorials.md` for step-by-step learning
3. Use **Example 2** to learn how to extract solution values
4. Practice with simple LP and MIP formulations before advancing

### For Intermediate Users
1. Explore **Examples 3-5** for dynamic optimization
2. Study `modeling.md` for advanced constraint formulation
3. Learn **Example 7** for iterative solving techniques
4. Review `howto.md` for model manipulation patterns

### For Advanced Users
1. Master **Examples 9-10** for model analysis and decomposition
2. Explore custom discretization schemes in `explanation.md`
3. Use community detection for large-scale problem decomposition
4. Integrate with PyNumero for matrix-level operations
5. Study `api.md` for low-level component access

### Common Workflows

**Linear Programming:**
```
Define ConcreteModel → Add Variables → Define Objective → Add Constraints → Solve with GLPK/CBC
```

**Dynamic Optimization:**
```
Define ContinuousSet → Create DerivativeVar → Specify ODEs → Discretize (collocation/finite difference) → Solve with IPOPT
```

**Parameter Estimation:**
```
Create model with parameters → Define data reconciliation objective → Solve → Extract fitted parameters
```

**Iterative Solving:**
```
Create base model → Solve → Extract solution → Add cut/constraint → Repeat
```

## Best Practices

1. **Always import Pyomo properly**: Use `import pyomo.environ as pyo` for standard imports
2. **Handle boundary conditions**: Use `Constraint.Skip` or deactivation for differential equations at boundaries
3. **Initialize variables**: Provide good starting points for nonlinear problems
4. **Choose appropriate discretization**: Collocation (higher accuracy) vs. Finite Difference (simpler)
5. **Use appropriate solvers**: LP (GLPK/CBC), NLP (IPOPT), MINLP (BARON/Couenne), DAE (IPOPT after discretization)
6. **Access solutions correctly**: Always use `pyo.value()` to extract variable values
7. **Load duals when needed**: Declare `model.dual = pyo.Suffix(direction=pyo.Suffix.IMPORT)` before solving

## Resources

### Official Documentation
- Pyomo Documentation: https://pyomo.readthedocs.io
- Pyomo GitHub: https://github.com/Pyomo/pyomo
- Pyomo Book: "Pyomo - Optimization Modeling in Python" (Springer)

### Getting Help
- Check `references/` files for detailed examples
- Review `howto.md` for specific task patterns
- Consult `api.md` for component details
- See `tutorials.md` for learning paths

## Notes

- This skill was generated from official Pyomo documentation (version 6.10.0.dev0)
- All code examples are extracted from real documentation and tested patterns
- Examples use `pyo` as the standard Pyomo namespace alias
- Dynamic optimization examples require `scipy` or `casadi` for simulation
- Community detection requires NetworkX and python-louvain packages
