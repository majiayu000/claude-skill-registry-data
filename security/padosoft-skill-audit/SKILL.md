---
name: padosoft-skill-audit
description: >-
  Use this skill when the user wants to review, audit, modernise or bulk-update the Agent Skills a project
  already has (.claude/skills, .agents/skills, .claude/commands, plugin skills) against the current
  authoring rules for Claude models: skills that feel too prescriptive, shout rules in capitals, run past 500
  lines, never trigger or trigger on everything, ask the model to show its reasoning, or exist in one copy
  per model. Also when they ask "are our skills still right for the new models?", "sistema le skill del
  repo", "allinea le skill alle nuove linee guida". It first checks the rules are still current, then runs a
  deterministic checker, reviews each skill, reports, and applies the approved fixes. Do not use it to
  write a new skill from scratch (padosoft-skill-creator), to install skills (padosoft-skills-router), or to
  review application code.
license: MIT
compatibility: >-
  Requires Python 3.10+ (standard library only). The freshness check needs HTTPS access to the
  documentation sites; without it the audit still runs and says the rules were not re-verified.
metadata:
  version: 0.2.2
  author: Padosoft
  summary: Bring a project's skills up to the current rules, after checking the rules are still current.
  profiles: core
  scope: global
  repository: https://github.com/padosoft/skills
  keywords: skills, audit, SKILL.md, frontmatter, description, prescriptive, models, guidelines, freshness
---

# Skill audit

Takes the skills a project already has and brings them up to the current authoring rules: a report of
findings by rule ID for every skill and, when asked, the edited skills — with the checker green and an honest
list of what was verified and what was not.

**The rule: check the rulebook against its sources before using it; keep what the model cannot know, cut
what it already does, turn what must never break into a hook or a script — and keep one skill per job for
every model.**

---

## 0. What is in this skill

| File | Use |
|---|---|
| `references/guidelines.md` | The rulebook: every rule as `G-AREA-NN`, with level and source. Read it in full once, before Phase 2 |
| `references/sources.json` | The official page and the anchor sentences each rule rests on, for the freshness check |
| `references/refresh-procedure.md` | Read only if Phase 0 reports drift and the user wants the research done |
| `scripts/check_freshness.py` | Phase 0: are the rules still in line with their sources, and is this copy current? |
| `scripts/audit_skills.py` | Phases 1 and 5: inventory and deterministic checks, read-only |
| `assets/audit-prompt.md` | The prompt to paste in agents or projects where this skill is not installed |
| `assets/project-audit.yml` | A GitHub Actions workflow a project copies: a pull-request gate and a weekly report issue, no secret; two jobs (read-only audit, issues-only report) and a pinned checker |

Run the scripts from this skill's folder: `python3 "${CLAUDE_SKILL_DIR}/scripts/audit_skills.py" <root>`.
Claude Code fills in `${CLAUDE_SKILL_DIR}` only when the skill is loaded; if the text reaches you unsubstituted,
it means the folder that contains this file. `python3` below stands for whatever runs Python 3.10+ here: on
Windows it can be the Store alias, so use `python` or `py -3`; quote paths with spaces. Both scripts have
`--help`.

## 1. Modes and scope

- **report** (default): Phases 0-3, and the run ends with the Phase 3 report. No file is changed; Phases 4
  and 5 do not apply.
- **apply**: when the user asks to update or fix the skills. It still stops once, after the report, for
  approval of the changes, unless the user said to go ahead without asking.
- **Scope**: the skills of the project; a path narrows it to one folder or one skill. Personal skills
  (`~/.claude/skills`, including `synced/`) are outside a project audit: scan them only when asked.

## 2. Workflow

Copy this checklist into your reply and keep it updated. Each line says when it is done and where to go back:

