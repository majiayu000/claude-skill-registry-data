---
name: luke-deps
description: >
  Technology and Platform Governor for the Luke monorepo. Owns the approved
  stack, the dependency graph, the toolchain and the supply chain: detects
  platform drift, assesses proposed technology changes, and applies upgrades
  through evidence-based verification — within-major bumps together, every
  major alone, each proven by the level of test that can actually catch its
  failure mode. Also covers advisory response, pnpm overrides review,
  deprecated package migrations and Node/pnpm/base-image lifecycle.
  Use for a platform health check, a periodic dependency review, before a
  release, or when osv-scanner reports an advisory.
  Modes: /luke-deps (review) | platform | apply | security | toolchain |
  evaluate. Optional filter: /luke-deps apply apps/api
argument-hint: '[platform|apply|security|toolchain|evaluate] [path|proposal]'
---

# Luke Platform Governor

**Own and maintain the approved Luke technology platform, dependency graph and
toolchain. Detect platform drift, assess technology changes, and apply upgrades
through evidence-based verification.**

Not merely a package updater. Two halves, and the split is the point:
**everything read-only runs first**, apply only ever executes a plan the user
has seen.

A dependency bump is the one change that alters behavior without altering a
diff you can read. Everything in this skill exists because of that: the
verification ladder, one-major-at-a-time, the risk table. Green types are not
evidence.

## Modes

| Mode                  | Does                                              | Writes |
| --------------------- | ------------------------------------------------- | ------ |
| _(empty)_             | dependency review + platform summary (§1–§6)      | no     |
| `platform`            | platform integrity and architecture drift (§10)   | no     |
| `apply [path]`        | execute a reviewed plan (§7)                      | yes    |
| `security [path]`     | advisory-driven response (§9)                     | yes    |
| `toolchain`           | Node / pnpm / base image / Actions lifecycle (§8) | yes    |
| `evaluate <proposal>` | technology decision assessment (§11)              | no     |

**Invocation arguments:** $ARGUMENTS

The first token of the bound value above is the mode from the table; an empty
value is the review mode. What follows is that mode's own argument, as its
section defines it — a workspace filter for `apply` and `security`, the
proposal for `evaluate`.

**Any other first token fails closed.** Matching is exact and case-sensitive.
Print

```
luke-deps: usage — [platform | apply [<path>] | security [<path>] | toolchain | evaluate <proposal>]
```

and stop, having read nothing and written nothing.

**This skill is deliberately not forked.** `apply`, `security` and `toolchain`
run an approve-per-cycle loop with the user, and a forked context breaks it.
The fork/background contract in `tools/scripts/check-skill-integrity.ts`
therefore does not apply here.

**Read `.claude/skills/luke-shared/audit-protocol.md` first** and apply the
sections its applicability table assigns to `/luke-deps`: §3 escalation to a
deterministic rule, §4 `lessons.md` as a check input, §7 concurrent sessions.
§1 diff scoping does **not** apply — the input here is the registry and the
repository's own configuration, not the diff. A path in the invocation
arguments is a workspace filter (`apps/api`, `packages/nav`), never a git range.

**Ownership**: `.claude/skills/luke-shared/governance-map.md`. This skill owns
platform, dependencies, toolchain and supply chain. It does not own application
architecture, runtime bugs or application exploits. When a platform finding
explains an application finding, hand it over — do not audit the application.

**Platform facts are read live**, from the authority table in
`.claude/skills/luke-deps/references/platform-policy.md`. Never copy a version
into a skill, a reference or `CLAUDE.md`.

---

## Ground rules

1. **One major per verification cycle.** Batching majors tells you something
   broke, not which one. `cd1613d` batched and shipped the `@fastify/multipart`
   regression; `308256f` had to bisect it back out by hand.
2. **The verification level must match the failure mode**, not the size of the
   diff. See §4 — this is the core of the skill.
3. **Never hand-edit `pnpm-lock.yaml`.** Change `package.json`, run pnpm, commit
   what it produces.
4. **Never `git commit`** — show the diff, propose the message, wait
   (CLAUDE.md rule 3). This skill produces commits' worth of work, never commits.
5. **Never revert with `git checkout` / `git restore`** on a file (protocol
   §7.4). To undo a bump: edit the version back and re-run pnpm.
6. **A hold is a deliverable.** A major you decided not to take is only useful
   if the reason and the unblock condition are written down (§7).
7. **Never add a second library** for a job an installed one already does
   (`lessons.md`, "Don't duplicate libraries for the same purpose").

---

## 1 — Inventory

```bash
pnpm outdated -r                      # every workspace package
pnpm outdated -r --format json        # when you need to process it
pnpm install --frozen-lockfile 2>&1 | grep -i deprecat   # deprecations
pnpm security:deps                    # osv-scanner, advisories
```

