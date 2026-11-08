---
name: forge-token-economy
description: "Use for token or cost questions (hoe vol zit je, kosten) or caveman mode."
# W2-BUDGET original description (listing budget): "Use for token or cost questions (hoe vol zit je, usage, kosten, te duur, prompt caching, API spend) or for opt-in terse mode (caveman, kort antwoord, minder tokens). Never terse for QA or prompts."
---

# Forge playbook — Token and cost economy

**Self-improvement substrate:** before applying this skill, read `learnings.md` in this skill's own
folder and honor its corrections. After a run that produced a genuine correction, append it there with
a date and real evidence — never invent a lesson that did not happen.

Owner policy (`TOKEN_EFFICIENCY_GLOBAL_POLICY.md`): remove **waste**, never **rigour**. Quality and
security win every conflict. No savings figure is claimed unless it was measured.

## Where this skill stops (siblings)
| Question | Skill |
|---|---|
| The session degrades, when and how to compact | `forge-context` |
| Which model or effort for a task | GOAT routing (`.claude/FORGE_MODEL_ROUTING.json`, Head Chef triage) |
| How many parallel lanes now | `node .claude/forge-bin/forge-lane-budget.cjs` |
| Payments or billing features in an app | `forge-payments` |
| Write less code | `ponytail` |

## 1. "How full am I / what does this cost?" — measure, do not scan
Answer from the real meters first, in this order, and quote what they show:
1. `/context` — the current window by category (native, exact for this session).
2. `/usage` (and `/costs`, `/insights` where available) — plan usage and spend.
3. The per-prompt usage line and `node .claude/forge-bin/forge-lane-budget.cjs` — the 5-hour and weekly
   percentages Forge already tracks (`usage-guard.cjs status` refreshes them).
4. `node .claude/forge-bin/forge-usage-report.cjs [--by-run] [--cache]` — read-only history from the
   transcripts: tokens per run, compactions, cache-read share.
Do not start a file scan to answer "how full am I". A scan estimates; `/context` measures.

## 2. Always-loaded overhead audit (only on explicit request)
Bounded and read-only. Run `node .claude/forge-bin/forge-contextbudget.cjs` (add `--json` for detail);
it meters the global, workspace and project CLAUDE.md chain, the ECC rules and the skill catalogs against
a recorded baseline. Then classify what it shows:

| Bucket | Test | Action to propose |
|---|---|---|
| Always needed | Referenced by CLAUDE.md, backs a live command, fits this project type | Keep |
| Sometimes needed | Domain-specific, not referenced | Load on demand (a pointer instead of text) |
| Rarely needed | Duplicate, overlapping or no project match | Propose removal to the owner |

Look for: skill descriptions over 200 characters (the listing truncates them), agent files over about
200 lines, rules repeated between global and project files, MCP servers with many tools (each tool schema
costs context; `/mcp` can switch unused ones off), CLAUDE.md sections that belong in a skill.
Estimates: about words x 1.3 for prose, characters / 4 for code. Label every number **estimate** until
calibrated against a real `/context` reading. The audit proposes; it never deletes or edits global files.

## 3. Prompt caching (for projects that call an LLM API: forge-agent, forge-rag, bots)
- **Stable prefix first:** system prompt, tool definitions, fixed examples, long reference documents —
  byte-identical every call. Variable data (date, user, session id, the question) goes **after** it.
- **One changed character breaks the cache** downstream of it: no timestamps or version strings in the
  system prompt; do not reorder tools between deploys; roll prompt changes out deliberately.
- **Read the provider's counters** (for Anthropic: `cache_creation_input_tokens`,
  `cache_read_input_tokens` next to `input_tokens`) and report hit rate as **unmeasured** until a real
  run logged them.
- In Forge itself: do not switch the main-session model mid-task (full re-read at full price); delegate
  to a routed agent instead.
- Offline cost calculator (a small Node function, prices passed in, no price table): `references/cost-patterns.md`.

## 4. Cost burn in apps that spend API money
Check these before quality work, in this order (detail: `references/cost-patterns.md`):
1. App-generated events re-entering the expensive path (a bot reacting to its own output, a webhook
   triggered by its own write).
2. Quota checked before enqueue but charged only after the work (concurrent requests slip through).
3. Free or capped users reaching the expensive model.
4. Duplicate jobs and retries on errors that will never succeed.
5. Spending before persisting: the model ran, the result was lost.
Guards: a hard budget limit checked **before** each call; retry **only** transient errors (timeouts,
429, 5xx) with backoff and a cap; fail fast on auth and bad-request errors; log spend per run
(`node .claude/forge-bin/forge-cost.cjs <run_id> --agent <name> --tokens N` records a `cost_sampled` event).

## 5. Terse mode ("caveman") — opt-in only, never the default
On only when the owner asks for it ("caveman", "kort", "minder tokens", "be brief"); off on "stop
caveman", "normale modus" or "normal mode". Unsure whether it is on? Assume what the owner last said.

**Where it may apply at all** (owner policy `TOKEN_EFFICIENCY_GLOBAL_POLICY.md` → "Caveman / minimal mode
policy", allowed list): low-risk quick answers, simple terminal instructions and simple summaries. The
owner asking for it switches it on **only inside that space**; it never unlocks the never-list below.

Rules (adapted): answer first, then reason, then next step · no greeting, hedging, recap or closing
offer · short common words, no invented abbreviations · articles may go, **meaning never**: keep every
not/never/no/only/except and every number and unit · one idea per sentence, active voice · code,
commands, paths, API names and error text stay **verbatim** · stay in the owner's language (Dutch stays
Dutch) · never act out the style (no "me think", no prefix); if terse is not shorter, write plain.

