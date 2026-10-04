---
name: next-slice
description: Closes out a just-finished implementation slice and emits a self-contained handoff prompt for a fresh session — gates that the slice landed (else stops), re-anchors the plan's stale refs against current code, and harvests what building revealed. Use when the user says "next-slice", "hand off the next slice", "close out this slice", or asks to prepare a fresh-session prompt to continue a sliced implementation plan. Explicit-only; it hands off or halts, never re-plans, and never writes the always-loaded guidance file.
disable-model-invocation: true
license: MIT
metadata:
  version: "1.0.0"
  author: "bitcoin21ideas"
---

# next-slice

You are the agent that just finished implementing a slice. Convert the context you now hold — the stuff the plan's author never had — into a clean handoff before the session ends, so the next agent inherits reality, not a stale plan.

Ideally run by the implementer of the slice just completed; it holds the fresh context. If run cold, reconstruct from `git log` and the slice's diff before proceeding.

**Scale the output to the slice.** A trivial slice against a still-accurate plan yields a short prompt that just points at the plan, the branch, and the gate. Only real findings earn ceremony — every line in the handoff must be something the next agent would otherwise get wrong or waste time re-deriving.

## 1. Confirm the boundary

- **The plan file** the builders read. Ask the user if it's unclear — don't guess.
- **Which slice just finished (N) and which is next (N+1).** Infer from the plan's slice list and `git log`; confirm if ambiguous.

## 2. Landed-state gate — do not hand off on sand (mechanical; hard stop)

Before anything else, prove slice N actually landed. All three must hold:

- **Clean tree** — no uncommitted changes, or only files slice N was expected to touch.
- **Green gate** — run the project's own test/build command, read from the repo (its agent-guidance file, `package.json`, `Makefile`, CI config); don't assume one. It must pass now, not "should pass."
- **Committed** — slice N is committed. Capture the branch and commit SHA(s).

If any fails: **STOP.** Report exactly what is unlanded and hand it back to the human. Emit no handoff — a handoff layered on red or uncommitted work poisons the next session.

## 3. Harvest what building the slice revealed

Three lenses on one question: *what changed that N+1 must now cope with?* Keep a finding only if the next agent would otherwise get it wrong. Drop the rest.

**a. Pre-mortem (judgment).** Ask, in the implementer's voice: *what did I learn building this that the plan's author didn't know, that would bite the next agent?* Frame it forward (what breaks next), never backward (how it went) — the implementer is a biased judge of its own work, so hunt for problems, not reassurance. Harvest only the load-bearing:
- Plan **assumptions** that proved false or imprecise.
- **Deferred work / TODOs** the next slice now depends on.
- **Invariants this slice touched** — read the standing ones from the repo's guidance file and the plan's out-of-scope / risks sections.
- **Competing constraints** N+1 must satisfy at once — name each tension *and its resolution or ordering*. Never emit a bare "be careful."

**b. Re-anchor (mechanical — verify, don't trust).** The plan's `file:line` refs and symbol names go stale the moment code changes. For every anchor the *next* slice cites: grep the file and symbol, rewrite the line number to current reality. If the plan points at something that no longer exists (renamed, moved, deleted), flag it — that's a finding, possibly a blocker. Never carry a plan's line number forward on trust.

**c. Seam diff.** Enumerate every interface slice N created or changed that N+1 will call against — the contract between them. Only the seams N+1 actually touches; get the shapes exact, because this is what the next agent codes against:
- **endpoints** — method, path, request shape, response shape, error/status codes
- **props / store actions / exported signatures**
- **env vars, config keys**
- **DB columns / migrations**
- **new invariants** the seam imposes

## 4. Record durable findings in the plan — default nothing

Append to the plan file **only** a finding that is durable *and* not recoverable from the code or `git log`. A re-anchored line number the next agent will re-grep anyway does not qualify; most slices append nothing. When something does clear that bar, add it as one delimited block:

```
## Field notes — post-Slice N (<branch> @ <sha>)
- seam: <interface N+1 consumes>
- watch: <invariant / tension and its resolution>
- re-anchored: <old ref> → <new ref>   # only if N+1 won't re-grep it anyway
```

**Append only.** Never rewrite or delete existing plan prose — the plan's history stays intact. The plan is read on demand, so it is the right home for point-in-time detail; the always-loaded guidance file is not (see Hard rules).

## 5. Hand off — a delta-only prompt

Produce a prompt the user pastes into a fresh session. It carries only what the plan doesn't already say correctly — everything else is a pointer. Lead with commands and constraints, then prose (a fresh session reads the top first and drifts from rules a few messages in):

1. **One line** — the task and a pointer to the plan's §N+1 slice + the repo's agent-guidance file.
2. **State** — branch, what's committed (SHAs), what this slice changed; the **re-anchored refs** (§3b) and **seam contract** (§3c); the **tensions with their resolutions** (§3a).
3. **Scope fence** — what N+1 covers, plus an explicit **do-not-touch** list (files owned by later slices).
4. **The gate** — the exact command that must pass, and where to commit/deploy per the repo's convention.

Then run the **self-containment check**: would this work pasted cold, with zero memory of this session? Every fact must live in the prompt, the plan, or the repo's guidance file — no "as we discussed." Cut anything the plan already states accurately and point at the plan instead.

## 6. Verdict — go / no-go, and permission to say no

End with an explicit call: *clear to start Slice N+1, or blocked?* If a finding means N+1 should be re-split, resequenced, or needs a human decision, say so and stop — do not paper a blocker into a green prompt. This skill hands off or halts. It never re-plans.

## Hard rules

- **Read-only toward the always-loaded guidance file** (`CLAUDE.md` / `AGENTS.md`). Read it to pull invariants into the handoff; **never write it** — it loads on every request, so appending per slice is a compounding token tax. If a finding contradicts a rule there, emit one loud in-session line — `⚠️ CLAUDE.md may be stale: <rule> — <why>. Human review, not mine to edit.` — and continue. Only if that broken rule is an invariant N+1 depends on does the verdict flip to no-go.
- **The plan is the only file you write** — append-only (§4). No code edits, no commit, no deploy. Slice N is already committed via §2.
- **Never re-plan.** Re-anchoring is not re-architecting. Findings that demand a new plan go back to the human, or to the planning skill.
- **Evergreen skill.** No line numbers, SHAs, repo names, or dates in this file. Every point-in-time fact lives in what you generate.
- **Portable, repo-aware.** Read the gate command, plan path, commit convention, and invariants *from the repo it runs in* — hardcode none.

## Where this fits

`pressure-test` → `to-plan` → `plan-clash` → **[build slice]** → **`next-slice`** → **[build slice]** → **`next-slice`** → … Run it at every slice boundary, once the slice is committed and green.
