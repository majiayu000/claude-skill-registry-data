---
name: thermodynamic-economics
description: |
  Thermodynamic foundations for distributed systems design. Use when analyzing energy flows, 
  EROEI calculations, autopoietic closure, or validating economic models against physical constraints.
  Triggers: energy economics, thermodynamic analysis, EROEI, autopoiesis, Energy Seneca, 
  heterotroph/autotroph analysis, network energy costs, Fourth Transition concepts.
---

# Thermodynamic Economics

## Purpose

This skill provides the thermodynamic foundations required to validate any distributed economic 
system against physical reality. It addresses the critique that metaphorical frameworks 
(mycelial networks, Dunbar limits) often lack thermodynamic grounding.

## Core Principles

### The Heterotroph Problem

Any distributed network must answer: **Where does the energy come from and how does it flow?**

```
AUTOTROPH (Primary Producer)     HETEROTROPH (Consumer)
─────────────────────────────    ─────────────────────────
Captures external energy         Consumes already-captured energy
Examples: Plants, solar PV       Examples: Fungi, animals, most tech
Creates energy gradient          Dissipates energy gradient
Can be autopoietic alone         Cannot be autopoietic alone
```

**Key insight**: A mycelial/fungal network metaphor describes *distribution topology*, not *energy generation*. Fungi decompose dead organic matter (stored solar energy). Any "mycelial economics" must specify its autotrophic energy source.

### Energy Return on Energy Invested (EROEI/EROIp)

```
EROIp = Energy Delivered to Society / Energy Required for Extraction

Historical fossil fuel EROIp:    | Current status:
1930s oil: ~100:1                | Conventional oil: 10-20:1
1970s oil: ~30:1                 | Tight oil/fracking: 5-10:1  
Peak conventional: ~35:1         | Solar PV: 10-20:1
                                 | Wind: 15-25:1
                                 | Biofuels: 1-3:1

Minimum societal viability: ~7-10:1 (supports industrial complexity)
Below 5:1: Cannot maintain current infrastructure
At 1:1: Thermodynamic equilibrium (dead state)
```

### The Three Thermodynamic Laws Applied

1. **First Law** (Conservation): Energy cannot be created or destroyed
   - Implication: Total energy in = Total energy out + storage changes
   - For any network: Map all energy inputs, outputs, and stocks

2. **Second Law** (Entropy): Entropy always increases in isolated systems
   - Implication: Every energy transformation has losses
   - For any network: Calculate waste heat at each transformation step

3. **Third Law** (Absolute Zero): Perfect efficiency is impossible
   - Implication: No process achieves 100% conversion
   - For any network: Budget for irreversible losses

### Autopoiesis Defined

An **autopoietic system** produces and maintains itself by creating its own components.

```
Autopoietic requirements:
1. Self-production of components
2. Boundary/membrane maintenance  
3. Operational closure (processes produce processes)
4. Thermodynamic openness (energy/matter exchange with environment)
5. Positive net energy after self-maintenance

Dr. Arnoux's claim: Humankind ceased being autopoietic between 2010-2020
Meaning: Our civilization can no longer reproduce its operational basis 
         from currently accessible energy flows
```

## Analysis Framework

### Step 1: Map Energy Sources (Autotrophic Base)

For any proposed system, identify:

```markdown
| Source Type | Capture Method | Location | Capacity (W) | EROEI |
|-------------|---------------|----------|--------------|-------|
| Solar       | PV panels     | ...      | ...          | 10-20 |
| Wind        | Turbines      | ...      | ...          | 15-25 |
| Hydro       | Turbines      | ...      | ...          | 40-60 |
| Geothermal  | Heat exchange | ...      | ...          | 5-15  |
| Fossil      | Extraction    | ...      | ...          | 5-20  |
```

### Step 2: Map Energy Flows (Transformation Chain)

```
Source → Capture → Storage → Distribution → End Use → Waste
   ↓         ↓        ↓           ↓            ↓        ↓
100%      20-40%   70-90%      85-95%       20-80%   Heat
```

Calculate cumulative efficiency: E_net = E_source × η₁ × η₂ × η₃ × η₄

