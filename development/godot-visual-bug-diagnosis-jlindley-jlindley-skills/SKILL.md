---
name: godot-visual-bug-diagnosis
description: Debug visual and spatial bugs in Godot games through user observation, Godot-specific diagnosis, and test-driven fixes. Use when debugging visual or input issues in Godot where the user can observe the game but you cannot, when bugs involve rendering, positioning, animation, or coordinate systems, or when "what user sees" differs from expected behavior. For pure logic bugs use Systematic Debugging instead
---

# Godot Visual Bug Diagnosis

## Overview

Visual and spatial bugs in Godot games cannot be diagnosed from code alone. You cannot see the game running - only the user can observe what's actually happening.

**Core principle**: Work FROM the user's observations, diagnose using Godot-specific reasoning, test underlying logic where possible, iterate based on user validation.

**Announce at start**: "I'm using the Godot Visual Bug Diagnosis skill to debug this issue."

## The Iron Law

```
NO FIXES WITHOUT UNDERSTANDING WHAT THE USER OBSERVES
```

If you haven't gathered observations (Phase 1) and diagnosed from those observations using Godot terminology (Phase 2), you cannot propose fixes.

## When to Use

**Use for:**
- Visual bugs (rendering, positioning, alignment, animation)
- Input handling bugs (mouse/keyboard behavior, coordinate issues)
- Spatial/coordinate problems (zoom, camera, viewport transforms)
- Scene hierarchy issues (node positioning, parent/child transforms)
- Any bug where "what user sees" differs from "what should happen"

**Don't use for:**
- Pure logic bugs with no visual component → skills/debugging/systematic-debugging
- Performance issues
- Complex multi-component bugs → skills/debugging/systematic-debugging

## The Five Phases

Copy this checklist to track progress:

```
Godot Visual Bug Diagnosis Progress:
- [ ] Phase 1: Gather Observations (detailed visual behavior from user)
- [ ] Phase 2: Diagnose in Godot Terms (hypothesis using Godot concepts + research)
- [ ] Phase 3: Identify Testable Logic (decision: TDD or manual validation)
- [ ] Phase 4: Propose Fix (single fix following diagnosis)
- [ ] Phase 5: User Validates & Iterate (user confirmation or return to earlier phase)
```

**You MUST complete each phase before proceeding to the next.**

### Phase 1: Gather Observations

**If user report lacks details, ask clarifying questions:**
- What exactly do you see happening?
- Where is it relative to where it should be?
- Does it happen consistently or intermittently?
- Does zoom/camera/viewport position affect it?
- What are the exact steps to reproduce?

**If user already provided detailed observations**: Proceed to Phase 2

**Examples**:
- ✅ Good: "Hover indicator is 1.5 tiles southwest of cursor, worse when zoomed in"
- ✅ Good: "Selection slides onto tile smoothly, but hover jumps back half a tile first"
- ❌ Needs more: "Mouse thing is broken" → Ask what they observe
- ❌ Needs more: "It looks weird" → Ask what specifically looks weird

**Critical**: You CANNOT see the game running. Only the user can observe visual behavior. Work from their observations, not assumptions from code.

### Phase 2: Diagnose in Godot Terms

**Step 1: Research when needed**

**WHEN you encounter:**
- Unfamiliar Godot APIs (viewport transforms, coordinate conversion)
- Unclear Godot system behavior (canvas layers, input propagation)
- Potentially known issues

**THEN search:**
- Godot official docs (docs.godotengine.org) for API reference
- Godot GitHub issues/proposals for known bugs
- Community solutions for common patterns

**Examples**:
- Bug involves mouse coordinates → Search "Godot get_global_mouse_position viewport transform"
- Bug involves canvas layers → Search "Godot canvas layer coordinate system"
- API unclear → Search official docs for that method

**Don't assume Godot behavior - research it.**

**Step 2: Use Godot-specific reasoning**

Diagnose using Godot concepts:
- **Coordinate systems**: global vs local, screen vs world, viewport transforms
- **Scene tree**: node hierarchy, parent/child transforms, canvas layers, z-index
- **Input handling**: event propagation, input mapping, coordinate conversion
- **Rendering**: canvas layers, viewport rendering, camera transforms
- **Common Godot issues**: Known viewport transform bugs, global_position ambiguity

**Step 3: Explain hypothesis clearly**

"This sounds like [Godot concept] because [user's observation] indicates [specific Godot behavior]"

**Example**: "The offset getting worse with zoom suggests mouse coordinates are in screen space but being compared to world space without applying the viewport scale transform. This is a common coordinate conversion issue in Godot."

### Phase 3: Identify Testable Logic

**Ask**: "Can we test the underlying logic?"

**Testable** (write test first):
- Coordinate transformations (screen_to_world, viewport scale calculations)
- Scene tree queries (get_node, finding children by name)
- State changes (selection state, hover state transitions)
- Property calculations (tile positions, grid conversions)

**Not easily testable** (manual validation required):
- Visual appearance ("does it look right?")
- Animation feel ("does it feel smooth?")
- Rendering artifacts

**Decision**:
- **If testable**: Proceed with TDD
  - Write failing test first (using GUT or GdUnit4)
  - Test should reproduce the issue with specific inputs/outputs
  - See skills/testing/test-driven-development for TDD workflow
- **If not testable**: Document expected behavior, plan manual validation

**Don't skip testing because "fix seems simple"** - testable logic should have tests to prevent regression.

### Phase 4: Propose Fix

**Based on diagnosis and testability:**

**If testable (TDD approach)**:
1. **Write test first**:
   - Simplest test reproducing the issue
   - Use GUT (Godot 4: v9.x) or GdUnit4 for GDScript
   - Test should fail initially
   - Example: `assert_eq(world_to_screen(Vector2(5, 3)), expected_screen_pos)`

