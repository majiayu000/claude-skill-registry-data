---
name: agent-stocktake
description: "Audit the ~/.claude/agents definitions and give each a verdict."
license: MIT
metadata:
  author: shimo4228
  version: "1.0"
user-invocable: true
origin: shimo4228
disable-model-invocation: true
---

# agent-stocktake — Agent Definition Quality Audit

Evaluate every agent definition under `~/.claude/agents/*.md` and assign each a verdict:
`Keep / Improve / Update / Merge / Demote to skill / Dissolve / Retire`. The audit unit
is the file, but the cost unit is **split across two layers** — that split is the reason
this skill exists as a third sibling next to skill-stocktake and rules-stocktake.

> Design note — the hybrid cost model. A skill's cost is trigger pollution (probabilistic
> firing degrades selection); a rule's cost is residency (always loaded). An agent has
> **both at once**: its `description` is injected into every session via the
> "Available agent types" listing (**residency**, like a rule), while its body loads only
> when the agent is invoked (**invocation**, like a skill — but triggered by Claude's
> delegation judgment, not by description matching against the user's words). So the
> description is audited on residency density and the body on invocation quality, with
> different questions for each layer.

> Design note 2 — edits are applied in-session. Same reasoning as rules-stocktake: no
> improvement engine exists for agent definitions, and the corpus is small enough to
> read in one context — delegation would be overengineering. The handoff exception is Demote to skill
> (creating a skill is skill-creator's job).

## Modes (`$ARGUMENTS`)

| Argument | Behavior |
|----------|----------|
| none / `full` | Read and evaluate every agent definition (default) |
| `changed` | Re-evaluate only files whose mtime is newer than `results.json`'s `evaluated_at`; carry the rest forward from the ledger |

`changed` detects changes inline (no script):
> Paths below start at `${CLAUDE_SKILL_DIR}`, the directory holding this SKILL.md; an agent that does not substitute the variable reads it as that directory.

```bash
find ~/.claude/agents -name "*.md" -newermt "$(jq -r .evaluated_at "${CLAUDE_SKILL_DIR}/results.json")"
```

As in rules-stocktake, the Phase 1 integrity checks **always run over the full set** —
retiring a skill or hook silently breaks a reference inside an unmodified agent body, and
mtime cannot see that. Any agent whose reference check (Step 3 below) newly fails joins
the re-evaluation set. The script has no `changed` mode either, for a *different* reason:
the near-duplicate pairs and the residency total are set properties, so a partial corpus
would give wrong numbers rather than fewer ones.

## Phase 1 — Evidence, inventory, usage

### Step 1 — Run the evidence script (do not count by hand)

```bash
uv run --frozen --project "${CLAUDE_SKILL_DIR}" \
       --directory "${CLAUDE_SKILL_DIR}" \
       python scripts/agent_evidence.py --root ~/.claude
```

Evidence mode: JSON on stdout, exit 0 however many findings (exit 2 only when the
corpus is unreadable). It measures and enumerates; it never assigns a verdict.

**Transcribe the JSON into findings — never re-measure by eye.** What it gives you:

| JSON field | Replaces |
|---|---|
| `desc_words` / `body_lines` / `total_desc_words` | the `wc -w` / `wc -l` pass |
| `tools.items[].status` + `registry.known_tools` | `builtin` / `unverified` / `mcp`. **`unverified` means "not in the script's dated list", not "does not exist"** — you hold the live tool registry and the script does not, so confirm an `unverified` against your own tool list before calling it Update evidence. `registry.known_tools.as_of` is that list's date (`null` when `--known-tools` replaced it) |
| `tools.items[].server_in_config` + `registry.mcp_config_files` | **Not a verdict.** It says only whether the server appears in the local config files listed — servers supplied by a connector never appear there at all, so a `false` is not "retired". `null` means no config source parsed. Check the `status` of each source before using this at all; a `false` beside a non-`ok` source is not evidence |
| `unreadable` | files the scan could not open, with a reason. **Non-empty means the scan is incomplete** — name them and fix before stating any total, because a suppression instruction inside an unread file is now certified absent |
| `tools_unparsable` | agents whose `tools:` line did not parse (e.g. YAML flow style). Their `items` is `[]`, which looks identical to an agent with no `tools:` key — i.e. **unrestricted**. It is not; the list was simply not read |
| `description_near_duplicates` | the near-identical-description check; twins split delegation traffic, so each pair feeds the Stage 1 overlap question |
| `suppression_candidates` | line-numbered candidates for the Stage 1 suppression question (the catalog is bilingual because the corpus is) |
| `always_never_candidates` | line-numbered candidates for the over-constraint question, **body only** — a description is a delegation trigger, not an instruction to the agent |

The last two are **candidates, not findings** — read every cited line before writing it up. The catalog is also a **floor, not a
census**: it holds five phrasings drawn from one corpus, so a suppression written
some other way ("skip anything you're unsure about", "avoid findings that would just be noise")
appears in no JSON field. Keep reading for those; an empty list is not a clean bill.

For the measured false-positive ratios and which lines produced them, see
[ADR-0054](https://github.com/shimo4228/claude-harness/blob/main/docs/adr/0054-extract-agent-stocktake-and-learn-eval-mechanical-checks.md)
— they are recorded once, there, so this step does not carry numbers that go stale.

### Step 2 — Read the gates that already own the rest

Three checks stay outside the script because another gate owns them. Read their
output; do not re-implement:

- [ ] Frontmatter parses and carries `name`, `description`, `origin`, `model`, and
  `model` is an alias → `scripts/hooks/harness_lint.py` `lint_agents`, which runs
  in `.claude/verify.sh` and the pre-commit hook. A missing origin is still an
  integrity finding per rules/common/skills.md, feeding Improve.
- [ ] `name` equals the filename stem → the same `lint_agents` (RFC-0014). It admits no judgment and the delegation
  registry keys on it, so it belongs to a gate that stops a commit — not to
  evidence a reader may or may not transcribe. A finding here is a **blocked
  commit**, not a stocktake verdict.
- [ ] Markdown links inside agent bodies resolve → the same script's
  `lint_markdown_links` (its scopes include `agents`).

### Step 3 — Resolve bare-path references (the one check nothing else owns)

`lint_markdown_links` sees only link syntax, and `skill-health`'s `scan_refs.py`
scans the *skills* tree. A path written as prose inside an agent body
(`~/.claude/hooks/foo.sh`, `skills/foo/SKILL.md`) is covered by neither. Grep the
corpus for them and `ls` each one.

### Step 4 — Inventory

Enumerate with Glob: `~/.claude/agents/*.md`. Read every file into one context (the
corpus is small). The residency and body columns come from the Step 1 JSON —
never trust figures written in docs, including this one.

### Step 5 — Usage counts

Evidence input, never a verdict trigger. Read `~/.claude/metrics/agent-usage.jsonl`
inline (the hook `log-agent-usage.sh` appends one `invoke` event per Agent-tool launch,
keyed by `subagent_type`) and count per-agent events over 7 / 30 / 90 days. Aggregate with a throwaway `python3`/`jq` one-liner.

- If the log is **missing or its first event is younger than 90 days**, render usage as
  `—` (unmeasured). **Never render it as 0** — unmeasured and unused are different facts.
- Counts are **lower bounds**: only Agent (Task) tool launches are captured. Workflow
  `agent()` workers, plugin-internal dispatch, and built-in machinery that bypasses the
  tool call do not reach the hook. Never Retire/Dissolve on low usage alone — an agent's
  value can be episodic (e.g. paper reviewers fire only near a deposit).
- Log exists since **2026-07-27**; before that date there is no measurement at all.

State the scan result up front, taking the counts from the Step 1 JSON: `agents_total`
**minus anything in `unreadable`, which must be named**, `total_desc_words` (the per-session residency tax of the listing), integrity failures,
and whether usage is measurable. Carry failures into Stage 1 as pre-computed evidence.

## Phase 2 — Evaluation (fully inline, holistic)

Read every body while seeing the whole set.

**Stage 1 — binary screen (every agent).** Explicit Yes/No per item; surface only the
No answers. The first two questions audit the **description layer** (residency), the
rest the **body layer** (invocation):

- [ ] *Description earns its residency?* — dense, distinct, and selection-enabling in
  the always-loaded listing; states when to delegate AND when not to
- [ ] *Description truthful to the body?* — what it promises is what the body does
  (a drifted description misroutes delegation every session, even if the body is fine)
- [ ] *Body free of suppression instructions?* — start from this agent's
  `suppression_candidates` in the Phase 1 JSON, handled per Step 1.
  What counts: confidence thresholds ("only report findings you are ≥N% sure of",
  "assign each finding a confidence and discard the low ones"), severity floors ("only high-severity"), "be
  conservative" framings. The current-generation guidance is: report everything,
  filter in a separate pass — a suppression instruction is followed literally and
  silently drops findings. A No here is an **Improve-by-inversion** candidate:
  rewrite the instruction in the opposite direction, never just delete the section
  (deleting leaves the suppressive frame; inverting replaces it)
- [ ] *External-origin copy current?* — for an agent whose `origin` is an external repo
  and whose body is a verbatim copy (e.g. a built-in override such as `Explore`), the
  source version named in the body's leading comment matches the installed tool
  (`claude --version`); a mismatch is an Update (diff against the bundle and re-copy).
  The suppression and over-constraint questions are skipped for such copies — the body is the vendor's,
  not ours (ADR-0070)
- [ ] *Body free of previous-generation over-constraint?* — exhaustive step-by-step
  procedures for judgment the current model holds natively, repeated emphasis,
  ALWAYS/NEVER pairs that the surrounding-context judgment should own. Phase 1's
  `always_never_candidates` locates the tokens; deciding whether a hit is a
  directive or merely quotes the words is this question's job
- [ ] *Not absorbed by the substrate?* — does the harness now cover this agent's job
  natively (native review machinery, plan mode, built-in slash commands)? Absorption →
  Dissolve candidate; the claim must name its absorber concretely. Judge with the
  **fresh/rich context axis** ([ADR-0023](https://github.com/shimo4228/claude-harness/blob/main/docs/adr/0023-dissolve-planner-narrow-architect-to-essence-evaluation.md)):
  roles that gain from *fresh* context (review, adversarial verification, essence
  evaluation — decorrelation from the proposer's sunk cost) legitimately live in a
  subagent; roles that gain from *rich* context (planning, generation, implementation —
  user intent, in-conversation constraints) are main-loop work, so for them the main
  loop itself counts as an absorber. Two auxiliary rationales legitimately override
  the rich-context pull (ADR-0024): a **frozen-input render contract** — the caller
  freezes a self-contained packet before invocation, so conversation context is not
  needed by design (prompt-writer) —
  and **bulk context isolation** — the work reads or produces volume that would
  pollute the main context (refactor-cleaner)
- [ ] *Technical references current?* — **unconditionally verify** every artifact the
  body names: `ls` each referenced path, run `--help` / version checks for named
  commands, flags, model names and tool lists. "Verify if it looks stale" is banned
  phrasing — the condition is what dilutes; deterministically checkable claims get
  deterministic checks, every time
- [ ] *Unique within the set?* — no other agent (or skill) owns the same job; a
  documented orchestrator→sub-agent split is NOT overlap

Eight questions and no more — further decomposition degrades holistic judgment
(see References).

**Stage 2 — verdict pressure-test (non-Keep candidates only).** Generate 1–3
agent-specific atomic yes/no questions that try to **refute** the draft verdict, each
answered with one line of evidence (file read, path check, `--help`, WebSearch,
harness-doc check). For **Dissolve** candidates one question is mandatory: *"Can the
absorbing harness feature be named concretely — Yes/No"* — an absorption claim that
cannot name its absorber is refuted. And when a Dissolve is about to be *refuted* by a
capability the substrate counterpart lacks (a tool, a wired sub-agent), one
counter-question is mandatory before accepting the refutation: *"Is the subagent the
right place to use that capability — or does the main loop hold it anyway?"* Capability
existence is necessary but not sufficient; the fresh/rich context axis decides where the
capability belongs (precedent: the planner refutation collapsed because the main loop
holds the full Agent tool, ADR-0023). Keep-bound agents get no dynamic questions.

Evaluation is **holistic judgment, not a numeric rubric** — binary answers are evidence,
never aggregated into a score. Evaluation is **origin-blind** (ECC / shimo4228 /
customized all get the same checklist); a *missing* origin header is itself a finding.

**Aggregate residency cost (set-level):** every description loads into every session,
and the longer the listing, the weaker each entry's selection signal. The Keep bar
rises with total description words — a merely-adequate agent is a Merge/Retire
candidate on dilution grounds alone when the listing is crowded. A judgment input,
never a quota.

| Verdict | Meaning |
|---------|---------|
| Keep | Earns both layers: description dense and truthful, body current and unique |
| Improve | Worth keeping, needs tightening — includes **inversion** of suppression instructions (rewrite direction, don't delete) |
| Update | Referenced technology/tool/model is outdated (verified, with evidence) |
| Merge into [X] | Substantial overlap with another agent; name the target |
| Demote to skill | The value is the instructions, not the separate context/process — move to the skill layer via skill-creator |
| Dissolve | Absorbed by the substrate. Retirement by *success* — delete before the stale body overrides newer defaults; record the why in an ADR |
| Retire | Defect-based removal: low quality, stale, broken beyond repair |

**Mandatory-surface rule**: a No on the absorption question MUST surface the agent as a
Dissolve candidate (final call is the user's) — an absorbed agent still receives
delegation traffic and actively applies its stale body to current work.

## Phase 3 — Summary

Render a table: `Agent | Desc words | Body lines | Usage 90d | Verdict | Reason`
(`Usage 90d` is `—` while unmeasured, per Phase 1). Close with one
line reporting total description words and the delta since the previous audit —
input to the aggregate-residency judgment next run.

## Phase 4 — Consolidation

**Confirm one by one**: walk the non-Keep candidates
sequentially — evidence first, then `[y/n/skip]`. Never batch the approval; one agent,
one decision. `skip` records the verdict unactioned.

- **Improve / Update / Merge**: present the concrete edit → on approval, **apply it
  directly in this session** (Design note 2). Inversion edits show old and new
  direction side by side.
- **Demote to skill**: hand skill creation to `skill-creator`, then delete or reduce
  the agent file per the user's call.
- **Dissolve / Retire**: per file, present (1) the absorption evidence or defect,
  (2) what covers the need instead, (3) removal impact — **skills and rules that name
  this agent** (grep the harness) and the public repo copy. Act only after the user
  confirms. For Dissolve, offer to record the why via `adr-writer`.
- **Update the ledger**: Read `results.json` → merge verdicts → Write back
  (`evaluated_at` = real UTC from `date -u +%Y-%m-%dT%H:%M:%SZ`). In `changed` mode,
  preserve prior verdicts of files not re-evaluated.
- **Public-repo note**: editing or retiring an `origin: shimo4228` agent leaves the
  public repo stale — point the user at their publish step (the author's harness uses `harness-sync`).

## Reason quality (required)

Every `reason` must be self-contained and decision-enabling. For non-Keep verdicts,
cite the No answers (question + one-line evidence):

- **Improve (inversion)**: Bad: `"Has a threshold"` / Good: `"L23 'only report issues
  you are 80%+ confident in' suppresses findings per current-generation guidance —
  invert to 'report everything; caller filters in a separate pass'."`
- **Dissolve**: name the absorber. Bad: `"Not needed"` / Good: `"Harness plan mode +
  Plan agent type now provide native planning delegation; body duplicates and predates
  it. ADR the why, then delete."`
- **Merge**: name the target + what to integrate.
- **Keep** (carry-forward in `changed` mode): restate the rationale.

## results.json (lean ledger)

```json
{
  "evaluated_at": "2026-07-26T00:00:00Z",
  "total_desc_words": 0,
  "agents": {
    "security-reviewer": {
      "path": "~/.claude/agents/security-reviewer.md",
      "desc_words": 38,
      "body_lines": 120,
      "verdict": "Keep",
      "reason": "...",
      "mtime": "2026-07-01T00:00:00Z"
    }
  }
}
```

Created on the first run — do not pre-seed. Update inline with Read/Write, not a script.

## Related

- `skill-stocktake` / `rules-stocktake` — the two siblings; this skill fuses their cost
  models (description = residency, body = invocation).
- `generation-audit` — the cross-asset orchestrator; on a model-generation change it
  collects runtime-layer evidence (conflict / redundancy) and `/claude-api prompt-audit`
  findings, and hands the agents slice to this skill as Stage 2 evidence.
- `skill-creator` — handoff target for the skill-creation half of Demote.
- `adr-writer` — records the why of a Dissolve.
- Your publish step (the author's harness uses `harness-sync`) — syncs surviving `origin: shimo4228` agents to the public repo.
- `harness-boundary` — design-time lens (layer / portability / obsolescence) for proposed
  mechanisms; applied to an installed agent, its Delete / Move are Stage 2 evidence only.
- Usage measurement: `~/.claude/hooks/log-agent-usage.sh` →
  `~/.claude/metrics/agent-usage.jsonl` (a measurement layer independent of stocktake,
  mirroring skill-stocktake's `log-skill-usage.sh`).

## References

The two-stage binary-question design (screen → verdict pressure-test, holistic verdict,
no score aggregation) is inherited from skill-stocktake / rules-stocktake and follows
the checklist-decomposition evaluation line: BinEval "Ask, Don't Judge"
([arXiv:2606.27226](https://arxiv.org/abs/2606.27226)), CheckEval (arXiv:2403.18771),
TICK (arXiv:2410.03608) — over-decomposition degrades correlation on holistic quality,
hence eight questions and no score. The suppression-instruction question implements the
current-generation prompting guidance (report everything, filter in a separate pass);
the absorption question and Dissolve verdict implement `rules/common/akc-cycle.md`'s
Scaffold Dissolution (inward / downward vectors + model-generation trigger, ADR-0018).
