---
name: done
description: >-
  End-of-session shipping gate — "prove it works, then ship it." Runs an
  evidence checklist (full test suite, lint/typecheck, build, and actually
  running the change — output quoted, never asserted), then a fresh-context
  two-stage review by a sub-agent that sees only the diff and the spec:
  spec-compliance first, correctness second, style never — joined by a
  cross-model second opinion when a codex/gemini CLI is installed. Flags
  fake-green
  tripwires (edited or deleted tests, new TODOs or skips, hardcoded
  expectations) and ends with a verdict — SHIP, FIX FIRST, or NEEDS HUMAN —
  before drafting the commit/PR for the user's approval. Use at the end of
  any coding session or when the user asks "is this done", "ready to ship?",
  "/done", "wrap this up", "review and commit this". It is the closing step
  of both feature and bugfix, but works standalone on any uncommitted or
  branch diff.
---

# done — the evidence gate

`/done [what was being built, or a path to its spec/plan]`

Answer one question: **is there evidence this change works and does what was
asked — or does it merely look finished?** "The work looks done" is the
weakest signal in agentic coding; this gate replaces it with quoted output
and an independent review. It never makes the change better — it decides
whether the change is *ready*.

## Step 0 — Establish the yardstick

Identify **the diff** (uncommitted changes, or the branch vs its merge base)
and **the intent**: the change folder's `spec.md`/`plan.md` if this came from
the feature skill, the bug repro if from bugfix, otherwise ask the user for
one sentence of "what was this supposed to do". No yardstick → the review
below can only check correctness, not compliance; say so.

## Step 1 — Evidence checklist

Copy this checklist into the response and fill it in as you go — every line
gets **quoted command output or an explicit ✗ with the reason**. An
unticked line with a reason is honest; a ticked line without evidence is the
exact failure this skill exists to prevent.

```
- [ ] Full test suite: <command> → <pass/fail counts, verbatim tail>
- [ ] Lint / typecheck: <command> → <result>          (✗ if repo has none)
- [ ] Build: <command> → <result>                     (✗ if n/a)
- [ ] Ran the actual change: <command / flow> → <observed behavior>
- [ ] Diff hygiene: no debug prints (grep the diff for [DEBUG- — the tag
      bugfix leaves), no commented-out code, no stray files
- [ ] Tripwires (fake-green + source-security, below): clean
```

Every line is quoted **redacted**: secrets replaced with `<REDACTED>`, long
output cut to its signal-carrying lines. A live secret in pasted evidence is
itself a finding — treat it like a tripwire hit (→ FIX FIRST)
until it's out of the evidence; whether it's also in the *code* is the
source-security scan's job below.

**"Ran the actual change"** is the line agents skip and humans value most: a
green suite proves the tests pass, not that the feature works. Execute the
spec's end-to-end check — start the app, curl the endpoint, run the CLI on
real input — and report what actually happened. On **auth, payment, or
data-migration** surfaces, "ran the change" means the *failure* path too, not
just the happy one — an expired or tampered token is rejected, a declined
card and a replayed webhook are handled, a migration's rollback is actually
run — because that's where these surfaces break. Happy-path evidence alone on
one of those surfaces **can't reach SHIP**: it's incomplete evidence (→ FIX
FIRST, or NEEDS HUMAN when the missing check is a judgment call).

**Fake-green tripwires** — scan the diff itself; any hit is called out
loudly and blocks a SHIP verdict until the user rules on it:

- an existing test **modified or deleted** in the same diff that makes it pass
- new `skip` / `xfail` / `.only` / commented-out assertions
- new TODOs or "temporary" workarounds standing in for the actual behavior
- assertions hardcoded to the current output rather than the intended behavior
- a test whose expected value is **recomputed the way the code computes it**
  — expected values come from an independent source of truth

**Source-security tripwires** — the source-side twin of the block above:
scan the diff for a catastrophe pattern *shipped into the code*, not a faked
test. Same rule — any hit is called out loudly with the **file:line** and
blocks a SHIP verdict until the user rules on it. This is a scan of the diff,
not an audit of the repo: a pattern the change doesn't introduce isn't a
finding. Some clauses below are *missing-safeguard* ones — no tested
rollback, no signature check — where the safeguard may live in an unchanged
file; there the tripwire fires on the dangerous operation the diff *does*
introduce, and the user's ruling is where a safeguard already present
elsewhere gets confirmed.

- **Secrets in source** — an API key, token, password, or private key in a
  committed file (not `.env`, not a placeholder); an OAuth or signing secret
  anywhere but a secret manager.
- **Injection** — a SQL query built by string-concatenation with
  user-controlled input (no parameterization / ORM escaping); a shell command
  assembled from user input via `exec`/`spawn`/`eval`; a template rendered
  with unescaped user input where XSS is reachable.
- **Auth bypass** — a middleware check with a path that skips it (early
  return, swallowed exception, condition that always resolves to
  "authenticated"); a role or permission check forgeable by a request
  parameter; a JWT accepted with `alg: none` or verified against a secret
  hardcoded in source.
- **Payment / webhook** — a handler that swallows errors silently (empty
  catch, unhandled rejection); a webhook with no signature verification; an
  amount or recipient derived from untrusted input without server-side
  validation.
- **Destructive data** — a migration with a `DROP` or destructive `ALTER` and
  no tested rollback; a bulk delete or update with no `WHERE` or a
  user-controlled one; a cache or store wipe with no restore path.
- **Plaintext sensitive data** — a password or PII logged or stored
  unencrypted; an SSN, payment card, or health field in an unencrypted
  column.

