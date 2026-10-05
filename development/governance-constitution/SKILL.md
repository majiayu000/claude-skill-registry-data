---
name: governance-constitution
description: >
  Create, amend, or check a project's governing "constitution" - the small set of
  non-negotiable engineering principles that every agent run (Claude Code and
  GitHub Copilot) should honour. Use when the user says "create/set up a
  constitution", "add a rule/principle to the constitution", "amend/update the
  constitution", "make this a non-negotiable", "what are our project
  principles", or asks to bootstrap the AGENTS.md contract; and in check mode when
  the user says "check my changes against the constitution", "does this violate a
  clause", "constitution check", or "review this for constitution compliance". Do
  NOT use for authoring a single architectural decision (that is governance-author-adr),
  for validating doc or graph link integrity (that is governance-check-graph), for
  ordinary docs, or for editing tracker tickets.
---

# Constitution

Owned by the **Lead** persona (custodian of the contract and graph integrity). Invoked as `/governance-constitution`.

Create and maintain a project's **constitution**: a short list of non-negotiable
principles that govern how the team and its AI tools (Claude Code + Copilot) build
software. The constitution is the spine of the AI-SDLC contract. It works only if it
is **small, always-loaded, and every clause is enforceable** - a long prose document
that no tool loads and no check enforces is worse than nothing (it creates false
confidence).

## Where it lives and how it loads (do not get this wrong)

The contract is split into an always-loaded core and on-demand detail. This split is
load-bearing for token cost, so respect it:

| Part | Lives in | Load policy |
|---|---|---|
| **Constitution core** (clause statements only, aim <= ~12 clauses, one line each) | `AGENTS.md` (a `## Constitution` section) | **Always-on, by design.** Read natively by Copilot; by Claude via the root `CLAUDE.md` stub. Keep it tiny. |
| **Full constitution** (each clause's rationale, enforcement, history) | `docs/constitution.md` | **On demand.** Read only when someone needs the detail. |

Why not import the full file into context? In Claude Code, `@import` is **eager** (it
loads at launch and does not save tokens), and Copilot cannot import at all. So the
core must physically sit in `AGENTS.md`, and the detail must stay a separate on-demand
file. Never `@import docs/constitution.md` or the ADRs into `CLAUDE.md`/`AGENTS.md`.

**Claude reads `CLAUDE.md`, not `AGENTS.md`.** So the root `CLAUDE.md` must contain
`@AGENTS.md` (an import line) so Claude picks up the core. On Windows use the import
line, not a symlink (symlinks need admin). Copilot reads `AGENTS.md` directly.

## Modes

Detect which the user wants; ask if ambiguous.

- **create** - bootstrap a constitution for a repo that has none.
- **amend** - add, change, or supersede a clause in an existing constitution.
- **check** (read-only) - review proposed or recent changes against the constitution and report violations. No writes.

## Clause format

Every clause is a testable, non-negotiable rule. In `docs/constitution.md` each clause carries:

```
### C<NN>: <short imperative statement>
- **Statement:** <the rule, one sentence, verifiable not vague>
- **Rationale:** <why this is non-negotiable here>
- **Enforcement:** <mechanism> - <status>
    mechanism = CI gate | linter | hook | skill | code review (manual)
    status    = active | deferred (planned: <what + where, e.g. "ADO coverage gate">)
- **Added:** <YYYY-MM-DD>  **Version:** <bump on change>  **Supersedes:** none | C<NN>
```

The `AGENTS.md` core carries only the imperative statement line per clause (so the always-on cost stays minimal). Detail lives in `docs/constitution.md`.

**The enforcement field is mandatory.** A clause with no enforcement is the "constitution
as prose" anti-pattern. If the gate does not exist yet, record it as `deferred (planned: ...)`
so it is a tracked debt, not an aspiration. This is what lets the gate phase bolt on later.

Good clauses are concrete: "Test line coverage must be >= 80% on changed projects",
"Every Bicep module reference pins an explicit version tag (no @latest)", "Load-bearing
architectural decisions require an ADR in docs/adrs/ before merge". Avoid "write clean
code" style non-clauses.

## create workflow

1. **Seed from what exists, do not invent.** Read the repo's current standards and lift the real, already-followed rules: `CLAUDE.md`, `AGENTS.md`, `.github/copilot-instructions.md`, `docs/conventions/*`, any `docs/adrs/*`. The constitution should ratify the team's actual non-negotiables, not impose new ones.
2. **Interview for the gaps.** Briefly confirm the candidate clauses with the user and ask what else is truly non-negotiable (security, coverage, naming, decision-recording, deployment safety). Keep pushing items that are "nice to have" out of the constitution and into conventions or docs.
3. **Draft both artefacts.** Write `docs/constitution.md` (full, every clause with rationale + enforcement) and the `## Constitution` core in `AGENTS.md` (statements only). Keep the core to ~12 clauses; if there are more, the extra ones probably belong in path-scoped conventions, not the constitution.
4. **Wire the loaders.**
   - If `AGENTS.md` does not exist, create it with: a short project-facts section, the `## Constitution` core, and a `## Where the detail lives` pointer block (to `docs/constitution.md`, `docs/adrs/`, conventions).
   - Ensure the root `CLAUDE.md` makes Claude read `AGENTS.md` (see "Handling an existing CLAUDE.md").
   - Remove `.github/copilot-instructions.md` only if its content has been folded into `AGENTS.md` (Copilot reads `AGENTS.md`); otherwise leave it and note the overlap.
5. **Confirm the diff before writing**, then write. Report what loads always (the core) vs on demand.

## amend workflow

1. Read `docs/constitution.md` and the `AGENTS.md` core first (never blind-write).
2. Apply the change: add a new `C<NN>`, modify an existing clause, or supersede one (mark the old clause `Superseded by C<NN>`, keep it in `docs/constitution.md` for history, remove it from the `AGENTS.md` core).
3. Bump the document version and append a one-line entry to a `## History` section in `docs/constitution.md` (date, what changed, why). Git history is the backstop, but the explicit log helps reviewers.
4. Keep the `AGENTS.md` core and `docs/constitution.md` in sync (statements identical). If the core grew past ~12 clauses, flag it and propose moving the weakest clause out.
5. Confirm the diff, then write.

## Handling an existing CLAUDE.md (important)

Many repos already have a large `CLAUDE.md` (this is common). **Never overwrite it with a one-line stub.** Instead:
- Offer to migrate: move its durable, tool-neutral content into `AGENTS.md`, then reduce `CLAUDE.md` to `@AGENTS.md` followed by any genuinely Claude-only notes.
- If the user does not want to migrate now, leave `CLAUDE.md` as-is and add `@AGENTS.md` at its top so Claude still loads the core. Note the duplication risk for later cleanup.
Either way, surface the existing file and the proposed change before touching it.

## Guardrails

- **Police the core's size.** The `AGENTS.md` core is the only always-on cost for both tools. If it exceeds ~1 screen, move detail to `docs/constitution.md` or to path-scoped conventions.
- **Confirm before writing** any of `AGENTS.md`, `CLAUDE.md`, or `docs/constitution.md`. Show the diff. These files are load-bearing.
- **Respect repo doc rules.** No source line numbers in any clause or doc (reference files by path + symbol). No em-dashes; use commas, colons, parentheses, or " - ". Match the repo's existing heading style.
- **Verify clauses against reality.** Do not write a clause the codebase already violates without flagging it - either the clause is wrong or there is debt to record. State which.
- **Every clause names its enforcement.** Deferred is allowed; absent is not.

## Next steps

- If a new or amended clause needs a code or doc change to comply, run `/create-code-generation` (Developer) or `/create-upsert-documentation` (Tech Writer).
- If the clause came out of a specific architectural decision, record it with `/governance-author-adr` (Architect) and backlink it via `/governance-enrich-ticket`.
- A clause's enforcement (its gate) is wired in the deferred gate phase; until then it is upheld in review.
