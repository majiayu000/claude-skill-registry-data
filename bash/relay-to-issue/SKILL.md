---
name: relay-to-issue
description: >-
  Turn a finished /relay producer↔reviewer thread into a single checklist-style
  GitHub issue, filed in the repo the relay was actually about. Reviews the relay
  transcript, summarizes the conclusion (including agreements AND unresolved
  disagreements), and synthesizes the actionable findings into a markdown
  checklist issue body so each box can be spun off into a quick task. Use when
  the operator says "file this relay as an issue", "turn the relay into a GitHub
  issue", "open an issue from the relay review", "spin the review into tasks",
  "capture the relay follow-ups", or asks for the actionable summary of a relay
  to land in a repo's GitHub issues — typically AFTER a relay closes. Auto-detects
  the newest relay-system/<date>/<slug>.md thread (or takes a path/slug), resolves
  the target repo (cross-repo aware), dedups against an already-filed issue, and
  auto-posts via `gh`. NOT for scaffolding or running a relay (that is /relay or
  /relay-xyz); this runs once a relay has produced a thread.
---

# relay-to-issue

Convert a closed relay thread into one trackable GitHub issue: a short conclusion
plus a markdown checklist of the actionable follow-ups, posted to the right repo.

**Split of work:** the shipped `relay-to-issue.sh` does the deterministic plumbing
(locate the thread, resolve which repo, dedup, preflight `gh`, create the issue,
stamp provenance back). **You** do the judgment — reading the transcript and writing
the title + body. Don't reimplement the plumbing inline; call the script.

`SKILLDIR` below = this skill's directory (where this file and `relay-to-issue.sh`
live). Always call the script by its absolute path so it resolves from any CWD.

---

## Step 1 — Resolve + preflight (always first)

```bash
bash "$SKILLDIR/relay-to-issue.sh" resolve            # newest thread
bash "$SKILLDIR/relay-to-issue.sh" resolve --thread 2026-06-22/dueling-claudes
```

Read the printed block and gate on it **before reading the thread**:

- `GH_AUTH: missing` → STOP. Tell the operator to run `gh auth login`; do nothing else.
- `ALREADY_FILED: <url>` (not `NONE`) → STOP. This thread was already filed — report
  the existing URL. Only proceed if the operator explicitly wants a second issue
  (then pass `--force` in Step 4).
- `TARGET_REPO: AMBIGUOUS` → the thread cites paths in more than one repo. Show the
  `TARGET_CANDIDATES` and ask the operator which repo (or to add a `TARGET-REPO: owner/name`
  header to the thread). Pass the chosen repo as `--repo owner/name` in Step 4.
- `TARGET_REPO: UNRESOLVED` → ask the operator for `--repo owner/name`.
- Otherwise note `TARGET_REPO` + `TARGET_SOURCE` (explicit / declared / inferred /
  current-repo). If `inferred`, state which repo you're about to file into so a wrong
  inference is visible before posting.

## Step 2 — Read the thread

Read the resolved `THREAD` file in full — every block under `## Log`. Identify the two
roles (Producer/Reviewer, or Reporter/Maintainer) and **every graded finding**
(`[Blocker]` / `[Should]` / `[Nit]` / `[Pass]`) and its disposition.

## Step 3 — Empty-relay guard (don't file noise)

If the relay closed `Approved`/`Closed` with **no** `[Blocker]`/`[Should]` items, no
parked/disagreed items, and nothing actionable left to do → **STOP. Do not create an
issue.** Report: "Relay closed clean — no actionable items, nothing filed." A hollow
issue is worse than none.

## Step 4 — Write the body and file it

Write the issue body to a temp file using the template below, then file:

```bash
bash "$SKILLDIR/relay-to-issue.sh" file \
  --thread "<abs thread path from resolve>" \
  --title  "Relay follow-ups: <slug> — <one-line gist>" \
  --body-file "$TMPDIR/relay-issue-body.md" \
  --labels relay-followup
  # [--repo owner/name]  only if resolve said AMBIGUOUS/UNRESOLVED
  # [--inbox]            also drop a PROJECT/1-INBOX/GH-<n> pointer (only when the
  #                      issue lands in THIS repo) — keeps the ledger closed-loop
  # [--force]            file a second issue for a thread already filed
```

The script auto-posts, prints the issue URL, and appends a provenance+dedup stamp to
the thread (`<!-- relay-to-issue: filed <url> @ <hash> on <date> -->`). Report the URL
to the operator.

### Issue body template

```markdown
## Relay follow-ups — <slug>

**Source:** `relay-system/<date>/<slug>.md` @ `<HEAD short hash>` · target repo `<owner/name>`
**Outcome:** <Closed | Approved | Changes requested> after <N> round(s) · Producer `<id>` ↔ Reviewer `<id>`

### Conclusion
<2–4 sentences: what the two agents concluded, and whether they converged.>

**Agreed / dispositioned**
- <finding that was accepted, fixed, or explicitly declined-with-reason>

**Disagreements / parked** (or "None")
- ⚠️ <unresolved point — also appears as a DECIDE box below>

### Actionable checklist
- [ ] <task> — `[Blocker]` _(Round N)_
- [ ] <task> — `[Should]` _(Round N)_
- [ ] ⚠️ DECIDE: <unresolved/disagreed item> _(needs a human call)_
- [ ] <optional cleanup> — `[Nit]` _(Round N)_

<!-- Each box is a spin-off-ready task. Generated by relay-to-issue. -->
```

**Body rules**
- One issue, one checklist (the operator's chosen shape). Every box must be a concrete,
  independently-actionable task — not a restatement of a whole round.
- Keep `[Blocker]` and `[Should]` items; fold `[Nit]`s in only if genuinely worth doing.
- Never drop a disagreement or parked item — surface it as a `⚠️ DECIDE` box.
- Preserve grades and cite the source round so each task is traceable.

---

## Cross-repo notes

- The "repo the relay was about" is the repo whose files were under review — often **not**
  the harness repo (relays can review a foreign repo; see GH-11 cross-repo targeting).
- Threads don't declare their subject repo in a machine-readable field today, so the script
  **infers** it from the absolute paths cited in the thread. To make it explicit and remove
  any ambiguity, add a header line to the thread: `TARGET-REPO: owner/name`. That always wins
  over inference.
- The script **never auto-posts to a guessed repo**: if paths point at more than one repo it
  exits ambiguous and asks for `--repo`.

## Prerequisites

- `gh` installed and authenticated (`gh auth login`), with access to the target repo.
- Run un-sandboxed if `gh` needs the keychain.

## What this skill does NOT do

- It does not scaffold or run a relay — that's `/relay` (portable) or `/relay-xyz` (this repo's
  harness). This is the **post-relay** step.
- It does not edit code or the thread's review content — its only writes are the issue, the
  one-line provenance stamp, and (opt-in) a 1-INBOX pointer.
