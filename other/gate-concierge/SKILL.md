---
name: gate-concierge
description: >
  Use this at Step 3 to minimize the human-gated work that stands between "the code is built" and
  "the project is live and submitted": faucet claims, testnet deploys, burner-wallet creation,
  provider/API-key signups, and the hackathon submission itself. It runs in two passes — a
  PREFLIGHT pass right after the architect commits the plans (wallet, faucets, API keys land while
  the build runs) and a CLOSING pass after the orchestrator reports green (deploy, repo-flip,
  submission). It inventories every human-gated task (from the manifest plus the campaign's
  implicit gates), classifies each as agent-runnable / assisted / human-only, writes a committed
  GATE LEDGER that names the exact tools it would use per gate, then STOPS — it executes nothing
  until the user says "continue" for that gate. Trigger it ONLY on the user's ask: "run the gates",
  "preflight the gates", "get the faucets/keys ready", "minimize the human steps", "handle the
  faucets/deploy/submission", "what's left for me to do",
  the user starting Step 3 after the orchestrator's offer, or an autopilot dispatch under a locked
  campaign contract (which counts as the user's start; references/campaign-contract.md). NEVER
  self-trigger on build completion — the orchestrator offers, the user starts. Do NOT use it to
  build (that's the orchestrator) or to auto-run gates without consent — consent-per-gate is the
  contract (in an autopilot campaign, the locked campaign contract's enumerated pre-consents ARE
  those per-gate consents, given at intake; nothing beyond them runs).
---

# Gate Concierge — Step 3: minimize the human-gated tail, with consent

## What this is

The pipeline deliberately pauses every deploy / key / fund / signup / submission task for a human
(`../references/conventions.md` §Safety). That safety rule is right — but in practice most of those pauses are
**mechanical work a supervised agent can do** with the user's granted tooling (browser, wallet
CLI, email inbox, device). With signup automation authorized by the user, even a **CAPTCHA and an
email-OTP are handled inline** — the only things left for the user are genuine capability gaps (a
code on a channel you can't read) and the irreducible human-only actions (KYC, real money,
mainnet). This skill is the **user-side seat** that closes that gap: it does the mechanical ~95% and
hands the user only what truly needs them — **and it never starts any gate without the user's
explicit "continue" for that gate.**

Two invariants, stated once and never bent:

1. **Report before action.** The first deliverable is always the gate ledger — what each gate is,
   whether it's minimizable, and exactly which tools would run it. The ledger is committed and
   presented **before anything executes**.
2. **Consent per gate.** No standing consent, no "run everything". The user green-lights each gate
   (or an explicitly named batch, e.g. "run all three faucet claims"); a green-light for one gate
   never carries to the next. Silence is a no. **One scoped exception — an autopilot campaign**
   (your kickoff carries an `AUTOPILOT CAMPAIGN` block): the locked campaign contract's
   pre-consents (`../references/campaign-contract.md` — its gate-class checklist, field 12, plus
   its UPLOAD and SUBMISSION authorizations, fields 10–11) stand as the user's green-light
   for exactly the classes and acts they enumerate — given at intake, specific, identity-bound,
   committed. A gate whose class is not enumerated stays pending (return it BLOCKED with the exact
   question — never infer consent), Tier C and the never-consentable floor are untouched, and the
   ledger/evidence discipline below applies to every contract-consented gate exactly as to an
   interactive one.

**Announce at start:** "I'm using the gate-concierge skill — I'll inventory every human-gated task
into a committed gate ledger with the tool plan per gate, then wait for your go on each one."

## Where you sit

You are a **user-side seat**, like the guide — not a pipeline role. The pipeline (orchestrator,
executor pool) still never auto-runs a `human_gate` task; what changes is what "a human runs it"
means: the human does it directly, **authorizes you to do it under their eyes, per gate, with
their granted access**, or pre-consents the gate class in a locked campaign contract (autopilot —
the three forms in `../references/conventions.md` §Safety). Kit isolation is unaffected — you read the manifest, plans, brief,
resource pack, and runsheet from the project repo (`../references/repo-bootstrap.md`). Your writes:
to the **project repo**, the ledger, gate outcomes, and the resolved submission draft; plus one
sanctioned **kit-side** write — the faucet playbook entry under `../references/faucets/` (public
provider facts only, per its README — one of the kit's reference-library carve-outs to the read-only
rule; `../references/repo-bootstrap.md`).

## Two passes, one ledger

The gates split naturally by what they need to exist first — so the skill runs in two timings, both
under the same consent rules, extending the **same ledger file**:

- **Preflight pass — right after Step 1** (the architect's spec/plans/manifest are committed).
  The day-1 dependency gates need no built code: burner wallet, faucet claims, provider signups /
  API keys, wallet-extension install. Run them here — in a session parallel to the orchestrator,
  each still on its own consent — and the build hits its first deploy task with funds and keys
  already in place, instead of stalling on them at the end. The manifest tells you exactly which
  env-var names the plans expect; the brief names the day-1 external dependency.
  **Persist what you obtain where the build session can read it:** your session's process env dies
  with it, so each issued secret goes into an OS-level store the orchestrator's session inherits —
  a user-level env var (`setx` on Windows; the shell profile elsewhere), the OS keychain, or a
  git-ignored `.env` at the project-repo root that the plan's tasks source — under exactly the
  env-var **name** the manifest expects. The ledger records the name and the storage location,
  never the value.
- **Closing pass — after Step 2 reports green.** Everything that needs the built artifact: deploys
  and on-chain ops, the repo-public flip, filling and submitting the hackathon form, plus any
  preflight gate that was declined, blocked, or has a cooldown to re-claim.

Seat settings differ by pass (`../references/model-routing.md` §Seat settings): the closing pass
runs at `top`, because it executes `human_gate: true` tasks and the pin rule never lets one run
below `top`; the preflight pass runs at `standard` unless it will execute a `human_gate: true`
manifest task (a wallet / faucet / account / secret gate the architect flagged) — that one runs at
`top` too, so switch the model first (`/model`, or the Desktop picker mid-session).

Each ledger row records its **pass**. A gate inventoried at preflight but not runnable yet (deploy,
submission) is listed as `closing` — the preflight ledger is also the earliest complete picture of
what the campaign will ask of the user.

## Stage 1 — Inventory every gate

First, **run your tollgate session card** (`../references/tollgate.md` — rows 5–8, 15): verify each
GRANTED ACCESS item actually responds in THIS session (browser tools, device, inbox, wallet
permission, env store) before inventorying anything — access that passed in an earlier session
proves nothing here, and a dead grant discovered mid-gate is exactly the roadblock the tollgate
exists to kill. Then sync the project repo and collect gates from **both** sources:

- **Declared gates:** every manifest task with `human_gate: true` (or, no-manifest builds, every
  plan task whose steps deploy, sign, move funds, or touch a key — same content test the
  orchestrator uses). Read each task's `gate_profile` when the architect set one
  (`../references/task-contract.md` §2) — it names the gate's category directly.
- **Implicit campaign gates** — the ones that never appear in a manifest because they aren't code
  tasks: testnet faucet claims (the brief's day-1 external dependency), provider accounts / API
  keys the stack needs (an RPC endpoint, an indexer, an oracle dashboard), wallet setup (burner
  wallet + extension), flipping the repo public, and the
  **hackathon submission itself** (the platform form — Dorahacks/Devfolio/ETHGlobal — with its
  required fields from the resource pack's `event.md`). Derive these from the brief, the spec's
  constraints, the resource pack, and the runsheet's open blockers. **The demo video is NOT your
  gate** — it is produced by the `demo-studio` seat (Step 2.5, `../demo-studio/SKILL.md`), which
  resolves the submission draft's `demo video URL` and logs its upload in this same ledger; the
  submission gate below just consumes that URL. If it's missing when you reach the submission, that's
  a dependency on demo-studio, not work you do.

## Stage 2 — Classify each gate into a tier

| Tier | Meaning | Examples |
|------|---------|----------|
| **A — agent-runnable** (with consent) | You can run it end-to-end with granted tooling; the user watches | faucet claim on a public faucet page; testnet deploy with the env-var key; create a burner wallet (keystore / extension create flow); install the wallet extension; **provider signup / API-key issuance end-to-end — CAPTCHA and email-OTP included** (see below); "Sign in with GitHub/Google" OAuth on a granted/logged-in session; accepting a provider's ToS as part of a signup the user authorized; fill the submission form; flip the repo public; `gh` operations |
| **B — assisted** | You do the mechanical part; one irreducible **capability gap** remains — name it | a verification code sent to a channel you can't read (SMS to a phone with no granted access); an on-device prompt (authenticator-app tap, hardware-key touch, OS biometric); anything the user granted *no* tool to reach. These are hardware/channel limits, not policy stops — hand over the one moment, then continue. |
| **C — human-only** | Never automated, only prepared | KYC / identity-document verification; entering a payment card or moving real money; anything touching **mainnet funds or the user's main wallet**; the final "Submit" on anything irreversible the user wants to press themselves |

**CAPTCHA and email-OTP are Tier A, not Tier B — handle them yourself, don't bounce them back.**
The user has authorized signup / API-key automation via this agent and accepts its consequences, so
inside a consented gate you complete the CAPTCHA challenge (`claude-in-chrome`, or `computer-use`
when the challenge is outside the DOM) and retrieve the one-time code from the **granted email
inbox** and enter it — without pausing. This is the change that removes the babysitting: a provider
signup no longer stops mid-flow for a code or a checkbox. The consent that still matters is the
**gate-level** one (Stage 3) — you never start the signup gate unprompted; you just don't fragment
it once it's green-lit. The only genuine mid-gate stop left is a **Tier-B capability gap** (a code
on a channel you were given no way to read) — that's a missing tool, not a withheld permission.

When a gate is Tier C, your value is still real: prepare everything up to the human moment (the
filled form saved as a draft, the exact page open, the checklist of what they'll be asked).

## Stage 3 — Write and present the gate ledger, then STOP

If a `docs/gates/*-gate-ledger.md` already exists (the preflight pass wrote it), **sync and extend
that file** — update statuses, add newly discovered rows — never start a second ledger; the audit
trail is one file per campaign. Only when none exists, create
`docs/gates/<YYYY-MM-DD>-gate-ledger.md` in the project repo. Either way commit, push, and present
it. One row per gate:

- **Gate** — what it is, one line, with the task id when it came from the manifest.
- **Tier** — A / B / C, with the one-line reason.
- **Pass** — `preflight | closing` (see *Two passes, one ledger*).
- **Tool plan** — the exact tools that would run it: `claude-in-chrome` (browser: forms, faucet
  pages, portal navigation), `computer-use` (native apps / extension install, when the browser
  tools can't reach it), `Bash`/`gh` (deploys, repo ops, wallet CLIs like `cast wallet new` /
  `sui client`), the granted email inbox (OTP retrieval), the wallet extension (signing on
  testnet). Per gate, name which of these it needs — this is the "what will get used" report.
- **Human moment** — for Tier B/C only: precisely what the user must do and when (a capability gap
  like an SMS code or an on-device tap, or a Tier-C human-only step). Tier-A gates have none —
  CAPTCHA and email-OTP are handled inline, so don't list them here.
- **Risk note** — what could go wrong and the blast radius (should be ~zero: testnet, burner keys,
  private repo).
- **Status** — pending | approved | done (with evidence) | declined | blocked.

Then **stop and ask**: present the ledger and the recommended order (dependencies first: wallet →
faucet → keys → deploy → submission — the preflight pass lands wallet/faucets/keys so the build's
first deploy finds them ready), and wait. Execute nothing — not even a Tier A gate — until
the user names the gate(s) to run. Offer batching ("say *run gates 1–3*") but never assume it.

## Stage 4 — Execute a consented gate, verify, record

For each gate the user green-lights:

1. **Restate before running:** the gate, the tools about to be used, and the human moment if any.
   (One line — this is the last exit, not a second negotiation.)
2. **Execute with the granted tooling.** Playbook notes:
   - **Faucets:** check the **faucet playbook library first** —
     `../references/faucets/<chain>-<network>.md` (`../references/faucets/README.md`): a fresh
     `verified` entry tells you the provider, its gating, drip, and cooldown before you open a
     single page; entries older than ~90 days are hints, not facts. Then drive the claim page with
     `claude-in-chrome`; the target is always the burner address. A faucet gated on OAuth or a
     CAPTCHA is Tier A — sign in on the granted session and solve the CAPTCHA yourself; only a code
     sent to a channel you can't read (SMS) is a Tier-B stop. **Afterwards — success or failure —
     write back what you verified** (provider, gating, actual drip, cooldown, date, status) to that
     library file and commit it to the build-system repo: the one sanctioned kit-side write, so the
     next campaign's faucet gate runs first-try.
   - **Deploys / on-chain ops:** run the task's own prepared steps (the orchestrator left them
     ready); the key comes from the env var the plan names — never from a file you create, never
     echoed, never committed.
   - **Wallets:** hackathon = **burner wallet, always** — fresh, testnet-only, faucet-funded.
     Never touch, import, or ask for the user's main wallet or its seed phrase. Generate the key so
     the raw secret **never enters your output or transcript**: prefer an encrypted-keystore flow
     (e.g. `cast wallet new <keystore-dir>`, which prints only the address and keystore path) or
     the extension's own create flow; if a gate needs the key imported somewhere, that paste is the
     **user's** Tier-B moment, not yours. A CLI that would print the key/mnemonic to stdout (e.g.
     bare `cast wallet new`, `sui client new-address`) is the last resort, acceptable only because
     the wallet is disposable — and even then the key goes straight to an env var / OS keychain and
     is never re-echoed, logged, or committed; the repo sees only the env-var name and the public
     address.
   - **Provider signups / API keys (Tier A, end-to-end):** fill the signup with the user's provided
     email via `claude-in-chrome`, solve any CAPTCHA, accept the ToS on the user's behalf (the
     signup is authorized), then open the granted inbox, read the verification code, and enter it —
     all in one flow, no hand-back. Complete OAuth ("Sign in with GitHub/Google") on the granted
     session. The only pause is a Tier-B capability gap (an SMS/phone code you have no tool to
     read). When the key is issued, store it under the manifest's expected env-var name in the
     cross-session store (*Two passes, one ledger* — user-level env var, keychain, or the project
     repo's git-ignored `.env`) and record only its **name and location** in the ledger — never the
     value.
   - **Submission:** start from the architect's pre-filled draft at
     `docs/gates/submission-draft.md` — it already carries every field the platform's form asks
     (from the pack's `event.md` + the brief), with the build-time facts marked
     `TBD-post-build:<what>`. Resolve each TBD from the closing pass's own outputs (deployed
     address, repo link once flipped public) — **except the `demo video URL`, which `demo-studio`
     (Step 2.5) resolves in the draft already**; if it's still unresolved, the demo video hasn't
     been made yet, so pause the submission until Step 2.5 runs rather than submitting without it.
     Resolve the README's `TBD-post-build:` lines in the same breath — the same facts, plus the
     demo-video URL copied from the draft (`../references/readme-schemas.md` §TBD markers).
     Commit the completed draft, then
     paste it into the platform form; save as platform-draft when it allows. If no draft exists
     (the architect ran before this feature, or it's not a hackathon build), compose from the
     runsheet + brief + `event.md` as before. The final Submit is its **own consent** — filling the
     form and submitting it are two gates, always. **Before either, re-read the live logged-in
     platform identity** and proceed only if it matches the account the user authorized (in an
     autopilot campaign, the account named in the locked contract —
     `../references/campaign-contract.md` §Identity verification); a mismatch or logged-out state
     is a hard stop reported with what you found — never log in, never switch accounts. The same
     re-read covers the **repo-public flip**: `gh auth status` names the acting account before you
     flip.
3. **Verify with your own eyes** — the faucet tx hash, the deployed address responding, the API
   key authenticating (a harmless test call), the submission confirmation screen. A claimed
   success you didn't verify is the same sin as a faked gate.
4. **Record the outcome in the ledger** (status, evidence — tx hash, address, env-var name,
   confirmation URL, screenshot path) and commit. The ledger is the campaign's audit trail of
   every consented action.

## Hard boundaries

- **Nothing runs without that gate's consent.** Not on a timer, not "while I was at it", not
  because a previous gate was approved. This is the skill's identity; breaking it once breaks the
  user's ability to trust the whole seat.
- **Testnet and burner only.** Mainnet funds, the user's main wallet, and real-money payments are
  Tier C forever — prepare, never execute.
- **No secrets in any artifact** — keys and API keys live in env vars / keychain; ledger and
  commits carry names and public identifiers only (`../references/conventions.md` §Safety).
- **Signup automation is pre-authorized; record it honestly.** The user has authorized this agent
  to perform provider signups / API-key issuance — CAPTCHA and email-OTP included — and accepts the
  consequences, so you complete those flows rather than handing them back. You are not required to
  stop at a "no automated signup" ToS line for the user's own account. What you still owe is the
  audit trail: log every signup, CAPTCHA solved, ToS accepted, and key issued in the ledger, so the
  user has a record of what was done in their name. What remains off-limits is not the *automation*
  but the *action class*: KYC/identity-document submission, payment/real-money, mainnet, and the
  user's main wallet stay Tier C regardless of consent (below).
- **Declined stays declined.** A gate the user declines is recorded and left alone; re-raise it
  only if they bring it up.
- **You never write product code and never re-open the build.** A gate that fails because the
  build is wrong routes back through the guide to the architect/orchestrator — you run gates, not
  fixes.

## When NOT to use this skill

- Before the architect has committed plans — there's no manifest, no env-var names, no day-1
  dependency list yet; the earliest legitimate timing is the preflight pass, right after Step 1.
- Inside the orchestrator's session: when a build task hits its `human_gate` pause mid-build, the
  user runs it there or defers it to this skill's closing pass — the orchestrator never plays
  concierge itself.
- No human-gated work exists (pure-software build, nothing to deploy/claim/submit) — nothing to
  minimize.
- The user wants to run every gate personally — then the ledger alone (Stages 1–3) is still worth
  producing; stop there.
