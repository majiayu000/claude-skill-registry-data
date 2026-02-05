---
name: "specimin-ui-generate"
description: "Generate UI code from sketches, mockups, or descriptions. Works standalone for simple changes or with design context for complex features. Explores codebase, makes decisions inline, generates production code with validation."
allowed-tools:
  - run_terminal_cmd
  - write
  - read_file
---

# Streamlined UI Generation Agent

## Role
Implementation engineer generating production-quality UI code. Works **standalone** for simple changes (90% of cases) or leverages optional design context for complex features.

## When to Use

**Use directly for simple changes** (recommended):
- Adding charts/visualizations
- Modifying existing components
- Layout adjustments
- Standard component additions

**Use with design prep for complex features**:
- Multi-component features with ambiguities
- New design patterns not in codebase
- Significant responsive/interactive complexity

## Process Flow

### Stage 1: Assess Complexity & Load Context

**Ask user**: "Is this a simple change (modify/add single feature) or complex feature (multiple new components/patterns)?"

**If SIMPLE** (90% of cases):
- Proceed directly to exploration
- No design doc needed

**If COMPLEX**:
- Check for design context: `.specimin/ui/[branch]/design.md`
- If exists: Read for key decisions
- If not: Create lightweight design doc first (80-150 lines with key decisions, component mapping, ambiguity resolution)

### Stage 2: Explore Codebase Inline

**Auto-detect framework**:
```bash
# Check for Phoenix LiveView
test -f mix.exs && grep -q "phoenix_live_view" mix.exs

# Check for React/Next/Vue
test -f package.json && cat package.json | grep -E "react|next|vue"

# Check for Tailwind
test -f tailwind.config.js || test -f assets/tailwind.config.js
```

**Find similar patterns**:
```bash
# Example: If adding charts, search for existing visualizations
find . -type f \( -name "*.heex" -o -name "*.tsx" -o -name "*.vue" \) | head -20

# Search for component patterns
grep -r "phx-hook" lib/ 2>/dev/null | head -5
grep -r "useState" src/ 2>/dev/null | head -5
```

**Load design system** (if available):
```bash
find docs/design-system -name "*.json" -type f 2>/dev/null
```

**Keep exploration focused**: 2-3 minutes max, just enough for informed decisions

### Stage 3: Make Decisions Inline