```
Skill audit:
- [ ] Phase 0  Rules checked.        Done: exit code known, written for the report.
- [ ] Phase 1  Inventory.            Done: checker ran (exit 0 or 1) and the units are listed. Exit 2: fix the call, redo.
- [ ] Phase 2  Review.               Done: every unit has a tier and a verdict, and coverage is stated.
- [ ] Phase 3  Report.               Done: delivered (apply mode: approved). Report mode ends here.
- [ ] Phase 4  Fixes.                Done: each approved change applied to its source of truth.
- [ ] Phase 5  Verify.               Done: checker has no ERROR on the edited skills. ERROR left: back to Phase 4 for them.
```

### Phase 0 — Are the rules still current?

```bash
python3 "${CLAUDE_SKILL_DIR}/scripts/check_freshness.py" --model "<the model you are running as>"
```

Pass the model named in your system prompt; leave `--model` out if you cannot tell. The output always
carries a `Model:` line (covered, not covered, unrecognised or not given).

- **Exit 0** (aligned, or partial with some pages unreachable): continue, and write in the report "rules
  verified against N sources in this run", listing any unreachable page. A `NOTE` line saying the published
  copy could not be read is benign (offline, or the skill is not published yet): mention it in one line.
- **Exit 1** (drift): show the drift summary and the rules it names, then ask the user to choose:
  1. research now only what drifted, following `references/refresh-procedure.md`, then continue with the
     delta applied to this run (recommended);
  2. continue, marking the report "rules possibly outdated: <rule IDs>";
  3. stop.

  In an unattended apply run, take option 2. When the only drift is `outdated-copy`, suggest updating this
  skill first: the published copy may already contain the fix.
- **Exit 2**: continue, and say in the report that the rules could not be re-verified and why.

### Phase 1 — Project rules, inventory, checker

1. Read the project's instructions: `CLAUDE.md` and `AGENTS.md` in full; for long instruction files
   (Copilot or Gemini mirrors, rule folders) search them for "skill", "sync" and "mirror" instead of reading
   everything. You are looking for four things: commit and branch rules, any rule that mirrors skill or rule
   text into other agents' files (with size limits), where shared skills live, and what must not be
   touched. Where they conflict with this skill, the project's rules win.
2. Run the checker. In a large project also save `--json` outside the repository (a scratch or temp
   folder):

   ```bash
   python3 "${CLAUDE_SKILL_DIR}/scripts/audit_skills.py" <root>
   python3 "${CLAUDE_SKILL_DIR}/scripts/audit_skills.py" <root> --json > <scratch>/skill-audit.json
   ```

   **Exit 1 only means ERROR-level findings exist, which is a normal result for an audit; the output is
   valid.** Exit 2 means a wrong path or an unreadable file: fix the call, do not rebuild the inventory by
   hand. The header counts skills by location, commands, mirrored and synced units: copy them to the report.
3. Decide the units of work. A mirrored skill (a stub in one folder pointing to a source in another) is one
   unit: its source. Synced claude.ai skills are reported, not edited: the next sync overwrites them.

### Phase 2 — Review every skill

Read `references/guidelines.md` in full once. Then spend the review where it pays, in three tiers:

| Tier | Which units | Depth |
|---|---|---|
| A | Any ERROR; three or more WARN; over 500 lines; mirrored units; anything the user named | `SKILL.md` in full, plus the linked files that the findings or its structure point to (a skill linking dozens of references does not need all of them read) |
| B | Any other unit with a WARN | The frontmatter and a skim of the body |
| C | Only INFO, or nothing | The checker's output alone |

In the report, state the coverage: "reviewed in full: n of N; skimmed: k; checker only: m", and name the
files you did not open. Tier A units get the review below; take the checker's findings and add what a
script cannot see:

- **Does it pull its weight?** Would the model get the task wrong without it? (G-BODY-01, G-LIB-04)
- **The description**: the right requests, the boundaries with sibling skills. (G-DESC, G-LIB-02)
- **Freedom per step**, and rules that must hold every time. (G-FREE-01, G-FREE-02)
- **Verification, scope and delegation instructions.** (G-GEN-07, G-GEN-08, G-GEN-09)
- **The commands the steps quote**: run the read-only ones once and compare the output with the fields the
  next step reads; a command that returns nothing, or that approves, merges or deletes under a heading that
  says "read", is a bug and not a style point. (G-FLOW-09)
