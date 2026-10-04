---
name: cgagentharness-gotchas
description: Session-tested traps for working on CG-agent-harness. Load before install/verify, desktop packaging, Chrome acceptance CI, clippy/toolchain fights, write-gate debugging, or when something hangs or looks green for the wrong reason.
---

# CG-agent-harness gotchas

Session-process traps for this repo. Canonical contracts live in `AGENTS.md` /
`INVARIANTS.md`; this file is the "looks green for the wrong reason" list.
Paths are relative to the CG-agent-harness root. Skills are repository guidance,
not runtime `/api/skills` plugins.

## 1. Server imports `crate::agentic`

- **Symptom:** `tests/invariant_guard.rs` fails; or a "cleanup" PR "shares types"
  across the console and the pipeline.
- **Wrong fix:** Make the agentic module a library dependency of the server, or
  call pipeline functions in-process "just for this route."
- **Right fix:** Keep I6. Put server-side behavior in `src/server`; cross only
  through `src/shim` spawning `current_exe() agentic <action>` with the ACTIONS
  whitelist. Declared MCP children in `src/common/mcp.rs` are a separate
  capability boundary. Exit codes `0/2/3/4` remain the agentic interface.
- **Evidence:** `INVARIANTS.md` I6; `AGENTS.md` traps; `tests/invariant_guard.rs`.

## 2. Deduplicating intentional boundary copies

- **Symptom:** Drift PR removes duplicated `RUN_ID_PATTERN`, timeout constants, or
  the check-profile table "to DRY."
- **Wrong fix:** Share the type/module across `server` and `agentic`.
- **Right fix:** Leave the duplication; keep the sync tests green
  (`invariant_guard::duplicated_constants_still_agree` and peers).
- **Evidence:** `AGENTS.md` traps.

## 3. Quoted YAML `"true"` arms a gate

- **Symptom:** Operator sets `enabled: "true"` (quoted) and expects writes; or a
  test assumes string `"true"` is on.
- **Wrong fix:** Teach operators that quotes are fine; loosen `flag_is_true`.
- **Right fix:** Unquoted YAML booleans only. Quoted `"true"` is **OFF** for every
  `flag_is_true` gate. Auth/TLS switches instead reject invalid types at
  configuration load; see `tests/common_layer.rs`.
- **Evidence:** `AGENTS.md`; `README.md` security defaults; shipped-config tests.

## 4. CSRF placeholder / header rename "cleanup"

- **Symptom:** Console or middleware renames `__CYCLAW_CSRF_TOKEN__`,
  `__CYCLAW_CSP_NONCE__`, or `X-CyClaw-CSRF` to a "harness" spelling.
- **Wrong fix:** Rename for branding consistency.
- **Right fix:** Keep placeholders and header name verbatim — contractual from
  the port. `invariant_guard::console_asset_is_verbatim_with_both_placeholders`.
- **Evidence:** `AGENTS.md` traps; `INVARIANTS.md` guard chain.

## 5. Tests assert developer `GROK_API_KEY`

- **Symptom:** Local suite fails on a clean CI image, or passes only because a
  real key is in the environment.
- **Wrong fix:** Require the key in test setup; commit a dummy that looks real.
- **Right fix:** Tests must not assert key presence. CI blanks
  `GROK_API_KEY` / `ANTHROPIC_API_KEY` / `DEEPAGENT_API_KEY`. Mirror that in
  `scripts/verify-local.sh`.
- **Evidence:** `AGENTS.md`; `README.md`; `scripts/verify-local.sh`.

## 6. scrypt / unoptimized dev builds make tests crawl

- **Symptom:** Auth/key derivation tests take forever in debug; people propose
  lowering scrypt `n`.
- **Wrong fix:** Reduce `n=2^17` or delete the cost.
- **Right fix:** Keep `n=2^17`. Keep `[profile.dev.package."*"] opt-level=3` —
  load-bearing for test time.
- **Evidence:** `AGENTS.md` traps.

## 7. Clippy is the wrong binary on some Macs

- **Symptom:** `scripts/verify-local.sh` fails clippy with toolchain/proxy skew;
  Cargo, Clippy and rustc resolve to different installations.
- **Wrong fix:** `#allow` the warnings or drop `-D warnings`.
- **Right fix:** Resolve the repository toolchain through rustup; inspect
  Cargo/Clippy/rustc versions before using the script's `CLIPPY` override.
  A Homebrew override must match the selected compiler.
- **Evidence:** `AGENTS.md`; `cgagentharness-verify` skill.

## 8. Browser failure needs current evidence

- **Symptom:** Chrome startup, attach or console assertions fail.
- **Right fix:** Inspect the current CI Chrome resolution and
  `scripts/chat-browser-acceptance.mjs`. Reproduce at the failing SHA and
  distinguish launch failure from a product assertion. An old issue or one
  successful retry does not classify the current failure.
