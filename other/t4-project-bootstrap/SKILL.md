---
name: t4-project-bootstrap
description: Use when starting, scaffolding, or setting up a new repository for the T4 team (T4 Labs / Slow-Inc) — or retrofitting an existing one — so an agent-primary repo gets the team's standard operating layer (domain glossary, product brief, decision records, durable memory, dev workflow) in one pass instead of hand-copying docs from a sibling repo. Triggers include "set up a new T4 project", "scaffold the docs/conventions", "add CLAUDE.md + docs/agents", "bootstrap the governance layer", "port the MangaDock conventions".
---

# T4 Project Bootstrap

## Overview

The T4 team (T4 Labs / `Slow-Inc`) runs several repos — MangaDock, T4-Fastwork, and more — where **the coding agent is the primary developer**. They share one operating standard, built so an agent keeps context across sessions and compaction. This skill scaffolds that standard into a new (or under-documented) repo in one pass.

**Core principle:** the standard is agent infrastructure, not team paperwork. You are installing the files a future agent will read at session start to know *what the words mean, why the code is the way it is, what's still open, and how to ship*. Copy the structure and rules; fill `<PLACEHOLDER>` tokens with this project's specifics; never carry another project's domain content across.

This skill owns the **domain + product layer** and orchestrates the install. The ongoing-use disciplines are sibling skills — install their files here, but read them for the how:

- **`using-t4`** — the entry-point map routing a task to the right skill below. The repo's `CLAUDE.md` should point a fresh agent here first.
- **`t4-agent-memory`** — durable working memory (open-work ledger, ship log, survey-manifest, memory vault, Serena). The retrieval-first backbone of an agent-primary repo.
- **`t4-engineering-records`** — ADRs, post-mortems, the impact register, the bug-case catalog.
- **`t4-dev-workflow`** — the grill→PRD→issues→TDD pipeline, bilingual tracker rules, triage labels, auto-triggered skills.

## When to use

- Standing up a brand-new T4 repo (before or just after the code scaffold).
- An existing T4 repo missing the operating layer (no memory ledger, no `CONTEXT.md`, no `docs/agents/`).
- You caught yourself about to hand-copy a doc from MangaDock/T4-Fastwork — do this instead.

**When NOT to use:** a throwaway prototype; a non-T4 project (the bilingual tracker rule and label vocabulary are team-specific).

## Tier by agent-context-load, not team size

An agent-primary repo needs its **memory layer from day one** — that's what makes work survive a context reset. So the memory backbone is default-on; scale the rest by how much the agent has to hold.

| Repo stage | Install |
|---|---|
| **Seed** (new repo, first sessions) | `CLAUDE.md` wiring · **the workflow-hooks layer** (`references/hooks-layer.md`) — keeps the session on the rails from day one · **the CI/CD gate** (`references/ci-cd-layer.md`) — required checks on `main` from the first PR, before there's a habit of merging without them · `docs/agents/{domain,issue-tracker,triage-labels,workflow}.md` (`t4-dev-workflow`) · `docs/adr/README.md` (`t4-engineering-records`) · **`docs/OPEN-WORK-LEDGER.md` + `DONE.md` + the memory vault** (`t4-agent-memory`) — memory is not deferred. Create `CONTEXT.md`/`UBIQUITOUS_LANGUAGE.md`/`PRODUCT.md` **lazily** (proceed-silently rule). |
| **Active** (real feature work, growing surface) | + `CONTEXT.md` + `UBIQUITOUS_LANGUAGE.md` + `PRODUCT.md` + `DESIGN.md` + `docs/reports/README.md` + `post-mortem` / `impact-register` / `bug-catalog` (`t4-engineering-records`) + `docs/superpowers/{plans,specs}/` (`t4-dev-workflow`) + the `survey-manifest` (`t4-agent-memory`). |
| **Consolidating** (work scattered; agent misses MD-only items) | + a full `docs/OPEN-WORK-LEDGER.md` reconciliation pass + Serena `mem:` graph. This is the tier where the ledger earns its keep. |
| **Formal delivery** (academic / client dossier) | + the optional 7-phase SE set — see `references/se-deliverables.md`. On demand only. |

