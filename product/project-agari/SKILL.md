---
name: project-agari
description: CPO-posture skill that declares a project's Agari (上がり) — the terminus that says when the product is complete or shipped. Requires CPO posture and halts if invoked outside a cpo session or the cpo subagent. Non-interactive by design — it drafts the terminus best-effort from the settled PRD and the project card, and instead of interviewing live it parks what it cannot settle in a companion open-issues file (open issues, choices to confirm) for the owner to answer async. On re-run it retires the owner's answered file whole to a permanent trail, folds their answers in, and when nothing is left unresolved it deletes the companion — its absence means the Agari is declared. Declared off the back of the settled PRD and before the SRS, as station 2 of a project's setup seed. Fills the project's agari.md in the instance repo. Use when declaring or revising what done means for a managed project. Do not use for the instance's identity or Michi (kensaiapp-michi), the PRD (product-prd), or a single change's done (the change pipeline).
license: MIT
metadata:
  author: Eyal Golan
  version: "2.7.0"
  created: "2026-07-04"
  category: product-definition
  tags: agari, cpo, project, done, declaration
  risk: safe
---

# project-agari

## Purpose

Declare a managed project's **Agari** (上がり — the product's "done"): the terminus that says
when the product is complete or shipped. The Agari is a **declaration**, settled with the
owner through files and committed into the project's `agari.md`.

This is the project-level sibling of `kensaiapp-michi`. Michi (道) declares the **instance's**
endless Way — the bearing the instance never finishes. Agari (上がり) declares a **project's**
terminus — the condition under which *this one product* is done.

---

## Posture

**CPO role required.** If invoked outside CPO posture (neither a `cpo:` session nor the `cpo`
subagent), stop and say: *"project-agari requires CPO posture. Switch? (Open a session with the
`cpo:` prefix, or run the `cpo` subagent.)"* Do not shed the role — this is the CPO's
declaration skill, the sibling of `product-prd`.

Take care not to confuse the CPO with the delivery-tier **Product Owner** who writes per-change
specs downstream — a different role that only shares the word "product". The Agari is the
CPO's.

**Non-interactive.** Throughout, **the owner** is the person whose product this is — the one
whose taste the terminus is settling. You work *with* them, but through files, not a live
interview:

- **Draft, don't ask.** Draft the whole Agari best-effort from the settled PRD and the project
  card. Never open a blank-page interview; never block waiting for an answer.
