---
name: quickstart
description: >
  Guided first-run that produces a real verified win in under five minutes
  using the skill library on a seeded offline fixture. Load when a new user
  asks how to start, run the demo, try agent-loom, or get a quick win.
  Also triggers on "quickstart", "first run", "demo agent-loom", "try the
  skills", or onboarding to the library. Zero external credentials required.
  Idempotent — safe to run multiple times.
license: MIT
metadata:
  author: dvy1987
  version: "1.0"
  category: project-specific
  sources: microsoft/apm oss-growth-hacker, GitHub-Driven GTM patterns
  resources:
    references:
      - DEMO-FLOW.md
      - examples.md
---
# Quickstart

You get a new user to a **real, verified result** in ~5 minutes — not a staged fake. Demo uses `safe-change` on `examples/seed/calc/`.

## Hard Rules

Zero external credentials — offline fixture only.
Invoke a **real skill** (`safe-change`) — never simulate success.
Idempotent — if fix already applied, run impact map + tests and report "already done."
End with one-line "what just happened" + link to `examples/` tours.
Total flow ≤5 minutes wall clock.

---

## Workflow

### Step 1 — Confirm install

User has agent-loom skills visible (`.agents/skills/` or global install). If missing, point to `README.md` Installation.

### Step 2 — Run demo (read `references/DEMO-FLOW.md`)

1. `cd examples/seed/calc` (or pass path to verify.sh)
2. `dependency-mapping` on `divide` in `calc.py`
3. `safe-change` — add zero guard; **verify fails before fix, passes after**
4. `bash .agents/skills/safe-change/scripts/verify.sh examples/seed/calc`

### Step 3 — Explain

```markdown
**What just happened:** You ran impact mapping → one verified edit → tests green.
That's the safe-change loop — the library's highest-leverage coding skill.
```

### Step 4 — Next steps

Point to:
- `examples/safe-change-demo/README.md`
- `examples/structured-planning-demo/README.md`
- `examples/deploy-anywhere-demo/README.md`
- `docs/why-agent-loom.md`

---

## Gotchas

- pytest may need `pip install pytest` once — document if missing.
- User on Windows: use same paths with forward slashes in agent prompts.

---

## Output Format

```markdown
## Quickstart complete

Result: [KEPT | already fixed]
Verify: pytest → [pass]
What happened: [one line]
Next: [examples link]
```

---

## Examples

Full walkthrough: `references/DEMO-FLOW.md`

---

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "Fake a passing test" | Destroys trust — run real safe-change. |
| "Skip install check" | User without skills gets a confusing failure. |
| "Long architecture tour first" | Win first, depth second. |
| "Use a remote repo" | Needs network + creds — seed is offline. |
| "Combine all five skills" | One win — safe-change only. |

## Verification

- [ ] Real skill invoked (not simulated)
- [ ] pytest run on seed fixture
- [ ] User told what happened in one line
- [ ] Next-step links provided

## Red Flags

- Simulated verify pass
- Demo requires API keys
- No reference to examples/

## Prune Log
Last pruned: 2026-07-05
- Initial release from high-leverage skill spec (Skill 5 family)

## Impact Report

```
Quickstart: [pass|already-done] | Skill: safe-change | Fixture: examples/seed/calc
```
