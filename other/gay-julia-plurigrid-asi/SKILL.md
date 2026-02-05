---
name: gay-julia
description: Wide-gamut color sampling with splittable determinism using Pigeons.jl
version: 1.0.0
---


# Gay.jl - Wide-Gamut Deterministic Color Sampling

Wide-gamut color sampling with splittable determinism using Pigeons.jl SPI pattern and LispSyntax integration.

## bmorphism Contributions

> *"We are building cognitive infrastructure for the next trillion minds"*
> — [Plurigrid: the story thus far](https://gist.github.com/bmorphism/a400e174b9f93db299558a6986be0310)

**Author**: [@bmorphism](https://github.com/bmorphism) (Barton Rhodes)

Gay.jl embodies the Plurigrid principle of **autopoietic ergodicity** — self-sustaining systems that explore all accessible states. The deterministic color generation from seeds mirrors the broader pattern of reproducible, verifiable computation across distributed systems.

**Related bmorphism projects**:
- [bmorphism/slowtime-mcp-server](https://github.com/bmorphism/slowtime-mcp-server) - MCP server for time intervals
- [plurigrid/act](https://github.com/plurigrid/act) - cognitive category theory building blocks
- Parametrised optics for cybernetic systems

## Repository
- **Source**: https://github.com/bmorphism/Gay.jl
- **Author**: [@bmorphism](https://github.com/bmorphism)
- **Language**: Julia
- **Pattern**: SplitMix64 → GF(3) trits → LCH colors

## Core Concepts

### SplitMix64 Determinism
```julia
# Deterministic color from seed
using Gay

seed = 0x598F318E2B9E884
color = gay_color(seed)  # Returns LCH color
trit = gf3_trit(seed)    # Returns :MINUS, :ERGODIC, or :PLUS
```

### GF(3) Conservation
Every color operation preserves the tripartite balance:
- **MINUS** (-1): Contractive operations
- **ERGODIC** (0): Neutral/balanced operations  
- **PLUS** (+1): Expansive operations

Sum of trits across parallel streams must equal 0 (mod 3).

### LispSyntax Integration
```julia
using LispSyntax

# S-expression colorization
sexp = @lisp (defun factorial (n) (if (<= n 1) 1 (* n (factorial (- n 1)))))
colored = colorize(sexp, seed=seed)
```

## Integration with plurigrid/asi

### With gay-mcp skill
```julia
# MCP tool registration with deterministic colors
using Gay, MCP

tool = MCPTool("color-palette", seed=0x1069)
palette = generate_palette(tool, n=5)
```

### With spi-parallel-verify
```julia
# Verify GF(3) conservation across parallel execution
using Gay, SPI

streams = trifurcate(seed, [:task1, :task2, :task3])
verify_conservation(streams)  # Asserts sum(trits) ≡ 0 (mod 3)
```

### With triad-interleave
```julia
# Interleave three color streams
using Gay, TriadInterleave

schedule = interleave(
    minus_stream(seed),
    ergodic_stream(seed),
    plus_stream(seed)
)
```

## Key Functions

| Function | Description |
|----------|-------------|
| `gay_color(seed)` | Generate LCH color from seed |
| `gf3_trit(seed)` | Extract GF(3) trit assignment |
| `splitmix64(state)` | Advance RNG state |
| `colorize(sexp, seed)` | Color S-expression nodes |
| `palette(seed, n)` | Generate n-color palette |

## Use Cases

1. **Deterministic UI theming** - Same seed → same colors everywhere
2. **Parallel task coloring** - GF(3) ensures balanced distribution
3. **CRDT conflict resolution** - Trit-based merge ordering
4. **Terminal session coloring** - vterm integration via crdt-vterm-bridge

## Julia Scientific Package Integration

From `julia-scientific` skill - related Julia packages:

| Package | Category | Use with Gay.jl |
|---------|----------|-----------------|
| **Catlab.jl** | ACSets | Colored schema parts |
| **AlgebraicRewriting.jl** | Rewriting | Colored rule application |
| **StructuredDecompositions.jl** | Sheaves | Colored adhesions |
| **GraphNeuralNetworks.jl** | ML | Node/edge coloring |
| **Makie.jl** | Visualization | Deterministic plot colors |
| **Graphs.jl** | Networks | Colored graph analysis |
| **Flux.jl** | Deep Learning | Layer coloring for debug |

### Scientific Domain Coloring

```julia
# Protein structure coloring
using Gay, BioStructures
pdb = read("1CRN.pdb", PDB)
chain_colors = Gay.palette(seed, nchains(pdb))
visualize_structure(pdb, colors=chain_colors)

# Quantum circuit coloring
using Gay, Yao
circuit = chain(4, put(1=>H), control(1, 2=>X))
gate_colors = [Gay.color_at(seed, i) for i in 1:length(circuit)]

# Graph neural network visualization
using Gay, GraphNeuralNetworks, GraphMakie
node_colors = Gay.palette(seed, nv(graph))
graphplot(graph, node_color=node_colors)
```

## Related Skills
- `gay-mcp` - MCP server with Gay.jl colors
- `spi-parallel-verify` - Strong Parallelism Invariance verification
- `triad-interleave` - Three-stream scheduling
- `bisimulation-game` - GF(3) conservation in game semantics
- `julia-scientific` - Full Julia package mapping (137 skills)



## Scientific Skill Interleaving

This skill connects to the K-Dense-AI/claude-scientific-skills ecosystem:

### Visualization
- **matplotlib** [○] via bicomodule
  - Hub for all visualization

### Bibliography References

- `general`: 734 citations in bib.duckdb

## Cat# Integration

This skill maps to **Cat# = Comod(P)** as a bicomodule in the equipment structure:

```
Trit: 0 (ERGODIC)
Home: Prof
Poly Op: ⊗
Kan Role: Adj
Color: #26D826
```

### GF(3) Naturality

The skill participates in triads satisfying:
```
(-1) + (0) + (+1) ≡ 0 (mod 3)
```

This ensures compositional coherence in the Cat# equipment structure.