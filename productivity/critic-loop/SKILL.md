---
name: critic-loop
version: 1.0.0
description: |
  LLM-as-judge quality gate. Before any deliverable ships, spawn an independent
  critic subagent (or N critics with distinct lenses) that ADVERSARIALLY grades
  the artifact against an explicit rubric, returns PASS/FAIL + a prioritized fix
  list, and loops (build → critique → fix) until it passes or N rounds hit.

  The builder must NOT grade its own work. Critic defaults to FAIL on uncertainty.
  Output is a scorecard + prioritized fixes + a hard ship/no-ship verdict.

  Domain rubrics baked in for SkynetLabs work: client website, content/copy,
  automation/n8n, Upwork/Fiverr proposal. Generic mode takes any artifact + rubric.
  Multi-critic mode runs 3 lenses + majority vote (ties to fanout-ship pattern).

  Trigger when user says: "critic loop", "/critic-loop", "judge this", "grade this
  before I send", "is this good enough to ship", "quality gate", "have a critic
  review", "second-agent review", or before ANY billable deliverable leaves.

  Auto-trigger heuristic: a deliverable (site, copy, workflow, proposal, audit) is
  about to be sent to a client / deployed / posted, and no independent grade exists.
license: MIT
compatibility: claude-code
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Agent
  - TaskCreate
  - TaskUpdate
---

# critic-loop

LLM-as-judge quality gate. Operationalizes the "2nd agent grades/self-corrects
before you accept" lesson (claude-code-mastery, video 8). SkynetLabs only had the
manual `/review`; this is the automated gate that runs before a deliverable ships.

## Core principle

**The builder never grades its own work.** A model that wrote an artifact is biased
toward approving it. Spawn a SEPARATE critic agent with a clean context, give it the
artifact + rubric + adversarial framing, and let IT decide. Loop until PASS.

```
build → spawn critic (FAIL-biased) → PASS? ship : apply fixes → re-critique
                          ↑________________________________________|
                                 max N rounds (default 3)
```

## When to use

USE before:

- A client deliverable is sent (website, copy, audit, proposal, automation)
- A deploy / publish / `git push` to production
- Anything with secrets, credentials, or money flow

SKIP when:

- Throwaway scratch work, internal notes, exploratory spikes
- Already passed critic this session AND artifact unchanged
- Time-critical hotfix where the fix is trivial + reversible (still log it)

## Inputs required

1. **Artifact** — path(s), URL, pasted text, or git diff (`git diff main`)
2. **Type** — one of: `website` | `copy` | `automation` | `proposal` | `generic`
3. **Rubric** — auto-selected from type (below), or user-supplied for `generic`
4. **Mode** — `single` (1 critic, default) | `multi` (3 lenses, majority vote)
5. **Max rounds** — default 3
6. **Pass bar** — default: ZERO blockers + score ≥ 85/100

If type unclear → ASK before spawning. Wrong rubric = useless verdict.

## The recipe

### 1. Classify + load rubric

Detect artifact type. Load the matching rubric from `rubrics/<type>.md` (or the
inline blocks below). For `generic`, demand a rubric from the user — never invent
acceptance criteria silently.

### 2. Snapshot the artifact

- Code/diff: `git diff <base> > .critic/round-N.diff`
- Site: capture URL + run `/browse` or `/qa` to gather live evidence (CWV, links)
- Copy: save the exact text to `.critic/round-N.txt`
- Proposal: save text + the original JD it answers

Critic grades the SNAPSHOT, not a moving target.

### 3. Spawn critic(s) — ONE message

`single` mode: 1 `Agent` call with the critic prompt.
`multi` mode: 3 `Agent` calls IN ONE MESSAGE (true parallel), each a distinct lens:

- **Lens A — Correctness/Function:** does it work, is it true, no broken parts
- **Lens B — Standards/Craft:** meets the domain rubric, polish, brand
- **Lens C — Adversary/Risk:** what breaks in prod, secrets, legal, edge cases

Each critic gets a CLEAN context (`subagent_type: general-purpose`) and the
adversarial prompt below. Critics do NOT see each other's verdicts.

### 4. Collect verdicts

- `single`: that verdict is final.
- `multi`: majority vote. 2/3 PASS → PASS. Tie/any blocker → FAIL (default to
  caution). ANY critic raising a SECURITY blocker → FAIL regardless of vote.

### 5. Loop or ship

- PASS → emit final scorecard + ship verdict. Done.
- FAIL → take the prioritized fix list, apply fixes (builder context), bump round,
  go to step 2. Stop at max rounds.
- Hit max rounds still failing → STOP. Emit scorecard + remaining blockers +
  **NO-SHIP** verdict. Escalate to human. Do NOT ship a failing artifact.

### 6. Hard security gate