- **Surface, don't interrogate.** What the inputs can't settle goes to the **companion
  open-issues file**, in one of two buckets — an **open issue** (a question about the terminus
  you have no basis to decide) or a **choice to confirm** (a call you drafted that is the
  owner's to sign off). The companion template owns their shape.
- **The terminus is the owner's call.** Draft it and reason for it; never treat your draft as
  settled because it is defensible.

---

## What the Agari is (the journey model)

**Agari (上がり — "done", the terminus)** is the **project**-level declaration: the terminal
condition under which the product is complete or shipped, set by the CPO. A project reaches
its Agari; unlike the instance's Michi, it is a terminus, not an endless bearing.

- It is a **declaration, not a queue.** It names the terminus; it is not a task list or a
  milestone log. The work *toward* the Agari lives in the project's `journey/`
  (根回し Nemawashi seedbed, 宿場 Shukuba station, 飛び石 Tobiishi change-units).
- A project has **no Michi.** It serves the instance's Way (`system/michi.md`). Michi is
  instance-level and endless; Agari is project-level and a terminus. (Manifest:
  `<CORE>/doctrine/setup/kensaiapp_structure.md` §2.)
- Revising an Agari later is fine — a product's definition of "done" can be resharpened.

---

## The files and the loop

Everything this skill writes lives in the **instance** repo, beside the project card — the
Agari is a management artifact, not a product document. A caller names the **project**, never
the paths.

| File | What it is | Lifecycle |
|---|---|---|
| `system/projects/<name>/agari.md` | The Agari declaration — best-effort complete on every run. | Permanent; revised in place, never forked. |
| `system/projects/<name>/agari_open_issues.md` | The companion, holding what the run couldn't settle, in the buckets `agari_open_issues_template.md` defines. | Transient — exists only while something is unresolved. **Its absence is the done signal.** |
| `system/projects/<name>/trail/agari/cycle-<N>.md` | Each answered companion, retired whole. | Permanent. |

**Cycle numbering:** `N` is one higher than the **highest** `cycle-<N>.md` already in
`trail/agari/` — list the directory and take the max, so a removed or renamed cycle can't
collide with an existing one. The first is `cycle-1.md`; create `trail/agari/` if it isn't
there. Never overwrite an existing cycle.

**The loop, repeated until clean:**

1. The run drafts or revises the Agari and writes the companion with what it couldn't settle.
2. The **owner answers inline** — filling the companion's answer slots — and commits the file,
   then re-runs the skill.
3. The run **copies the answered companion whole to the next trail cycle**, folds the answers
   into `agari.md`, and rewrites the companion with only what is still unresolved.
4. When the answers resolve everything, the run is the close: it folds, copies the answered
   companion to the trail, and **removes** the companion instead of rewriting it — through the
   builder's `--rm`, never a hand-`rm`. **No open-issues file = the Agari is declared.**

**The close needs the owner's answers already committed.** Re-entry is inline answers, so the
first closing touch normally finds the companion dirty — and then it **changes nothing at
all**: no fold, no trail copy, no rewrite, no commit. It reports the state, asks for that
commit, and stops; the re-run after it is the close, start to finish. This is not a live
interview — it is a report with an ask. The reason is mechanical: the close removes the file
through git, and git refuses to remove a file carrying uncommitted edits, so a dirty companion
would strand a run that had already rewritten the Agari.

The trail is why the owner's reasoning survives. Folding rewrites the companion and the close
removes it — without the trail, what the owner decided and why would live only in git history.
It costs one copy on the same commit. It is the skill's job; the owner never manages it.

---

## When to Use

- **Station 2 of a project's setup seed** — the PRD is settled and the terminus is next, before
  the SRS. The ordinary trigger.
- An existing `agari_open_issues.md` is still present and the round needs continuing.
- The owner wants to **revise** an already-declared Agari.

**Do not use for:**
- The **instance's** identity or Way — that is `kensaiapp-michi`. An instance has a Michi and no
  Agari; a project has an Agari and no Michi.
- The **PRD** — that is `product-prd`, upstream of this and a precondition for it.
- A **single change's** done — that is the change pipeline's per-Tobiishi seal, not the
  product's terminus.

---

## Input material

- **`<product>/docs/PRD.md` — the settled PRD. A precondition, not a preference.** It is the
  primary source for the terminus: what the product is, who it is for, what success looks like
  and what is out of scope are already settled there, so the terminus is read off them rather
  than re-derived. Its location is `product-prd`'s to name — resolve the path from
  `<CORE>/../skills/cpo/.claude/skills/product-prd/SKILL.md`, never from a path remembered here.
  **If there is no PRD at the resolved path, halt and report**, pointing at `product-prd`. Do
  not draft from the project card alone: an Agari with no PRD behind it is a finish line for a
  product nobody has defined, and every later station would inherit it.
- **`system/projects/<name>/project.md`** — the project card. Its `Product path:` field resolves
  where the PRD lives. If more than one project exists and the target is ambiguous, halt and
  report the candidates.

---

## Workflow

### Step 1 — Identify the project, read current state

Identify the target project and read:

- `system/projects/<name>/project.md` — the binding, and the `Product path:` that resolves the
  PRD.
- the PRD, in full, at the resolved path — including its status line. A PRD still mid-round
  (its own companion still present) is a weak base for a terminus; say so in the companion
  rather than halting on it.
- `system/projects/<name>/agari.md` — the placeholder or the existing declaration.
- `system/projects/<name>/agari_open_issues.md` — the existing companion, if any. **This is the
  loop's re-entry point:** the owner's inline answers are read here. An answer marked *(the session's suggestion, accepted by the owner as shown)* or *(the
  session's suggestion, edited by the owner)* came from `project-setup`'s interview: it is the
  session's suggestion, which the owner accepted, so weigh it as that rather than as the owner's
  own words — except that in an edited one, what the owner changed is theirs — and never copy the
  mark into the document. The same marks reach the trail's first cycle; read them there the same
  way.
- `system/projects/<name>/trail/agari/` — every answer the owner has already given, and their
  reasoning. A value the owner set in an earlier cycle is authorized; changing it needs a fresh
  authorization. It also gives you the next cycle number.

### Step 2 — Draft the Agari and write the companion (no interview)

**Gate first.** When a companion existed at intake, its inline answers would resolve everything
unresolved, and the file is **uncommitted**, this run is the first closing touch and **writes
nothing** — skip the rest of this step and Step 3, and report at Step 4 asking for the commit.

Otherwise, draft or revise `agari.md`. Shape:

- **A lead sentence** naming the terminus in plain language — the condition under which the
  product is done or shipped.
- **Optionally, a short set of named conditions** (a few bullets) that together constitute
  "done", when the terminus is genuinely multi-part. Prefer one clear terminus over an inflated
  checklist — the Agari is a terminus, not a backlog.
- Keep the file's heading and framing note from
  `<CORE>/templates/project-templates/agari_template.md`, which owns the section shape, and
  remove its `PLACEHOLDER` blockquote — while that word stands, the chain reads the Agari as not
  yet declared and launches this skill again. Follow
  the instance's writing bar (`system/doctrine/writing_bar.md`).

Then write `agari_open_issues.md` from
`<CORE>/templates/project-templates/agari_open_issues_template.md` with everything the PRD and
the card couldn't settle. Typical items: is "done" a single terminus or a small named set; is a
condition really terminal, or is it journey work that belongs in the Nemawashi seedbed; does a
PRD success metric double as a terminal condition or merely track progress toward one.

On a re-run, copy the answered companion to `trail/agari/cycle-<N>.md` **before** folding, then
rewrite the companion with only what is still unresolved — or remove it, if nothing is.

### Step 3 — Commit through the builder

Commit **through the one commit builder**, never a hand-written `git commit` or a spelled-out
trailer block. Follow the shared recipe `<CORE>/doctrine/governance/commit_via_builder.md`; the
project-agari specifics:

- **Stage** `system/projects/<name>/agari.md`, the companion, and the trail cycle. The Agari
  always lives in the instance repo, so **`--repo .`** — never an external product repo.
- **The closing round passes `--rm system/projects/<name>/agari_open_issues.md`** so the
  removal rides in the same commit as the fold.
- **Identity — pass exactly one.** `--role CPO` (interactive `cpo:` session) or `--actor cpo`
  (the `cpo` subagent). Both derive `Role: CPO`.
- **`--directional`** — resolved against the project's journey (see
  `<CORE>/doctrine/governance/commit_format.md` §Directional trailer). The Agari is normally
  declared **as a station** of the project's setup seed, so there is normally an **open
  station**: `Shukuba: <YYYY-MM-DD>_<slug> — progress: <how this round advances the declaration>`. Only when
  the project is walking no station at all does the terminus become the referent —
  `Agari: <name> — progress: declared the <name> Agari`. Never `Shukuba: none`.
- **`--surface "Claude Code"`** and **`--co-authored-by "<your model> <noreply@anthropic.com>"`**.

```bash
python3 "<CORE>/tools/commit_builder.py" --repo . commit \
  --add system/projects/<name>/agari.md system/projects/<name>/agari_open_issues.md \
  --subject "cpo: declare the <name> Agari (round <N>)" \
  --body "<what the round settled, and what it left open>" \
  --role CPO \
  --directional "Shukuba: <YYYY-MM-DD>_<slug> — progress: <how this round advances the declaration>" \
  --surface "Claude Code" --co-authored-by "<your model> <noreply@anthropic.com>"
```

The flag forms and the staged-set guard are `<CORE>/doctrine/governance/commit_via_builder.md`'s, not
restated here. The `commit-msg` hook fires and a builder-made commit passes it; on hook failure, stop
and surface the error.

### Step 4 — Close and report

Report the commit with its SHA and which state the round ended in:

- **OPEN** — the companion is present; name what it is waiting on, and that the owner answers
  inline, commits, and re-runs.
- **CLOSING** — the first closing touch found uncommitted answers. Nothing was written. Ask for
  the commit and say the next run is the close.
- **DONE** — the companion is gone. The project's Agari is declared; what "done" means for the
  product is settled.

Do **not** enumerate downstream steps; settling the Agari is this skill's whole job.

---

## Output

| What | File | Settled |
|---|---|---|
| Agari | `system/projects/<name>/agari.md` | Drafted Step 2, committed Step 3 |
| Companion | `system/projects/<name>/agari_open_issues.md` | Written Step 2; removed on the closing round |
| Trail | `system/projects/<name>/trail/agari/cycle-<N>.md` | Written Step 2 on every re-run |

## Critical Rules

- **Non-interactive.** Draft the whole Agari and park what you can't settle in the companion.
  Never open an interview, never block waiting for an answer. The one stop is the first closing
  touch, and that is a report with an ask.
- **The PRD is a precondition.** No PRD at the resolved path, no Agari — halt and point at
  `product-prd`. Never draft a terminus from the project card alone.
- **The companion's absence is the done signal.** Remove it through the builder's `--rm` on the
  closing round, never a hand-`rm`, and never before the owner's answers are committed.
- **Retire answers to the trail before folding.** The owner's reasoning is copied whole; it is
  the skill's job, never the owner's.
- **Agari is a declaration, not a queue.** Name the terminus; do not turn it into a task list.
  Work toward the Agari lives in the project's `journey/`.
- **Agari is project-level.** Never write an Agari at instance level (the instance has a Michi
  and nothing reaches it). Never write a Michi into a project.
- **Instance repo, always.** `--repo .`. The Agari never lands in the product repo.
- **CPO posture required** — a `cpo:` session or the `cpo` subagent. Do not author the Agari in
  a neutral or wrong posture.
- **Self-contained close.** Settle the Agari and stop. Do not point the user at the skills that
  come after.