## Before you start: check what this bootstrap depends on

Three prerequisites, and all three fail the same way — **quietly, leaving a trail that looks like success.** Steps 1–5 each drop a visible file, so a run that never loaded the disciplines, could not create a single label, or reached no companion skill is indistinguishable from one that did all three. Check all three before you reach the step that needs them; this is step 11's argument applied to the inputs rather than the outputs.

### 1. Load the disciplines yourself — nothing in the repo will do it for you

**Invoke `using-t4` and `t4-bro` before you read the target repo.** Not "consult", not "keep in mind" — invoke them, the way `using-t4` says to invoke a skill rather than work from memory of it.

**Why this step exists, and why it is not redundant.** Every mechanism that normally surfaces the T4 disciplines is an artifact **this procedure installs**:

| Surfacing mechanism | Installed by | Present during this session |
|---|---|---|
| `.claude/t4.json` marker — every hook exits silently without it | step 6 | **no** |
| `.claude/settings.json` hooks — session-start injection, per-turn reminder | step 6 | **no** |
| `CLAUDE.md` carrying `using-t4` as a standing default | step 3 | **no** |
| `.claude/using-t4.snapshot.md` | step 6 | **no** |

The wiring that would have loaded `using-t4` **is the thing being written**, so it cannot have fired yet. The bootstrap session is, by definition, the only session in a T4 repo's life where none of them exist — **the one session that most needs the standard is the one guaranteed to run without it.**

**The step and the session-start hook cover different sessions; they are not duplicates.** The hook covers every session after step 6 lands. This step covers the one before it. Written down because a maintainer who reads them as duplicates deletes this step, and **the deletion is invisible: a bootstrap that skipped the disciplines produces byte-identical files to one that followed them.** Same class as step 11's argument, one level up.

**`ask-xeno` does not close the gap.** It names `using-t4` as the destination, but nothing checks that the agent arrived and nothing fails when it does not — which is exactly how `#244` happened: `/ask-xeno` was invoked at the top of the session, `using-t4` was never entered, and several thousand words went to the developer with `t4-bro` never loaded.

**Two, not three.** `using-t4`'s own session-start protocol carries `karpathy-guidelines` and `t4-agent-memory`, so invoking it reaches them; do not write a separate instruction for either.

**Audited: which other skills run before the wiring exists?** Two entry points are reachable in an unwired repo — `ask-xeno` and this skill — and only this one has a procedure to open. `ask-xeno` is a four-row routing table that also serves non-T4 work, so a "load the T4 disciplines" step there would fire on repos that are not T4 repos. Every other `t4-*` skill is reached either through this procedure (`t4-agent-memory` at step 4, the tracker skills at step 5) or after step 6 has landed the wiring, so neither is exposed to this gap.

### 2. Resolve every tool you depend on — "not on PATH" is not "not installed"

**Before any step that shells out, check `command -v <tool>`. If it comes back empty, resolve the absolute path before concluding the tool is absent** — Windows: `where <tool>` from cmd (git-bash has no `where`); POSIX: `which <tool>`; then the known install locations. Use the resolved **absolute path**, quoted, for the rest of the run.

**The two states look identical from a failed `command -v` and need opposite responses.** Measured on the developer's machine, in this repo:

| tool | `command -v` | actually installed at |
|---|---|---|
| `gh` | **fails** | `C:\Program Files\GitHub CLI\gh.exe` |
| `bun` | **fails** | `%USERPROFILE%\.bun\bin\bun.exe` |
| `git`, `node`, `npx` | resolve | on PATH |

Both of the ones that fail are tools this skill depends on — `gh` in steps 5 and 7, `bun` in the package-manager rule. An agent that reads `command not found` as "not installed here" skips the step, and **steps 1–5 each leave a visible file behind, so a bootstrap that could not create a single label looks exactly like one that did** — the argument step 11 makes for saying the hooks result out loud, applied to the inputs.