If the artifact touches secrets / credentials / deploy / payment / PII, run
`/security-review` (or a dedicated Lens C security pass) as a NON-NEGOTIABLE gate
BEFORE the ship verdict, even if all critics passed. Exposed secret = auto NO-SHIP.

## Adversarial critic prompt (the heart of it)

Each spawned critic gets THIS (vars filled):

```
You are an INDEPENDENT critic. You did NOT build this artifact. Your job is to
REFUTE it — find every fault, not to praise it. You are the last line before this
reaches a paying client. A miss costs the agency its reputation.

ARTIFACT TYPE: <type>
ARTIFACT: <path / url / inline text / diff>
LENS (multi-mode only): <A correctness | B craft | C adversary>

RUBRIC (grade against EACH line, cite evidence):
<rubric criteria>

RULES:
- Default to FAIL. Approve ONLY if you cannot find a real fault.
- Every claim of a fault MUST cite the exact line / element / sentence.
- Do NOT invent praise to soften. No "looks great overall."
- Severity each finding: BLOCKER (cannot ship) | MAJOR | MINOR | NIT.
- If you are UNCERTAIN whether something is correct → treat as a fault and FAIL.
- Check the artifact against the rubric ONLY. No scope creep.

OUTPUT (exactly this shape):
## Verdict: PASS | FAIL
## Score: <0-100>
## Blockers (must fix to ship)
1. [location] problem → required fix
## Major
...
## Minor / Nits
...
## Evidence checked
<what you actually inspected: ran links? viewed render? grepped secrets?>

ultrathink before grading. Be specific. Be harsh. Be fair.
```

## Baked-in domain rubrics

Full versions in `rubrics/`. Summaries:

### (a) website — `rubrics/website.md`

- [ ] Responsive: no horizontal scroll / broken layout at 375 / 768 / 1440px
- [ ] Zero broken links (internal + external) — critic must actually check
- [ ] SEO meta present: unique `<title>`, meta description, OG tags per page
- [ ] Schema.org JSON-LD present + valid for page type (LocalBusiness/Article/etc)
- [ ] Core Web Vitals: LCP < 2.5s, CLS < 0.1, no render-blocking obvious sins
- [ ] NO lorem ipsum, NO placeholder text, NO `#` dead hrefs, NO TODO comments
- [ ] All images have alt text + are not broken
- [ ] Favicon + 404 page exist
- [ ] Forms submit somewhere real (not `action=""`)
- BLOCKER if: any lorem/placeholder, broken link, missing title/meta, layout break

### (b) content / copy — `rubrics/copy.md`

- [ ] Run `/humanizer` check — no AI tells (em-dash overuse, rule-of-three,
      "in today's fast-paced", negative parallelisms, inflated symbolism)
- [ ] NO fabricated claims, fake stats, invented testimonials, or unverifiable numbers
- [ ] Brand voice matches (for the author: contrarian hook → reframe → arrow lines →
      vulnerability beat → CTA; 1 local authenticity anchor; 1 real client win)
- [ ] Reading level + length fit the channel
- [ ] CTA present and singular
- [ ] No spelling/grammar errors; no broken markdown/links
- BLOCKER if: fabricated claim, fails humanizer hard-fail, wrong brand for channel

### (c) automation / n8n — `rubrics/automation.md`

- [ ] Error handling on every external call (retry / error branch / no silent fail)
- [ ] NO exposed secrets — keys in credentials store, not in node params / code / URLs
- [ ] Idempotent: re-running won't double-charge / double-send / duplicate records
- [ ] Webhook auth / signature verification where applicable
- [ ] Rate-limit + timeout handling on HTTP nodes
- [ ] Validated via n8n-mcp `validate_workflow` (no orphan nodes, valid expressions)
- [ ] Timezone correct (America/New_York for GHL, NOT America/Cancun — known trap)
- [ ] Logging / observability on failure path
- BLOCKER if: any exposed secret, no error handling on money/send action, non-idempotent

### (d) Upwork / Fiverr proposal — `rubrics/proposal.md`

- [ ] Mirrors the JD: echoes the client's exact words / stack / outcome in first 2 lines
- [ ] Price anchored (a number or range stated with rationale, not "let's discuss")
- [ ] Real proof woven in (named relevant SkynetLabs win, not generic flattery)
- [ ] 2-3 sharp questions that prove expertise + qualify the client
- [ ] Presumptive CTA (assumes next step: "I can start Monday — want the Loom?")
- [ ] 120-180 words, no AI-template smell, no "I am writing to express my interest"
- [ ] Red flags in JD surfaced (scope creep, low budget, vague deliverable)
- BLOCKER if: doesn't mirror JD, no price anchor, no questions, generic/templated

## Scorecard output (final)

Emit exactly this when the loop ends:

