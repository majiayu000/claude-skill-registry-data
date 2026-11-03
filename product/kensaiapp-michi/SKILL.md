---
name: kensaiapp-michi
description: Posture-neutral skill (CTO / principal-PM level, no role prefix) that settles a kensaiapp instance's identity and declares its Michi (道 — the endless Way it steers by), in that order. Works WITH the user — drafts first, interviews only the genuine gaps leading with a recommendation, lets the user make the calls, and commits each artifact once confirmed. Fills the `kensaiapp.md` § "What this is about" and `system/michi.md` placeholders that setup-kensaiapp stamps, then reconciles the README to match. Use when declaring or revising what a kensaiapp instance is and the Way(s) it commits to — at instance setup, or later to revise identity / add a Way; also when handed a filled-in identity brief for an instance.
license: MIT
metadata:
  author: Eyal Golan
  version: "1.3.3"
  created: "2026-07-04"
  category: setup
  tags: identity, michi, direction, instance-setup, declaration
  risk: safe
---

# kensaiapp-michi

## Purpose

Declare, in one collaborative session, the identity and direction of a kensaiapp
instance — settling **three faces of the same identity**, each drafted, confirmed,
and committed on its own:

1. **`kensaiapp.md` § "What this is about"** — what this instance *is*. Settled **first**.
2. **`system/michi.md`** — the 道 Michi: the endless Way(s) the instance steers by.
   Drafted to *follow from* the settled identity.
3. **`README.md`** — the front door. Reconciled **last**, once identity is known.

The order is load-bearing: the Way follows from what the instance is for, so the
identity is settled before the Michi is drafted, and the README is written after
both — by then the one fact that decides its shape (does this instance go public?)
is known, not guessed.

---

## Posture

This is **posture-neutral, top-level direction work** (CTO / principal-PM level).
It is **not** a pipeline role — no loader, no `<role>:` prefix, no inbox. Do not
adopt architect / PM / developer posture. Work **with** the user as a thinking
partner on what the instance is:

- **Draft first.** Hand the user a first draft to react to — never open with a
  blank-page interview. The draft is what makes the gaps concrete.
- **Interview only the genuine gaps** — the forks the draft can't resolve. For
  each, **lead with your recommendation and your lean**, then let the user decide.
  Do not present a bare menu of options; do the reasoning, surface a position.
- **The user makes the calls.** This is owner-level identity — taste and direction
  are theirs. Your job is the draft, the reasoning, and the honest recommendation.

---

## The Michi it declares (the journey model)

**Michi (道 — "the Way")** is the **instance**-level declaration: the endless
guiding goal(s) the instance commits to and never finishes — the bearing it steers
by. It is a **declaration, not a queue** — set once, never worked-and-retired.
**1..N Ways** per instance. There is **no Agari** (no "done") at instance level; nothing
reaches the Michi.

A **project** (`system/projects/<name>/`) has **no Michi** — it serves the
instance's Way, and has its own Agari (上がり, the product's "done"). Keep the two
straight: the Michi belongs to the whole instance, not to any one project inside it.

Because a Michi is set-once, **adding a Way appends a new heading — it never
overwrites an existing Way.** Revising identity (face 1) is fine any time; retiring
a Michi is not part of this skill.

---

## When to Use

- A fresh instance still carries the placeholders `setup-kensaiapp` stamped —
  `system/michi.md` says "PLACEHOLDER — declare at instance setup" and `kensaiapp.md`
  § "What this is about" holds the `<One or two sentences…>` stub.
- The user wants to declare, or later revise, **what this instance is** and the
  **Way(s)** it steers by.
- The user hands you a filled-in identity **brief** (see `references/brief_template.md`).

**Do not use for:**
- A **project's** requirements or "done" — that is `product-fdr` (the behavioural contract)
  and the project's `agari.md`. Michi is instance-level; a project has none.
- Adding a *feature* to a product — that is the change pipeline (`development-specs`).

---

## Two input modes

- **Brief mode** — the user (or a launching session) hands you a filled-in brief
  from `references/brief_template.md`. Use it as the starting material for the
  face-1 draft; you still interview the gaps it leaves open.
- **Interview mode** — no brief. Ask three framing questions before drafting:
  *what is this instance for, where does it sit (upstream/downstream), and does it
  go public?* Then draft. Keep it to those three — the draft surfaces the rest.

---

## Workflow

### Step 1 — Read current state and intake

Read the two identity placeholders as they stand now:

- `kensaiapp.md` § "What this is about"
- `system/michi.md`

