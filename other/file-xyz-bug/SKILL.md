---
name: file-xyz-bug
description: File a bug against the xyz-3-agents-swarm harness from ANY repo or session — lands a PDDA-compliant capture in that repo's PROJECT/1-INBOX/ (GH-<n>-*.md), files the tracking GitHub issue, and parks a one-line ROADMAP pointer, without touching the repo you are standing in. Use when the xyz harness misbehaves while you are working somewhere else — a relay/marathon driver fails, `tick` misbehaves, a turn shim exits wrong, a vendored `.xyz/` drifts, an xyz skill (relay-xyz, consult, hq, xyz) breaks — and you want it recorded where it will actually be triaged instead of lost in the current session. Trigger on /file-xyz-bug, "file an xyz bug", "report this to the swarm repo", "log this harness bug upstream", "send this bug to xyz". NOT for bugs in the repo you are currently working on (use that repo's own intake, e.g. /idea or /triage).
---

# /file-xyz-bug — cross-repo bug front-door into the xyz intake

You hit a harness bug **while working somewhere else**. This skill records it in the repo that
owns the harness — `xyz-3-agents-swarm` — as a proper PDDA intake capture, then gets out of the
way so you can go back to what you were doing.

It is the **inbound-from-elsewhere** sibling of `/idea`
(net-new ideas, same repo) and `/triage` (incoming external reports). Same intake format, same
preview-first discipline, same `PROJECT/PDDA.md` contract. The one thing it adds is **cross-repo
addressing**: everything is written to the *intake* repo, and **nothing** is written to the repo
you are standing in.

## Usage

```
/file-xyz-bug <one-line what broke>   # harvest → single preview → capture (issue + doc + park)
/file-xyz-bug                         # ask for the one-liner first
```

## Steps

0. **Locate the intake repo (preflight).** Never hardcode a path — this skill runs from foreign
   repos, so a cached absolute path is the first thing that breaks. Run the bundled locator:

   ```bash
   for L in "${XYZ_REPO:+$XYZ_REPO/skills/2-daily/file-xyz-bug/find-xyz.sh}" \
            "$HOME/.claude/skills/file-xyz-bug/find-xyz.sh" \
            "$(git rev-parse --show-toplevel 2>/dev/null)/skills/2-daily/file-xyz-bug/find-xyz.sh"; do
     [ -n "$L" ] && [ -x "$L" ] && break
   done
   [ -x "$L" ] || { echo "file-xyz-bug: locator not found — set XYZ_REPO to your xyz-3-agents-swarm clone"; exit 1; }

   eval "$("$L" --env)" || exit 1   # XYZ_REPO, XYZ_INBOX, XYZ_BRANCH, XYZ_DIRTY, XYZ_SLUG,
                                    # XYZ_CALLER, XYZ_CALLER_NAME, XYZ_HAS_GH
   "$L" --check                     # intake path + gh availability + branch/dirty warnings
   ```

   If it can't resolve, **stop and ask** for the clone path — do not guess, and do not fall back
   to writing the report into the current repo (that buries it exactly where nobody triages).
   Read `--check`'s warnings before Step 4: they decide whether committing is safe.

   > **These exports do not survive to your next Bash call.** Each tool invocation is a fresh
   > shell — only the working directory persists, not environment. `$XYZ_SLUG` in a later call
   > expands to empty, and `gh issue create --repo ""` fails (or worse, guesses). So in **every**
   > later command that needs these values, either re-resolve in the *same* invocation —
   > `eval "$(<locator> --env)" || exit 1 && gh issue create --repo "$XYZ_SLUG" …` — or paste the
   > literal absolute values you read out of `--check`. Never write a bare `$XYZ_*` reference
   > into a command that did not itself just set it.

1. **Harvest first, ask second.** Most of a good bug report is already in *this* session's
   transcript. Reconstruct from what you have before asking the operator anything:

   | Field | Harvest from |
   |---|---|
   | What broke | the failing tool call / the operator's one-liner |
   | Exact command | the actual invocation, verbatim, including env prefixes |
   | Observed | the real error text + exit code |
   | Where | `XYZ_CALLER_NAME` (bare repo name — the locator pre-sanitizes it; never the full path) |
   | Harness version | `git -C <intake repo> rev-parse --short HEAD`; plus `.xyz/VERSION` in the caller repo if vendored |
   | **Runtime** | which twin actually **ran**, not the language of the buggy function — **Python** (default, `XYZ_PYTHON` unset/`=1`) or **Bash** (`XYZ_PYTHON=0`). A `.py` traceback ⇒ Python; an inline `line NNN:` shell error ⇒ Bash. If unsure which ran, check whether `XYZ_PYTHON=0` was set — unset means Python. `parity` is only when the two twins *diverge* at the same commit; a shared bug the Python entry point reaches by **delegating to** the bash core (e.g. `rtl.py` shelling out to `relay-turn-lib.sh`) is still `runtime:python` by the entry point that ran, **not** parity. Drives the `runtime:*` label in Step 4. |

   Then ask **only what you could not harvest**, capped at three questions (prefer `AskUserQuestion`):
   1. **Expected behavior** — what should have happened. Nearly always needs the operator; the
      transcript shows the failure, not the intent.
   2. **Reproducibility** — `every time` / `intermittent` / `once so far`. Drives the severity rating.
   3. **Blocking?** — is the operator stuck right now, or is this a "log it and move on"?

   Never invent a repro you did not actually observe. If a step is inferred rather than seen, mark
   it `TODO(operator)` — a plausible-but-wrong repro costs a triager more than a missing one.

