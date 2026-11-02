---
name: extend-skillset
description: Use when the stack profile names a tool no installed skill covers, or the user asks for a new skill. Authors one in the house style, audit-first and profile-aware, into the project's .claude/skills or this plugin repo, then checks it.
---

# Extend Skillset

Turns "no skill covers X" into a skill that fits the set. Template and checklist: [skill-template.md](skill-template.md). House style: this repo's `CONTRIBUTING.md`.

## 1. Audit (change nothing)

```bash
cat .claude/stack-profile.md 2>/dev/null
ls .claude/skills 2>/dev/null; ls skills/*/ 2>/dev/null | head -80
grep -rli "<tool or topic>" .claude/skills skills 2>/dev/null | head
```

Answer three questions before writing anything:

1. Is there already a skill that covers it (even partly)? Extend that one; do not add a twin.
2. Is the gap a *procedure* with a trigger ("when X, do Y")? If it is only a fact, add it to a reference file or `_shared/` instead.
3. Is the stack stable enough to encode? A tool in the "Assess" ring of [tech-radar.md](../_shared/tech-radar.md) gets a short skill with a warning, not a full one.

## 2. Decide

| Situation | Action |
|---|---|
| Existing skill covers it | Edit it; add the case; stop. |
| Fact only | Add a rule to the nearest reference file; stop. |
| New procedure | Continue. |

Choose the destination (ask once with `AskUserQuestion`, recommended first):

- **Project** (Recommended): `.claude/skills/<name>/` — private to this repo, zero release cost.
- **Upstream**: `skills/<catalogue>/<name>/` in this plugin repo — for skills useful to others. Needs registration by the maintainer (README, CHANGELOG, validator).

## 3. Research the stack live

Follow [version-protocol.md](../_shared/version-protocol.md). For each tool the skill touches: latest stable version, current install command, config keys, breaking changes of the last major. Read the official docs page, not a blog. Write each verified fact with its source into the reference file, and into the catalogue's `_shared/stack-versions.md` when one exists. If you cannot verify a fact, mark it `unverified` and say so in the skill.

## 4. Write the skill

Use [skill-template.md](skill-template.md). Requirements:

- Folder `<name>` kebab-case, verb-first (`set-up-x`, `configure-x`, `build-x`, `audit-x`); `name` equals the folder.
- `description` starts with `Use when`, one sentence, **at most 300 characters**, names the trigger situation, not the topic.
- Body: numbered, audit-first, idempotent: Audit → Decide → Detect track → Install only the missing → Generate seams → Wire → Verify (exact command and expected output). At most about 180 lines.
- Step 1 reads `.claude/stack-profile.md` and branches on it; if absent, it detects from the repo and asks one question only when detection is ambiguous and the answer changes the output (then suggests `set-up-stack-profile`).
- Reference file: each rule as `## Rule:` with **Why**, **How to apply**, optional **Anti-example**; ends with `## When to deviate`.
- Link to the shared contracts instead of restating them: [engineering-principles.md](../_shared/engineering-principles.md), [security-baseline.md](../_shared/security-baseline.md), [logging-contract.md](../_shared/logging-contract.md), [observability.md](../_shared/observability.md).
- Code snippets compile against the current API. One canonical pattern, not a menu.
- Plain prose; none of: simply, just, seamless, robust, leverage.

## 5. Check against the checklist

Run the checklist at the end of [skill-template.md](skill-template.md). In this plugin repo, also run:

```bash
bash scripts/validate.sh
```

Expected: `OK: validator passed`. Outside the repo, run the checklist's shell snippet, which reproduces the three checks (frontmatter, description rule, links).

## 6. Verify the skill triggers

Describe a realistic task in one sentence and check that the `description` would match it and not match an unrelated one. Rewrite the description if not. Then run the skill's own audit step on a real repo and confirm it changes nothing on a second run.

## 7. Report

Print: path written, the verified versions with sources, what is `unverified`, and (for upstream) the registration steps left for the maintainer: README list, CHANGELOG entry, manifest listing. Do not edit those yourself unless asked.