**This is not a new pattern; the repo already ships it.** `run-hook.cmd` searches two Git-for-Windows locations for `bash` before falling back to PATH, for exactly this reason. Generalise that rather than re-deriving it per tool.

**And it has already gone wrong on the record.** PRD `#129`'s problem statement is an agent writing *"this tool has never been installed or run"* into a research document — the tool was installed, under `~/.bun/bin/`, simply absent from PATH, and had never been checked. Same directory as `bun` above.

**Only when it resolves nowhere is it missing.** Then name the step you are leaving undone and why; do not let a PATH lookup decide it silently. Do not edit the developer's environment either — resolving the path is the bootstrap's job for the length of the run, not a change to their machine.

**This instruction is safe to give only since `#84`.** Until that fix an executable invoked by absolute path escaped the `PreToolUse` gate entirely, so falling back to `"C:\Program Files\GitHub CLI\gh.exe" pr create` would have skipped the PR-needs-an-issue rule with no signal that anything had been skipped. The gate now reduces an executable to its basename before matching, so the quoted absolute path meets exactly the same rules as a bare `gh`. In a repo whose gate predates `#84`, the fallback is still correct and the gate is still blind to it — check before relying on it.

### 3. Check the companion ecosystems, and let the developer decide

**This bootstrap depends on them and never checked.** Step 5 *invokes* `/setup-matt-pocock-skills` outright, and the `CLAUDE.md` wiring written in step 3 routes work to superpowers and 9arm — so on a machine without them, step 5 fails the way a missing `gh` does and the tracker conventions never land, while the docs that surround them do.

**Check the session's available-skills list for one entry per ecosystem** — the skills are what the wiring actually reaches, so their presence is the check that matters:

| Ecosystem | Present if you can see | What the bootstrap uses it for |
|---|---|---|
| **matt pocock** | `setup-matt-pocock-skills`, `grilling`, `to-prd`, `to-issues` | step 5 — the tracker choice and the five canonical triage roles |
| **superpowers** | `superpowers:using-superpowers` | the general process discipline `using-t4` routes to |
| **9arm** | `debug-mantra`, `scrutinize`, `post-mortem`, `qwen-agent` | the debugging and adversarial-review gates the workflow names |

**Anything missing: ask the user whether to install it — one at a time, recommended answer first, exactly as step 2 asks every other question.** Say what each one buys and what stays undone without it. **Do not install it yourself:** putting software on the developer's machine is outward-facing and hard to undo, and nothing else in this skill touches anything outside the repo.

**Use the commands `using-t4` records; do not invent one.**

- **9arm** — `npx skills add thananon/9arm-skills`. Run it from **outside** the `xeno-skills` clone: pointed at that library it rewrites the source tree it is reading.
- **matt pocock** — `/setup-matt-pocock-skills`, which installs *and* configures the tracker/label/domain layout, so it replaces step 5's invocation rather than preceding it.
- **superpowers** — **no install command is recorded anywhere in this family.** Ask the developer how they install it. A plausible-looking guess is worse than the question: it fails on their machine with this skill's name on it.

**Record the answer in `CLAUDE.md` either way**, the way the `clink-masteragent` question in step 3 is recorded — so a later reader can tell a declined ecosystem from one nobody asked about. A skipped install that was *chosen* is fine; a silent one is the failure this section exists to close.

## Bootstrap procedure

1. **Read the target repo first.** `git remote -v` (get `<ORG>/<REPO>`), the existing `CLAUDE.md`/`AGENTS.md`, `package.json` (package manager, pinned framework versions), any `docs/` present. Never overwrite a governed doc — reconcile.
2. **Pick a tier** with the user; memory layer is in from the Seed tier. **Ask the way `setup-matt-pocock-skills` asks** — the discipline is borrowed deliberately, because a wall of choices gets skimmed and answered wrongly:

   - **One section, one answer, then the next.** Never present every decision at once.
   - **Lead each section with the recommended answer** so it can be accepted in a word. Add an explainer only where the choice genuinely branches.
   - **Skip a section entirely when exploration already settled it.** An absent capability is not a question — do not raise it.
   - **Show a draft and let the user edit before you write.** Anything written before that is a fait accompli, not a decision.
   - **File selection is a rule, not a judgement:** edit `CLAUDE.md` if it exists, else `AGENTS.md`; **never create one when the other exists**; and update an existing block **in place** rather than appending a second copy of it.