- Run the console contract scripts from `.github/workflows/ci.yml`; keep
  assertions intact and record unavailable browser execution as NOT RUN.

## 9. Desktop packaging: lipo / sign / embed-SHA256 order

- **Symptom:** Checksums never match after local resign; Gatekeeper weirdness;
  sidecar digest verification fails.
- **Wrong fix:** Re-sign the sidecar **after** digest embed; mix ad-hoc and
  Developer ID steps without documenting which artifact is which.
- **Right fix:** Order is **lipo → sign → embed-SHA256**. Never re-sign a sidecar
  after digest embed. Ad-hoc (`--sign -`) ≠ Developer ID / notarized. WKWebView
  shell ≠ HTTP console semantics — don't assume fetch/CSRF behavior is identical
  inside the native wrapper.
- **Evidence:** `cgagentharness-release` packaging discipline; `scripts/package-release.sh` (ad-hoc note).

## 10. Seatbelt permission errors ≠ app regression

- **Symptom:** Sandbox verify fails with permission denied; patch softens the
  Seatbelt profile or skips sandbox tests.
- **Wrong fix:** Weaken assertions or broaden the profile to silence noise.
- **Right fix:** Reproduce with owned temp `CGAGENTHARNESS_HOME` + unique port.
  Distinguish environment/Seatbelt noise from product bugs. No backend ⇒ exit 3
  remains correct fail-closed behavior.
- **Evidence:** `INVARIANTS.md` judged-before-land; `agentic_foundations` sandbox_* tests; `cgagentharness-verify`.

## 11. Shared listener ≠ this bundle

- **Symptom:** Smoke "passes" against a leftover `serve` on `:8790` from another
  checkout or build.
- **Wrong fix:** Hit the default port and assume it's your binary.
- **Right fix:** Owned temp `CGAGENTHARNESS_HOME`, unique port, kill/own the
  process you started (`scripts/smoke-ollama.sh` pattern).
- **Evidence:** `scripts/smoke-ollama.sh`; verify skill.

## 12. Draft PR / template / driver prefix skipped

- **Symptom:** CI template check fails; review bots bounce; mergeability unclear.
- **Wrong fix:** Force a ready PR to skip draft discipline; invent a free-form body.
- **Right fix:** Draft PR, one concern, driver-prefixed branch (`claude/`,
  `codex/`, `grok/`, `kimi/`, `agent/`), body from
  `.github/PULL_REQUEST_TEMPLATE.md` after `scripts/check-pr-template.sh`.
  Core-path diffs need an explicit invariant statement. Skill selection still
  does **not** authorize push/merge/release.
- **Evidence:** `AGENTS.md` quality bar.

## 13. Write-gate debugging "just set confirm default true"

- **Symptom:** Publish/write path 4xx; agent proposes defaulting `confirm` or
  making `reason` optional.
- **Wrong fix:** Default `confirm` on; drop reason; OR the kill switch.
- **Right fix:** Keep `confirm` never defaulted, `reason` required, kill switch
  AND-ed only (`CGAGENTHARNESS_AGENTIC_WRITE_DISABLE`). Debug which gate refused
  with the exit-code API (`4` = write refused).
- **Evidence:** `INVARIANTS.md` write gates; `writer_gates_in_order_and_plan_integrity`.

## 14. `github.paginate` result consumed as `{data}`

- **Symptom:** A workflow step dies with
  `TypeError: Cannot read properties of undefined (reading 'find')`, and the
  check fails on *every* PR rather than intermittently.
- **Wrong fix:** Wrap the access in `?.` and move on, or revert to the
  unpaginated call that only ever saw page 1 of 30.
- **Right fix:** `github.rest.issues.listComments(...)` resolves to `{data: [...]}`;
  `github.paginate(github.rest.issues.listComments, ...)` resolves to the **array
  itself**. When switching to `paginate`, change the consumer too —
  `comments.find(...)`, not `comments.data.find(...)`. Audit every
  `await github.paginate` call site in `.github/workflows/`; each must read
  the array directly.
- **How to check before pushing:** the `github-script` block can be extracted
  from the YAML and run under stubs (`github`, `context`, `core` are just
  arguments), with `listComments` honouring the 30-per-page default and a marker
  planted on page 2. Cheaper than a CI round trip, and it reproduces both the
  original duplicate-comment bug and the `TypeError`.
- **Evidence:** `.github/workflows/pr-template-check.yml` — its two jobs
  disagreed on this for a while; the `base-branch` job was always correct.

## 15. Ephemeral port handed to a child, and `serve` exits **0** when it is taken

- **Symptom:** Intermittent red in `scripts/test-desktop-backend.py` with
  `AssertionError: 0 is not None : headless startup exited`, or
  `AssertionError: 0 == 0` — neither of which mentions ports.
- **Wrong fix:** Widen a timeout, retry the whole job, or call it a runner
  problem.
