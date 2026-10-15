---
name: session-review
description: >-
  Evidence-grounded retrospective of a Codex or Claude Code session, or an explicit group of sessions. Use for /session-review, retrospective, rétrospective, post-mortem, retour d'expérience, or an assessment of how a session went. Inspects real traces. Not a code review or design review.
---

# Session Review

Explain what helped, what caused avoidable work, and the smallest justified
change. Do not turn every retrospective into a tooling project. Match the
user's language, requested format and scope.

## Establish the perimeter

Identify the requested session or explicit group of sessions, original
objective, later user-authorized objectives and endpoint. For an ongoing
session, freeze a cutoff before the retrospective so the analysis does not
count its own work as part of the task being judged.

A user correction, a new request, a permission, a hook message and a resumed
internal prompt are different events. Do not classify them all as human
interventions. Distinguish the initial task from later testing, documentation,
governance or review work.

For an explicitly hypothetical session, use only the supplied dossier and
label the assessment simulated. Do not run a real-session analyzer or claim
to have opened absent files to fill that hypothetical example.

## Run the installed analyzer first

Before qualitative conclusions about a real session, run the analyzer adjacent
to the SKILL.md actually loaded. Do not replace an installed runtime-specific
script with a repository copy.

```sh
python3 <skill-directory>/scripts/analyze_session.py --session <session-id> --json
```

Without a requested session, use the current-session discovery supported by
that installed script. Existing common options are `--cwd`, `--session`,
`--file`, `--json` and `--md`. Inspect `--help` if the interface is unknown or
an additional option is requested. Some Claude installations support
`--rollup`, `--last` or `--roster`; do not assume the Codex installation does.
Use an advertised aggregate mode only for an explicit multi-session request.

Codex traces normally live under `~/.codex/sessions/YYYY/MM/DD/`; Claude Code
traces normally live under `~/.claude/projects/`. Prefer the exact path
returned by the analyzer or supplied by the user. Keep raw logs local. Extract
only relevant, sanitized coordination and verification evidence; never copy
credentials, signed URLs or business records into a report.

If analysis fails, report the precise missing evidence or tool failure.
Inspect a known trace or use a clearly limited assessment. Retry only with
new evidence or a changed approach, never an arbitrary number of retries.

## Treat measurements according to what they count

The analyzer supplies observations and heuristics, not a causal verdict.

- Use its tool counts with their unit: direct parent calls, nested calls,
  accepted/rejected dispatches, child sessions or a deduplicated aggregate.
  Never call a parent-only count the fleet total.
- Calendar span includes waiting and additional objectives. Active-time
  estimates remain estimates, not exclusive work time or CPU time.
- Token totals may include repeated cached input. Do not equate them with
  new work, money spent, or a model speed comparison.
- Scope tiers and user-turn classifications are hints. Verify synthetic
  wrappers, hooks, apparent corrections and changes of objective in the trace.
- A temporal Git list does not prove commit ownership. Include only changes
  attributable to the reviewed session.
- A text match for a skill, a paste attempt or an agent alias does not prove
  a skill was loaded, a message was delivered or an independent review occurred.
- Compaction counts do not prove lost context. Inspect visible behavior before
  and after each relevant compaction. If the summary is opaque, say so.

When adding a manual count, state its method, cutoff and exclusions. Do not
change the analyzer merely because a one-off query was useful.

## Read the decisive evidence

1. Follow the user's objective through its first useful result, failed
   assumptions, corrections and final observable state.
2. For each material problem, connect an event to its consequence and
   responsible decision. Distinguish orchestrator choices, executor defects,
   instruction conflicts, tool limitations and authorized scope changes.
3. Read the actual diff, relevant command result or external readback before
   accepting a completion claim. A worker's report is a lead, not certification.
4. Inspect compacted-session recovery using checkpoints, revisions, active
   operations and recorded authority. Distinguish repeated reading from an
   actual replay, lost decision or unauthorized action.
5. When comparing direct and delegated work, include framing, monitoring,
   corrections and verification. A direct takeover that reuses prepared code
   is not an independent benchmark.
6. Check prior reports and durable lessons against the trace. State where the
   new assessment agrees, corrects a claim, or cannot decide.

