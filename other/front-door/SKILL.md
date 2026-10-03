---
name: front-door
description: >
  Walk a repo's front door as a brand-new user would and report whether they can
  actually get from clone to working — not just whether the docs exist. Use whenever
  the user asks to audit, review, or critique a repo's onboarding, installation,
  setup, getting-started, or quickstart experience; asks "can a new user install
  this," "is the setup too hard," "why is onboarding so painful," "are there too
  many READMEs," "which doc is the source of truth," "did we leak an API key,"
  or wants install scripts and auth/login/credential
  paths checked for friction. Also fire automatically before you reassure someone
  that their setup is "easy" or sign off on a README — verify the path first.
  Covers competing/duplicate onboarding docs, install-script red flags, auth and
  access gates, prerequisites, first-run success, doc-vs-code drift, and
  accidentally committed secrets (API keys, tokens, private keys) in the tree or
  git history — honestly separating friction an AI agent can absorb from friction
  that needs a human. Can also save the audit as a persistent FRONTDOOR.md
  dashboard — a re-runnable health board whose every finding carries a
  deterministic check — and refresh that board on later runs.
---

# Front Door

Knock on the repo's front door as a cold newcomer with zero context — and report whether they get inside.

You tend to grade onboarding on whether the *artifacts* exist ("there's a README, there's an install script") instead of whether the *path works* ("a real person, starting from nothing, reaches a running state without getting stuck or guessing"). You also tend to praise tidy structure while missing that three docs quietly disagree about the install command. This skill makes you walk the path, not inventory the files.

## Operational safety — this skill is read-only

Every command this skill runs against the audited repo must be **non-mutating**: `ls`, `Read`/`cat`, `grep`/`git grep`, `git status`, `git log`, `git diff`, `git show`. Inspect install/test scripts — don't execute them.

**Never run a mutating or destructive command against the audited repo** — `git clean`, `git reset --hard`, `git checkout -- .`, `git worktree add`/`remove`, `rm -rf`, force-push, branch deletion, or anything in that family. This holds even when "just testing" the skill itself: an agent once tested this skill's write path using a git-worktree isolation mode, and the worktree machinery destroyed the entire repo. If you ever need to exercise this skill end-to-end, do it against a disposable `cp -r` copy in a scratch directory — never a git worktree of the real repo, and never the real repo itself.

The **only** write this skill ever performs is the optional `FRONTDOOR.md` dashboard file (see Dashboard mode below) — one file, at the repo root, and only after the user explicitly opts in on that specific run. No other file is ever created, edited, deleted, moved, or overwritten, and no git state is ever changed.

## Core idea

Two questions drive the whole audit:

1. **Is there one obvious front door, or several competing ones?** A newcomer should hit exactly one authoritative entry point. Multiple overlapping docs (root README + a `QUICKSTART` + a `docs/getting-started`) that each hold 60% of the truth and disagree on the rest are worse than one honest doc.
2. **Where does the path stall — and can an AI agent unstick it, or does it need a human?** This is the honest core. Assume ~70–80% of users can lean on an AI agent for friction. So the audit's job is to separate friction an agent absorbs from friction no agent can jump for them, and never disguise the second kind as the first.

## What to inspect

Walk these in order. Verify against the actual repo (file tree, file contents, manifests, scripts) — don't infer from the project's reputation. Note **which tree you're auditing**: a newcomer clones `HEAD`, not your uncommitted working copy, so if the tree is dirty say whether a finding reflects what a cloner gets or only your local edits.

