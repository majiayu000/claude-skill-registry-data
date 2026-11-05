---
name: shaping-requirements
description: Iteratively define problem and solution shapes.
phase: 3 (Discovery)
role: Lead
---

# Shaping Requirements

**Role Constraints:** Lead (Write/Bash access allowed).
**File Access:** Do NOT use literal placeholders for file paths. Use the `glob` tool to search for the active feature directory under `.jonggrang/.output/features/`.

## Methodology

Use this methodology when collaboratively shaping a solution with the user - iterating on problem definition (requirements) and solution options (shapes).

### Step 1: Understand the Problem
Before suggesting any solutions, explore the problem space.
- What is the actual user struggle?
- Ask clarifying questions to dig deeper into the "why" behind the request.
- Define what is explicitly out of bounds (what we are NOT solving).

### Step 2: Establish the Appetite
- How much time/effort is this problem worth? Is it a quick patch or a major feature?
- Constraint-driven design: The appetite determines the scope of the solution.

### Step 3: Explore Solution Shapes
Draft rough concepts, not high-fidelity designs.
- Use natural language to describe the moving parts.
- Propose 2-3 different conceptual approaches (shapes) with tradeoffs.
- Keep it abstract enough to leave room for designers/engineers to invent, but concrete enough to know what we are building.

### Step 4: Address Risks and Rabbit Holes
- What could go wrong? What are the technical unknowns?
- Call out potential "rabbit holes" where the team might get stuck.

### Step 5: Write the Pitch
Use your `write` tool to create or update `pitch.md` inside the active feature directory found via `glob` under `.jonggrang/.output/features/`.
Structure the pitch with:
1. Problem
2. Appetite
3. Solution (the shape)
4. Rabbit holes
5. No-gos

## Completion Signal
When the shaping process is finalized and the pitch is saved, output exactly:

SHAPING_COMPLETE