### Step 3: Calculate Network Energy Costs

For distributed systems, include:

```python
# Network maintenance energy
E_network = (
    E_node_operation +      # Computation, storage per node
    E_communication +       # Data transmission between nodes
    E_consensus +           # Distributed consensus overhead
    E_redundancy +          # Fault tolerance copies
    E_infrastructure        # Physical infrastructure maintenance
)

# Net available for productive work
E_available = E_captured - E_network - E_losses

# System viability condition
VIABLE = E_available > 0 AND EROEI_system > 7
```

### Step 4: Autopoietic Closure Check

```python
# Can the system reproduce itself from available energy?
reproduction_energy = (
    E_replace_components +   # Physical replacement of worn parts
    E_train_operators +      # Knowledge transfer to new operators  
    E_maintain_supply_chain +# Energy to maintain material inputs
    E_adapt_to_changes       # Energy for system evolution
)

AUTOPOIETIC = E_available > reproduction_energy
```

## Integration with Univrs.io

### The Hyphal Network Critique

Current state: The Hyphal Network describes a *distribution topology* based on:
- Small-world network properties (Watts-Strogatz)
- Dunbar-limited local clustering
- Market-based "Kiers model" coordination

**Missing**: Explicit energy source and flow specification

### Required Integration

```
Proposed Architecture:
                                    
┌─────────────────────────────────────────────────────────┐
│                  AUTOTROPHIC LAYER                       │
│  Solar/Wind/Hydro → Energy Capture → Primary Storage    │
└────────────────────────────┬────────────────────────────┘
                             │ Energy Flow
                             ▼
┌─────────────────────────────────────────────────────────┐
│                  DISTRIBUTION LAYER                      │
│  Hyphal Network Topology (Small-World + Dunbar)         │
│  Spirit Packages (.dol → .spirit) for coordination      │
│  VUDO VM Runtime for execution                          │
└────────────────────────────┬────────────────────────────┘
                             │ Net Energy
                             ▼
┌─────────────────────────────────────────────────────────┐
│                  HETEROTROPHIC LAYER                     │
│  Productive work, value creation, ecosystem services    │
│  (Constrained by available net energy)                  │
└─────────────────────────────────────────────────────────┘
```

## Small Worlds Mathematics

See references/small-worlds-math.md for complete Watts-Strogatz formalism.

Key metrics for any proposed network:
- Clustering coefficient C(p)
- Characteristic path length L(p)  
- Small-world coefficient σ = (C/C_random) / (L/L_random)
- Scaling behavior: L ∝ log(N)/log(k) for small-world

## Scripts

- `scripts/eroei_calculator.py` — Calculate EROEI for energy systems
- `scripts/energy_flow_analyzer.py` — Map energy flows through network
- `scripts/small_world_metrics.py` — Calculate Watts-Strogatz metrics

## References

- references/small-worlds-math.md — Complete Watts-Strogatz formalism
- references/eroei-database.md — EROEI values for energy sources
- references/arnoux-framework.md — Fourth Transition concepts
- references/autopoiesis-checklist.md — Maturana-Varela framework applied

## Learning Path

1. **Thermodynamics primer**: Entropy, exergy, dissipative structures
2. **EROEI deep dive**: Hall, Murphy, Cleveland's work
3. **Autopoiesis**: Maturana & Varela's original formulation
4. **Small worlds**: Watts & Strogatz 1998 paper
5. **Fourth Transition**: Dr. Arnoux's Medium series and FTI work
6. **Integration**: Apply to Univrs.io architecture

## Validation Checklist

Before claiming any system is "sustainable" or "viable":

- [ ] Energy sources explicitly identified (autotrophic base)
- [ ] EROEI calculated for each energy source
- [ ] Energy flow chain mapped with efficiency at each step
- [ ] Network energy costs calculated (computation, communication, consensus)
- [ ] Net energy positive after all losses
- [ ] Autopoietic closure demonstrated (can reproduce operational basis)
- [ ] Small-world metrics calculated if claiming network benefits
- [ ] Dunbar limits applied correctly (cognitive, not just numerical)
