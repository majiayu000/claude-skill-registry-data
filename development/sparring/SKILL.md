---
name: sparring
description: The relay's synchronous mode — make Claude and Codex argue BEFORE you build, inside one session, with zero copy-paste. Four phases — SCOUT (recon from the vault's layered memory), LOCK (interrogate the user until intent is locked), SPAR (the rival model attacks the plan in bounded rounds, read-only), SHIP (one model builds, the other grades the diff, then the argument is compiled into the Wiki). Use when the user says "/spar", "spar this", "have codex review this plan", "argue this with codex", "cross-model review", "stress-test this plan", "codex build this", "have the models fight", or is about to build something high-stakes (auth, schema, migrations, concurrency, payments, greenfield architecture). NOT for trivial changes, and not a substitute for the async relay baton (that's the `relay` skill).
---

# Sparring — the models argue so production doesn't

The relay (`_relay/STATE.md`) hands work between agents **across** sessions.
Sparring runs both models **inside one** session: the driver plans and builds,
the rival model attacks — plan first, diff later. One invariant governs every
phase: **whoever made the thing never grades the thing.**

Everything mechanical (rounds, verdict parsing, the append-only log, resumable
state) lives in `scripts/spar_tool.py` under `_relay/spar/`. If a spar is
interrupted, any later session runs `python scripts/spar_tool.py status` and
picks it up — the loop is part of the relay, not of anyone's chat history.

Stakes test before starting: would a wrong plan cost a migration, a rewrite, a
security hole, or user trust? No → skip sparring, just build.

---

## Phase S0 — SCOUT (driver alone, minutes not hours)

Recon before asking the user anything — and in an Omnia Vault, recon is
cheap because the knowledge is already compiled. Use the layered memory, not
sweeps:

1. `_relay/STATE.md` + `python scripts/relay_tool.py status` — what's in
   flight.
2. **Graph:** `graphify query "<the task's subsystem>" --graph graphify/<repo>/graph.json`
   (+ `explain` / `affected` for the touched nodes).
3. **Wiki:** `python scripts/wiki_tool.py search-catalog --query "<topic>"` —
   decisions already made, constraints already recorded, open questions
   already known.
4. **Raw/code, narrowly** — only files the layers above pointed at.
5. Greenfield (empty vault, no graphs)? Say so, and offer ONE round of
   targeted web research on prior art + known pitfalls before the interview.

Then `python scripts/spar_tool.py start --task "<task>" [--rounds N]` and open
with an **Assumptions Ledger** — one batch, never a drip:

```markdown
## Assumptions Ledger
_Confirm or correct in one reply; anything unmarked I treat as confirmed._
1. <assumption> — source: [[wiki-note]] / graphify:<node> / <file> / convention
```

Every entry cites where it came from. The vault is the point: most of what a
naive interview would ask is already answered here, with receipts. Corrections
that open real questions promote into the S1 decision map.

## Phase S1 — LOCK (driver ⇄ user)

Interrogate until intent is locked — but only on decisions that earn a
question.

**Decision map first** (shown, and updated as items resolve):

```markdown
## Decision Map
### Load-bearing — asked one at a time
- [ ] <decision>        (wrong answer = migration / rewrite / breach / churn)
### Cosmetic — batched, veto by exception
- [ ] <decision>        (cheap to change later)
```

**Load-bearing questions, one at a time, each carrying its own justification:**

> **Q<n>: <question>**
> **Why this is load-bearing:** <the dependency that makes it so>
> **My recommendation:** <a committed answer, not a menu>
> **Cost of guessing wrong:** <the concrete failure>

If "cost of guessing wrong" comes out weak while drafting, the question was
cosmetic — demote it. If the vault can answer it, answer it yourself and
ledger it instead of asking. **Escape hatch** (offer it explicitly past ~8
questions): the user says *"lock all recommendations"* and every open decision
locks at its recommended answer, marked as such in the plan.

When the map is fully checked, write `_relay/spar/PLAN.md` (the stub is
already there): Goal · Approach (numbered, concrete) · **Key decisions &
tradeoffs** (named explicitly — this is what the reviewer bites) ·
Assumptions (the confirmed ledger, with sources) · Risks / open questions ·
Out of scope. The plan is now **locked** — S2 changes it only through logged
revisions.

## Phase S2 — SPAR (driver ⇄ rival model, bounded)

### Resolve the reviewer once

```bash
CODEX=$(command -v codex || ls -t "$LOCALAPPDATA/OpenAI/Codex/bin/"*/codex.exe 2>/dev/null | head -1)
"$CODEX" --version   # need ≥ 0.130
```

(No hit → `npm install -g @openai/codex` + `codex login`, or the OpenAI Codex
desktop app which bundles the CLI.) **Echo the reviewer's identity before
round 1** — the `model` line from `~/.codex/config.toml` (absent = "CLI
default") + the CLI version — so the user can veto before a round burns.
Don't pass `-m` yourself: ChatGPT-account auth rejects pinned `-codex`
variants, and the user's config default is their choice.

### The reviewer's contract (write to a temp file each round)

> Act as a hostile reviewer for the implementation plan at
> `_relay/spar/PLAN.md`. Your job is finding what breaks — never be agreeable.
> You have read-only access to this repository: check the plan's claims
> against the actual code, schema, and docs it references. Report each flaw as
> `[FATAL]` (cannot be built / corrupts data / security hole), `[MAJOR]`
> (breaks under real conditions), or `[MINOR]` (worth fixing, not blocking) —
> one line of concrete fix each. Do not modify any file. Your reply MUST end
> with exactly one line: `VERDICT: APPROVED` or `VERDICT: REVISE`.

### Round 1 — fresh session, capture the thread

```bash
P=$(mktemp); C=$(mktemp)
# ...write the contract prompt to "$P"...
"$CODEX" exec -s read-only --json -o "$C" - < "$P" 2>/dev/null | grep '"type":"thread.started"'
python scripts/spar_tool.py set-thread --id "<thread_id from that line>"
python scripts/spar_tool.py record-round --critique-file "$C"
```

### Rounds 2..N — resume the SAME thread (the reviewer remembers)

```bash
# resume rejects -s; force the sandbox via -c or it inherits config.toml,
# which may be full-access. This line is the loop's most important safety rail.
"$CODEX" exec resume "$THREAD_ID" -c sandbox_mode="read-only" --json -o "$C" - < "$P2" 2>/dev/null >/dev/null
python scripts/spar_tool.py record-round --critique-file "$C"
```

where `$P2` says: the plan was revised — verify your prior findings are
resolved, hunt for anything new, same severity tags, same verdict line.

### After every round — arbitrate, don't obey

`record-round` prints `round=N verdict=...`. On **REVISE**: the driver is the
arbiter. Every `[FATAL]`/`[MAJOR]` gets exactly one of: **accepted** (revise
PLAN.md accordingly) or **rebutted** (with the reason). Log it —
`python scripts/spar_tool.py respond --text "..."` — then resume. Caving to
everything defeats the cross-check; ignoring findings defeats the point.
`[MINOR]`s may be batched or deferred, but say so in the response.

### Ending the loop

- **APPROVED** → present the final plan + a 3-bullet "what the argument
  fixed" + round count. The user signs off; only then does S3 exist.
- **Round cap without APPROVED** → a **deadlock**, and that's a legitimate
  result: list each still-open finding with the driver's counter-position and
  let the user break the tie. Never massage a deadlock into a fake approval.
- Either way the verdict is the user's gate — **no code before sign-off.**

## Phase S3 — SHIP (roles flip)

The user picks the builder; the rival grades the result either way.

**Codex builds** (mechanical work orders, migrations, well-specced features):

1. **Clean-tree gate:** `git status -sb` must be clean — a full-access build
   that can't be isolated can't be reverted. Non-negotiable.
2. Prompt = a work-order contract in a temp file: GOAL / SPEC (read
   `_relay/spar/PLAN.md`, implement exactly; deviations reported, never
   redesigned) / KEY PATHS / CONSTRAINTS / NON-GOALS / PROOF (the exact test
   command — ask the user once if the plan lacks one) / OUTPUT (files-changed
   report + proof output + deviations).
3. Launch: `"$CODEX" exec -s workspace-write --json -o "$C" - < "$P" 2>/dev/null | grep thread.started`
   — sandboxed writes inside the repo. Escalate to
   `--dangerously-bypass-approvals-and-sandbox` only when the build genuinely
   needs it (network installs, global tools) AND the user approves that
   escalation. Long builds run in the background; when one finishes, the next
   message to the user OPENS with a loud completion banner before any
   verification output.
4. **The driver verifies, always:** read the ENTIRE `git diff` like a hostile
   PR review, run the proof command yourself (the builder's pasted output is
   advisory, not proof), log the verdict to the spar log.
5. Fix rounds resume the same thread (`-c sandbox_mode="workspace-write"`),
   at most 2 — then the driver takes over and finishes directly. Unbounded
   delegation ping-pong burns more than it saves.
6. Human gate on the diff. Commits are authored by the driver, never the
   builder, and never before the gate.

**Claude builds** (design-heavy work, anything needing session tools): build
as usual, then **cross-inspection** — a FRESH read-only Codex session (new
thread; the inspector must see the code cold, not through its own plan
critiques) reads the plan + the diff and reports PR-style findings with the
same severity tags, no verdict line. Arbitrate each (fix or rebut), one
re-inspection max, log everything. Skipping the inspection requires the user
saying so, and the log records the opt-out — silence never skips it.

## Phase S4 — the argument becomes knowledge

This is what sparring adds over any standalone review loop: the argument
doesn't evaporate when the terminal closes.

1. `python scripts/spar_tool.py finish --outcome approved|deadlock|abandoned --summary "..."`
   — archives PLAN.md + SPAR-LOG.md to `_relay/spar/archive/<date>-<slug>/`.
2. Capture the argument as a Raw source
   (`Raw/Sources/<date>-<slug>-spar.md`, `Reference:` the archive path):
   summary, the findings that changed the plan, the rebuttals, the outcome.
3. Compile: fold the plan's Key Decisions into the project note and concept
   notes (`search-catalog` first; enrich over duplicate) — next quarter's
   "why is it built this way?" gets answered by the wiki, not by archaeology.
4. Gate → relay handoff (`_relay/STATE.md` mentions the spar's outcome) →
   commit.

## When Codex is the driver (the mirror)

The loop is symmetric. A Codex session working this vault (per `AGENTS.md`)
runs the same phases with the roles swapped, using Claude headless as the
read-only reviewer:

```bash
claude -p "<the reviewer contract, pointed at _relay/spar/PLAN.md>" \
  --permission-mode plan --output-format json      # → parse .session_id + .result
claude -p --resume "<session_id>" "<revision prompt>" --permission-mode plan --output-format json
```

Same state tool, same log, same rules — `--driver codex --reviewer claude` on
`start`. Whoever drives, the rival grades.

## Mechanics that will bite you (verified on codex-cli ≥ 0.130)

- **`- < "$P"` stdin feeding is mandatory.** `codex exec` reads stdin in
  addition to its prompt argument; under a non-TTY driver (an agent's bash
  tool, CI) an unredirected call blocks forever at ~0% CPU. Feeding the
  prompt file gives it content AND immediate EOF, and sidesteps quoting bugs.
- **`resume` rejects `-s`.** Re-force the sandbox with
  `-c sandbox_mode="..."` on every resume or it silently inherits
  `config.toml` — possibly full access, mid-"read-only"-loop.
- **Resume by explicit thread id only, echoed into the command.** Never
  `--last` (parallel sessions grab the wrong thread), and a garbage id can
  silently fall back to the most recent session instead of erroring.
- **Read results from the `-o` file**, never by parsing the JSONL stream.
- **Timeout ceiling on every codex call:** 10 minutes via the bash tool's
  `timeout: 600000` (the default 2-minute tool timeout kills real reviews
  mid-run). A tripped ceiling = a failed round: stop and tell the user, don't
  retry blind.
- **Failure signature:** no critique file + no `thread.started` line = the
  run died (auth/model). Surface it; `spar_tool.py record-round` refuses
  empty critiques so a dead round can't masquerade as a real one.

_The headless-Codex mechanics above were hardened by the claudex-loop project
(chaseai-yt/claudex-loop, MIT) — see THIRD-PARTY-NOTICES.md. The vault-scout,
spar-state relay integration, severity-tagged arbitration, workspace-write
builds, and the SHIP/knowledge-compile phase are Omnia Vault's own._

## Hard rules

- The reviewer is read-only in every review round, no exceptions.
- The loop ALWAYS terminates at the round cap; a flagged deadlock beats a
  fake approval.
- Every FATAL/MAJOR finding gets an accept-or-rebut in the log. No silent
  drops, no silent caving.
- No code before the user signs the converged plan; no commit before the
  user signs the diff; the driver authors all commits.
- The spar log is a deliverable. So is its Wiki compilation — a spar that
  never reaches the vault only did half its job.