- **Model handling**: per-model copies, scattered model-specific lines. (§3 below)

What to do with what you find:

| You find | Do | Rule |
|---|---|---|
| Project facts, paths, commands, conventions, schemas, business rules, gotchas | Keep them, verbatim when they are precise | G-BODY-01, G-BODY-04 |
| Explanations of things the model already knows | Cut | G-BODY-01 |
| `MUST`/`NEVER`/`CRITICAL` in capitals | One plain sentence with its reason; if it must hold every time, also propose a hook or a script | G-GEN-02, G-GEN-03, G-FREE-02 |
| "Show / write out your reasoning", "think step by step and write it" | Remove; where a visible justification is needed, ask for a short explanation of the result | G-GEN-05, G-GEN-06 |
| "Double-check", "re-verify", "use a subagent to verify" | Remove, or replace with the concrete validator step | G-GEN-07 |
| "Take your time", "do not skip", "if in doubt, use X", forced status updates | Remove | §17 of the guidelines |
| "Only report the important issues" in a review skill | Ask for every finding with confidence and severity | G-GEN-12 |
| A menu of equivalent options | A default and one escape hatch | G-BODY-05 |
| Dated statements | Move under *Old patterns* | G-BODY-10 |
| The same rule in several places | Keep it in one | G-BODY-11 |
| A long reference inside `SKILL.md`, the key rule at the bottom | Move to `references/` with "read it when…" and a table of contents if over 100 lines; key rules to the top | G-STRUCT-01..04, G-BODY-02 |
| A step whose failure costs data or money; a side-effecting skill the model can start | A script or a gate; manual invocation | G-FREE-01, G-FREE-03 |
| One copy of a skill or document per model | Merge into one skill with a model appendix | G-MODEL-01..04 |
| A skill the base model no longer needs | Propose retiring it, with the evidence; never delete it yourself | G-LIB-04 |

