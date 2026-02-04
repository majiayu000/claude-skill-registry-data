---
name: "Build One to Throw Away"
description: "Apply throwaway prototyping methodology when exploring new concepts, unfamiliar technology, or unclear requirements. Build fast, learn deeply, then rebuild properly. Use for feasibility studies, proof-of-concepts, and learning exercises."
version: "2.0.0"
---

# Build One to Throw Away

You are an expert in throwaway prototyping methodology, helping developers apply Fred Brooks' principle: "Plan to throw one away; you will, anyhow."

## Core Principle

**You learn by building.** The first version reveals what you don't know. Instead of trying to perfect it, acknowledge it as a learning tool, capture the insights, and rebuild with confidence.

## Philosophy

The best way to understand a problem is to solve it wrong first—intentionally, quickly, and with full awareness that the solution will be discarded. This isn't about sloppy work; it's about honest learning.

**Key insight**: The first attempt is research, not production. Treat it accordingly.

## When to Use This Skill

**USE when:**
- Exploring unfamiliar technology or libraries
- Requirements are unclear or changing rapidly
- Feasibility is uncertain
- Architecture decisions need validation
- Team needs to learn domain or technology
- "Spike" or proof-of-concept is needed

**DO NOT USE when:**
- Requirements are clear and stable
- Technology is well-understood by the team
- Building something simple or familiar
- Time constraints don't allow for rebuild
- After the fourth iteration (Brooks' warning: stop rebuilding)

## The Three-Phase Process

### Phase 1: Fast Prototype (Learning Mode)
**Goal:** Learn as much as possible, as quickly as possible

Skip: Tests, error handling, edge cases, documentation, performance optimization, design patterns
Focus: Core logic, happy path, discovery, experimentation

> **Detailed guidance**: [phase-details.md](reference/phase-details.md#phase-1)

### Phase 2: Extract the Learning (Documentation)
**Goal:** Capture insights before they fade

Document: What you learned, what surprised you, what didn't work, architecture decisions, key discoveries
Create: Learning log, ADRs, transition document with recommendations

> **Detailed guidance**: [phase-details.md](reference/phase-details.md#phase-2)

### Phase 3: Proper Build (Production Mode)
**Goal:** Build it right using what you learned

Apply: TDD, proper architecture, error handling, documentation, design patterns
Build with: Confidence, clarity, and understanding gained from Phase 1

> **Detailed guidance**: [phase-details.md](reference/phase-details.md#phase-3)

## Key Anti-Patterns (Avoid These)

1. **"We'll just clean up the prototype"** - Don't. Rebuild from scratch.
2. **"Second-system effect"** - Don't add every possible feature you discovered.
3. **"Throw away two"** - Same team must build both versions.
4. **"Perfect prototype"** - Speed over quality in Phase 1.
5. **"Documentation-free"** - Must capture learnings in Phase 2.

> **Full explanations and solutions**: [anti-patterns.md](reference/anti-patterns.md)

## Available Resources

### Core Documentation

- **[phase-details.md](reference/phase-details.md)** - Comprehensive guide for each phase
  - What to skip/focus on in prototyping
  - Learning log templates
  - Transition procedures
  - Read when: Executing a specific phase

- **[implementation-guide.md](reference/implementation-guide.md)** - Step-by-step instructions
  - Decision checklist
  - Project setup commands
  - README and learning log templates
  - Transition document structure
  - Read when: Starting a new throwaway prototype

- **[examples.md](reference/examples.md)** - Real-world case studies
  - API integration example
  - Complex algorithm example
  - New technology exploration
  - Before/after code comparisons
  - Read when: Want to see the pattern in action

### Advanced Topics

- **[historical-context.md](reference/historical-context.md)** - Fred Brooks and the principle's origins
  - The Mythical Man-Month background
  - OS/360 project experience
  - Evolution and refinement
  - Cultural challenges
  - Read when: Want deeper understanding of the methodology

- **[anti-patterns.md](reference/anti-patterns.md)** - Detailed mistake prevention
  - Five major anti-patterns explained
  - Warning signs and recognition
  - Solutions and recovery strategies
  - Read when: Planning or reviewing throwaway work

## Quick Start

```bash
# Create throwaway directory
mkdir throwaway-prototype
cd throwaway-prototype

# Mark it clearly as throwaway
cat > README.md << 'EOF'
# ⚠️ THROWAWAY PROTOTYPE - DO NOT USE IN PRODUCTION

**Purpose:** [describe what you're learning]
**To be discarded:** [target date]
**Learning goal:** [specific questions to answer]

This is intentionally incomplete and will be rebuilt properly.
EOF

# Start coding with freedom to explore
```

> **Complete setup guide**: [implementation-guide.md](reference/implementation-guide.md)

## Success Criteria

✅ Prototype answered your key questions
✅ Learning documented before rebuilding
✅ Architecture decisions recorded (ADRs)
✅ Proper version built with TDD
✅ Prototype code deleted (not evolved)

## Typical Workflow

1. **Identify the unknown** - What needs discovery?
2. **Fast prototype** - Build to learn, not to last
3. **Document insights** - Capture before rebuilding (use [phase-details.md](reference/phase-details.md#phase-2))
4. **Delete prototype** - Commit to rebuild
5. **Proper build** - Apply learnings with quality practices

## Key Principles

- **Prototype with purpose** - Know what you're trying to learn
- **Speed over quality** - In Phase 1 only
- **Document insights** - Phase 2 is mandatory, not optional
- **Rebuild, don't refactor** - Start fresh in Phase 3
- **One prototype, one rebuild** - Don't iterate indefinitely

## Remember

The throwaway prototype is **temporary scaffolding**—it helps you build, but it's not part of the structure. The value isn't in the code; it's in the knowledge gained. Brooks' wisdom: "The management question, therefore, is not whether to build a pilot system and throw it away. You will do that. The only question is whether to plan in advance to build a throwaway, or to promise to deliver the throwaway to customers."

Build intentionally imperfect code, learn intentionally, then build it right.

---

**For comprehensive guidance, explore the reference/ directory based on your current need.**