2. **Explain fix approach**:
   - What will change and why
   - Which Godot APIs/methods will be used
   - Expected outcome

3. **Implement single fix**:
   - ONE change at a time
   - No "while I'm here" improvements
   - Follow the diagnosis from Phase 2

4. **Verify test passes**

**If not testable (manual validation approach)**:
1. **Explain fix approach** clearly
2. **Implement single fix**
3. **Explain what user should observe** when testing

**Always**:
- ONE fix at a time
- Follow your diagnosis, don't guess
- No bundled refactoring

### Phase 5: User Validates & Iterate

**User tests in-game and reports results:**

**If fixed**: ✅ Done!
- If testable: Test prevents regression
- If manual: Document expected behavior for future

**If partially fixed**: "Still happening but different now..."
- **Return to Phase 1** with new observations
- Treat as new bug with fresh diagnosis
- Original diagnosis was incomplete

**If not fixed**: "No change"
- **Count failed attempts**
- **If < 3 attempts**: Return to Phase 2, re-diagnose with new information
- **If ≥ 3 attempts**: STOP
  - Question the approach
  - See skills/debugging/systematic-debugging Phase 4.5
  - Discuss architecture/approach with user
  - Don't try fix #4 without reconsidering fundamentals

**If new bug appeared**: "Now it does X instead..."
- This is a **symptom, not root cause**
- Return to Phase 2 with broader diagnosis
- Original fix treated symptom, not cause

## Common Godot Issues (Quick Reference)

| Symptom | Likely Godot Cause | What to Check |
|---------|-------------------|---------------|
| Offset gets worse with zoom | Coordinate conversion without viewport transform | `get_viewport().get_canvas_transform()` |
| Mouse position wrong in sub-viewport | Viewport coordinate system not accounted | `get_local_mouse_position()` vs `get_global_mouse_position()` |
| Node appears in wrong position | Parent transform not applied | Check node hierarchy, use `global_position` vs `position` |
| Input not working on Control node | Mouse filter or focus issues | `mouse_filter` property, `focus_mode` |
| Z-order wrong | Canvas layer or z-index | Check `z_index`, `z_as_relative`, canvas layer |

## Red Flags - STOP and Follow Process

If you catch yourself:
- Proposing fixes without asking what user observes
- Assuming you understand visual behavior from code alone
- Skipping testing for testable logic ("too simple to test")
- Trying fix #2 without re-diagnosing
- Guessing about Godot API behavior instead of researching
- Providing generic debugging instead of Godot-specific reasoning

**ALL of these mean: STOP. Return to correct phase.**

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "I can see the problem in the code" | You can't see what the user sees. Ask for observations. |
| "Testing coordinate math is overkill" | Coordinate bugs recur. Test prevents regression. |
| "Let me try this quick fix" | Without diagnosis, "quick fixes" create more bugs. |
| "Godot docs are slow to search" | Guessing about API behavior wastes more time. Research it. |
| "One more fix attempt" (after 2 failures) | 3+ failures = wrong approach. Stop and reconsider. |
| "Visual bugs can't be tested" | Underlying logic often CAN be tested. Identify testable parts. |

## Integration with Other Skills

**Reference these when:**
- Complex logic bugs (no visual component): skills/debugging/systematic-debugging
- Tracing through call stacks: skills/debugging/root-cause-tracing
- Writing tests: skills/testing/test-driven-development
- After 3+ failed fixes: Systematic Debugging Phase 4.5 (question architecture)

**Godot testing frameworks:**
- GUT (Godot Unit Test): v9.x for Godot 4.x, v7.x for Godot 3.x
- GdUnit4: Embedded framework with scene testing support

## Quick Reference

| Phase | Key Question | Must Complete Before Next Phase |
|-------|-------------|--------------------------------|
| **1. Observations** | What does user see? | Clear description of visual behavior |
| **2. Diagnose** | What Godot concept explains this? | Hypothesis using Godot terminology + research |
| **3. Testability** | Can we test the logic? | Decision: TDD or manual validation |
| **4. Fix** | What change addresses diagnosis? | Single fix following diagnosis |
| **5. Validate** | Did it work? | User confirmation OR return to Phase 1/2 |

## Real-World Example

**User**: "Hover indicator is 1.5 tiles southwest of cursor, worse when zoomed in"

**Phase 1**: ✅ User provided detailed observations (skip clarifying questions)

**Phase 2**:
- Research: Search "Godot mouse position viewport transform zoom"
- Diagnosis: "This is a coordinate space conversion issue. Mouse position is in screen space, but tile selection needs world space. The viewport transform (which includes zoom) isn't being applied to the mouse position before converting to tile coordinates."

**Phase 3**:
- Testable? YES - coordinate math
- Decision: Write test for `screen_to_tile_coords()` function

**Phase 4**:
```gdscript
# Test (in GUT)
func test_screen_to_tile_at_2x_zoom():
    var screen_pos = Vector2(100, 100)
    var zoom = 2.0
    var result = screen_to_tile_coords(screen_pos, zoom)
    assert_eq(result, Vector2(2, 2), "Should account for zoom in conversion")

# Fix - apply viewport transform
func screen_to_tile_coords(screen_pos: Vector2, zoom: float) -> Vector2:
    var world_pos = screen_pos / zoom  # Account for zoom
    return Vector2(int(world_pos.x / TILE_SIZE), int(world_pos.y / TILE_SIZE))
```

**Phase 5**: User validates → "Fixed! Cursor aligns perfectly now at all zoom levels"
