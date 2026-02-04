---
name: gay-mcp
description: Deterministic color generation with SplitMix64, GF(3) trits, and MCP. Colors are the perceptual rendering of solved constraint systems.
version: 1.0.0
---

<!-- Propagated to codex | Trit: 0 | Source: .ruler/skills/gay-mcp -->

# Gay-MCP Skill: Deterministic Color Generation

**Status**: ✅ Production Ready
**Trit**: +1 (PLUS - optimistic/generative)
**Principle**: Same seed → Same colors (SPI guarantee)
**Implementation**: Gay.jl (Julia) + SplitMixTernary (Ruby)

---

## Manifesto

> **The colors are not arbitrary—they are the perceptual rendering of a solved constraint system.**

We are building a **deterministic, parallelizable, human-adapted coordinate system** that renders formal constraints as perceptual reality, in a way that can be:

| Property | Mechanism | Verification |
|----------|-----------|--------------|
| **Verified** | SPI fingerprints, GF(3) conservation | Sheaf cohomology gluing |
| **Merged** | Worlding patterns, Möbius inversion | Derangement CRDTs |
| **Learned** | Enzyme autodiff, reafference loops | Compression progress |

The color IS the proof. The hue encodes the trit. The seed determines the universe.

---

## Overview

**Gay-MCP** provides deterministic color generation via SplitMix64 + golden angle. Every invocation with the same seed produces identical colors, enabling:

1. **Parallel computation**: Fork generators, get same results
2. **Reproducibility**: Colors are functions of (seed, index)
3. **GF(3) trits**: Each color maps to {-1, 0, +1}

## Core Algorithm

```
SplitMix64:
  state = (state + γ) mod 2⁶⁴
  z = state
  z = (z ⊕ (z >> 30)) × 0xBF58476D1CE4E5B9
  z = (z ⊕ (z >> 27)) × 0x94D049BB133111EB
  return z ⊕ (z >> 31)

Color Generation:
  L = 10 + random() × 85    # Lightness: 10-95
  C = random() × 100        # Chroma: 0-100
  H = random() × 360        # Hue: 0-360
  trit = hue_to_trit(H)     # GF(3) mapping
```

## Constants

```ruby
GOLDEN = 0x9E3779B97F4A7C15  # φ⁻¹ × 2⁶⁴
MIX1   = 0xBF58476D1CE4E5B9
MIX2   = 0x94D049BB133111EB
MASK64 = 0xFFFFFFFFFFFFFFFF
```

## MCP Server

The Gay MCP server provides these tools:

| Tool | Description |
|------|-------------|
| `color_at` | Get color at specific index |
| `palette` | Generate N-color palette |
| `golden_thread` | Golden angle spiral |
| `reafference` | Self-recognition loop |
| `loopy_strange` | Generator ≡ Observer |

## Hex Color Output (#RRGGBB)

Convert OkLCH to hex for CSS/web usage:

```python
def oklch_to_hex(L: float, C: float, H: float) -> str:
    """Convert OkLCH to #RRGGBB hex string."""
    import math
    
    # OkLCH -> OkLab
    a = C * math.cos(math.radians(H))
    b = C * math.sin(math.radians(H))
    
    # OkLab -> Linear RGB (simplified)
    l_ = L/100 + 0.3963377774 * a + 0.2158037573 * b
    m_ = L/100 - 0.1055613458 * a - 0.0638541728 * b
    s_ = L/100 - 0.0894841775 * a - 1.2914855480 * b
    
    l, m, s = l_**3, m_**3, s_**3
    
    r = +4.0767416621 * l - 3.3077115913 * m + 0.2309699292 * s
    g = -1.2684380046 * l + 2.6097574011 * m - 0.3413193965 * s
    b = -0.0041960863 * l - 0.7034186147 * m + 1.7076147010 * s
    
    # Clamp and convert to 0-255
    def to_byte(x): return max(0, min(255, int(x * 255)))
    
    return f"#{to_byte(r):02X}{to_byte(g):02X}{to_byte(b):02X}"
```

## Trit Mapping

```
Hue 0-60°, 300-360° → +1 (PLUS, warm)
Hue 60-180°         →  0 (ERGODIC, neutral)
Hue 180-300°        → -1 (MINUS, cold)
```

## Out-of-Order Proof

```ruby
proof = SplitMixTernary.prove_out_of_order(seed)
# => { 
#      ordered_equals_reversed: true,
#      ordered_equals_shuffled: true,
#      proof: "QED: Math is doable out of order"
#    }
```

## Example Output

```
╔═══════════════════════════════════════════════════════════════════╗
║  GAY.JL: Deterministic Color Generation                          ║
╚═══════════════════════════════════════════════════════════════════╝

Seed: 0x42D

─── Palette (12 colors) ───
  1: #D8267F (trit=+1)
  2: #2CD826 (trit=0)
  3: #4FD826 (trit=0)
  ...

─── Out-of-Order Proof ───
  Indices: [1, 5, 10, 20, 50]
  Ordered = Reversed: true
  Ordered = Shuffled: true
  QED: Math is doable out of order
```

---

**Skill Name**: gay-mcp
**Type**: Deterministic Color Generation
**Trit**: +1 (PLUS)
**GF(3)**: Conserved via tripartite streams
**SPI**: Guaranteed (same seed → same output)

---

## End-of-Skill Interface

## Commands

```bash
# Start MCP server
julia --project=@gay -e "using Gay; Gay.serve_mcp()"

# Generate palette
just gay-palette seed=1069 n=12

# Test determinism
just gay-test
```

## API (Ruby)