Three things `pnpm outdated` will not tell you, and you must check by hand:

- **Deprecated-but-current packages.** A package can be on its latest version
  and still be abandoned. `06fb83b` migrated
  `@opentelemetry/instrumentation-fastify` → `@fastify/otel` for exactly this:
  never flagged as outdated, deprecated upstream.
- **The release-age quarantine.** Run `pnpm config get minimumReleaseAge`. If it
  is set, versions younger than that window are invisible to resolution, so
  "latest" in the report is not latest on the registry.
  `minimumReleaseAgeExclude` in `pnpm-workspace.yaml` is the per-package
  exemption list — read it before concluding a package cannot be updated.
- **Overrides that outrank the bump.** Anything in the `overrides` block of
  `pnpm-workspace.yaml` wins over `pnpm update`. Cross-check every advisory
  finding against that block (§6), and against `osv-scanner.toml`: an entry
  there turns a still-present advisory into a clean scan until it expires,
  and hides its fixed version. Retire an entry as soon as one ships.

Then read `lessons.md` per protocol §4 — the Always row and the rows naming
`luke-deps`.

---

## 2 — Classify

Every outdated package lands in exactly one bucket. The bucket decides the
batching and the commit.

| Bucket             | What                                          | Batching                     | Commit                                                                    |
| ------------------ | --------------------------------------------- | ---------------------------- | ------------------------------------------------------------------------- |
| **A** within-major | patch + minor                                 | all together, one cycle      | `chore(deps): bump dependencies within existing majors`                   |
| **B** major        | any major jump                                | **one at a time**            | `chore(deps): bump <pkg> N->M` (or one commit for a verified run of them) |
| **C** toolchain    | Node, pnpm, Docker base image, GitHub Actions | own cycle                    | `chore(infra): ...`                                                       |
| **D** advisory     | anything osv-scanner flags                    | jumps the queue              | `fix(deps): ...`                                                          |
| **E** deprecated   | replaced or abandoned upstream                | own cycle, it is a migration | `fix(<scope>): migrate ... to ...`                                        |
| **F** held         | not taken this round                          | no change                    | none — goes in the report                                                 |

Bucket A is not automatically safe: `@fastify/multipart` 10.0.0 → 10.1.1 was a
**patch-range** bump and broke uploads. A within-major bump on a package in the
risk table (§3) still gets that package's proof.

Code changes forced by a bump are **not** `chore(deps)` — they are
`fix(<scope>)` in their own commit (`d13d906` for argon2, `06fb83b` for otel).
That separation is what makes a bad bump revertable without losing the fix.

---

## 3 — Risk lookup

Before planning anything, look up every candidate in
`.claude/skills/luke-deps/references/verification-matrix.md`. It maps the
packages this repo actually depends on to **the invariant they can silently
break** and **the command that proves they did not**.

A package in that table is never verified by types alone: level 4 or it did
not happen. A package not in the table gets levels 0–2 and, if it is a runtime
dependency of `apps/api`, level 3.

---

## 4 — The verification ladder

| L   | Command                                                | Catches                                              |
| --- | ------------------------------------------------------ | ---------------------------------------------------- |
| 0   | `pnpm install` · `pnpm check:overrides`               | resolution failures, peer-range conflicts, an override cap below a consumer's range |
| 1   | `pnpm lint` · `pnpm typecheck` · `pnpm typecheck:test` | changed API shape (argon2 `Options` → `HashOptions`) |
| 2   | `pnpm test`                                            | unit-visible regressions                             |
| 3   | `pnpm test:integration:local`                          | wire-level regressions (multipart teardown)          |
| 4   | targeted runtime proof (see the matrix)                | **same shape, different behavior**                   |
| 5   | `pnpm check:drift` · `pnpm security:deps`              | skill/doc drift, new advisories                      |

**Level 4 is the only level that catches the failures that matter most, and no
CI job runs it for you.** The fastify 5.12 `trustProxy` regression passed levels
0–3: numeric hop counts stopped being honored, so `req.ip` would have collapsed
to the `apps/web` container and reopened the rate-limit bypass fixed on
2026-08-07, with identical types and a rate-limit suite that stubbed `req.ip`.

Three rules follow from that:

- **Prove the behavior, not the compile.** `d13d906` verified argon2 with a real
  hash/verify round trip. `308256f` verified `p-limit` 7 ESM-under-CJS
  end-to-end, not just at import time. `06fb83b` verified the OTel SDK actually
  started and instrumented.
- **When a bump needs a new test, prove the test fails on the broken version.**
  Re-apply the bad version, watch it go red, then restore. A regression test
  written against already-fixed code proves nothing (`ec78c6f` did this).