2. **Redact before you write.** The harvested command lines and error output are the highest-risk
   field in this skill: they come from a *different* repo and routinely carry tokens, API keys,
   `Authorization:` headers, connection strings, and absolute paths with a client's name in them.
   Scan every harvested block and replace secrets with `<redacted>` before the preview. The issue
   body is **public on GitHub** — this is the step that keeps a foreign repo's secret from being
   published by a convenience skill.

3. **Preview the whole capture as one bundle, then get ONE confirmation.** Render together: the
   `gh issue create` title + body, the full capture doc (with a `GH-<new>` placeholder), and the
   ROADMAP line. Say plainly which repo each lands in. This single preview **is** the human
   checkpoint — nothing is filed or written before the operator confirms once.

4. **On confirm, execute in order** (issue-first SOP; a harness bug is above the trivial-fix bar):
   - `gh issue create --repo <owner/repo>` → capture the returned number `<n>`. Re-resolve the slug
     in the same invocation or paste it literally (see Step 0's shell-state note). **Run `gh`
     un-sandboxed** (`dangerouslyDisableSandbox: true`): the Bash sandbox blocks the keyring and
     produces a false "auth broken". If the operator named an existing issue, reuse that number,
     skip creation, and check for an existing `GH-<n>-*.md` to **update** rather than writing a second doc.
     - **Tag the runtime.** Pass `--label "runtime:<python|bash|parity>"` matching the Runtime you
       harvested in Step 1, so triage can tell a Python-twin bug from a legacy-Bash-path bug at a
       glance (the harness runs Python by default since the flip; a bug seen only under `XYZ_PYTHON=0`
       is `runtime:bash`, a twin divergence is `runtime:parity`). These three labels already exist in
       the intake repo — don't recreate them. If you genuinely can't tell which twin ran, omit the
       label rather than guess; a wrong runtime tag misroutes triage.
   - Write `<intake repo>/PROJECT/1-INBOX/GH-<n>-<SHORT-SLUG>.md` (SCREAMING-KEBAB, ~2–4 words, no
     zero-padding). `<SHORT-SLUG>` is a *title* slug (e.g. `RELAY-DRIVE-EXIT6`) — do not confuse it
     with the locator's `XYZ_SLUG`, which is the `owner/repo` origin slug and contains a `/`.
   - Park the ROADMAP pointer (Step 5).
   - **Do not commit and do not push.** See Guardrails — this is the rule most likely to bite.

5. **Park the intake in the RELEASES DB** — run against the resolved XYZ checkout, never
   the caller's repo (the CLI writes that repo's `releases.db`): 
   `(cd "$XYZ_REPO" && python3 utils/py/releases_app.py --root "$XYZ_REPO" roadmap add …)`;
   or `hq park <project> …`, which resolves the target itself — required at capture time
   (`ROUTER.md`, `PROJECT/PDDA.md` → RELEASES DB contract; ROADMAP.md is retired, GH-269):

   ```md
   - **GH-<n> — <short title>** (<YYYY-MM-DD>) - <one-line symptom>. Bug filed via /file-xyz-bug
     from `<caller repo name>`. Issue [#<n>](<issue-url>). ->
     [PROJECT/1-INBOX/GH-<n>-<SHORT-SLUG>.md](PROJECT/1-INBOX/GH-<n>-<SHORT-SLUG>.md)
   ```

6. **Report + verify.** Run `bash <intake repo>/utils/pdda/pdda.sh roadmap-coverage` to confirm the
   capture is parked. Note `pdda.sh frontmatter` scans `2-WORKING` only — it does **not** validate a
   1-INBOX capture, so don't claim it did. Then report back in three lines: the issue URL, the doc
   path, and **the fact that the capture is uncommitted in the intake repo** (with the branch it is
   sitting on), so the operator knows there is one action left that only they should take.

## Doc template

Frontmatter — PDDA minimum for a `GH-*` capture, bug-shaped. Ratings are always provisional
(PDDA's selection rule excludes `ratings_provisional: true` docs from auto-eligibility, so a rough
guess parks itself out of auto-selection rather than misfiring):