```ruby
require 'splitmix_ternary'

# Create generator
gen = SplitMixTernary.new(1069)

# Get color at index
color = gen.color_at(42)
# => { L: 45.2, C: 67.8, H: 234.5, trit: -1, index: 42 }

# Generate trits
gen.next_trit  # => -1, 0, or +1

# Split for parallelism
child = gen.split(7)  # Independent child generator
```

## API (Julia)

```julia
using Gay

# Set seed
Gay.gay_seed(1069)

# Get color
color = Gay.color_at(42)

# Generate palette
palette = Gay.palette(12)

# Golden thread
colors = Gay.golden_thread(steps=10)
```

## API (Python)

```python
from gay import SplitMixTernary, TripartiteStreams

# Create generator
gen = SplitMixTernary(seed=1069)

# Get color at index (returns dict with L, C, H, trit, hex)
color = gen.color_at(42)
# => {'L': 45.2, 'C': 67.8, 'H': 234.5, 'trit': -1, 'index': 42, 'hex': '#2E5FA3'}

# Generate hex color directly
hex_color = gen.hex_at(42)  # => '#2E5FA3'

# Generate palette as hex list
palette = gen.palette_hex(n=12)
# => ['#D8267F', '#2CD826', '#4FD826', ...]

# Generate trits
trit = gen.next_trit()  # => -1, 0, or +1

# Split for parallelism (deterministic child)
child = gen.split(offset=7)

# Tripartite streams (GF(3) = 0 guaranteed)
streams = TripartiteStreams(seed=1069)
triplet = streams.next_triplet()
# => {'minus': -1, 'ergodic': 0, 'plus': 1, 'gf3_sum': 0, 'conserved': True}
```

## Integration with discrete_backprop

Color learning via gradient-free optimization:

```python
from gay import SplitMixTernary
from discrete_backprop import DiscreteBackprop

class ColorLearner:
    """Learn optimal color sequences via trit-based backprop."""
    
    def __init__(self, seed: int, target_palette: list):
        self.gen = SplitMixTernary(seed)
        self.target = target_palette
        self.backprop = DiscreteBackprop(dims=3)  # L, C, H
    
    def loss(self, index: int) -> float:
        """Compute color distance to target."""
        color = self.gen.color_at(index)
        target = self.target[index % len(self.target)]
        return sum((color[k] - target[k])**2 for k in ['L', 'C', 'H'])
    
    def step(self, indices: list) -> dict:
        """Discrete gradient step via trit perturbation."""
        losses = [self.loss(i) for i in indices]
        
        # Compute trit-based gradient (Δtrit per dimension)
        gradients = self.backprop.discrete_gradient(
            params=[self.gen.state],
            losses=losses,
            perturbation='trit'  # Use {-1, 0, +1} perturbations
        )
        
        # Chain seed based on gradient direction
        direction_trit = sum(g for g in gradients) % 3 - 1  # Map to {-1, 0, +1}
        self.gen.chain_seed(direction_trit)
        
        return {
            'loss': sum(losses) / len(losses),
            'gradient_trit': direction_trit,
            'new_seed': hex(self.gen.seed)
        }

# Usage
learner = ColorLearner(seed=0x42D, target_palette=[
    {'L': 50, 'C': 80, 'H': 30},   # Target warm
    {'L': 70, 'C': 60, 'H': 150},  # Target neutral
    {'L': 40, 'C': 90, 'H': 240},  # Target cold
])

for epoch in range(100):
    result = learner.step(indices=[0, 1, 2])
    if result['loss'] < 0.01:
        break
```

## Integration with Langevin Dynamics (NEW)

Track which colors affect which noise calls in Langevin training:

```julia
# Instrument Langevin noise via color tracking
function instrument_langevin_noise(sde, step_id)
    color = color_at(rng, step_id)
    noise = randn_from_color(color)
    return (color, noise, step_id)
end

# Export audit trail showing cause-effect
audit_log = export_color_trace(
    trajectory=sde_solution,
    seed=base_seed
)
# Shows: step_47 → color_0xD8267F → noise_0.342 → parameter_update

# Verify GF(3) conservation across trajectory
gf3_check(color_sequence, balance_threshold=0.1)
```

## Integration with Unworld

Colors are derived, not temporal:

```ruby
# Seed chaining
next_seed = Unworld.chain_seed(current_seed, color[:trit])

# Derive color
color = Unworld.derive_color(seed, index)
```

## Tripartite Streams

Three independent streams with GF(3) = 0:

```ruby
streams = SplitMixTernary::TripartiteStreams.new(seed)

triplet = streams.next_triplet
# => { minus: -1, ergodic: 0, plus: 1, gf3_sum: 0, conserved: true }

## r2con Speaker Resources

| Speaker | Handle | Repository | Relevance |
|---------|--------|------------|-----------|
| bmorphism | bmorphism | [r2zignatures](https://github.com/bmorphism/r2zignatures) | Zignature-based function recognition with Gay.jl color integration |
| bmorphism | bmorphism | [Gay.jl](https://github.com/bmorphism/Gay.jl) | Source of deterministic color generation for r2 analysis |
| pancake | trufae | [r2pipe](https://github.com/radareorg/r2pipe) | Scripted access to radare2 for color pipeline integration |
| swoops | swoops | [libc_zignatures](https://github.com/swoops/libc_zignatures) | Signature similarity patterns inform color fingerprinting |
```

## Patterns That Work

- Deterministic color via SplitMix64
- GF(3) trit derivation from hue
- Cross-session fingerprint verification

## Patterns to Avoid

- Non-deterministic color generation
- Ignoring seed provenance