- **Differential verification before blame.** A failure that appears after a
  bump is not necessarily from the bump. Reproduce it on the pre-bump tree
  first. During `c9a816e` the `apps/web` Docker build failed after the Node 24
  bump and failed identically on Node 22 — pre-existing, wrongly attributable,
  and correctly left out of scope.

**Before any level 3 run**: protocol §7.3 — if `pgrep -f vitest` finds another
session's run, wait or skip and say so. Never `pnpm test:db:down`.

**`pnpm-lock.yaml` and `node_modules` are shared the same way the test database
is.** Two sessions installing at once fight over one lockfile. Check
`pgrep -f "pnpm (install|update|add)"` before installing, and treat the lockfile
as a file you own for the duration (protocol §7.2 — append it to your ledger).

---

## 5 — Report (review mode ends here)

Write the report in the shape of
`.claude/skills/luke-deps/references/review-report.md`.

Then stop. Review mode writes nothing. Ask whether to proceed with
`/luke-deps apply`.

---

## 6 — Pinning, overrides, alignment

**Carets do not protect you.** Reverting `@fastify/multipart` to `^10.0.0` still
resolved 10.1.1. A revert is an **exact pin plus a comment naming the version it
excludes and why** — otherwise the next install silently undoes it.

**Overrides are debt with an expiry date** (`lessons.md`). Pin a _range_, never
an exact version: an exact pin keeps forcing the vulnerable version after the
patch ships (GHSA-mh99-v99m-4gvg stayed live behind a `brace-expansion` pin).
Cap the range only when an uncapped one would drag consumers onto a new major
(`js-yaml: '>=4.3.2 <5'`), and only after `pnpm why -r <pkg>` shows no consumer
already declares it: a `<4` cap ran `fast-json-stringify@7` on fast-uri 3.x for
a month. Every override comments its GHSA or CVE id and its reason.
`check:drift` enforces the mechanical half — P15 in `check-platform-integrity`
(no exact pin, an advisory id in the comment) and `check-override-consumers`
(no cap below an installed consumer). Whether a cap or an upward unlock is
right, and whether an override has expired, stays this review.

On every run, review the whole `overrides` block: an override whose upstream has
since published a clean version in the natural range is dead weight — propose
removing it, then confirm resolution with `pnpm why <pkg>`.

**Version alignment across the workspace is CLAUDE.md rule 9, and this skill
owns it** (`.claude/skills/luke-shared/governance-map.md` §2).
`checkVersionAlignment` in `tools/scripts/check-platform-integrity.ts` enforces
it in `pnpm check:drift` on every push: a package carried at two versions is
fixed in the same cycle. `luke-audit` must not carry a second copy of the gate.

---

## 7 — Apply mode

Runs only on `/luke-deps apply`, and only against a plan from §5.

For each cycle, in plan order (D before everything else):

1. **Edit** the `package.json` files for this cycle only. Append every file you
   touch to your ledger (protocol §7.1), lockfile included.
2. `pnpm install` — read the output. Peer warnings are findings, not noise.
3. **Climb the ladder** to the level the matrix demands. Stop at the first
   failure.
4. **On failure**: decide, do not retry blindly.
   - upstream regression → revert to the last good version as an **exact pin**
     with a comment, and move the package to Held
   - intentional breaking change → the migration is its own `fix(<scope>)`
     commit, written and verified before the cycle closes
   - pre-existing failure → prove it with differential verification (§4), then
     say so and leave it out of scope
5. **Report the cycle** — packages, levels run, evidence, files changed — and
   propose the commit message. **Wait for approval.** Never commit.
6. Next cycle only after the previous one is committed or explicitly parked.
   Never leave two unverified cycles stacked in the working tree: that is the
   state that made `308256f` a bisection job.

A cycle that touches more than 3 files needs confirmation before it starts
(CLAUDE.md rule 2) — a majors cycle usually does not, a toolchain cycle always
does.

---

## 8 — Toolchain mode

Read `.claude/skills/luke-deps/references/toolchain-mode.md` in full before acting:
Node, pnpm, base images and GitHub Actions, and every site that pins them.

---

## 9 — Security mode

Read `.claude/skills/luke-deps/references/security-mode.md` in full before acting:
the advisory-driven procedure, the smallest change that clears the finding.

---

## 10 — Platform mode

Read `.claude/skills/luke-deps/references/platform-mode.md` in full before acting:
the deterministic gate first, then the semantic checks, then the report.

---

## 11 — Evaluate mode

Read `.claude/skills/luke-deps/references/evaluate-mode.md` in full before acting:
what a technology decision must weigh, and the four verdicts.