**1. Source of truth & navigation.** Enumerate every onboarding-flavored file: `README*` (at every level), `QUICKSTART`, `GETTING_STARTED`, `INSTALL`, `SETUP`, `CONTRIBUTING`, `docs/`, wiki pointers. For each: where it lives, what journey it claims to cover, and whether it *agrees* with the others on the critical commands. Flag competition (two docs in one folder, a root README plus a subfolder README both claiming to be the start), conflicts (different install commands), and orphans (a newcomer can't find the entry point at all). Note: the fix is usually "designate one canonical entry, demote the rest to pointers" — not always "delete."

**2. The install path.** Read the actual scripts and commands. Check: undeclared prerequisites (specific Node/Python/runtime versions, package manager, OS, ARM vs x86, build tools); copy-paste fidelity (do commands run *as written*, or do they hide `<PLACEHOLDERS>`, assume a working directory, or break across a code fence); platform coverage (does a bash script silently exclude Windows/WSL; is there a Docker path); and the number of distinct manual steps to a usable state.

**3. Execution environment & network egress.** The path can pass every doc-and-script check and still fail at runtime because of *where* it runs. **Scope, so this doesn't blur with its neighbors:** point 2 owns broken commands and missing prereqs; point 4 owns whether the credential/account/scope exists; point 3 owns an *otherwise-correct* step that fails at an external boundary. Check: **sandbox/isolation** (does the tool — or the AI agent running it — run in a sandbox that blocks the keychain/secret-store, the filesystem outside a worktree, or host services?); **network egress** (does first-run reach a host a proxy, firewall, or an agent's allowlist would block? Name the host when you can see it in code/config/logs; mark it inferred otherwise); **secret-store access** (CLIs that read the OS keychain for credentials or root CAs fail when that store is unavailable). And flag that **the AI agent's own environment is part of this** — a command that's smooth in a plain terminal can be Blocked under a sandboxed agent, and that's a real wall, not a repo bug. (For the misleading errors these failures throw, see *The error message is a symptom* in Principles.)

**4. The auth & access path.** Trace what credentials, accounts, and permissions are required and *when*. Flag: secrets handling (is there a `.env.example`; are keys explained or assumed); login/OAuth/SSO/2FA steps; **transitive tool auth** — if the product orchestrates *other* CLIs/services (it shells out to a second tool), each of those needs its own install *and* its own independent login, which the product's docs usually can't satisfy for you (one tool → several separate auth walls); and — critically — **access gates** that no script reveals: account creation, ToS acceptance, paid tier or credit card, waitlist/invite/beta, an org admin who must grant a role or scope. These are the real walls.

**5. First success.** Is there a verifiable "it works now" checkpoint, and is it the *right kind* for the artifact — a running app (hello-world, expected output), a library (a passing import/usage snippet), a CLI/tool (a `--help` or a real command), a test/validation suite going green, or a skill/plugin actually registering? Roughly how long from clone to that checkpoint? Is there a troubleshooting / common-errors section, or does the path fail silently?

**6. Drift.** Does the doc match the code? Renamed scripts, dead links, commands referencing removed flags, version mismatches between the docs and the package manifest (e.g. a README claiming "12 tests" when the suite now runs 23). Drift quietly breaks even a well-structured front door.