Also skim `README.md` so you know what the README currently claims (it is often a
stale copy of another instance's — see Step 4). If a brief was provided, read it.
If not, ask the three framing questions above. Do not draft until you have either a
brief or the three answers.

### Step 2 — Settle the identity (face 1)

Draft `kensaiapp.md` § "What this is about": **2–4 plain-language paragraphs** saying
what this instance is — its role, what it's for, and where it sits relative to any
upstream/downstream instances. Follow the instance's writing bar
(`system/doctrine/writing_bar.md`).

Hand the draft to the user. Interview the genuine gaps — leading with your
recommendation each time. Iterate until the user confirms.

**Commit face 1 on its own** once confirmed. Then move on — do not batch it with
the Michi.

### Step 3 — Declare the Michi (face 2)

Now draft `system/michi.md`, **derived from the identity just settled**. One `##`
heading per Way; **1..N Ways**. Each Way is the endless bearing, not a task —
phrase it as a direction the instance never finishes, not a deliverable it ships.
Also retitle the file's top heading to name **this** instance
(`# 道 Michi — <instance>'s Way(s)`).

**Give each Way a slug.** Write every Way heading as
`## Way N — <title>  (slug: `<kebab-slug>`)`. The slug is the greppable name the
commit-format doctrine's `Michi:` trailer uses to record which Way a commit serves
(`Michi: <way-slug> — serves: …`, per `<CORE>/doctrine/governance/commit_format.md`) —
without it, instance-level commits have no Way to reference. Keep the slug short,
kebab-case, and **stable**: retitling a Way is fine, but changing its slug breaks
`git log --grep`.

If `system/michi.md` already declares Ways, **append** — never overwrite an
existing Way (a Michi is set-once).

Hand the draft over, interview the gaps (how many Ways? what bearing does each
name?), lead with your lean. **Commit face 2 on its own** once confirmed.

### Step 4 — Reconcile the README (face 3)

The README is the third face of the same identity. A fresh instance's README is
predictably wrong: it is inherited as the **public product's README verbatim**
(clone-and-run "Getting started", "Updating", "Customizing"). Whether that is wrong
depends on one identity fact settled in Step 2 — **does this instance go public?**

- **Internal instance** (a workbench that will not be cloned-and-run) → the whole
  clone-and-run framing is wrong. Replace it with a **pointer-style README**: a
  short identity summary (title + a few paragraphs + a posture note), then a
  "Where the identity lives" list linking to `kensaiapp.md` § "What this is about",
  `system/michi.md`, and `<CORE>/doctrine/governance/system_anatomy.md`, then a brief
  "Working in here" note. Keep that scaffolding as boilerplate; the only
  instance-specific bits are the identity paragraphs and the active project name.
  A pointer barely rots, which is why it is safe to leave in sync.
- **Public-bound instance** → the inherited README is *nearly right already*. Keep
  the clone-and-run scaffolding, adapt only the top identity paragraphs, and leave
  final polish to an editorial pass before publish. **Do not clobber a real
  public-facing README** — adapt its top, don't rewrite it.

Draft the README, hand it over, confirm, and **commit face 3 on its own**.

### Step 5 — Close

Report the three commits (identity, Michi, README) with their SHAs. State plainly
that identity and the Way are settled, and name anything left (e.g. a public
instance's README polish deferred to an editorial pass). Nothing in-flight.

---

## Output

Three files, three separate commits:

| Face | File | Settled |
|---|---|---|
| Identity | `kensaiapp.md` § "What this is about" | Step 2 — **first** |
| Michi | `system/michi.md` | Step 3 — follows from identity |
| Front door | `README.md` | Step 4 — **last**, branches on public/internal |

## Critical Rules

- **Identity before Michi.** The Way follows from what the instance is for. Never
  draft the Michi before the identity is settled and committed.
- **Draft before interviewing.** Open every face with a draft, not a blank-page
  question. The draft makes the gaps concrete; interview only what the draft can't
  resolve, and lead with a recommendation, not a menu.
- **The user owns the calls.** This is owner-level direction — taste and priority
  are the user's. Recommend and reason; do not decide identity or Ways for them.
- **One commit per face.** Identity, Michi, and README commit separately — three
  commits, never a batch. Each is confirmed before it is committed.
- **A Michi is set-once.** Add a Way by appending a heading; never overwrite or
  retire an existing Way. Revising the identity (face 1) is fine any time.
- **Every Way carries a slug.** Each Way heading ends with `(slug: `<kebab-slug>`)`.
  The `Michi:` commit trailer references it (per
  `<CORE>/doctrine/governance/commit_format.md`); a slug-less Way leaves instance
  commits with nothing to cite. The slug is stable — retitle freely, but don't
  change a slug once commits reference it.
- **No posture.** This skill is posture-neutral. Do not adopt a pipeline role, read
  a loader, or touch an inbox. If invoked mid-role, drop the role for this work.
- **Michi is instance-level.** Never write a Michi into a project. A project serves
  the instance's Way and has its own Agari instead.
- **Don't clobber a real public README.** For a public-bound instance, adapt the
  inherited README's top; leave its clone-and-run body and final polish alone.
