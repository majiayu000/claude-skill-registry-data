---
name: spec
description: >-
  Turn a fuzzy goal or existing Task into one self-contained, execution-ready
  Task plan. Scope the surface, resolve standards, research load-bearing behaviour,
  remove ambiguity, and post the versioned execution plan whose highest version is the plan.
argument-hint: "[a goal to scope, or an existing task key (<task>) to deepen]"
disable-model-invocation: true
effort: max
---

Turn this goal or work item into a **Task** (or **Bug** for a defect fix) containing everything a fresh `/sy:ship` session needs to land one coherent PR. Code work is read-only; tracker writes use the `tracker` skill (`/sy:tracker`). End at the approved plan — or, when research invalidates the premise, at a shelve-with-evidence closure (§6); do not implement.

Plan against fresh `origin/main` unless the user names another immutable base.

Before anything else — before the surface scan below spends any research — run the tracker preflight (`${CLAUDE_PLUGIN_ROOT}/skills/shared/references/preflight.md`). A failure stops here with its single `## Action needed` block, not partway through the plan.

$ARGUMENTS

## Scope before routing

- small cohesive module/doc/diff ⇒ read directly;
- large repetitive surface ⇒ `sy:sweep` breadth brief;
- one load-bearing end-to-end behaviour ⇒ `sy:trace`, one path per agent, at most the resolved `limits.max_depth_agents` cap in flight — resolve per `${CLAUDE_PLUGIN_ROOT}/skills/shared/references/config-values.md`.

Agent output is a lead. Verify decisive spans and own the plan. Seed every agent prompt with known anchors — paths, symbols, entry points, keys — and name ground already covered; agents must not rediscover what the caller knows. Resolve standards early (in a delegate, per step 3) so the plan reflects authoritative repository policy and risk lenses.

Ask one question at a time, via `AskUserQuestion`, only when research cannot settle a decision that changes scope, design, or acceptance — see `${CLAUDE_PLUGIN_ROOT}/skills/shared/references/user-interaction.md`.

## 1. Surface scan and interview

- Fetch and inspect the intended base.
- Run the premise + prior-work check before deep archaeology: confirm the goal's premise still holds on the intended base, and search for existing, shipped, duplicate, or sibling work — tracker `find-issues` over summary/label plus a code/PR search. A premise already delivered, invalidated, or owned by an open sibling stops here with that evidence (correct or close the item via the `tracker` skill) rather than producing a plan for work that should not ship.
- Map entry points directly or through `sy:sweep` according to size.
- Establish goal, definition of done, boundaries, constraints, and priorities.
- Suggest, as a single optional aside (not a gate), that the user run `/rename spec: <goal-slug>` or `/rename spec <task> <slug>` once nameable.

## 2. Create or load the Task

### New goal

Draft Summary, Context/constraints, and Out of scope. Write the body as short natural prose by default — a few sentences someone reads once and understands, not a nested outline of headings; when supporting detail is genuinely load-bearing and would bloat the body, it goes in a companion comment instead, the same body/comment split `/sy:pr` already makes between a PR description and its evidence comment. Run `/sy:tighten` over the drafted body before it is created — destination an issue body — and over that companion comment's human half the same way. Use Bug for a defect fix, Task otherwise. Every Task/Bug must be parented to an Epic. Confirm parent and draft before creation via the `tracker` skill.

### Existing Task