3. **Write the `CLAUDE.md` wiring** — engineering north-star, repo layout, commands, the **session-start read protocol** (point it at `docs/OPEN-WORK-LEDGER.md` + the memory vault `Home.md` — see `t4-agent-memory`), the dev-notification protocol, the bilingual writing-conventions block, and pointers to `docs/agents/*`. Two parts of this wiring are not free-form:

   **`using-t4` goes in as a standing default, not as a pointer.** Write it in those words, requiring a re-route **at every phase boundary** and naming them (after writing code → `simplify`; before merge → `code-review` + `scrutinize`; touched auth/secrets → `security-review`) and the sentence that forecloses the read-once reading: **a check at task start does not discharge a later trigger**. A "pointer to the entry map" is read once at session start and never returned to, which is the one behaviour the map forbids of itself — and a repo bootstrapped with the pointer wording ran that way for months before anyone noticed, because nothing fails when it happens.

   **`clink-subagents` goes in as the delegation default, with the two rules that do not relax.** In an agent-primary repo the orchestrator's context window is the scarce resource — the clink back-ends bill against flat subscriptions and the master does not — so delegation is the default rather than the optimisation. Write both guardrails, because they are what stop that default becoming a liability: **verify everything a subagent returns** (a report is a hypothesis until checked; a worker in this family's history claimed a merged PR that did not exist), and **never delegate the final verification** or a security-boundary change. **Skip this section entirely if `clink` is not configured.**

   **`clink-masteragent`: ask the user, do not decide.** **Skip this section entirely if `clink` is not configured** — an unavailable capability is not a question. Otherwise ask whether it is wired as a delegation default, and offer the two shapes that differ materially — *invoke before any `clink` call* (cheap; nothing loaded on sessions that never delegate) or *load at session start alongside `using-t4`* (strongest, but ~19 KB every session against the 9 KB ceiling `using-t4` is held to). **Record the answer in `CLAUDE.md` either way**, so a later reader can tell a decision from an omission. If the question goes unanswered the default is **not wired**, and that is written down rather than left implied. Do not apply this reasoning to `using-t4` above: that one is not a question.
4. **Install the memory layer** from `t4-agent-memory` (ledger, ship log, vault `Home.md` + note format). This is what makes the repo agent-durable.
5. **Install the workflow layer.** Three of these files are not T4's to author: `using-t4` records that the tracker / label / domain-doc conventions are **reused** from the matt pocock ecosystem, and the family's rule is to hand the technique to the ecosystem skill rather than keep a second copy of it.

   **Invoke `/setup-matt-pocock-skills`** for **`docs/agents/{issue-tracker,triage-labels}.md` only**. It owns the tracker choice (GitHub / GitLab / local markdown) and the five canonical triage roles — those five names are pocock's, and T4 uses them unchanged.

   **`domain.md` is a name collision, not a shared file — do not hand it off.** pocock's `domain.md` is *consumer rules* ("how the skills should read `CONTEXT.md` and the ADRs"); T4's `docs/agents/domain.md` is the **domain glossary** ("what the words mean here"). Same path, different document. Letting that skill write it overwrites the glossary with a file about reading habits. If you want pocock's consumer rules as well, take them at a different path and say which is which.

   Then apply the **T4 delta** on top — the part pocock does not carry, and the only part this skill should be maintaining:

   - **Type / Component / Severity** groups, and the rule that a `security` issue must be `critical` or `Major`. pocock stops at the five triage roles.
   - **The bilingual governance-doc convention** (`<!-- lang:en/th -->`, full mirror) — see `references/governance-docs.md`.
   - **`docs/agents/workflow.md`** from `t4-dev-workflow` — no pocock equivalent; entirely T4's. Replace `<ORG>/<REPO>` and the E2E/verify command.

   **Then create the labels, with `gh label create`, and report which were created, which already existed, and which the vocabulary names but you skipped.** Neither skill did this before: pocock's `triage-labels.md` is a mapping table that assumes the labels exist, and T4's told the agent to create them lazily and proceed silently if the vocabulary was thin — which combine into never creating them and never saying so. Measured 2026-08-04 on a repo that had been bootstrapped: **8 of 19 documented labels existed**, `needs-triage` among the missing. A documented vocabulary with no labels behind it is the failure this step now forecloses.