## Step 2 — Fresh-context review (two stages, one sub-agent each)

Preflight first: confirm the yardstick resolves and the diff is non-empty —
reviewers fanned out on a wrong ref or an empty diff are pure waste. Then
spawn reviewers that see **only** the diff plus the yardstick — not this
conversation. A reviewer with no memory of writing the code has no loyalty
to it. Run both concurrently:

1. **Spec compliance:** does the diff do what the spec/intent asked — fully,
   and *nothing beyond it*? Unrequested changes are findings (scope creep),
   missing acceptance criteria are findings. Returns: covered / missing /
   out-of-scope, each tied to a spec line — by decision/assumption ID
   (`D2`, `A1`) when the spec numbers them — and a diff location.
2. **Correctness:** bugs only — logic errors, unhandled edge cases, broken
   callers, concurrency/resource hazards. Instruct it explicitly: *"report
   only defects that affect behavior; style, naming, and architecture
   preferences are out of scope."* (Unbounded reviewers always find
   something; that way lies over-engineering.)

Every finding — from either stage or the second opinion below — **quotes
the diff lines that motivate it**. A finding that can't quote its evidence
is reported as *unverified*: on the record, but it never blocks the
verdict. (Phantom findings — confident claims about code that isn't in the
diff — are the reviewer-side twin of fake-green.)

**Second opinion — optional, cross-model:** if another model's agent CLI is
installed (`command -v codex`, `command -v gemini` — checked separately,
since one exit code for both false-negatives when only one exists; also
check `~/.local/bin`, which non-login shells often drop from PATH), invoke
it **by the path detection found** — a CLI discovered in `~/.local/bin`
won't resolve by bare name — and run it as one more correctness
reviewer with exactly the same inputs and instructions — the diff, the
yardstick, the "style is out of scope" line — e.g.
`codex exec "Review only the diff below — do not read skill definitions,
.claude/, or other repo files. Report defects that affect behavior...
<diff>"`. The leading boundary line matters: an unscoped reviewer wanders
off into whatever else it finds in the repo. Bound the call with a timeout
(~5 min); a timeout or error means **second opinion unavailable** — note it
in the gate and move on, never retry, and never substitute a same-model
stand-in (a Claude sub-agent isn't *outside*).
Fresh context removes loyalty to the code; a **different model** removes
shared blind spots — a same-model reviewer tends to miss what the author
missed, and LLM judges measurably favor their own model's output. No such
CLI on the PATH → skip this layer and note it; never install one for it.

Weigh the findings — a reviewer can be wrong; check disputed claims against
the code before accepting them. Don't silently drop any finding: each one is
**accepted (→ fix list)** or **rejected (with the reason)**. Cross-model
findings carry two extra rules: **agreement** (both models flag it
independently) is near-certain — accept it; and the gate **rejecting the
other model's behavior-affecting finding** is itself the material
disagreement — silence from one reviewer isn't consent, and the local
model overruling its cross-model critic re-creates the self-judging this
layer exists to break. That rejection isn't the gate's to make: route the
finding to NEEDS HUMAN.

## Step 3 — Verdict, then ship

One of three, stated plainly with the reasons:

- **SHIP** — evidence complete (including the failure-path check on any
  auth/payment/migration surface), tripwires clean — fake-green *and*
  source-security — and no accepted findings.
- **FIX FIRST** — the accepted findings, as a short ordered list. Fix them
  (or hand back to feature/bugfix), then re-run **only the affected lines**
  of the gate — not the whole ceremony.
- **NEEDS HUMAN** — a judgment call the gate can't make: a tripwire the user
  must rule on, a spec ambiguity, a disputed reviewer finding (including a
  cross-model split), a trade-off.

On SHIP (human-in-the-loop, in this order):

1. Draft the commit message per the repo's convention — read `CLAUDE.md` /
   recent `git log` for the house style. Commit.
2. **Ask before push / PR** — never push or open a PR unprompted. If a PR is
   wanted, the body is the spec's summary + the evidence checklist (a
   reviewer who sees the proof reviews faster).
3. If this change came from a feature folder: move `out/dev/<change>/` to
   `out/dev/archive/`.
4. **One-line retro (optional but offered):** if the session surfaced a
   recurring agent mistake — a convention repeatedly missed, a check
   repeatedly forgotten — suggest the one-line `CLAUDE.md` rule or lint that
   would make it impossible next time. Harness engineering beats repetition;
   the **tune** skill runs this same audit at scale across past sessions.

## Auto mode — under autopilot

Driven by the **autopilot** skill, the gate's logic is unchanged — only the
waiting is removed: the run's itemized charter (not a question) governs
commit, push, and PR, and a **NEEDS HUMAN** verdict **parks** the change
with its findings on the record instead of blocking on a conversation. The
gate still never fixes, and evidence rules still apply — auto mode changes
who's waiting, not what's proven.

## Guardrails

- **Evidence over claims.** No verdict without running things. If nothing
  can be run (no tests, no build, no entry point), say so and mark the
  verdict NEEDS HUMAN — never SHIP on inspection alone.
- **The gate doesn't fix.** Finding-then-quietly-fixing hides the finding;
  fixes happen after the verdict, on the record, then re-gate.
- **Fresh context is the point.** The sub-agent isolation is what makes
  stage 2 honest.
- **Correctness only in review.** Style debates are for humans who enjoy
  them, not shipping gates.
- **A second model is another reviewer, not an arbiter.** Its findings enter
  the same accept/reject triage with no extra weight; no model's verdict —
  local or cross — outranks the test suite.
- **Never push without a yes.** Committing locally is reversible; pushing
  and PRs are announcements.
