---
name: verify-bootstrap
description: "Set up a repo's machine gates (format, lint, type check, security, dependency audit, tests), or audit whether existing gates have gone stale. Use when a repo has no automated gate (lint を入れて), or its tools may be outdated."
compatibility: Developed and tested on Claude Code; portable to other Agent Skills-compatible agents.
license: MIT
metadata:
  author: shimo4228
  version: "1.0"
user-invocable: true
origin: shimo4228
---

# verify-bootstrap — set up machine gates in a repo

Humans cannot read code as fast as AI writes it. So judging structural correctness is
**moved to machines**. For each repo, this skill sets up
the best checking tools available at that moment.

## What this skill does not carry (the core of the design)

**It carries no list of tool names. It carries no language-detection table either.** Tools go stale
(flake8 + black + isort → ruff happened within two years). A fixed table rots,
and the rotten table gets handed out to repos.

It carries only **how to investigate, and a contract**:

- a procedure that enumerates what the repo actually contains (no static language list)
- what to ask search-first for each category
- the contract of the generated `.claude/verify.sh` (the only thing a pre-commit hook or CI needs to know)
- the discipline of strictness and staleness detection

As a result, the same procedure works for languages and tools that did not exist when this skill was written.

## Modes

| Mode | Trigger | What to do |
|---|---|---|
| **bootstrap** | No `.claude/verify.sh` | Run Steps 1–6 |
| **audit** | It already exists (`--audit` / "audit" / 「棚卸し」) | Re-run Step 1, re-derive the selections in `.claude/verify.md` with search-first, and propose the differences |

## Step 1 — Enumerate what the repo actually contains (detection, no static table)

Do not guess. **Measure.**

```bash
# Extension distribution of tracked files (top) — excludes generated and dependency directories
git ls-files | sed -n 's/.*\.\([A-Za-z0-9_]*\)$/\1/p' | sort | uniq -c | sort -rn | head -20
# Which build/dependency manifests exist
git ls-files | grep -iE '(^|/)(pyproject\.toml|package\.json|Cargo\.toml|go\.mod|Gemfile|pom\.xml|build\.gradle.*|[^/]*\.xcodeproj/.*|Package\.swift|mix\.exs|composer\.json|Makefile|justfile)$'
# Traces of existing gates (prevents installing twice)
git ls-files | grep -iE '(pre-commit-config|lefthook|\.github/workflows/|trunk\.yaml|\.golangci|\.eslintrc|ruff\.toml)'
```