6. **Install the hooks layer** from `references/hooks-layer.md` — copy the marker (`.claude/t4.json`), the `.claude/hooks/` scripts + `run-hook.cmd`, merge the hook entries into `.claude/settings.json`, and write `using-t4.snapshot.md`. This keeps a session on the rails: session-start injects `using-t4`, a per-turn reminder re-anchors it, and a `PreToolUse` gate blocks a PR with no issue and dangerous git. **Arm the local ship gate** by setting `.claude/t4.json` `"verify"` to the repo's *fast* command (lint + typecheck + unit + build). Tell the user what the gate will block.
7. **Install the CI/CD layer** from `references/ci-cd-layer.md` — the workflows in `references/ci/` into `.github/workflows/`, then make `lint`/`typecheck`/`test`/`build` **required checks** on `main` and disallow direct pushes. Do this in the same pass as step 6: a repo with the local gate and no CI has the *appearance* of enforcement with none of the guarantee. Where a ruleset isn't available, set `.claude/t4.json` `"requireGreenCI": true` as the (weaker) fallback. Add `t4-deploy.yml` only if the repo deploys.

   **If CI cannot run at all — a locked billing account, an exhausted quota, Actions disabled — that fallback is the wrong one and makes things worse:** `gh pr checks` reports non-zero for *no checks* exactly as it does for *failing*, so `requireGreenCI` then denies every merge forever. Turn it off and follow **"When CI cannot run at all"** in `references/ci-cd-layer.md`, which lists what to do instead to keep the codebase quality the missing tier was carrying.
8. **Install the guards layer** from `references/guards-layer.md` — copy `references/guards/` into `<repo>/.githooks/`, tell the user to run `git config core.hooksPath .githooks`, and wire the same three scripts into the CI gate. This is the tier that binds Codex/Gemini/humans; the Claude hooks in step 6 do not.
9. **Install the records layer** from `t4-engineering-records` (`docs/adr/README.md`; the templates the tier calls for).
10. **Write the domain/product docs** from `references/governance-docs.md` at the chosen tier.
11. **Verify the hooks layer is actually installed** — **list all three and report which are missing**: `.claude/hooks/` (the scripts + `run-hook.cmd`), `.claude/t4.json` (the marker every hook exits silently without), and the `hooks` key inside `.claude/settings.json`. **Say the result out loud even when it passes.** Steps 1–5 each leave a visible file behind, so a skipped step 6 looks identical to a successful one — **a repo with the docs and no hooks looks bootstrapped**, and that is how `pal-mcp-server` ran with the PR-without-an-issue gate, the dangerous-git denial and the pre-merge `verify` all absent while its own `CLAUDE.md` described them as enforced. An agent that has read `t4-dev-workflow` *plans around* a gate that is not there.
12. **Verify placeholders are cleared** — grep the new files for `<PLACEHOLDER>` / a stale `<ORG>/<REPO>` and any residual sibling-project domain words (e.g. manga/cache/MIT). A leftover is a defect.
13. **Reconcile, don't duplicate** — upgrade any narrower existing rule to the team standard; don't leave two conflicting statements.

## Retrofitting a repo that already has the docs

The common case is not a fresh repo — it is one bootstrapped before a layer existed, or one where a step was skipped and nobody looked. **Run step 11 first:** it reports which layers are missing, rather than which you remember installing.

Then run **steps 6 to 8 in order and nothing else** — hooks, CI, guards. Those are the enforcement tiers, and they are the ones that go missing, because they are the only steps whose absence leaves no file behind to notice.