**7. Leaked secrets.** Scan the tracked tree — and, if `git` is available, the history — for credentials that should never be in version control: live-looking API keys, tokens, private keys, connection strings with embedded passwords. Check the obvious places (a committed `.env` instead of `.env.example`, source, config, CI files, notebooks) and the easy-to-miss ones (real keys pasted into the README's *own* install examples, and keys deleted from the current tree but still sitting in history). Separate a **live-looking secret** — high-entropy string in a known provider format (`sk-…`, `ghp_…`, `AKIA…`, a PEM block) — from a harmless **placeholder** (`<YOUR_KEY>`, `sk-xxxx`, obvious dummy); don't cry wolf on examples. Report the file, line, and key *type* **redacted — never echo the full value** — and whether it's in the working tree, history, or both. Remediation is always **rotate first, then purge**: a leaked key must be revoked and reissued at the provider, because removing it from the repo does not unexpose it — every existing clone and the git history still hold it. Scrubbing history (`git filter-repo` / BFG) is the second step, never a substitute for rotation.

## Classify every friction point

Two axes. Get both on the table for each finding.

**Who can clear it:**
- **Agent-soluble** — an AI agent with terminal/web access absorbs this: interpreting vague or out-of-order steps, fixing a typo'd command or wrong path, inferring and installing an undeclared dependency, reading an error and applying the fix, reconciling competing docs by reading the code, porting a script to another platform. This is the 70–80% case.
- **Human-gated** — no agent jumps this *for* the user: creating/verifying an account, accepting ToS, payment or paid-tier/quota, waitlist/invite/approval, an admin granting access, provisioning a real API key from a real provider account, interactive 2FA / hardware token / SSO consent, physical hardware or an OS they don't have. **Name these plainly — they are the hoops.**
- **Partially gated** — the agent can prep everything up to the wall (scaffold the `.env`, draft the access request, stage the command) so the human's residual action is one click. Say what the agent does and what the one human step is.

**How hard the step is:** Smooth (works as written) / Bumpy (works but needs interpretation or a fix) / Blocked (stops a newcomer cold without outside help).

## Be honest about the AI-agent assumption

Assuming most users have an agent is fair — but it is not a license to wave away friction. Three rules:
- Never relabel a human-gated wall as "the agent will handle it." If the user must pay, get approved, or have an admin grant a scope, that hurdle stands regardless of how good the agent is.
- Count the residual human steps even in the agent-assisted path. "Smooth with an agent" still means *something* if the user must paste a real secret or click an OAuth consent. List those clicks.
- **The agent itself runs in an environment — and that environment can be the wall.** An agent that executes in a sandbox with a network allowlist can be *blocked from running the very command it would use to unstick the user* (a host it can't reach, a keychain it can't read). Don't assume "the agent absorbs this" without checking the agent can actually execute it; a command that's smooth in a plain terminal may be Blocked under the agent. When that's the fix, name it — e.g. "the agent must run this outside its sandbox."

## Output format

Lead with the verdict. Then the source-of-truth map (the thing most audits skip). Then findings ordered **quick wins first, then progressively heavier** — matching how the work actually gets done. Drop any section that doesn't apply; don't pad.

**Verdict:** [✅ Smooth / ⚠️ Bumpy / 🚧 Blocked] — one sentence: can a cold newcomer get to working, and what's the single biggest obstacle. (A live-looking leaked secret forces 🚧 regardless of how smooth the rest is.)

**🔑 Leaked secrets:** *(leads the report when found; omit the header only when the scan is clean and say so in one line.)* File + line + key *type*, **redacted**; working-tree / history / both; and the rotate-then-purge action. A live-looking committed credential is a stop-everything finding, not a fix-order item.

**Source of truth:** The competing-docs map. List each onboarding doc, where it lives, and the conflict/overlap. Name the one that *should* be canonical. (E.g., "root `README` and `docs/QUICKSTART` give different install commands; the root one is stale.")

**Path walk:** The journey from clone to first success as numbered steps, each tagged `[Smooth / Bumpy / Blocked]` and `[Agent-soluble / Human-gated / Partially gated]`. When a step is gated by the **environment** rather than the docs (point 3), name the blocking boundary or host — e.g. "blocked by the agent's network allowlist; `api.vendor.com` unreachable" — so the runtime wall doesn't hide behind a `[Blocked]` tag. This is where the honesty lives.

**The hoops:** The human-gated walls, called out separately so they can't hide — accounts, payment, approvals, real secrets, admin grants. If there are none, say so.

**Fix order:**
- **Quick wins** — minutes to an hour; high friction-removed-per-effort. (Add a `.env.example`; fix the stale command; add one "Start here" pointer at the top of the root README.)
- **Medium lifts** — an afternoon. (Collapse three competing docs into one canonical + pointers; add a verification checkpoint; document prerequisites.)
- **Heavy lifts** — real project. (Cross-platform install; reduce a multi-account auth flow; restructure docs/ navigation.)

*Add only if you couldn't verify something —* **Couldn't check:** [what, and why it matters].

## Dashboard mode — the persistent FRONTDOOR.md board

The report above is a point-in-time read. For a repo you'll re-check over time, the skill can also emit a **persistent dashboard file** — `FRONTDOOR.md` — that turns the same findings into a board you *refresh by re-running checks* instead of re-auditing by hand. This is the one write this skill ever performs — see *Operational safety* above; it still requires explicit opt-in every time, never a worktree, never any other file. Every status on the board is verified by a command in its checks block, so nothing is merely asserted. The shipped [`FRONTDOOR.md`](FRONTDOOR.md) in this skill's folder is the worked example; copy its shape.

**Offer it once, after the first audit.** When you finish the conversational report and the repo has **no** `FRONTDOOR.md` yet, offer a single time: *"Want me to save this as a persistent FRONTDOOR.md dashboard at your repo root? Each finding becomes a re-runnable check, so next time you refresh the board with one command instead of re-auditing from scratch."* Generate the file only if the user accepts. If a `FRONTDOOR.md` already exists, don't re-offer — **refresh** it instead (see below).

**Where it goes.** Default to `<repo-root>/FRONTDOOR.md` — a sibling of `README.md`, so its relative links and checks all resolve from the repo root. Only write it elsewhere if the user asks.

**Structure** — mirror the example, in this order:

1. **Title + one-paragraph charter** — what the board is, and when to refresh it (which onboarding docs / structure changes invalidate it).
2. **Metadata table** — `Last audited` (date **and which tree**: HEAD vs a dirty working copy), `Method`, `Verdict` (✅ Smooth / ⚠️ Bumpy / 🚧 Blocked + one line), and an *optional* `Remediation plan` pointer to a deeper fix doc (omit the row if there's none).
3. **Health at a glance** — one row per inspection dimension (`One front door`, `🔑 Leaked secrets`, `First success works`, `Doc ↔ code drift`, `Agent front door`, `Recent features documented`, …), each scored ✅ / ⚠️ / 🚧 with a one-liner. These are the seven *What to inspect* points, graded. (Here 🚧 marks a dimension that has open findings; reserve the *verdict's* 🚧 for a true wall.)
4. **Findings** — a table with `ID` (`FD-01`, `FD-02`, … — **stable across refreshes**), `Area`, `Sev` (🔴 high / 🟠 med / 🟡 low, tracking the Path-walk Blocked/Bumpy weight), `Status` (⬜ OPEN / ✅ FIXED), and `Fix`. Every row maps to exactly one check below. The quick/medium/heavy *Fix order* grouping can live in the optional remediation doc.
5. **Verified baselines (keep green)** — the ✅ facts that must not regress (secrets clean, one front door, first success passes), each with its check.
6. **Deterministic checks — re-run to refresh** — a single `bash` block, run from the repo root, with the invariant stated at the top: **empty output = all green; any printed line names an OPEN finding.**

**The checks block is the whole point — author it carefully:**
- One check per finding ID **and** per baseline. Label each printed line with its ID: `echo "FD-02 OPEN: README test count != recorded baseline"`.
- Each check prints **only when the finding is still open**, so a fully-green board produces *silence*: `grep -q '12/12' AGENTS.md && echo "FD-03 OPEN: ..."`.
- Keep checks **read-only and deterministic** — `grep` / `test` / `sed` / `git grep`. No mutations, no network except the secrets baseline, and **never execute the audited repo's own scripts, tests, or build to derive a number** — piping a run of `validate.sh` or the test suite through `sed` is execution wearing a read-only disguise, and it's the exact pattern that has destroyed a repo before (see *Operational safety*). For a moving number like a test-pass count, record it as a literal the operator updates by hand after running the suite themselves, then have the checks block only `grep` for that recorded value across the docs: `EXPECTED=36  # updated by hand after a manual run — never auto-derived by this block`.
- The leaked-secret baseline check stays in this block, and a hit forces the 🚧 verdict — same stop-everything rule as the conversational report.

**Refreshing an existing board.** Re-run the checks block. Any printed line → that finding stays ⬜ OPEN; silence on a line's ID → flip it to ✅ FIXED. Then update `Last audited`, re-derive the `Verdict` and the at-a-glance colors, and add new `FD-##` rows (each with its check) for anything the re-walk surfaced. Keep IDs stable — never renumber a fixed finding.

## Evidence discipline

Separate what you verified from what you're inferring, so the report is defensible:
- **Verified** — you read the file, ran/inspected the command, confirmed the version. State it as fact.
- **Inferred** — "a newcomer will likely stall here" is a judgment, not a fact. Mark it as such. Don't present a predicted confusion as a confirmed defect.

## Principles

**Walk the path, don't inventory the files.** "There's a README" is not a finding. "Step 3 tells you to run `setup.sh`, which assumes Python 3.11 but the repo never says so" is.

**One front door.** Competing entry points are a top-tier finding even when each doc is individually fine. Newcomers don't read all three; they pick one, and it's often the wrong one.

**Don't disguise a wall as a bump.** Agent-soluble friction is a bump. A required paid account is a wall. Keep them in separate buckets, always.

**A leaked live credential outranks everything.** It's not a friction bump or a fix-order item — it leads the report and sets the verdict. And the fix is rotate-then-purge: deleting the key from the repo does not unexpose it. Report the location redacted; never reproduce the value.

**Name the systems, not "it's complex."** "Requires a Klaviyo API key, an org-admin OAuth grant, and a paid tier" beats "auth is involved."

**The error message is a symptom, not the diagnosis.** A first-run failure often names the wrong cause — a blocked host or a sandbox can surface as "no keychain available" or "restart your computer." Trace what actually failed (which host, resource, or boundary) where you can observe it; where you can't, mark the cause **inferred** rather than restating the misleading message as fact. Either way, don't route the newcomer toward the fix the error literally names when the real wall is elsewhere.

**Order by effort, lead with quick wins.** The reader should be able to fix three things before lunch and know what the real project is.

**Coach, don't nitpick.** The goal is a smoother front door, not a list of everything wrong. Tie each finding to the newcomer it unblocks.

## Example (compressed)

**Verdict:** 🚧 Blocked — a live-looking API key sits in git history (rotate before anything else); separately, an agent-assisted user would otherwise reach working in ~15 min, but a real key and an admin grant remain unavoidable walls the docs never mention.

**Source of truth:** Three doors. Root `README` (full but stale install cmd), `docs/QUICKSTART` (current cmd, but no auth section), `CONTRIBUTING` (mixes contributor setup into the user path). Canonical should be `docs/QUICKSTART`; root README should point to it, not duplicate it.

**🔑 Leaked secrets:** Clean in the working tree, but git history holds a live-looking `sk-…` in an old `config.js` (commit `a1b2c3d`) — **rotate that OpenAI key now**, then scrub history. (`.env` is correctly gitignored; only `.env.example` is committed.)

**Path walk:**
1. Clone — `[Smooth] [Agent-soluble]`
2. Install deps — `[Bumpy] [Agent-soluble]` — undeclared Node 20 requirement; agent infers and installs.
3. Configure `.env` — `[Bumpy] [Partially gated]` — no `.env.example`; agent scaffolds it, but the user must paste a real key.
4. Provision API key — `[Blocked] [Human-gated]` — requires a provider account + paid tier.
5. First CLI call — `[Blocked] [Partially gated]` — `vendor-cli` reaches `api.vendor.com`, blocked by the agent's sandbox allowlist; it errors as "no keychain available" (a red herring — the real wall is egress). Fix: run it outside the agent's sandbox. *(point 3 — the failure the docs and auth both pass.)*
6. First run / verify — `[Smooth] [Agent-soluble]` — once keyed and reachable, `npm run dev` confirms it works.

**The hoops:** (1) provider account + payment for the API key; (2) org admin must grant the integration scope. Neither is in any doc.

**Fix order:**
- *Quick wins:* add `.env.example`; fix the stale root command; add "👉 Start at docs/QUICKSTART" to the top of the root README.
- *Medium:* fold the user-setup half of CONTRIBUTING into QUICKSTART; add an "Access you'll need (account, paid tier, admin grant)" callout before step 1.
- *Heavy:* single canonical onboarding doc with role-based branches (user vs contributor).

## What success looks like

The reader knows in one line whether a newcomer gets in, can see at a glance which doc is the real one, knows exactly which hurdles an agent removes and which they'll have to clear themselves, and has a fix list they can start on in the next ten minutes.