Read its body/comments directly and preserve settled decisions. Delegate only large parent-Epic or PR tails to `sy:sweep`. Edit the body only when research changes framing, and then as a deliberate full rewrite authored from scratch — never a merge around body content read back from the tracker, and it does not carry over rich text a description read cannot represent (see the selected adapter's `ADAPTER.md` on what that read does not guarantee). That governs research-phase edits; §7 Step 2 never writes the Task body at all. Ensure the parent Epic is `in-progress` when active work begins; the Task stays in `backlog` until its plan is approved (then `ready`, per step 7).

## 3. Resolve standards and deep research

- Resolve standards in the `repo-standards` delegate (running `/sy:standards resolve <scope>` at the model `agent_model {"name": "repo-standards"}` reports) that returns only the compact contract — authority, task-relevant constraints, primitives, risk lenses; the raw rule and doc reads stay out of the spec context, where standards loaded early would be re-paid on every later turn.
- Deep research starts only after the §1 premise + prior-work check has survived; evidence against the premise found later still stops the spec (see §6, shelving with evidence) rather than merely reshaping it.
- Read durable cross-session memory early — `memory_list` (or `memory_search` on the tools/surfaces the task touches) per `${CLAUDE_PLUGIN_ROOT}/skills/shared/references/memory.md`; a lesson that bears on the task enters the plan as a known anchor, and a lesson this task's own research directly contradicts is refuted immediately (`memory_refute`, same reference) rather than carried forward or silently dropped.
- Trace every load-bearing claim to code, current primary docs, or real data.
- Use `sy:sweep` for breadth and `sy:trace` for one end-to-end path; verify decisive spans directly.
- Verifying a decisive span means confirming one already-cited pointer with a read or a single targeted command; when that check — or a delegate's own findings — comes back inconclusive and continuing would move past what's already been pointed at (a live external system, a scratch probe script, or a second follow-up command still chasing the same question), stop and dispatch a fresh, foreground `sy:trace` for it instead of continuing turn-by-turn; the dispatch draws on the same `limits.max_depth_agents` budget set above, not a separate one.
- Pull representative data when shape/frequency matters.
- Actively look for breaking cases and evidence against the preferred approach.
- Before the plan reaches sign-off (§7), pressure-test its core design decision with `sy:debate` — unconditionally, not only when this search happened to surface a two-sided fork: `${CLAUDE_PLUGIN_ROOT}/skills/shared/references/debate.md`. When research does surface a genuine fork, debate it here, as soon as the choice is stated in one sentence, rather than carrying it unresolved into the plan.
- Then, once the plan is fully drafted and before it is presented (§7), put the plan itself through the `sy:spec-gate` review: resolve its model with `agent_model {"name": "spec-gate"}` and pass the reported model as the `Agent` invocation's model override, per `${CLAUDE_PLUGIN_ROOT}/skills/shared/references/model-dispatch.md`, seeding the prompt with both §7 parts as drafted, the resolved standards contract, the activated risk lenses, and the plan's base commit and repo to read against — name the inspected base explicitly (`PLAN_BASE_SHA` and the repo path) and confirm the working tree is at that commit, since the reviewer checks the plan's anchors against a checkout it cannot otherwise identify. Triage every finding before presenting anything: a plan defect is fixed in the draft, a real risk you cannot design out becomes a "risks/edge cases" entry, and a finding whose fix is "take the rejected alternative" is dropped — the debate above settled that, with the user's steer. Nothing reaches sign-off undispositioned. The checklist and the re-dispatch rule live in `${CLAUDE_PLUGIN_ROOT}/skills/shared/references/spec-gate.md`; cite them, do not restate them.

Record standards compactly, for example:

```text
Standards authority
- the skill `skills.standards` names

Task-specific constraints / risk lenses
- public response schema remains backward compatible
- migration needs rollback evidence
```

Convert every activated risk lens into a **verification obligation** — a claim plus named evidence `/sy:ship` must produce and `sy:gate` will verify:

```text
Verification obligations
- lens: concurrency; claim: duplicate delivery is idempotent;
  evidence: deterministic duplicate-delivery test, concurrent-update test
- lens: migration; claim: old and new versions coexist safely;
  evidence: expand/contract sequence, compatibility test
```

An obligation with no realistic evidence is a plan risk to surface, not a silent drop.

When the task generates or reviews images (figures, screenshots, plots, marketing visuals), add the standing image-inspection invariant to the plan's design invariants and a verification obligation whose named evidence is a `sy:img-inspector` text verdict: visual inspection is delegated to a short-lived inspector and never `Read` into a long-running context. See `${CLAUDE_PLUGIN_ROOT}/skills/shared/references/image-inspection.md`.

## 4. Resolve ambiguity as it surfaces

Ask immediately, via `AskUserQuestion`, when research reaches a real owner decision that changes the plan. Record answers durably so `/sy:ship` does not re-ask.

## 5. Too big for one PR? Return to `/sy:plan`

Do not split an oversized Task ad hoc.

For an existing `/sy:plan` leaf, post a `# SEAMS` comment — `human` is why this has to be cut and along what line, `agent_detail` is the pieces, interfaces, and dependencies — then stop with `/sy:plan <epic>`. `/sy:plan` performs the tracker's canonical decomposition (see the `tracker` skill).

For a standalone objective, confirm via `AskUserQuestion` before promoting it to an Epic, then post the seams report and stop with `/sy:plan <epic>`.

## 6. Premise gone? Shelve: close with evidence, no plan

Not every spec ends in a plan. When research shows the premise is already delivered, invalidated, or superseded — whether at the §1 prior-work check or from evidence surfacing later — the blessed terminal state is a shelve: the Task closes with evidence instead of acquiring a plan for work that should not ship. This is distinct from §5, where a sound premise is merely too big for one PR.

1. Present the evidence as a status update, then close the turn with a single `AskUserQuestion` (shelve as described / keep researching / other), naming the mutations the go-ahead covers: post the evidence comment and set the Task's terminal status.
2. Post a durable evidence comment on the Task: `human` is what was found and why no plan should exist, `agent_detail` is the decisive pointers (commits, PRs, work items, spans).
3. Set an **existing** status via the `tracker` skill — `done` when the premise was already delivered or the item should close, `backlog` when it is merely premature — never a new status; the evidence comment is what distinguishes this closure from delivery (decomposed/superseded/invalidated closure is not delivery).
4. Capture the session per §8 as on every run.

## 7. Capture the plan as the highest version

Nothing here starts until both mandatory §3 passes have run — the `sy:debate` pass over the core decision and the `sy:spec-gate` review of the drafted plan — with every spec-gate finding already dispositioned.

The plan itself has two clearly labeled parts, so a human reviewer and a fresh `/sy:ship` session each get only what they need without wading through the other's. Both parts are drafted under `${CLAUDE_PLUGIN_ROOT}/skills/shared/references/context-economy.md`; read it before writing either. The sign-off half is additionally written to the reader `text.reader` names — resolve it and apply `${CLAUDE_PLUGIN_ROOT}/skills/tighten/SKILL.md` § The reader. The `/sy:ship` half is agent-facing, and that setting never reaches it.

**For your sign-off** (rationale and judgment calls):

- approach and why;
- strongest rejected alternative and why — the adversary's strongest objection from the §3 debate plus the user's steer, not a restatement invented after the fact;
- risks/edge cases;
- unverified assumptions;
- out of scope — what this plan deliberately excludes, under the fold-in-versus-follow-up policy in `${CLAUDE_PLUGIN_ROOT}/skills/shared/references/scope-discipline.md`, which the exclusion is read against rather than restated from.

**For `/sy:ship`** (mechanical and self-contained):

- ordered concrete changes with file anchors/key signatures;
- existing primitives to reuse;
- standards authority and task-specific constraints/risk lenses;
- verification obligations (lens → claim → named evidence);
- design invariants — the deliberately small load-bearing list `sy:gate` must protect;
- `docs requiring updates: <list, or 'none'>`;
- `visual-debug obligations: <list, or 'none'>`;
- `pre-gate checkpoint: <channel: 'draft PR' or 'running preview'>, or 'none'` — whether `/sy:ship`'s parent pauses for a human look at the draft PR (or a running local preview) before dispatching GATE, framed as "is this the right thing", never as a correctness review; `/sy:ship` never launches a preview itself, only points at the channel declared here. Default when absent is `none`: an unattended or overnight ship run that never declares one sees no change at all;
- `reviewer orientation: <one sentence>` — optional, and the only optional field here: one sentence telling the repository's own reviewer what this ticket is really about, such as that it is a performance change rather than a feature. It reaches `repo-review` appended to that agent's instructions as orientation only, and can never override its return contract, its never-fixes/promotes/dispositions rule, or its five `blocked` returns. Omit the field and nothing is appended;
- tests and acceptance criteria;
- plan base: `PLAN_BASE_SHA` of the inspected base.

Backtick every identifier, path and URL in the `/sy:ship` half that contains a `_` or a `*`: `/sy:ship` reads this half back off the tracker with `plan_file`, and a rich-text tracker escapes un-backticked Markdown punctuation on the way through, so a bare `some_name` reaches the builder as `some\_name`.

The docs-sync, visual-debug, and pre-gate-checkpoint fields are all required and all legitimately answerable with `none`; what counts for each, and what an honest answer looks like, is axes 4–6 of `${CLAUDE_PLUGIN_ROOT}/skills/shared/references/spec-gate.md` — read it there rather than from a copy here. An omitted field is what `sy:spec-gate` flags; a `none` on work that plainly touches a doc or a visual is what it flags harder; a `none` on the pre-gate checkpoint is the plan author's call, and is never second-guessed that way.

`reviewer orientation` is the one field collected by asking, and only when there is a reviewer to orient: resolve `skills.reviewer` (per `${CLAUDE_PLUGIN_ROOT}/skills/shared/references/config-values.md`) while drafting this half and, when it is non-null, close that drafting step with one `AskUserQuestion` — the sentence you would write / a different sentence / none — per `${CLAUDE_PLUGIN_ROOT}/skills/shared/references/user-interaction.md`. When it resolves `null` the question is never asked and the field is never written, so a repository naming no reviewer skill sees no extra question and no extra field. Ask it here, while drafting, never folded into Step 1's sign-off call below, which stays a single question about the plan itself.

End the `/sy:ship` part with `/sy:ship <task>` and a one-line ship profile that names every phase's model explicitly: `START <model> / BUILD <model> / GATE <model> / effort <tier> / process <full|light>`, such as `START opus / BUILD opus / GATE frontier / effort high / process full`. Naming the phases individually leaves `/sy:ship` nothing to infer — a single-word tier forced it to guess which phases the word applied to, and `/sy:ship` passes each stated model straight through as that phase's model override.

Model tier is a quality floor, not a cost lever. Each phase's floor is declared in `config/floors.json` — `ship-start` cheap, `ship-build` standard, `sy:gate` frontier (frontier is absolute and cost-scaling-exempt, and the `GATE` model names the reviewer's tier rather than the lightweight GATE controller's) — and a plan may state a higher model for a phase when its own judgment calls for it. A stated model below a phase's floor is clamped up to the floor, never honored downward, by the resolver rather than by anyone remembering to. See `${CLAUDE_PLUGIN_ROOT}/skills/shared/references/model-dispatch.md`. Tune cost through **effort**: request lower effort only with evidence the work is mechanical end to end, and never lower review effort. Process tier `light` (no transcript attachment at handoff) is allowed only when no risk lenses are activated and the plan's declared file set is at most the resolved `spec.light_tier_max_files` cap (resolve per `${CLAUDE_PLUGIN_ROOT}/skills/shared/references/config-values.md`); default `full`.

The ship profile never lowers review or build: `sy:gate` remains frontier tier and max effort, BUILD remains at least opus (the profile may raise it, never lower it), and immutable CI/review coverage is identical in both process tiers.

### Step 1 — ask for sign-off on the judgment, not the mechanics

Present a short natural-prose summary: what you are going to do, why this way, the strongest alternative you rejected and why, the risks worth knowing, and what this deliberately excludes. A few paragraphs, read once and understood — no nested outline, no file inventory, no restatement of the `/sy:ship` section. What is being approved is the judgment; the mechanics exist for `/sy:ship`, and pasting them here buries the decision the user is being asked to make. The `/sy:tighten` pass over the sign-off half completes before the summary is presented. Hand the pass the drafted `/sy:ship` half as its companion: both parts exist by now, and without the companion in hand the pass is barred from moving any anchor out of the sign-off half. The text the user reads is therefore the text they approve; hold the pre-pass draft for the duration of this step rather than discarding it.

Send that summary as direct text first, in full — two acts, not one, and the summary is never folded into the question call or replaced by a pointer at it. Only then close the turn with a single `AskUserQuestion` call — approve as-is / request changes / see the fuller version / other — per `${CLAUDE_PLUGIN_ROOT}/skills/shared/references/user-interaction.md`. Name the mutation the approval authorizes: on approval the run will post the full plan as one new comment at the next version and set the Task `ready` — it edits no comment already on the issue, and it does not touch the Task body (a body edit during research, §2, is governed separately by that section, not by this rule). Under auto-mode this sign-off is the consent point for those writes, so it states them rather than implying them. This is the plan's sign-off gate: do not infer approval from a reply that doesn't answer it.

A `request changes` answer revises the draft and returns to this step; re-run `sy:spec-gate` only when that revision is material, per the re-dispatch rule in its reference. One option sends the pre-pass sign-off half in full and returns to this step. It is not a re-run, and it does not count against `spec.max_spec_gate_rounds`. What it expands is that pre-pass draft — never the `/sy:ship` half, which stays a Step 2 reveal.

### Step 2 — after approval, post the full plan

Both labeled parts are revealed here, in full, rather than at Step 1. This step never writes the Task body — not for a pre-existing Task, and not even for one this run just created — so no existing body content is ever a target of this run's write. (A body edit during research, §2, is governed separately by that section, not by this rule.) It edits no comment already on the issue either: an earlier plan version stays posted exactly as it was, and the new version corrects it by naming what it supersedes. That additive form is what the retroactive-honesty invariant in `${CLAUDE_PLUGIN_ROOT}/skills/shared/references/write-integrity.md` takes here — an overruled record is corrected on the record that overrules it, never emptied out.

1. run `/sy:tighten` over the `/sy:ship` half. It runs on **every** plan, unconditionally — never only on one that looks long — and it rewrites that half alone; the sign-off half had its own pass at Step 1, before it was presented. The `/sy:tighten` pass over the `/sy:ship` half completes before any tracker mutation. Its placement here, after sign-off, is deliberate: what Step 1 approved is the post-pass sign-off half, and this pass touches only the `/sy:ship` half, so the rewrite cannot invalidate the approval; and running it last means nothing added late escapes it.

   Splitting the half across comments is not the remedy for a long one, and is not available: a plan lives in exactly one comment (`${CLAUDE_PLUGIN_ROOT}/skills/tracker/CONTRACT.md`). Tightening is the remedy.

2. append the new comment, carrying both labeled parts above in full. `post-comment`'s split is the plan's own split, so pass them as they are: `human` is this heading block plus **For your sign-off**, `agent_detail` is **For `/sy:ship`** — never one hand-composed body:

```text
# Execution Plan v<N>
Supersedes: v<N-1>   # omit for v1
```

3. verify by rereading that this is the highest plan version on the issue and that no other comment claims it.
4. set the Task to `ready` via the `tracker` skill — the plan is approved and it is now shippable.

The bar: a fresh session reading the Task and its highest plan version can implement and open the PR without missing design decisions.

## 8. Capture the session

When `transcript.attach` resolves true, render and attach this session's transcript to the Task (`$KIND=spec`) per `${CLAUDE_PLUGIN_ROOT}/skills/shared/references/transcript-attach.md`.