**Do not re-run steps 1–5 on a repo that already has the docs.** That overwrites governance a team has since edited; step 13's reconcile rule exists precisely to avoid leaving a second, conflicting copy. A retrofit ends the way an install does — by reporting what is now present and what you deliberately left.

## Reference files

- **`references/governance-docs.md`** — the domain/product/index layer this skill owns: taxonomy + status system, and skeletons for `CONTEXT.md`, `UBIQUITOUS_LANGUAGE.md`, `PRODUCT.md`, `docs/agents/domain.md`, and the reports/research/plans README indexes. (ADR, memory, and workflow skeletons live in the sibling skills.)
- **`references/se-deliverables.md`** — the optional 7-phase Software-Engineering deliverable set + UML outline (formal delivery only).
- **`references/hooks-layer.md`** + **`references/hooks/`** — the workflow-hooks layer (path A): the `.claude/t4.json` marker, the `.claude/hooks/` scripts + `run-hook.cmd`, and the `settings.json` hook entries. Session-start / prompt-reminder / PreToolUse-gate keep a session on the rails. The scripts are byte-identical to the `xeno-skills` plugin's `hooks/` (a repo test enforces the sync).
- **`references/ci-cd-layer.md`** + **`references/ci/`** — the server-side gate: `t4-verify.yml` (lint · typecheck · test · build as separate required checks), `t4-e2e.yml` (the slow suite, kept out of the local `verify`), `t4-deploy.yml` (CD gated on a green verify), plus the ruleset commands that make them required and block direct pushes to `main`. This is the layer that also covers a human merging on the web.
- **`references/guards-layer.md`** + **`references/guards/`** — the agent-agnostic tier: a git `pre-push` hook running `check-issue-ref`, `check-tree-budget` and `check-gate-ledger` (a push must state every judgment gate as `ran` / `not-run` / `n-a` — silence about one is what it forbids). The Claude `PreToolUse` gate only sees tool calls Claude makes (Bash, and the GitHub MCP tools since #83); these bind every agent and human on the clone, and the same scripts go into CI.

## The non-negotiable team rules

These are the rules the skeletons carry; know them so you don't dilute them.

- **Agent memory is first-class.** The ledger + ship log + vault exist so a fresh agent recovers state. Install them early; keep them retrieval-first (see `t4-agent-memory`).
- **Bilingual (TH + EN) is GitHub-tracker-only, Thai mirrors English exactly** — issue bodies, PRD bodies, PR descriptions. Not chat/reports. Identifiers stay English. (See `t4-dev-workflow`.)
- **PRD → issues → PR.** Never a PR without a referenced issue. Issues are the source of truth.
- **TDD is mandatory** for features and bugfixes.
- **Non-standard framework version → read the vendored docs first** (e.g. `node_modules/<pkg>/dist/docs/`), not prior knowledge.
- **Verify every frontend change end-to-end** — unit tests can't see real layout/hydration; run the repo's E2E/verify pass and add a case per new page/interactive UI.
- **Bun** is the default package manager/runtime for a new T4 repo — commit `bun.lock`, use `bunx`; where a workspace already uses npm/yarn, honor its lockfile rather than forcing Bun.
- **Close issues with a stated reason**; **domain glossary is load-bearing**; **proceed silently if a governance file is absent** (details in the sibling skills + `references/governance-docs.md`).

## Common mistakes

- **Deferring the memory layer.** In an agent-primary repo that's the one thing you can't defer — without it, the next session starts blind.
- **Carrying sibling-project domain content across.** Strip every manga/cache/MIT/wallet word. Grep before you commit.
- **Duplicating a sibling skill's skeleton here.** Bootstrap installs those files but the skeletons + discipline live in `t4-agent-memory` / `t4-engineering-records` / `t4-dev-workflow`. Reference, don't copy.
- **Weakening the bilingual rule** to match an older repo's narrower version — upgrade to the team standard.
- **Leaving `<PLACEHOLDER>` tokens or a stale `<ORG>/<REPO>`.** Step 11 exists for this.
- **Installing the hooks layer and skipping the CI layer.** The local gate only binds commands the agent runs; without required checks the repo *looks* enforced and isn't.
