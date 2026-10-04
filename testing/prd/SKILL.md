---
name: prd
description: Convert current conversation context into a structured Product Requirements Document (PRD) and optionally post it to GitHub Issues. Use before /supergraph:plan when requirements came from a conversation, user story, or feature discussion rather than a formal spec.
---

# /supergraph:prd

Turn conversation into a machine-readable PRD. Gives `/supergraph:plan` a concrete spec to work from.

Announce: "📋 /supergraph:prd — extracting requirements..."

## Steps

### 1. Read CONTEXT.md (if exists)

```bash
head -60 CONTEXT.md 2>/dev/null || echo "No CONTEXT.md"
```

Use domain vocabulary from CONTEXT.md in the PRD — never invent new terms for existing concepts.

### 2. Extract requirements from conversation

Gather from current conversation context:
- What the user wants to accomplish
- Any constraints or non-goals mentioned
- Technical decisions already made
- Edge cases or concerns raised

Ask one clarifying question if a critical piece is missing. Do not ask multiple questions at once.

### 3. Write PRD

```markdown
# PRD: [Feature/Fix Name]

## Problem
[One paragraph: what is broken or missing, and why it matters]

## Solution
[One paragraph: the approach — what will be built]

## User Stories
- As a [role], I want [action] so that [outcome]
- (2-5 stories max)

## Acceptance Criteria
- [ ] [Observable, testable condition]
- [ ] [Observable, testable condition]
- (Each maps to a test in /supergraph:plan)

## Implementation Decisions
- [Technology/pattern chosen and why]
- [What was explicitly ruled out and why]

## Testing Decisions
- [Unit: what gets unit tested]
- [Integration: what needs integration tests]
- [E2E: what needs Playwright coverage, if any]

## Out of Scope
- [Explicitly not included in this work]

## Notes
- [Domain terms: add to CONTEXT.md if new]
- [Dependencies on other work]
- [Security considerations]
```

### 4. Present for approval

Show PRD to user. Ask: "Does this capture what you need? [yes / adjust]"

Incorporate feedback, re-present if needed.

### 5. Post to GitHub Issues (optional)

If user confirms and repo has GitHub remote:
```bash
gh issue create \
  --title "[PRD] <feature name>" \
  --body "$(cat <<'EOF'
[PRD content]
EOF
)" \
  --label "enhancement,ready-for-agent"
```

Report issue URL.

### 6. Save locally

Save to `docs/supergraph/plans/YYYY-MM-DD-prd-<slug>.md`.

### 7. Update CONTEXT.md

If the PRD introduced new domain terms:
```bash
# Append to CONTEXT.md
printf '\n## <term>\n[definition from PRD]\n' >> CONTEXT.md
```

### 8. Report

```
✅ /supergraph:prd complete
- PRD: docs/supergraph/plans/YYYY-MM-DD-prd-<slug>.md
- Issue: #N (if posted)
- Acceptance criteria: N
- Next: /supergraph:plan
```

## Rules

- Never skip user approval (step 4)
- Acceptance criteria must be observable and testable — no vague criteria
- Out of scope section is mandatory — prevents scope creep in plan
- Post to GitHub only if user has confirmed the PRD