- **Right fix:** Binding `:0`, reading the port back and closing the socket is
  inherently advisory — the reservation *must* be released before the child can
  bind, so anything on the runner can take it in between. Retry on a fresh port.
  Two traps make this worse than it looks:
  - **`serve` exits 0 on port-in-use**, printing "CGagentHarness may already be
    running on 127.0.0.1:PORT" to **stdout** (stderr empty), because
    `port_in_use` is checked *before* `.env` is read. So a test asserting a
    non-zero refusal fails, and the path it meant to exercise never runs.
  - **Do not truncate captured output between attempts** if a later assertion
    reads that file. The credential-disclosure `assertNotIn` checks in that
    suite read the child's captured stdout/stderr; truncating means a leak on a
    failed attempt is erased and the check passes on a clean retry.
- **Related discipline:** when you fix one instance of a race, re-audit every
  site you *refactored* as well as the one that was failing. Converting a second
  site to the shared helper without its retry leaves the bug live at a site your
  own commit touched.
- **Evidence:** `scripts/test-desktop-backend.py` (`free_port`,
  `await_headless`, `serve_expecting_refusal`); `ModelFixture` and
  `test_unrelated_listener_is_never_adopted` show the keep-the-listener-open
  variant where that is possible.

## 16. A green check does not prove the current head was reviewed

- **Symptom:** You address review findings, push, see the PR go green, and merge
  — with the fixes themselves never reviewed.
- **Wrong fix:** Assume the green check covers the new commits, or read a stale
  "Completed" summary row as a verdict on the current head.
- **Right fix:** Compare the reviewed commit with the current PR head.
  Read unresolved threads and the advisory `review gate`; it does not fail CI.
  A cancelled review is not a verdict. Request another review only within
  the authorized workflow.
- **Evidence:** `.github/workflows/review-gate.yml` and the actual PR review.
  Thread resolution alone fires no webhook; re-run the gate when needed.

## 17. The docs audit agent can cite lines that do not exist

- **Symptom:** A drift report says "USER_MANUAL.md line 15 says sessions are
  written to `sessions/*.json`"; the file has no such line. Applying the edit
  blindly fails, or worse, inserts prose at a guessed location.
- **Wrong fix:** Trust a subagent's line numbers or quoted text as evidence.
- **Right fix:** Every audited claim is a *hypothesis*. Before editing, `rg`
  the quoted anchor in the named file; skip the finding if it does not match.
  Quote code values (config defaults, ranges, alias spellings) from `rg`, never
  from the report. The `doc-sync` skill's "grep it" rule exists for this.
- Respect `DOCS_BUDGET` in `tests/invariant_guard.rs`. Change existing owner
  sections and put evidence in PR bodies, without adding Markdown files.

## 18. Memory gate slash aliases are not the config key names

- **Symptom:** Docs (or a doc fix) write `/memory auto-retrieval on` or
  `/memory auto-consolidation on`; the console rejects them.
- **Wrong fix:** Derive the alias from the `structured_memory.*` key.
- **Right fix:** The console alias map is `gateMap` in
  `assets/static/harness.html` and the help line in `src/server/views.rs`:
  `capture|recall|retrieval|auto-retrieve|consolidation|auto-consolidate|
  auto-suggest-chat|auto-suggest-coding`. The HTTP body for
  `POST /api/structured-memory/gates` takes the *config* name
  (`episode_capture`, `explicit_recall`, `auto_retrieval`, ...) instead.
  Two spellings, two surfaces; grep the one you are documenting.

## 19. Do not cut a release the maintainer already cut

- **Symptom:** Asked to "cut a release after the PR", you dispatch
  `release.yml` with `publish=true`; it fails with
  "Candidate tag already exists" or "Release already exists (including drafts)".
- **Wrong fix:** Retry, delete the draft, or push a tag by hand.
- **Right fix:** Before any dispatch, list `release.yml` runs and releases. A
  tag push (`push` event, `head_branch: vX.Y.Z`) or a pending
  `workflow_dispatch` on the same SHA means the release is already in flight;
  watch that run instead. The planner (`scripts/release-plan.py`) fails closed
  on collisions by design. Also note: a green `Bundle` run on the exact main
  SHA is a hard precondition for `schedule`/`workflow_dispatch` releases.
- **Evidence:** `docs/RELEASING.md`, `scripts/release-plan.py` and current
  workflow runs. Preview on a feature branch never publishes.

## Related skills

Load `cgagentharness-project-guidance` for read order;
`cgagentharness-invariant-guard` / `cgagentharness-config-guard` before merging
core-path or config diffs; `cgagentharness-write-policy-redteam` for write/git/
argv/jail hardening loops; `verification-specialist` to adversarially verify a
supplied patch; `cgagentharness-parity` for CyClaw↔harness ledger work;
`cgagentharness-verify` / `cgagentharness-release` / `cgagentharness-optimize`
for those jobs; `fable-protocol` for evidence-first discipline.