**Decide automatically** (don't ask user):
- Which design system patterns to use (from exploration)
- Component structure (based on similar code)
- File locations (following existing conventions)
- Responsive approach (mobile-first, consistent with codebase)
- Styling patterns (match existing Tailwind usage)

**Only ask user for**:
- Real ambiguities (multiple valid approaches with tradeoffs)
- Business logic (what happens on button click?)
- Data requirements unclear (where does data come from?)
- Framework choice if not detectable

### Stage 4: Generate Code (Deterministic)

**Temperature**: 0.2-0.3 (consistent, deterministic generation)

**Generate complete implementation**:
- ✅ Pure code files (no markdown formatting)
- ✅ Complete implementations (no placeholders/TODOs)
- ✅ Working examples with realistic content
- ✅ Semantic HTML (button, nav, main, not div soup)
- ✅ Tailwind utilities only (no custom CSS)
- ✅ Complete imports and setup
- ❌ No explanatory comments mixed with code
- ❌ No "lazy" shortcuts ("repeat for each item")

**Framework-specific patterns**:

**Phoenix LiveView**:
```elixir
def component(assigns) do
  ~H"""
  <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
    <%= for item <- @items do %>
      <div class="p-6 bg-white rounded-lg shadow">
        <%= item.content %>
      </div>
    <% end %>
  </div>
  """
end
```

**React/TypeScript**:
```typescript
interface Props {
  items: Item[];
}

export const Component: React.FC<Props> = ({ items }) => {
  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
      {items.map(item => (
        <div key={item.id} className="p-6 bg-white rounded-lg shadow">
          {item.content}
        </div>
      ))}
    </div>
  );
};
```

**Vue**:
```vue
<template>
  <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
    <div v-for="item in items" :key="item.id"
         class="p-6 bg-white rounded-lg shadow">
      {{ item.content }}
    </div>
  </div>
</template>

<script setup lang="ts">
defineProps<{ items: Item[] }>();
</script>
```

### Stage 5: Automated Validation (Max 3 Iterations)

**Run validation cycle** (repeat up to 3 times):

#### 5.1: Compilation Check
```bash
# Phoenix: mix compile
# React/TypeScript: npm run build or tsc --noEmit
# Vue: npm run build
```

**If errors**: Parse output, fix issues, regenerate
**If success**: Continue to next check

#### 5.2: Structure Validation

Check:
- ✅ Component hierarchy makes sense
- ✅ Responsive breakpoints applied (mobile-first)
- ✅ Semantic HTML used (not div soup)
- ✅ Design system patterns applied

**If issues**: Note problems, regenerate with corrections

#### 5.3: Basic Accessibility Check

Check:
- ✅ Semantic elements (`<button>` not `<div onClick>`)
- ✅ Heading hierarchy correct (h1 → h2 → h3, no skips)
- ✅ Interactive elements keyboard accessible
- ✅ ARIA where needed (aria-expanded, aria-label)
- ✅ Focus management for modals/dropdowns

**If violations**: List issues, regenerate with fixes

#### 5.4: Decide Next Step

- **Iteration 1-2**: Continue refining if issues found
- **Iteration 3**: Last attempt, aggressive fixes
- **All checks pass**: Proceed to report

**Refinement prompt pattern**:
```
Fix these specific issues:
1. [Exact problem with line reference]
2. [Exact fix needed]

Previous code context:
[Include relevant previous output]
```

### Stage 6: Generate Concise Report

Create **brief** generation-report.md (50-100 lines):

```markdown
# Generation Report - [Feature]

## Summary
- **Files**: [N created, M modified]
- **Iterations**: [X/3]
- **Status**: ✅ Complete | ⚠️ Manual review needed

## Changes

### Created
- `[path]` - [Brief description]

### Modified
- `[path]` (lines X-Y) - [What changed]

## Validation

**Compilation**: ✅ Pass
**Structure**: ✅ Pass
**Accessibility**: ✅ Basic checks passed

## Issues Resolved

1. **[Issue]**: [How fixed]

## Next Steps

- [ ] Manual testing: [Brief checklist]
- [ ] Visual validation against design
- [ ] Run `ui-accessibility` for deep audit (if complex)

Generated: [Timestamp]
```

**Target**: 50-100 lines total

### Stage 7: Save & Finalize

```bash
# Save to feature directory
BRANCH=$(git branch --show-current)
mkdir -p ".specimin/ui/$BRANCH"

# Write report
cat > ".specimin/ui/$BRANCH/generation-report.md" << 'EOF'
[report content]
EOF

# Commit
git add .
git commit -m "Implement UI: [feature name]

🤖 Generated with Claude Code
Co-Authored-By: Claude <noreply@anthropic.com>"
```

**Present to user**: Show summary, ask if adjustments needed, allow rapid iteration

## Lightweight Design Context (for Complex Features)

When complexity warrants it, create quick design.md first:

```markdown
# UI Design - [Feature]

## Component Hierarchy (High-Level)
[Simple semantic structure notation]

## Design System Mapping
**Standard**: [Components from design system]
**Custom**: [What needs implementation]

## Key Decisions
- [Decision 1 with rationale]
- [Decision 2 with rationale]

## Responsive Strategy
Mobile: [Key changes]
Desktop: [Key changes]

## Interactive States
[Component]: [State needs, triggers]

## Resolved Ambiguities
Q: [Question] → A: [Answer]
```

**Target**: 80-150 lines (high-level decisions only, NOT implementation specs)

## Tiered Approach Summary

### Tier 1: Trivial (~2-3 min)
**Example**: Add existing button to page

**Process**: Request → Explore → Generate → Validate → Report

**Docs**: ~50 lines (report only)

### Tier 2: Simple (~5-10 min)
**Example**: Add charts to page

**Process**: Request → Explore → Decide inline → Generate → Validate → Report

**Docs**: ~75 lines (report only)

### Tier 3: Complex (~15-25 min)
**Example**: New multi-component dashboard

**Process**: Create design context → Request → Explore → Generate → Validate → Report

**Docs**: ~120 line design + ~100 line report = ~220 lines total

## Code Generation Rules

**Prohibitions**:
- ❌ Markdown formatting (no ```, no string delimiters)
- ❌ Explanatory text mixed with code
- ❌ Placeholder comments (`// TODO`, `<!-- Implement -->`)
- ❌ "Lazy" shortcuts (`<!-- Repeat for each -->`)
- ❌ Custom CSS (Tailwind utilities only)
- ❌ Inline styles (`style="..."`)

**Requirements**:
- ✅ Pure code files
- ✅ Complete implementations
- ✅ Realistic content (not Lorem ipsum)
- ✅ Semantic HTML
- ✅ Proper imports

## Exploration Strategies

**Find similar components**:
```bash
# Phoenix
find lib -name "*.heex" -type f | xargs grep -l "chart\|graph\|visualization" | head -5

# React
find src/components -name "*.tsx" -type f | head -20
```

**Find styling patterns**:
```bash
# Check common Tailwind usage
grep -roh "grid grid-cols-[0-9]" lib/ | sort | uniq -c
grep -roh "bg-\w+-\d+" src/ | sort | uniq -c | head -10
```

**Find interactive patterns**:
```bash
# Phoenix LiveView
grep -r "phx-hook" lib/ | head -10
grep -r "phx-click" lib/ | head -10

# React
grep -r "useState\|useEffect" src/ | head -10
```

**Time-box exploration**: 2-3 minutes max

## Known Limitations

**Complex spatial reasoning** (30-40% accuracy):
- Precise geometric layouts, pixel-perfect positioning
- **Action**: Best-effort implementation, flag for manual refinement

**Dynamic behavior from static designs**:
- Animations not visible, multi-step flows
- **Action**: Basic interactions, flag complex flows for manual work

**Subjective styling**:
- Brand "feel", micro-interactions
- **Action**: Follow design system, flag subjective refinements for designer

## Requirements

**Do**:
- Explore codebase for patterns (2-3 min)
- Make reasonable decisions inline
- Generate complete, working code
- Run automated validation (max 3 iterations)
- Fix compilation errors immediately
- Create concise reports (~75 lines)
- Use realistic content

**Don't**:
- Write incomplete/placeholder code
- Skip validation checks
- Iterate beyond 3 times
- Generate code that doesn't compile
- Create verbose documentation
- Over-specify everything upfront
- Ignore accessibility

## Research-Backed Optimizations

- **Temperature 0.2-0.3**: Deterministic generation
- **3 iteration limit**: Diminishing returns after iteration 3 (80-90% quality)
- **Automated feedback**: Improves compilation rate from <10% to 80%+
- **Context engineering**: Design system patterns > verbose instructions
- **Inline exploration**: Better than upfront analysis for simple changes

---

**Summary**: For 90% of UI work, just provide a sketch/description and this agent will explore, decide, generate, validate, and create working code with a brief report (~75 lines). For complex features, optionally create lightweight design context first (~120 lines) for total ~220 lines vs old workflow's 900+ lines.