**Never terse, even when the owner asked for it.** The owner policy's never-list applies **in full**, for
the whole task and not only its final message (write normal full sentences; resume terse only after the
task is over):
- prompts the owner will send to Claude (copy-paste prompts; they stay complete);
- website builds and n8n builds, from the first message to the handoff;
- security and auth work (including every security warning);
- production deployment;
- QA reports;
- business and client deliverables;
- anything where missing detail could cause rework.

Forge adds, on top of that list:
- any QA gate verdict: Test Boss, Review Boss, Verify Boss and Security Boss outputs, a PASS/FAIL,
  verification verdicts and the final `forge-report`;
- anything irreversible (deletes, overwrites, credentials);
- anything persisted: code, comments, commits, docs, memory files, messages to third parties;
- a question to the owner or a list of options; when the owner is confused or repeats a question;
- step orders that a fragment could scramble.
In doubt whether a task falls under the never-list: it does.

**Terse review lines (opt-in, informal self-review only):** one line per finding,
`<file>:L<line>: <bug|risk|nit|q>: <problem>. <fix>.`, allowed only for a Boss's in-flight self-check
or a quick chat look at a diff when the owner asked for terse mode. **Never** for a review that is a QA
gate (a Review Boss, Verify Boss or Security Boss pass, a code review the work package needs before
"done"): those keep the full `forge-code-review` format, file + line + what is wrong + the fix + the
reason. Security findings and architecture disagreements always get full prose. The severity scale of
`forge-code-review` still decides blocking.

Pre-send check: first sentence only announces? Delete. Last sentence recaps or offers help? Delete.
All negations, numbers, paths and errors still present and exact? Any sentence with two readings? Make
it a full sentence.

## Not adopted (and why)
Output filters that hide test output (they can hide a failing test from verification), status-bar
daemons, compression scripts that send file text to a provider or rewrite memory files, and "ask a
depth question before every answer" (conflicts with the autonomy rules). Haiku-first routing and old
price tables are not used: GOAT routing governs models.

## Provenance
- **ECC `skills/context-budget/SKILL.md`** — pinned local catalog commit
  `e2b8a51cea2228e515e1c3653effbeb62a2800fa`; MIT License, Copyright (c) 2026 Affaan Mustafa. Taken
  (rewritten): inventory → classify → detect → report, the three buckets, the words x 1.3 / chars / 4
  estimates, MCP schema overhead as the biggest lever. Excluded: the `/context-budget` command, Codex rows.
  The lane evidence describes a newer upstream version that routes "how full" questions to `/context`;
  that version is NOT in the pin, so section 1 is Forge's own wording of the idea, nothing copied.
- **ECC `prompt-caching-strategy`** — NOT present in the pinned catalog `e2b8a51`; used as an idea only
  (stable prefix, provider counters, "unmeasured unless measured"), nothing copied.
- **ECC `skills/ecc-tools-cost-audit/SKILL.md`** — same pin and license. Taken (generalised): the burn
  patterns and the burn-order fix sequence. Excluded: everything specific to the ECC-Tools repo and
  GitHub App, its skill stack.
- **ECC `skills/cost-aware-llm-pipeline/SKILL.md`** — same pin and license. Taken (rewritten): immutable
  cost tracker with a hard budget cutoff, retry only transient errors. Excluded: model routing by
  complexity (Haiku-first, contradicts GOAT), the pricing table (stale), all Python code (replaced by a
  Node function in `references/cost-patterns.md`).
- **JuliusBrussee/caveman** — paths `skills/caveman/SKILL.md` and `skills/caveman-review/SKILL.md`; pinned
  SHA `2e068f735253cce28256744804785f01887d9646`; Apache License 2.0 (`LICENSING.md`: everything from
  Caveman 3.0.0 on), NOTICE: "Caveman — Copyright 2026 Julius Brussee". Taken (rewritten, changed for
  Forge): the terse-voice rules, when-to-break list, pre-send check, the one-line review format and its
  Auto-Clarity exception. Excluded: hooks, the CLI, SDKs, MCP server, Engine/Proxy/Browse runtimes,
  agents and their `.mjs` compiler, `caveman-compress` (sends text to a provider), the `ultra`/`wenyan`
  modes, status-command plumbing, install steps and emoji severity markers. Changed for Forge: upstream
  keeps terse mode on for every response for the whole session once switched on, with its own short
  break list; here the owner policy's never-list and the Forge QA-gate
  rule override it (section 5).
- **Owner policy** `TOKEN_EFFICIENCY_GLOBAL_POLICY.md` → "Caveman / minimal mode policy": the allowed list
  and the never-list in section 5 restate it in full; on any conflict the policy wins.
Verified 2026-11-05: both caveman paths plus `LICENSE` (Apache 2.0), `LICENSING.md` and `NOTICE` were
fetched read-only at the pinned SHA from raw.githubusercontent.com (HTTP 200; the GitHub API was
unreachable); the NOTICE copyright line matches the one quoted above. The ECC catalog was confirmed at
`e2b8a51` with the three ECC skills present and `prompt-caching-strategy` absent. Hidden-Unicode scan: clean.

For full-output requests (complete prompt, whole file, deliverable): see `references/full-output.md`.
