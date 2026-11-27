---
name: hoa-practice-retro
description: >-
  Periodic retro on the owner's engineering practice across repos and agent sessions: evidence-cited
  habits to stop, decisions never executed, unknown unknowns, and recurring work worth a skill. Use
  when asked for a self-retro across repos. Not for one repo's agent-session friction (ce-retro) or one
  repo's machinery (suggest the user run hoa-repo-reckoning).
disable-model-invocation: true
metadata:
  revision: "5"
  areas: "self-management,work-management"
  targets: "runtime-agnostic"
  summary: "periodic retro on the owner's own engineering practice across repos, sessions and memory: habits to stop, decisions never executed, unknown unknowns, each with two independent origins"
  summary_zh: "定期复盘负责人跨仓库、会话与记忆的工程实践：应停止的习惯、未执行的决定、未知的未知，每条都有两个独立来源"
  kind: "entry"
---

# hoa-practice-retro

Look back over a window of the owner's work across every repo and agent runtime and report what
the owner keeps doing that costs more than it returns, what was decided and never done, and what the
owner does not know that would change the practice. Each finding is cited from at least two
independent origins and survives an adversarial verifier.

Explicit invocation only, heavyweight. Never run it as a side effect of another skill. For one repo's
machinery, suggest the user run the explicit-only `hoa-repo-reckoning`; the model cannot invoke it.
For one repo's session friction use Compound Engineering's `ce-retro`.

## Inputs

Record each as `available`, `unavailable` or `out-of-scope` in `scope.md`. Absence of evidence is
never evidence of absence.

1. **Agent session history** as a Retrieval Bundle ([schema](references/bundle-schema.md); hoa's
   `prompts/cross-agent-history-retrieval.md` produces one), or bounded mode over only the paths the
   user supplied. Bounded mode lowers scope, not rigor; say what it excludes. If history is unavailable,
   use a manifest-only bundle that records the gap for the scripts; do not invent session records.
   When a decision-model endpoint is configured, reduce transcript-reading cost for `treadmills`,
   `delegation`, `boundary`, `recurrence`, and unknown unknowns by pre-filtering session history
   and memory stores first: Read `../hoa-practice-mine/SKILL.md` (relative to this skill's
   directory) and follow it. Do not call the Skill tool for it.
2. **Memory store** with search, if present: the owner's dated decisions.
3. **Cross-repo activity** in the window: PRs authored (for example
   `gh search prs --author @me --created ">=SINCE"`) and `git log` across the workspace roots listed
   under `roots` in `${XDG_CONFIG_HOME:-~/.config}/hoa-practice-retro/config.yaml`. No default roots.
4. **Prior practice-retro ledgers** (see [the panel](references/panel.md)): read only prior
   `hoa-practice-retro` runs. Reckoning reports are now free-form and are not an input.
   A finding kind that recurs in two or more repos, or in three or more runs, is promoted to a
   practice finding. This is the cheapest strong signal.

Config keys (same file): `roots` (list of workspace paths; no default), `report_language`
(default `en-US`; narrative only, never numbers, ids or citations). See [the panel](references/panel.md)
for their environment overrides.

## L1: usage facets (deterministic)

```text
uv run scripts/aggregate.py --bundle <bundle> --output <run>/facets.json
```

The JSON is the only authority for counts ([facet definitions](references/facets.md)). Narrate it;
never recount records or estimate a percentage. A zero denominator means "not measured".

## L2: the panel

Follow [the panel protocol](references/panel.md) with these dimensions:

1. **build-before-measure**: features shipped while their eval or measurement is unrun.
2. **decided-not-done**: memory decisions compared with git and PR activity after the decision date.
3. **treadmills**: review→fix chains of three or more rounds on one surface (a design fault, not bad
   luck); fix PRs larger than the feature they fix.
4. **ceremony-vs-outcome**: write-ups, gates and evidence produced compared with outcomes measured.
5. **delegation and acceptance**: delegated "done" accepted without re-derivation; parallel work
   beyond the owner's review bandwidth.
6. **boundary**: work/personal bleed, identity, secrets.
7. **recurrence**: the same manual fix three or more times, which earns a Rule-of-Three proposal.
8. **external**: practices and tools peers use that would make a habit obsolete.

Every finding meets [the evidence floor](references/evidence-floor.md). After the find files exist,
run `uv run scripts/audit.py --bundle <bundle> --run <run>` before the verifiers.

## Anti-drift rules

- Never write or remove a rule, config, or `AGENTS.md` line from inside the retro. A proposed rule
  carries a fire count or cost estimate and goes to the owner as a diff for the owning repo.
- A silent rule is not evidence that the rule is useless (survivorship).
- No new triage tiers or default promotions without three cited instances.

## Repeatable-work candidates

A candidate qualifies only when observed three or more times across two or more projects and not
already covered by an installed skill. Before citation checks and verification, write each candidate
as a finding in `find-recurrence.json`. Run the panel's `findings.py report` to build `ledger.jsonl`;
present at most three candidates from that ledger, using their finding ids.

Only an approval that names a single candidate id records `accepted`. A vague or grouped approval
("looks good", "all of them") records nothing; ask which candidate the owner means. Record the
named decision with `uv run scripts/findings.py decide <run> <id> accepted "<reason>"` and route
creation to `hoa-skill-create` only after that succeeds.

## Privacy

Keep all drafts outside the subject. Run `uv run scripts/pii_gate.py --target <path>` before writing
each artifact, including generated output, or pass `--content-file <draft>` to write via the gate.
It refuses tracked or unignored repository paths. Reports cite ids,
never quote transcripts. The chat echo carries no paths, session ids, secrets or transcript text.

## Output

`report.md` in the run: coverage and caveats, L1 panorama, meta-diagnosis, A (habits still being
done), B (unknown unknowns), the decided-not-done list, at most three repeatable-work candidates,
follow-through on the last retro (`uv run scripts/findings.py report <run> --prev <last>`), and **On the Horizon**
(the next measurement worth taking). Plus `facets.json` and `ledger.jsonl`. With no usable signal,
write `_No insights generated_` rather than filling the report.

The chat reply is short and redacted: coverage status, the most useful L1 fact, surviving finding
count, top decided-not-done item, and one horizon item.

## Cadence

Monthly, or at quarter end with a 90-day window. Unattended runs stop at the report and record no
decisions.

## Provenance

Absorbs hoa's earlier introspection skills (deterministic facets, citation floor, PII gate, and
the repeatable-work qualification rule). The decision ledger and the
proposing-nothing-is-complete bar adapt Compound Engineering's `ce-retro`.

Only if a script command fails (for example `uv` is not found), read
[references/troubleshooting.md](references/troubleshooting.md).