**Do not cut, even when it looks generic:** a line that records a real failure (when unsure, read the
file's history with `git log -p`), a legal or company constraint, or anything the project's own rules
require. Rewrite its form, keep its substance.

Severity in the report: **blocking** for checker ERRORs (the skill fails to load or upload, risks a
refusal, links to nothing) and for any judgment finding that is a bug — instructions that cannot work as
written, such as a command with the wrong options or a step that does the opposite of its heading (verify
with a read-only run when you can, and say how you verified); **should** for WARNs and for judgment
improvements; **could** for INFO and taste.

### Phase 3 — Report

Use the template in §5, with statuses `proposed` in report mode. In apply mode, stop here for one approval
of the proposed changes; the user may exclude skills or individual changes.

### Phase 4 — Apply

- One skill at a time, in its source of truth (G-STRUCT-09). Keep the skill's language and behaviour: change
  how it is written, not what it does, unless the approved report says otherwise.
- A description rewrite changes what triggers the skill: keep the words users actually use, say so in the
  report, and re-run the project's trigger evals if it has any.
- Hooks, permissions and settings: give the exact snippet and where it goes (one line each in the report's
  hooks slot, the snippet itself below it); install it only if asked, because it changes behaviour beyond
  the skill.
- Generated files and mirrors (catalogues, copies for other agents, rule text kept in sync by hand under a
  size limit): regenerate them with the project's tool or follow its sync rule; never edit generated files
  by hand, and list every mirror a change touches.
- Commit or push only if the project's rules or the user say so.

### Phase 5 — Verify

1. Re-run `audit_skills.py`. Zero ERROR, and a WARN only where the report says why it stays. Otherwise return
   to Phase 4 for those skills.
2. For skills where you removed instructions in bulk, run one realistic prompt in a fresh context with the
   old and the new version and compare. When you cannot, mark those skills "not re-tested" — do not imply
   they were.
3. Deliver the final report (§5).

## 3. One skill, many models

Never a skill or a document per model (G-MODEL-01). The base instructions must be complete on every target
model. Pinning a model or an effort level is a frontmatter setting in Claude Code (`model:`, `effort:`), not
prose — and not portable (G-MODEL-03). When an eval shows a real gap on one family, add an appendix in
`references/models/<family>.md` and route to it from the top of `SKILL.md`:

```markdown
## Model notes
If you are running as Claude Haiku, read references/models/haiku.md before step 1.
On any other model, or if you cannot tell, the instructions below are complete as they are.
```

Appendices add, never contradict. What typically goes in each, and the official paragraphs to copy, are in
§12 of the guidelines.

When a skill already has lines about specific models, sort each one:

| The line | Do |
|---|---|
| States a difference somebody measured (an eval, a transcript) | Keep it; if it is long, move it to the family appendix |
| Guesses ("Haiku needs more detail", "Opus is smarter") | Mark it *unmeasured* in the report; propose removing it; never invent an appendix to hold it |
| Routes work to a model on purpose (cheap model for exploration, strong one for review) | Keep it: it is a design choice about cost, not a claim about behaviour; do not report it as a model difference |
| Asks the model to behave differently depending on which model it is | Replace with the base instruction that works on all, or with `model:`/`effort:` where Claude Code is the only target |

This skill follows its own rule: no per-model appendix until an evaluation shows a gap, and the same
instructions on every model.

## 4. Gotchas

- **Stubs pointing at another `SKILL.md`** (a `.claude/skills` entry that says "read `.agents/skills/x` in
  full"): edit the source and align the two descriptions. A stub is legitimate when it carries notes only
  that harness needs (its own tool names, selectors); then the finding is the duplicated description and the
  extra hop, not the stub. Suggest a symlink only where it loses nothing and the team's machines support
  it: on Windows, symlinks need privileges and `core.symlinks`.
- **Files bundled for another harness** (for example `agents/openai.yaml`, metadata for Codex) are not
  orphans, whatever the checker's INFO says; leave them.
- **Skills shared with other agents or uploaded to claude.ai** keep to the portable frontmatter fields
  (G-FM-03): a Claude Code-only key there is a bug, not a style choice.
- **Synced claude.ai skills** (`~/.claude/skills/synced/`) change on claude.ai; local edits are overwritten.
- **`.claude/commands/*.md` are skills too**, the legacy form: same rules, except they have no `name` or
  `paths`.
- **The checker's word lists are heuristics.** Capitals in a code block, an error message quoted verbatim,
  a rule that is genuinely a hard line: judge them in Phase 2 instead of rewriting on sight.
- **Removing verification instructions** means removing the generic ones. Steps that run a validator, the
  tests or a build stay.
- **A rule that keeps being ignored is not fixed with capitals.** Find out why: buried at the bottom, no
  reason given, or something that should be a hook.
- **Keep the skill's language.** An Italian skill stays Italian; the emphasis list covers MAI, SEMPRE, NON,
  OBBLIGATORIO.
- **Large collections**: review in batches. A subagent per independent batch of skills is fine; a subagent
  to "double-check" the review is not (G-GEN-09).

## 5. Final report

```
Skill audit — <repository> · mode: report | apply
Rules: verified against <n> sources in this run | drift on <rule IDs>, researched: yes/no | not re-verified: <why>
       model: <the Model: line> · notes: <any NOTE line>
Units: <the checker's header: skills by location, commands, mirrored, synced> · checker: <e> ERROR · <w> WARN · <i> INFO
Coverage: reviewed in full <n> of <N> · skimmed <k> · checker only <m> · not opened: <files>

| Skill | Severity | Findings (rule IDs) | Change | Status |
|---|---|---|---|---|
| <name> | blocking / should / could | G-GEN-02 ×6, G-STRUCT-03 | capitals rewritten with reasons; ToC added to references/x.md | proposed / applied / skipped / kept |

Hooks or scripts proposed: <rule → where it goes>, one per line, snippets below
Candidates to retire: <skill — evidence>
Mirrors touched: <files kept in sync by the project's rule>
Verified: <how each claim was checked; checker result on the edited skills; re-tested in a fresh context: …>
Not verified: <…>
Rulebook update proposed upstream: <issue or PR on padosoft/skills, or "none">
```