```
═══ CRITIC-LOOP SCORECARD ═══
Artifact: <name/path>      Type: <type>      Mode: <single|multi>
Rounds run: <n>/<max>      Pass bar: 0 blockers + ≥85

Round history:
  R1: FAIL (score 62) — 3 blockers, 5 major
  R2: FAIL (score 79) — 0 blockers, 2 major
  R3: PASS (score 91) — 0 blockers, 1 nit (accepted)

Multi-critic vote (if multi): A PASS · B PASS · C PASS  → 3/3 PASS
Security gate: PASS (no secrets) | N/A | FAILED

Remaining (non-blocking):
  - [MINOR] <thing> — optional polish

VERDICT: ✅ SHIP   |   ⛔ NO-SHIP (escalate)
```

## Files

- `rubrics/website.md` — full client-site rubric (responsive/links/SEO/schema/CWV/placeholder)
- `rubrics/copy.md` — content rubric (humanizer + no-fake-claims + brand voice)
- `rubrics/automation.md` — n8n rubric (error handling/secrets/idempotency/tz)
- `rubrics/proposal.md` — Upwork/Fiverr rubric (mirror JD/price/questions/CTA)
- `rubrics/generic.md` — template: how to author a one-off rubric
- `prompts/critic.md` — full adversarial critic prompt (copy-fill)
- `prompts/lenses.md` — the 3 multi-critic lens definitions (A/B/C)
- `scripts/snapshot.sh` — capture diff/text/url evidence into `.critic/round-N.*`
- `scripts/spawn-block.md` — copy-paste Agent call block (1 or 3 critics)
- `scripts/tally-votes.md` — majority-vote + security-veto decision logic
- `templates/scorecard.md` — final scorecard template

## Decision logic (multi-mode)

| Critics                | Blocker raised? | Security blocker? | Verdict                        |
| ---------------------- | --------------- | ----------------- | ------------------------------ |
| 3/3 PASS               | no              | no                | SHIP                           |
| 2/3 PASS               | no              | no                | SHIP                           |
| 2/3 PASS               | yes (1 critic)  | no                | FAIL — fix blocker, re-loop    |
| 1/3 PASS               | —               | —                 | FAIL                           |
| any                    | —               | yes               | NO-SHIP (auto, overrides vote) |
| max rounds, still FAIL | —               | —                 | NO-SHIP — escalate to human    |

Default to caution: when the vote is ambiguous, FAIL.

## Cost model

- `single` mode: ~1 critic agent per round × rounds. Cheap. Default for most work.
- `multi` mode: ~3 critic agents per round (parallel). Use for high-stakes / large
  deliverables (flagship site, big proposal, client-facing automation).
- Loop converges fast: most artifacts PASS by round 2-3. If round 3 still fails,
  the artifact has a structural problem — rebuild, don't keep patching.

Break-even: any billable deliverable. One caught lorem-ipsum or exposed key pays
for a year of critic runs.

## Integration with existing skills

- Use AFTER builder skills: `skynet-site`, `flagship-build`, `social-stack`,
  `upwork-proposal`, `aeo-daily`, n8n builds — critic-loop is the gate they exit through.
- Critic CAN call: `/humanizer` (copy), `/qa` + `/browse` (site), n8n-mcp
  `validate_workflow` (automation), `/security-review` (secrets gate).
- Complements `/review` (pre-landing PR) — `/review` is for code diffs; critic-loop
  is for finished deliverables of any type.
- Pairs with `fanout-ship`: fan out N builds → critic-loop each before integration.

## Failure modes + fixes

| Failure                         | Cause                                       | Fix                                                        |
| ------------------------------- | ------------------------------------------- | ---------------------------------------------------------- |
| Critic rubber-stamps everything | Not adversarial / builder graded itself     | Use the FAIL-default prompt; spawn SEPARATE agent          |
| Loop never converges            | Same blocker re-introduced each round       | Stop at max rounds → rebuild, don't patch                  |
| Critic invents fake faults      | Hallucinated criteria                       | Pin rubric; "grade against rubric ONLY, cite evidence"     |
| Passed but broke in prod        | Critic didn't actually check (links/render) | Force "Evidence checked" section; run /qa /browse for real |
| Secret shipped despite PASS     | No security gate                            | Hard gate step 6 — auto NO-SHIP on any secret              |
| Multi-critic all agree wrongly  | Same blind spot, same context               | Give each a DISTINCT lens; one is pure adversary           |

## Anti-patterns

- ❌ Builder grading its own artifact (bias = false PASS)
- ❌ Critic with a soft/balanced prompt (must default to FAIL)
- ❌ Vague rubric / no rubric (verdict is meaningless)
- ❌ Shipping after max rounds while still failing (escalate instead)
- ❌ Skipping the security gate because "critics passed"
- ❌ Spawning the 3 multi-critics in separate messages (loses parallelism)
- ❌ Letting the critic grade a moving target (snapshot first)