```yaml
---
title: <concise symptom title>
status: Proposed (1-INBOX — not yet active)
created: <YYYY-MM-DD>
owner: <git config user.name, else noel>
gh_issue: <n>
source: <origin issue URL>
doc_type: bugfix
complexity: <1-5>
risk: <1-5>          # blocking + every-time → 4-5; cosmetic + once → 1-2
effort: <1-5>
phases: 1
ratings_provisional: true
reported_from: <caller repo name>          # provenance: which repo hit this
harness_commit: <short sha of the intake repo at report time>
non_goals:
  - <what fixing this deliberately will not cover>
related:
  - <sibling issues/docs, or omit the key>
goal: >
  <2–4 lines: what "fixed" means, in observable terms.>
---
```

Body:

```md
# GH-<n> — <Title>

> **1-INBOX capture**, not the active-work doc — no `## Status` table yet. On promotion to
> `PROJECT/2-WORKING/`, add the status table + per-phase QA gates and carry `gh_issue` forward
> (`PROJECT/PDDA.md` → GitHub issue intake).

## Symptom
<the one-line report, verbatim>

## Environment
- **Observed from:** `<caller repo name>` (<vendored `.xyz/` | centralized harness>)
- **Harness commit:** `<short sha>`
- **Worker/CLI:** <codex | agy | claude | tick | n/a>, version if known
- **Runtime:** <Python (default) | Bash (`XYZ_PYTHON=0`) | parity (both / diverges)> — matches the `runtime:*` issue label
- **Sandbox:** <on | off> at the time of failure

## Reproduction
1. <exact step — the real invocation, redacted>
2. <…>

**Expected:** <what should have happened>
**Observed:** <what actually happened, incl. exit code>
**Frequency:** <every time | intermittent | once so far>

<!-- Redacted transcript excerpt. Keep it SHORT — the failing lines, not the whole log. -->
```text
<error output, secrets replaced with <redacted>>
```

## Impact
<who/what is blocked, and whether a workaround exists>

## Phase 0 — Diagnose & scope
> Discovery phase: its findings are written **back into this doc** before its QA gate can pass
> (`PROJECT/PDDA.md` → Discovery & spike phases).

### Checklist
- [ ] Reproduce it in the intake repo (not just in the reporting repo)
- [ ] Locate the responsible script/path — name the concrete write-set
- [ ] Decide fix vs. guard-and-document; reuse an existing code path before adding one (`/ponytail`)
- [ ] Set/correct the triage ratings; clear `ratings_provisional` once real

### QA checklist — Phase 0
- [ ] The repro is confirmed from the report, not assumed
- [ ] A regression test covers the failure path before the fix lands
- [ ] The fix composes with the existing harness rather than adding a parallel path
```

## Guardrails

- **Write to the intake repo only.** Never create, edit, or stage a file in the repo you are
  standing in — not a note, not a pointer, not a breadcrumb. The operator invoked this skill
  mid-task in someone else's tree; leaving artifacts there is the failure mode, and a cached
  absolute path left behind is worse than none at all.
- **Never commit or push the capture.** Write the files and stop. The intake repo is shared with
  marathon and relay drivers that can leave it dirty or parked on a `marathon/*` branch, and a
  commit from a foreign session can land off-branch or orphan a peer agent's work. `--check` warns
  you; report the uncommitted path and let the operator commit deliberately. (This is a real
  incident class in this repo, not a hypothetical.) If they explicitly ask you to commit, re-check
  `git -C <intake repo> branch --show-current` first and say which branch you are committing to.
- **Redact before filing.** The issue body is public. Secrets and client-identifying paths harvested
  from a foreign repo get `<redacted>` — see Step 2.
- **One preview, one confirmation.** Issue + doc + ROADMAP line rendered together; nothing outward-
  facing happens until the operator confirms once. `gh issue create` is durable and public.
- **Don't fix the bug here.** This skill files it. Diagnosing or patching the harness is separate
  work that starts from the parked capture — and a capture is not marathon-fireable until a human
  promotes it `1-INBOX → 2-WORKING`.
- **One doc per issue.** Check for an existing `GH-<n>-*.md` before writing.
- **Paths in the doc:** repo-relative for anything inside the intake repo. The *reporting* repo is
  external — name it (`bloomz-prod-08-15`), don't paste the operator's full home-directory path.
- **`gh` runs un-sandboxed.** A sandboxed `gh` gives a false auth failure; retry un-sandboxed before
  concluding auth is broken. If `gh` is genuinely unavailable, still write the doc — use a
  `GH-UNFILED-<SHORT-SLUG>.md` name, set `gh_issue: TODO`, and tell the operator the issue still needs filing.