Anchor material findings in a timestamp and trace line/call ID, an attributable
commit, or a file and line. Separate facts, interpretations and proposals.
A defect preceding a rule's creation cannot have been caused by that rule.

## Calibrate the assessment

Give a score when the evidence supports one, explaining its basis and limit.
Do not invent precision when the record is too incomplete to assess.

| Score | Calibration |
|---|---|
| 9-10 | Outcome proved, no material user correction or avoidable rework |
| 7-8 | Outcome proved with bounded friction; identify the actual inefficiency |
| 5-6 | Useful outcome with substantial avoidable rework or repeated correction |
| 3-4 | User intervention was needed to recover scope or avoid a compromised result |
| Below 3 | Important outcome incomplete or incorrectly claimed |

Cite at least two decisive events for a substantial session. Briefly state
what would justify a better or worse score. Do not reward a green badge that
does not prove the intended outcome, or penalize an authorized pause.

## Report only the useful dimensions

Follow the user's requested format. A requested single HTML report stays one
report; Markdown is appropriate for a temporary draft or agent-facing protocol.

Cover these dimensions at the depth justified by the evidence:

1. Assessment and outcome, including unmet criteria.
2. What worked and should be retained, with evidence.
3. What failed, its cause and impact, paired with a concrete remedy.
4. Material agent/skill contributions, only when used and observable.
5. Justified changes, validation and remaining uncertainty.

A trivial session may need only a score and two sentences. A large session
does not need hundreds of lines. There is no minimum suggestion count, no
mandatory future-model section, and no automatic analyzer-improvement appendix.
Combine repeated findings. Keep detailed provenance in a compact appendix when
the user needs a durable report.

For agents, inspect the actual runtime definition when available:
`.codex/agents/*.toml` for Codex, `.claude/agents/*.md` for Claude Code, or the
role supplied by the active runtime. Explain the observed contribution,
limitation and handoff friction. A refused dispatch or opaque output is not a
performance sample; leave it unscored. Do not invent configured agent names.
Assess the instance, not the general intelligence of its provider.

## Prefer subtraction before automation

For each justified improvement, consider in this order:

1. Remove an unnecessary obligation or narrow its trigger.
2. Clarify the next result, authority or acceptance criterion.
3. Reuse an existing command, checkpoint, test or communication channel.
4. Add a mechanism only for a demonstrated recurring gap that the simpler
   options cannot address, within the user's maintenance authority.

A missed instruction does not automatically call for a hook. A long session
does not automatically call for more tasks or subagents. Preserve protections,
simulations and real evidence that worked. Do not weaken a required gate to
make a short path look successful.

If changes are authorized, implement the smallest coherent change and update
its relevant evaluation expectations. Otherwise provide a concrete proposal,
without silently modifying global instructions or scripts. Avoid universal
time/retry thresholds inferred from one session. For an unproved benefit,
name the next observation that would confirm or invalidate it.

## Maintain the analyzer only when justified

A retrospective does not itself authorize analyzer maintenance. A demonstrated
measurement defect can justify a separate, authorized correction. One-off
trace inspection or a preference for a different report is not enough.

When maintenance is authorized:

- Work from the correct version-controlled source and preserve installed
  runtime adaptations and pre-existing changes.
- Reproduce the wrong measurement with a discriminating case before fixing it.
- Preserve supported CLI options and consumed JSON fields, or provide an
  explicit migration when a public contract must change. Compatibility does
  not forbid simplifying internal code or removing dead implementation.
- Run the affected regression and relevant JSON/Markdown checks. Do not retain
  a wrong result merely to obey an additive-only rule.
- Install only the changed artifacts after verification. A SKILL.md update
  must not overwrite divergent Codex or Claude analyzers.

Report an analyzer limit where it affects the conclusion. State that a fix is
unapplied when it is only proposed. Do not add scripts, backups or a release
ritual to every review.

## Delivery check

Can a reader tell what was achieved, what the evidence proves, why work grew,
what changed, and what remains uncertain? Correct unsupported claims and
remove filler before delivering. A short honest report is complete when those
questions are answered; extra sections are not evidence.
