---
name: grill
description: "Read-only pre-design interview that surfaces tacit intent before planning. Use on explicit request, or before design when intent risk stays high after discovery and at least two hold: large blast radius, irreversible or costly choice, multiple valid directions, unstated priority. Skip when one clarification suffices, for debugging, and inside another pm skill unless asked."
argument-hint: "[what to grill about]"
allowed-tools: Bash, Read, Glob, Grep, AskUserQuestion
effort: high
disable-model-invocation: false
---

Interrogate the user to extract tacit intent before the real work begins. **You are the questioner; the user is the validator.**

Subject: $ARGUMENTS (if empty, ask what to grill about)

## System — design's read-only pre-step

grill is an **optional read-only front-step to `design`** — not a pm-* loop node (it owns no per-task artifact, so the canonical loop is unchanged). It consumes the same per-task inputs `design` reads — pm-context links, retro memory, the pm-roadmap item — interrogates the user to resolve what they leave unstated, then hands the aligned intent to `design`. It **persists nothing**: the intent flows into the next step (`design` plan `Decisions`, or `retro` task memory). If no `design`/`retro` follows, the intent is intentionally session-volatile — by design, not a bug.

## Inputs — read BEFORE asking (do not ask what these answer)

```bash
pm_root="$HOME/.config/ai/skills/pm-roadmap"
repo_root="$(git rev-parse --show-toplevel 2>/dev/null)" || repo_root=""
if [ -n "$repo_root" ] && [ -x "$pm_root/node_modules/.bin/tsx" ]; then
  pm() { PM_ROOT="$repo_root" "$pm_root/node_modules/.bin/tsx" "$pm_root/pm-roadmap.ts" "$@"; }
fi
```

- Resolve the originating session first, using the exact injected metadata:
  `PM_SESSION_TOOL="<tool>" PM_SESSION_ID="<exact id>" node "$HOME/.config/ai/lib/worktree.mjs" resolve-session --root "$repo_root" --tool "<tool>"`.
- When it returns `ok`, run `pm get <resolved plan id>` and use its owning **`<KEY>`**
  to read `.agents/tasks/<KEY>/links.md` and `memory.md`, both read-only. An explicitly
  supplied item id may be passed directly to `pm get`.
- Always grep/read the **codebase** for anything answerable from code.
- An unbound session, no Task linked to its validated plan, or outside a repo → skip the
  PM probes and inspect code only. Never fall back to a launcher selection. **Never run
  `npm install` from grill.**

## Protocol

1. **Explore first.** Answer everything you can from the inputs. Only what code+context cannot answer goes to the user.
2. **One question at a time** via `AskUserQuestion`. Never batch.
3. **Each question carries your recommended answer first** + a one-line rationale.
4. **Dependency-tree order** — each answer narrows the next; prune branches a prior answer closed.
5. **Hunt tacit knowledge** — prioritize constraints / priorities / "why this way" over surface choices.
6. Default **1 round**; hard cap **3 rounds**.

## Stop conditions

Stop when ANY holds: the actionable choices are settled; the user says proceed/skip; questions start repeating; further questions no longer reduce design risk; the 3rd round is reached. Then emit a compact **Extracted Intent** bullet block for the next step to consume.

## Hard rules

- **Write nothing.** Write/Edit are omitted from `allowed-tools`, and Bash is restricted to read-only commands only: `git rev-parse`, `git status/log/branch`, `pm list|tree|get|next|recent|validate|current-task`, and read-only `rg`/`grep`/`find`/`ls`/`sed -n`. Forbidden: shell redirection, heredocs, `tee`, `sed -i`, `npm install`, and every pm write subcommand (`task`/`add`/`plan`/`approve`/`close`/`drop`/`triage`/`memory`/`links`/`persist`/`complete`/`migrate --apply`). Durable capture is delegated downstream — point there, never write it yourself.
- **Don't re-ask what code/context answers.** Exploring first is mandatory, not optional.
- **Recursion SKIP**: if already inside another skill flow (design / verify / …), do not start grill anew unless the user's latest message explicitly asks for it.
- Questions are decision-shaped (about intent), not a code review.
