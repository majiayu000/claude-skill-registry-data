---
name: skill-auditor
description: Audits SKILL.md files ("audit this skill", "review my skills", "score this SKILL.md") and writes a scored report with concrete fixes. Use when asked to review, audit, critique, grade, lint, or score a skill or a folder of skills, or before publishing or porting a skill into a plugin. For creating or rewriting a skill, or for skill usage and context cost, use the platform's skill-authoring and usage tools instead.
argument-hint: "[skill-file-or-dir] [report-path]"
---

# Skill Auditor

Static review of one or more skills. Reads each `SKILL.md` and the files it links to, grades eight dimensions, and writes one report. It judges what can be seen in the files.

## Inputs

- First argument: a `SKILL.md` file (single-skill mode) or a directory (multi-skill mode: every `**/SKILL.md` under it). With no arguments, scan the overlay's scan roots, else `.claude/skills/` in the project root plus the skill roots of any plugins in the project (each `.claude-plugin/plugin.json`'s `skills` path, default `skills/`).
- Second argument: report path. Defaults to the overlay's value, else `SKILLS-AUDIT.md` in the project root.
- Overlay `.claude/shipyard/skill-auditor.md` in the project root, read if present. It sets the project's conventions; its shape is in [references/overlay-example.md](references/overlay-example.md). Without it, conventions are inferred from the audited set (step 4).

## Output

One markdown report in the shape of [references/report-template.md](references/report-template.md): scorecard, cross-cutting issues (multi-skill only), top 5 fixes, what's well-designed, per-skill detail.

## Rules

- **Cite evidence for every finding**: `path:line` plus a short quote. A finding the reader can't locate can't be acted on or disputed.
- **Flag, don't fix.** Each finding carries dimension, severity, and a concrete remediation, but the audited files stay untouched. The skill's owner decides what to change.
- **Critical, with wins in their own section.** Honest critique is the value. Strengths go under "What's well-designed" so a clean dimension isn't mistaken for an unexamined one.
- **Project conventions beat global style.** When a skill follows a convention that the overlay or the rest of the audited set uses consistently, note the divergence from global guidance at low severity at most. Platform hard limits (dimension 1) are not conventions; those always apply.
- **Tag runtime claims `(prediction)`.** "This description will undertrigger" can't be settled by reading. Tag it and name the runtime check that would settle it.
- **Criteria live in [references/dimensions.md](references/dimensions.md).** Read it in full before grading; the checks and severities are there.
- Steps without a marker are agent-owned and proceed without asking.

## Leave to other tools

Defer schema checks, behavior evals, usage stats, and description tuning to whatever tools the platform provides. Cite their output in findings and point to them in remediations instead of redoing their work:

- **Schema validators** (plugin manifest, frontmatter, spec conformance). Read their warnings, not just pass/fail: a validator can pass a skill that has real problems, and it may not check what this audit grades (wrapped descriptions, lengths, unknown keys), so grade those by hand. Cite spec-validator errors as portability findings.
- **Eval runners** test behavior and triggering. Route "does it trigger / does it work" questions there.
- **Description optimizers** tune trigger accuracy against should/shouldn't-trigger queries. Recommend one for any description graded medium or worse.
- **Usage reports** show listing cost and never-invoked skills. A never-invoked skill is evidence for a description finding; cite it if the user has one.

## Steps

Copy this checklist and tick items as you go, so the position survives compaction:

```
- [ ] 1 Resolve inputs, read overlay
- [ ] 2 Run schema validation (plugin skills only)
- [ ] 3 Parse each skill
- [ ] 4 Settle conventions
- [ ] 5 Grade each skill
- [ ] 6 Cross-skill checks (multi-skill only)
- [ ] 7 Top 5 fixes and what's well-designed
- [ ] 8 Resolve report path (gate)
- [ ] 9 Write report
- [ ] 10 User review (gate)
```

1. **Resolve inputs, read overlay.** Pick the mode, list the skills found, read the overlay or note it's absent.
2. **Run schema validation** for each plugin that contains an audited skill, with the platform's validator if one is available. If none is, say so in the report header.
3. **Parse each skill.** Split frontmatter from body, record raw and substantive line counts (substantive excludes blanks and bare headings), and read every file the body links to, one level deep.
4. **Settle conventions.** Use the overlay's. Without one, take the majority usage in the parsed set (gate markers, section names) and say in the report header that they were inferred.
5. **Grade each skill** on the eight dimensions in `references/dimensions.md`, recording findings in the per-skill detail format of the report template. With more than 5 skills, dispatch one subagent per skill, because past a handful the early skills crowd the later ones out of attention. Give each subagent absolute paths, since it resolves relative ones against its own working directory: the skill path, and this skill's `references/dimensions.md` and `references/report-template.md` resolved to absolute paths (the template's per-skill detail block is the return format). Also pass the settled conventions and that plugin's validation output.
6. **Cross-skill checks** (multi-skill only; these need every skill in view, so they stay with you, not subagents):
   - Section order and gate-marker vocabulary consistent across siblings.
   - Issues recurring in 3 or more skills. Two repeats can be coincidence; three is a habit the project will keep reproducing.
   - Combined listing weight: the total `description` + `when_to_use` length across the set, and which descriptions are longest. With many skills installed, long listings compete for the same context.
7. **Top 5 fixes and what's well-designed.** Rank fixes by severity × number of skills affected; each says what to change, where, and why it ranks there. Then list patterns worth keeping, with the skill they appear in.
8. **Resolve report path.** `STOP — WAIT` if the file exists: ask whether to overwrite, append, or use a new path. An old audit may hold the owner's notes.
9. **Write the report** per the template. Before writing, check that every finding has `path:line` and a quote, and that each scorecard symbol matches the highest severity in its detail section.
10. **User review.** `HUMAN TRIGGER`: the user reads the report and replies *approve* or names verdicts to dispute. Re-grade only the disputed dimensions and update the report. If conventions were inferred, offer once to save them as the overlay.

Handoff — `next:` none. This skill is cross-cutting. Fixes go back to the skill's owner; re-run this skill on the changed files afterward.