The manifest grep above is **a discovery aid, not an authority**. The first command's extension distribution is the source of truth;
when an ecosystem shows up that the grep does not list, pass it straight to Step 2 (do not edit the table and
add it to this skill — carrying no table is this skill's design).

Include prose, configuration, and schemas. Code is not the only target of a gate
(Japanese prose in Markdown, YAML, CI definitions, and shell scripts can all be checked by machine).

## Step 2 — Research the current best tool for each category

For each detected ecosystem, fill in the **6 categories**. When a category cannot be filled, write "none" explicitly
(an empty cell and "this language has nothing for it" are different things).

| category | Question |
|---|---|
| **format** | Normalize formatting. Remove diff noise so that only changes in meaning are left to review |
| **lint** | Structural errors, complexity, dead code |
| **type check** | Contracts expressible as types. For an untyped language: "is there a way to introduce type annotations incrementally?" |
| **security** | Dangerous constructs and leaked secrets (if a pre-commit hook or CI already runs a secret scan, check for duplication) |
| **dependency** | Known vulnerabilities, unused dependencies, licenses |
| **test** | Test runner and coverage measurement |

**Do not rely on defaults for budget rules (rules that need a threshold: complexity, function/file length, bundle size, etc.).**
Major linters usually ship budget rules OFF by default (because the thresholds are opinionated) —
under "maximum strict" operation they structurally slip through (a 2026-08-28 measurement found zero coverage:
no budget rule in 104 lint/build configs across 82 repos). Ask about them explicitly when filling the lint category. When the stack's standard toolchain
has budgets on by default (e.g. SwiftLint's cyclomatic_complexity / file_length), confirm them and
record one line in verify.md. Do not set thresholds globally — distributions differ several-fold
between repos (same measurement).
Measure the distribution over the whole existing corpus first, then place the threshold where only current outliers turn red
(the exemption-boundary principle of the skill `review-to-lint`. A threshold that turns the gate red on day one is a design error).

**The lint / type check selection policy is LLM-first** (the reader and the editor are both LLMs; humans do not
read the code. Rationale: AKC ADR-0025 (LLM-first artifact readability)). Build the select set on the same 4 axes regardless of language:

1. **Bug-class detection** (undefined names, unused code, known dangerous patterns, type contradictions) — the core of an
   uncorrelated verifier. Highest priority
2. **Canonical form** (formatter, import order) — for diff stability, not for the eye. When another session
   touches the code, no spurious diff appears = golden files and reviews stay quiet
3. **Budget** (complexity, file length) — an edit-reliability budget for the next editor, who works within a limited context
   (thresholds from the distribution measurement above)
4. **Explicit type enforcement at boundaries** — types are a machine-verifiable specification and the frozen edge for regeneration and edits by other sessions.
   Production side only (test functions are not consumed boundaries, so they are excluded).
   Example implementation in Python: ANN001-003 + ANN201 + ANN401, excluding `tests/**`

**Do not select human-aesthetics rules (docstring style, naming conventions, comment formatting).** They are not something
to remove later; they are never put in. A rule whose only justification is "hard for humans to read" has no LLM-first
justification.

For each category, **call the `search-first` skill** (do not call WebSearch directly — search-first comes before
adding a dependency or writing your own utility). Every question must include the point in time, "**as of today's date**",
and "has there been a migration away from the established alternative?".
Do not answer with the standard tool you remember — that is exactly what this skill exists to prevent.

When the report comes back, confirm the following before adopting:

- **Was the last release within 12 months?** (do not bring an abandoned project into a new repo)
- **Can it run as a single binary, or on demand with an exact version pin?** (e.g. `uvx <tool>@<x.y.z>` /
  `npx <pkg>@<x.y.z>` / `brew`. Does it run without polluting the repo's runtime environment?)
- **Can the configuration be carried in?** (can strictness be declared, and exceptions allowlisted?)
- **Does the same thing run in CI and locally?** (if they diverge, the local gate becomes a formality)

## Step 3 — Install at maximum strictness

**The default is maximum strict.** AI does not complain about strictness, so the balance that used to be loosened
on account of "human patience" tips toward correctness.

- Do not leave warnings as warnings — **make them errors**
- **Forbid** type escape hatches (`any` equivalents, comments that suppress type checking)
- **Pin versions** (like `ruff==0.16.0`. Fixes the supply chain. Bumps are manual)
- Exceptions go **in the config file's allowlist with a reason, not as inline suppression comments**
  (inline suppressions lose their reasons and multiply without limit)
- When a repo-specific exception is needed, **first move the stack toward the standard** — only what remains after that
  goes into the allowlist with a reason ("only this repo is special" is a sign of insufficient design)

**A new repo is maximum strict from day one** (there is zero debt to drain, so no ratchet is needed).
**Use a ratchet only when retrofitting an existing repo** — install every rule as warn, drain the existing
violations completely, then raise them to error. Blocking from day one grows "workaround etiquette".

Budget-rule thresholds are likewise **one-way** — when exceeded, do not raise the threshold; **prune**
(remove dead code and duplication, split). Put the comment "prune, don't raise — record changes in verify.md
with a dated reason" on the threshold's config line. The spot that an agent touching the config sees the moment the gate turns red
is where this operating rule gets delivered.

## Step 4 — Generate `.claude/verify.sh` (the contract with pre-commit hooks and CI)

The repo's **single entrypoint**. A caller (a pre-commit hook, CI) looks only at this file's existence and its exit code
— so the caller needs no change whatever language the repo is written in.

**Contract (mandatory)**:

| Item | Specification |
|---|---|
| Path | `<repo root>/.claude/verify.sh` (executable) |
| Arguments | `--staged` = fast check at the commit boundary (staged files only). No argument = full check of the whole repo |
| Environment | If `$VERIFY_REPO_ROOT` is set, use it as the repo root (a caller that approves the content before running it passes it) |
| exit code | `0` = PASS / `1` = FAIL (blocks the commit) / `2` = cannot check (tool missing, etc.; fail-soft) |
| Output | On FAIL, **detection lines a human and an LLM can read and act on**. Output on PASS is **advisory** (things that do not block the commit but should be passed on — a ratchet awaiting promotion, a notice that a gate is asleep); the calling hook hands it to the model. With nothing to say, **no output** (do not add noise to a silent PASS). **stdout and stderr are not distinguished** — the caller captures both with `2>&1`, so progress lines and deprecation warnings written to stderr on success also become advisory. Silence what should stay silent |
| Run time | `--staged` **within a few seconds**. Anything slower goes only in the no-argument mode |

**The fast / slow split** (if it is not kept, bypass etiquette grows):

- `--staged`: format check, lint, security scan (things that complete per file)
- no argument: build, type check, test, dependency audit (whole repo, minutes)

Tool resolution: `use it if it is on PATH → otherwise run it on demand with an exact version pin (e.g. uvx <tool>@<x.y.z> / npx <pkg>@<x.y.z>, the same pin as Step 3) → if that is
not possible either, exit 2 fail-soft`. **Fail-soft is not silent** — print to stdout which gate is
asleep (a sleeping gate is more dangerous than a missing one).

**Implementation traps (both were hit in practice)**:

- **Determine the repo root in the order `$VERIFY_REPO_ROOT` → the script's own location** — if it starts from cwd,
  then when called through a hook it **checks a different repo and passes silently: fail-open**. A caller that approves content
  may run the verified bytes from a temporary file (to avoid TOCTOU), so `BASH_SOURCE` may not
  point into the repo. Supporting both is mandatory:

  ```bash
  if [[ -n "${VERIFY_REPO_ROOT:-}" ]]; then
    ROOT="$VERIFY_REPO_ROOT"
  else
    ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd -P) || exit 2
  fi
  ```
- **Confirm the file is tracked** — many repos have a `.gitignore` that excludes `.claude/*`.
  If it stays excluded, the gate disappears from CI and other clones. Check with `git check-ignore`, and
  add `!.claude/verify.sh` / `!.claude/verify.md` if needed

**Generating the file does not by itself make it run at the commit boundary.** Whatever runs `verify.sh` without a
permission prompt must run it only after **a human has read the content and approved it**, with the approval bound to
a content hash. A file that merely exists — for example in an external repo that was only cloned — must not run.
In the author's harness, a pre-commit hook (`verify-precommit.sh`) enforces this with
`python3 ~/.claude/scripts/hooks/verify_allow.py approve <repo>`, and passes PASS-time output to the model as advisory.

Because approval is bound to the content hash, a changed `verify.sh` needs approval again. In the author's harness, show the human `verify_allow.py diff <repo>` (the change since the approved version), then run `approve` through Bash; a hook asks the human to pass it at a permission prompt that carries the same diff. This is the trust boundary for repo-local code that runs without a permission prompt.

**Run the generated `verify.sh` once on the spot to confirm it works.** Then
**inject a violation temporarily and prove each category fires** (broken formatting, an unused import,
`eval`, etc.). A check that only passes is not evidence, because a sleeping gate also passes.
When the proof is done, always delete the injected probes.

## Step 5 — Record the selections (make staleness visible)

In `<repo root>/.claude/verify.md`, leave the following for each category:

```
## type check
tool: pyright ==1.1.x
selected: 2026-07-31
reason: faster than mypy and strict by default. ty / pyrefly are pre-1.0 as of 2026-07
re-research triggers: 12 months elapsed / an alternative reaches 1.0 / the current tool's last release is more than 12 months old
```

Without this record, audit mode cannot decide "what to re-derive".
**The selection date and the re-research triggers are mandatory**; one line of reason is enough. For budget rules, also record
**the threshold and the as-of date of the measured distribution** (e.g. `C901=15 — p99=14, measured 2026-08-28`. It is the baseline
compared against the re-measured distribution at audit time).

## Step 6 — Wire the same thing into CI

With only a local gate, a bypassed commit slips through. If CI has a job that runs `.claude/verify.sh`
with no argument, local and CI cannot diverge structurally
(**call the same entrypoint from both**. Writing a separate command sequence for CI always drifts).
In a repo where the implementing agent runs in a cloud session, CI is the only verify judge — the reviewer does not
re-run it locally but reads the conclusion of the run on the branch tip. Trust that conclusion only when the diff does not
touch `.claude/verify.sh`, `.github/` or `.claude/settings.json`: CI runs the branch's own copies, so send such a diff back. A repo without CI
cannot be handed to cloud sessions, so for a repo with a remote on github.com, include this Step in bootstrap.

The template is `references/ci-verify.yml`. Fixed parts: triggers on push to `main` and `claude/**` /
actions pinned by commit SHA (resolve from the tag with `gh api repos/<o>/<r>/git/ref/tags/<tag>`) /
`permissions: contents: read` / `persist-credentials: false` / a secret scan job over the whole history
(a local pre-commit secret scan sees only staged additions). Parts to fill in: installing the tools verify.sh
resolves from PATH (the selection record in `.claude/verify.md` is the source of truth) and the language setup.
Tests that fail on a Linux runner (macOS-only launchd / BSD `stat`) declare themselves with `skipif`, and a test
that hits `SystemExit` because of a production-side platform guard gets fixed — to keep "red in CI = red
locally".

## audit mode

1. Re-run Step 1 (has the stack changed? — if a language was added, categories open up)
2. For each category in `.claude/verify.md`, re-derive with search-first **only those that match a re-research trigger**
   (re-deriving everything costs every time)
3. Present the differences: current → candidate, switching cost, reason for staying
4. The user decides. **Do not switch automatically** — a tool change produces a repo-wide diff,
   and the cost of reverting exceeds the cost of introducing

## Related

- Entry point for Phase 0: skill `search-first` (tool selection always goes through it)
- The overall implementation flow that includes the gate: your implementation workflow (plan → test → review → verify)
