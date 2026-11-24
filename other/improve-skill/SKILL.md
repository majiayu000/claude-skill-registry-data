---
name: improve-skill
description: >
  Improve an existing agent SKILL.md through one gated cycle: select the target (default this skill), snapshot the committed baseline, diagnose against skill-design-principles plus four rubric dimensions, apply exactly one focused change, and ship only if a different agent than the author PASSes with quoted evidence. Use when the user says "improve this skill", "improve-skill", "iterate on SKILL.md", or "apply skill-design-principles to a skill". Do not use for code slop over a duration (anneal), generic timeboxed work (timeboxed-iterating), graph orchestration (workgraph), metric hill-climb on a codebase (autoresearch), or stripping slop from existing prose (catalog-deslop).
---

# Improve Skill

One cycle, one change, one independent verdict. You do not decide the skill got better.

## Role

You are the **orchestrator**. You:

1. Resolve the target `SKILL.md`.
2. Snapshot the baseline off-tree before any edit.
3. Diagnose against the lens below and pick exactly one hole.
4. Apply that one change, or dispatch an author who does only that.
5. Dispatch a **different** agent as judge. Enforce the verdict.

You do **not**: score your own (or the author's) change; skip the gate; rewrite the skill; hand-edit generated README catalog files; create a skill from scratch.

```
NO INDEPENDENT PASS → NO COMMIT. FAIL → RESTORE BASELINE.
```

If you cannot dispatch a different agent, stop. Leave the tree at baseline. Do not self-score.

## Inputs

| Input | Required | Default |
|---|---|---|
| Target skill | no | The `SKILL.md` next to this file (`improve-skill`) |
| Commit prefix | no | none; the dimension still goes in the subject |

If the user names a path that is not an existing `*/SKILL.md`, stop and say so. Do not ask them what to change.

Out of scope: README, cheatsheet, harness files, new skills, application code, duration-boxed work.

## Working files

`$d` is created in step 2 (`/tmp/improve-skill-<target-basename>-<epoch>/`).

```
baseline/          # committed (or pre-edit) copy of the skill tree
diagnosis.md       # one hole, or "nothing above the bar"
gate.md            # judge verdict — written by the judge, not you
log.md             # append-only
```

Pass **paths**, not file contents, to the author and the judge.

`references/` next to this file are procedure helpers. `$skill_dir/references/` is the target's. They coincide only when the target is this skill.

## Process

```
select-target → baseline → diagnose → one-change → independent-gate
  PASS: regen catalog if needed, commit, record hash
  FAIL: restore baseline, do not commit, record why
  nothing-to-do: stop, no commit (valid refused improvement)
```

### 1. Select target

Start-here checklist — first match wins:

1. If the user named more than one skill (a list, "all skills", more than one `SKILL.md` or skill directory), stop. One cycle accepts one target. Do not pick a favorite. Do not ask which.
2. If the user named a path that is not an existing `*/SKILL.md` and not a skill directory that contains one, stop and say so. Do not default to this skill. Do not ask them what to change.
3. If the user gave an existing `…/SKILL.md` (or a skill directory that contains one), that is the target.
4. Otherwise the target is this skill: the `SKILL.md` in the same directory as the file you are reading.
5. Confirm the file exists and YAML `name:` equals the directory name. If not, stop.

### 2. Capture baseline

Do this **before** any edit. `skill_dir` is the absolute path to the directory that contains the target `SKILL.md`. Run from a shell:

```bash
skill_dir=<absolute path>
slug=$(basename "$skill_dir")
d=/tmp/improve-skill-$slug-$(date +%s)
mkdir -p "$d/baseline"
repo=$(git -C "$skill_dir" rev-parse --show-toplevel)
rel=$(python3 -c "import os; print(os.path.relpath('$skill_dir', '$repo'))")
if git -C "$repo" rev-parse --verify --quiet "HEAD:$rel" >/dev/null; then
  git -C "$repo" archive HEAD "$rel" | tar -x -C "$d/baseline" --strip-components=1
else
  cp -R "$skill_dir/." "$d/baseline/"
fi
git -C "$repo" rev-parse --short HEAD > "$d/baseline-rev.txt"
```

If `HEAD:$rel` exists, that tree is the baseline even when the working tree is dirty. If it does not, the live `$skill_dir` tree is the baseline — not only `SKILL.md` + `references/`. Restore uses `$d/baseline/`.
If `$d/baseline/SKILL.md` is missing, stop. Do not edit. Do not invent a baseline.

### 3. Diagnose

Read the target `SKILL.md` and any `references/` one level under it. Write `$d/diagnosis.md`. Do not ask the user what is wrong.

**Lens** (apply all; pick one hole):

1. **Description = WHAT + WHEN.** Triggers named. Siblings that could steal load are excluded by name.
2. **Executable procedure.** A cold agent can name the next action and the stop/fail condition. Ordered steps, not principles.
3. **Degrees of freedom.** Fragile steps (baseline, one-change, independent gate, commit-on-pass) are locked. Wording of a change is free. "Use judgment" on a gated step is a hole.
4. **One home per fact; no sprawl.** No tutorial on what a skill is. No no-op restatement.
5. **Four rubric dimensions** (the judge scores these same four):
   - **Clarity** — every step names a next action or a stop condition.
   - **Trigger reliability** — intended utterances land here; sibling collisions do not.
   - **Procedure completeness** — no step the skill claims to require is missing or "figure it out".
   - **Anti-failure coverage** — each named failure mode has a named protection (restore, refuse, stop).

A hole is above the bar only if you can quote a missing next action, stop/fail condition, trigger or sibling exclusion, or named protection. Rephrase, shorter wording, synonym, extra example of an existing rule, restating a protection already in the table, or a user ask that is only polish / length / wording cleanup is not a hole — write `nothing above the bar`.

Write exactly one of:

```markdown
# Diagnosis
- Dimension or failure mode: <one name>
- Hole: "<quote from the current skill or ABSENT>"
- Change: <one sentence>
```

or

```markdown
# Diagnosis
nothing above the bar
```

If `nothing above the bar`, append that to `log.md` and **stop**. Do not edit. That is a valid cycle.

### 4. One focused change

Edit only the hole named in `diagnosis.md`. One dimension or one failure mode. Not a rewrite. Not "also cleaned up X".

- You may edit `SKILL.md` yourself or dispatch an author with the target path, the diagnosis path, and "change only this hole".
- Do not edit generated `README.md` files.
- After the edit, if `$repo/scripts/generate.ts` exists, run from `$repo`:

```bash
deno run --allow-read --allow-write scripts/generate.ts
```

Never hand-patch the root `### Skills` list.

Then revert extras before gating. Reuse `$skill_dir`, `$d`, and `$repo` from step 2. If `$skill_dir` is unset or `"$skill_dir/SKILL.md"` is not the live candidate, stop. Do not invent a revert.

An extra is a dirty path under `$skill_dir` that is not `$skill_dir/SKILL.md`, not `$skill_dir/README.md`, and not backtick-quoted (relative to `$skill_dir`, or as `$skill_dir/...`) in the `- Change:` line of `$d/diagnosis.md`. Generated `$repo/README.md` is not an extra. A new or non-`SKILL.md` path is kept only when that Change line quotes it.

```bash
change=$(sed -n 's/^- Change: //p' "$d/diagnosis.md")
prefix=$(python3 -c "import os; print(os.path.relpath('$skill_dir', '$repo'))")
git -C "$repo" status --porcelain -u -- "$skill_dir" | while IFS= read -r line; do
  path="${line#???}"
  rel="${path#"$prefix"/}"
  if [ "$rel" = "SKILL.md" ] || [ "$rel" = "README.md" ]; then
    continue
  fi
  case "$change" in
    *'`'"$rel"'`'*) continue ;;
    *'`'"$skill_dir/$rel"'`'*) continue ;;
  esac
  if [ -e "$d/baseline/$rel" ]; then
    git -C "$repo" checkout HEAD -- "$path"
  else
    rm -rf "$repo/$path"
  fi
done
```

### 5. Independent gate

Dispatch a **new** agent. Not you. Not the author. Give it only the baseline path, the live candidate path, this section, and the absolute path of `references/known-bad.md` next to this file.

Judge prompt (fill the brackets, keep the rest):

```
You are an independent skill judge. You did not author this change.
Baseline: < $d/baseline/SKILL.md >
Candidate: < live SKILL.md path >
Known-bad fixtures: <absolute path of references/known-bad.md next to this skill>
Also read sibling files in each tree if present.

Do not improve the candidate. Do not take the author's word.

1. Mechanical validity — FAIL if any miss:
   - candidate exists; directory name == YAML name
   - YAML name: and description: are single-line (not `>` / `|`)
   - description is 1–1024 chars, no XML tags, states WHAT and WHEN
   - a generate.ts-style first-line parse would capture the real description text
2. Score each dimension BETTER / SAME / WORSE. Quote both versions
   (or "absent in baseline") for every cell.
   - Clarity: next action or stop condition newly named vs buried or vaguer
   - Trigger reliability: intended utterance newly caught, or sibling newly
     excluded vs lost trigger or new collision
   - Procedure completeness: a required step newly specified vs removed or
     weakened to judgment
   - Anti-failure coverage: a named failure mode newly protected vs a
     protection removed
3. Known-bad — read that fixtures file. FAIL if the candidate matches any
   fixture (same shape, not only byte-identical). Do not invent shapes.
   Do not skip a fixture because the candidate added sentences.

Write < $d/gate.md > as:
- validity: PASS or FAIL + first miss
- four cells with quotes
- known-bad: match/no-match per shape
- Verdict: PASS or FAIL

PASS only if validity holds AND at least one BETTER AND zero WORSE AND no
known-bad match. 0 BETTER (rephrase, length-only, synonym churn) is FAIL.
Length is not a dimension. "Looks better" without quotes is FAIL.
```

You do not write `gate.md`. After the judge returns, go to step 6 even when `$d/gate.md` or a `Verdict:` line is missing. Do not invent either.

### 6. Commit only on PASS

Reuse `$skill_dir`, `$d`, and `$repo` from step 2. If `$skill_dir` is unset or `"$skill_dir/SKILL.md"` is not the live candidate, stop. Do not invent an add or restore path.

Parse `$d/gate.md` if it exists. Do not write it. PASS only when a `Verdict: PASS` line is present and no `Verdict: FAIL` line is present. Otherwise FAIL — missing file, missing `Verdict:`, unparseable, or FAIL.

**PASS**

Add only `$skill_dir/SKILL.md`, `$skill_dir/README.md` if present, paths backtick-quoted in the `- Change:` line (same contract as step 4), and `$repo/README.md` if generate.ts exists. Do not `git add "$skill_dir"`. If any other dirty path remains under `$skill_dir`, stop — do not commit.

```bash
change=$(sed -n 's/^- Change: //p' "$d/diagnosis.md")
prefix=$(python3 -c "import os; print(os.path.relpath('$skill_dir', '$repo'))")
git -C "$repo" add -- "$skill_dir/SKILL.md"
if [ -f "$skill_dir/README.md" ]; then git -C "$repo" add -- "$skill_dir/README.md"; fi
if [ -f "$repo/scripts/generate.ts" ]; then git -C "$repo" add -- README.md; fi
git -C "$repo" status --porcelain -u -- "$skill_dir" | while IFS= read -r line; do
  path="${line#???}"
  rel="${path#"$prefix"/}"
  case "$change" in
    *'`'"$rel"'`'*) git -C "$repo" add -- "$path" ;;
    *'`'"$skill_dir/$rel"'`'*) git -C "$repo" add -- "$path" ;;
  esac
done
if git -C "$repo" status --porcelain -u -- "$skill_dir" | grep -q '^.[^ ]'; then
  echo "extras remain under $skill_dir; stop; do not commit"
  exit 1
fi
git -C "$repo" commit -m "<prefix>improve-skill: <dimension> — <one line>"
```

`<dimension>` is the name from `diagnosis.md`. `<prefix>` is the caller's required prefix plus a trailing space, or empty.

Record the hash in `log.md`.

**FAIL**

Run the FAIL restore in `references/restore.md` next to this file (not `$skill_dir`): overlay `$d/baseline/`, then delete live paths with no baseline counterpart. Stop if `$d/baseline/SKILL.md` is missing. Then:

```bash
if [ -f "$repo/scripts/generate.ts" ]; then
  (cd "$repo" && deno run --allow-read --allow-write scripts/generate.ts)
fi
```

Do not commit. Record the judge's first failing clause in `log.md`, or `missing Verdict:` if the file or `Verdict:` line is absent.

You are not the judge. Do not override FAIL because the diff looks fine.

## Failure modes

| Failure mode | Protection |
|---|---|
| Author declares the new version better | Judge is a different agent; self-score is not a verdict |
| No subagent available | Stop at baseline; do not self-score |
| Kitchen-sink rewrite | Diagnosis names one hole; step 4 reverts dirty `$skill_dir` paths that are not `SKILL.md`, not generated `README.md`, and not Change-quoted |
| PASS add stages extras | Do not `git add "$skill_dir"`; add `SKILL.md`, generated `README.md`, and Change-quoted paths only; stop if extras remain |
| Edit with no snapshot | Step 2 runs before any write; stop if `$d/baseline/SKILL.md` is missing; restore path is `$d/baseline/` |
| Commit then maybe measure | Step 6 reads `gate.md` first; FAIL does not `git commit` |
| Judge returns no `gate.md` / no `Verdict:` | Step 6 still runs; missing or unparseable → FAIL restore; do not write `gate.md`; do not commit |
| FAIL restore or PASS add hits the wrong tree | Step 6 reuses `$skill_dir` from step 2; stop if unset or not the live candidate |
| FAIL restore leaves newly added `references/` | Always `rm -rf "$skill_dir/references"`; copy from `$d/baseline/references` only if that dir exists |
| FAIL restore leaves newly added files outside `references/` | Run `references/restore.md` next to this file: overlay `$d/baseline/`, delete live paths with no baseline counterpart |
| Untracked fallback omits `assets/` or extra root files | Step 2 else copies the whole `$skill_dir` tree; FAIL extra-delete cannot drop pre-existing extras |
| Catalog description becomes `>` | Single-line `description:` required; generate.ts after description edits |
| Hand-edited README catalog | generate.ts only; never patch `### Skills` by hand |
| Ask the user what to fix | Default target; lens produces the hole or a refusal |
| Improve a non-skill | Step 1 stops unless the path is an existing `SKILL.md` |
| More than one target | Step 1 stops; one cycle accepts one target |
| Sibling collision (duration work, code slop, graphs, metric loops, prose deslop) | Description excludes anneal, timeboxed-iterating, workgraph, autoresearch, catalog-deslop |
| Known-bad scored from memory | Judge reads this skill's `references/known-bad.md`; any fixture match → FAIL |
| Cosmetic-only / rephrase cycle | Step 3 refuses unless the hole quotes a missing action, stop, exclusion, or protection; user-asked polish is `nothing above the bar` |

## Red flags — stop and reread

- You are about to commit without a `Verdict: PASS` written by someone else.
- `$d/gate.md` is missing (or has no `Verdict:`) and you are about to commit or leave the candidate in the tree.
- You scored the change yourself.
- `diagnosis.md` lists more than one hole and you are fixing them all.
- You asked the user what to change.
- You are hand-editing a README.
- The working tree still has the candidate after a FAIL.
- You skipped baseline because it is a small edit.
- `$d/baseline/SKILL.md` is missing and you are about to edit.
- The target is untracked and `$d/baseline/` is missing live `assets/` (or extra root files) and you are about to edit.
- `$skill_dir` is unset (or not the live candidate) and you are about to `git add` or restore.
- Live `references/` is still present after a FAIL and `$d/baseline/references` was missing.
- Live `assets/` or an extra root file is still present after a FAIL and `$d/baseline/` did not have it.
- You are scoring known-bad from memory instead of reading this skill's `references/known-bad.md`.
- The hole is a wording preference (rephrase, shorter, synonym, restated protection) and you are about to edit anyway.
- The user named two skills (or all skills) and you are about to pick one or run both.
- The user named a path that is not an existing `SKILL.md` (or skill directory) and you are about to default to this skill.
- Dirty extras remain under `$skill_dir` (not `SKILL.md`, not generated `README.md`, not Change-quoted) and you are about to gate.
- You are about to `git add "$skill_dir"` (the whole directory) or extras remain under `$skill_dir` and you are about to commit.
