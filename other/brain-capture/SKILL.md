---
name: brain-capture
description: >-
  Extract 0-3 durable memories from the session about to end and submit them to the Second Brain
  CLI. Use ONLY when the global Stop hook (brain-capture-stop.mjs) blocks a session end under
  ~/Desktop/my-projets and tells you to invoke it. Never user-invoked, never speculative
  mid-session.
---

# Brain Capture

<!-- runtime-slot:intro -->
Second Brain (plan §08, V3) captures durable knowledge automatically at the end of every session under `~/Desktop/my-projets`, so decisions/lessons/preferences don't only live in a transcript that gets discarded. This skill is invoked once, right before the session actually stops, by the global Stop hook — never speculatively.
<!-- /runtime-slot:intro -->

## Step 1 — Decide if there's anything worth capturing

<!-- runtime-slot:step1 -->
Reflect on the session that just happened (you already have it in context — no need to re-read transcript files). Extract **0 to 3** candidate memories, one of these `kind`s each:

- `fait` — a fact learned about the user, a system, a codebase.
- `préférence` — a stated preference (tooling, style, workflow).
- `décision` — an architecture/product/process decision and its rationale.
- `leçon` — a lesson learned from a bug, an incident, a wrong assumption.
- `routine` — a recurring workflow/procedure worth remembering.
- `convention` — a project- or user-specific convention.

Bar for inclusion: would this matter to a future session that has no memory of this one? Routine tool calls, one-off debugging noise, or anything already captured earlier this same session do NOT qualify. **0 candidates is a normal, expected, and equally valid outcome** — most sessions won't produce anything durable. Never pad the count to hit a target.
<!-- /runtime-slot:step1 -->

## Step 2 — Resolve scope deterministically (never invent, never widen)

<!-- runtime-slot:step2 -->
This is a fail-safe boundary, not a judgment call:

1. Take the `cwd` reported by the hook (in its block reason).
2. Look up whether that `cwd` maps to a known project: run
   `bun run --cwd /Users/elmabi/Desktop/my-projets/second-brain cli/index.ts project list --limit 200`
   and check each row's context — a project is a match if its `repoPath` equals `cwd`, or (if `repoPath` is unset) if its `slug` equals the kebab-case name of the directory immediately under `~/Desktop/my-projets` that `cwd` is inside of.
3. **Match found** → inherit that project's `scope` and pass `--project <slug>` on every `remember` call below.
4. **No match** → scope is **`personnel`** (the most restrictive), no `--project`. Never fall back to `public`/`professionnel` without an explicit project match — an unmapped repo defaults to the safest scope, exactly so a stray capture on an unknown/new project never leaks past an approval gate.

Do not ask the user to disambiguate mid-capture — resolve deterministically per the rule above and move on. If the project genuinely needs a corrected `kind`/`scope`, that's a weekly-review fix, not this skill's job.
<!-- /runtime-slot:step2 -->

## Step 3 — Submit each candidate via the CLI

<!-- runtime-slot:step3 -->
For each candidate (in the order extracted), run:

```
bun run --cwd /Users/elmabi/Desktop/my-projets/second-brain cli/index.ts remember "<text>" \
  --kind <kind> --scope <scope> [--project <slug>] [--tags <csv>] [--confidence <0..1>]
```

Do not pre-filter for duplicates yourself — `remember` already does semantic dedup server-side (vector similarity ≥ 0.92, same scope/kind/project) and will report `skipped_duplicate` on its own; trust it and move on to the next candidate. Do not retry a failed submission more than once; if it errors, log it as a `submitted=false` case for step 4 and continue — a capture failure must never block the session from stopping.
<!-- /runtime-slot:step3 -->

## Step 4 — Log the run (mandatory, even at 0 candidates)

<!-- runtime-slot:step4 -->
Once all candidates have been attempted, ALWAYS run exactly one:

```
bun run --cwd /Users/elmabi/Desktop/my-projets/second-brain cli/index.ts capture-log \
  --candidates <N> --submitted <M> [--project <slug>]
```

`N` = candidates extracted in step 1 (may be 0). `M` = how many actually reached a `direct`/`pending`/`skipped_duplicate` outcome in step 3 (excludes hard failures). This writes an `audit_events` row (`tool: "brain-capture"`, `client: "claude-code"`) so a 0-memory pass is visible and auditable, never silent — this is what the V3 acceptance criterion "5/5 sessions trigger brain-capture, verifiable in audit_events" checks against.

Then touch the debounce sentinel — run `touch ~/.claude/.brain-capture-last-run` (even at 0 candidates). This starts the 30-minute debounce window the Stop hook (`~/.claude/hooks/brain-capture-stop.mjs`) checks before re-blocking a session end, so a burst of session restarts doesn't re-trigger the block every time.
<!-- /runtime-slot:step4 -->

## Step 5 — Stop normally

<!-- runtime-slot:step5 -->
After step 4, the capture pass is complete. End your turn as you normally would — the Stop hook's `stop_hook_active` guard ensures it will not block you again this turn.
<!-- /runtime-slot:step5 -->
