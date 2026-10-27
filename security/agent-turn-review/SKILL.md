---
name: agent-turn-review
description: >
  Internal ACE turn step — ACE's pre-send review: one inline §A–§F pass before every outbound
  reply, deliverable or PR.
user-invocable: false
---

# Agent turn review (ACE)

Run before every outbound action (the thing that gets dropped under load).

> ## Do NOT call the `Skill` tool for this review
>
> Not on `canopy:agent-turn-review`, not on `agent-turn-review` bare. Dispatching a skill hands
> back the fleet body and reads as "the review ran" — at which point everything in **§F** below,
> where ACE's send-path rules live (read-backs, capability-denial probes, the call ban,
> `bin/ace-email`), never gets applied. The fleet file contains no ACE rules at all: `grep -c
> 'bin/ace-email\|ace@dimagi-ai.com'` over it returns 0 (checked against canopy 0.2.441,
> 2026-08-27).
>
> **The review is ONE pass through §A–§F, applied inline by you.** §A–§E are canopy's; §F is
> ACE's; there is no boundary between them at review time. A pass that stopped at §E is not a
> review.

## Step 1 — READ the fleet body from disk (don't dispatch it)

```bash
sed -n '1,220p' "$(ls -d ~/.claude/plugins/cache/canopy/canopy/*/skills/agent-turn-review/SKILL.md | sort -V | tail -1)"
```

Read it, don't skim it — it is the source of §A–§E and it changes; ACE deliberately does not
copy it here, so this file cannot go stale against it. As of canopy 0.2.441 the sections are:

| § | Fleet section | What it catches |
|---|---------------|-----------------|
| A | Fidelity | the draft doesn't do what was actually asked |
| B | Grounded commitments | "I'll do X" / "I did X" with no executable mechanism or no verification |
| C | Presentation | buried verdict; §7a no-op turns and §7b problem-found turns must LEAD with the decision |
| D | Revision check | edit-introduced defects + repetition, re-run on EVERY revision |
| E | Counterpart framing | auditing the counterpart's own numbers; asserted-not-sourced facts |

Note canopy's closing "Adopting it in an agent" section still tells agents to write *"invoke
`canopy:agent-turn-review`"* — that instruction is the origin of this whole failure mode and ACE
deliberately does not follow it. Raised upstream; do not restore that wording here.

## Step 2 — apply §A–§E to the draft

Inline, in order, against the actual body you are about to send.

## Step 3 — apply §F below

Same pass, same draft. Not an appendix, not a follow-up.

## F. ACE specifics — the same pass, continued
- **A turn-closing report opens with the DECISION or the next step the human has to act on.**
  Canopy §C/7a covers the turn that concluded NO-OP and §7b the turn that FOUND a problem; this is
  the third shape they leave open — the turn that did real work and then buries the answer under
  how the session got there. **Environment and tooling housekeeping — plugin versions, MCP
  restarts, auth re-logins, worktree state, which command failed and what you tried next — goes
  BELOW the decision, or is cut entirely.** It is context for how you got the answer, not the
  answer; and it is disproportionately what an ACE turn accumulates, so it disproportionately
  gets written first. If a housekeeping item genuinely requires the human to act (a restart they
  must perform), that IS a decision — state it as one, at the top, in one line. Then answer,
  explicitly and every time, the two questions that otherwise get dropped: **are there open
  issues needing a decision, and is the session safe to continue as-is?** (Origin: Jon,
  2026-08-26/27 — two corrections on this exact shape in one window: *"stop talking about
  caffient it doesn't matter, what should we do next?"* and *"Do we have issues that need to be
  closed out? I can't tell based on what you said. And are we ready to continue or do I need to
  restart the session?"* Seven of eight human corrections that window were tagged `confusion`
  rather than direction. Fleet-general → candidate for promotion into `canopy:agent-turn-review`
  §C, alongside 7a/7b.)
- **An outbound message is judged on USABILITY as well as accuracy — every other check in this
  file tests whether the reply is TRUE, none tests whether it is usable.** A reply can pass §A–§E
  and §F clean and still fail, because correctness and legibility are different properties. Before
  sending, apply the recipient test: after ONE read, can they name (a) what changed, (b) the ONE
  thing to look at first, and (c) what is being asked of them? If not, **reorder — do not add.**
  **Length is evidence, not the defect:** a reply that runs long usually does so because ordering
  was never decided, so the reader is made to do the prioritising the sender skipped. For a message
  ASKING someone to review something, the shape that works is three explicit blocks: an OVERVIEW
  surface (one link, time-boxed — "about five minutes"), a SPECIFIC list in DEPENDENCY order (the
  item whose answer changes the most downstream first), and an explicit **"not worth your time
  right now"** list. That third block is what makes the second credible: without it every item
  reads as equally urgent, and naming what you are NOT asking for is the cheapest way to show the
  list was actually prioritised rather than dumped. (Origin: 2026-09-08,
  `poverty-graduation/20260908-0510` — a reply to an external design author passed the full review
  clean at ~1,180 words: fidelity verified against every open ask, all done-claims read back
  against live systems, rendering dry-run checked, recipients derived structurally. The operator's
  verdict was *"this email is quite bad … Be very clear on what you thnk she should review as an
  overview and then what you think she should review specifically before we iterate on a next
  run."* Nothing in it was untrue; the reader simply could not tell what to do. Rewritten into the
  three blocks above it came to 798 words. Fleet-general for every turn-based agent → candidate for
  promotion into `canopy:agent-turn-review` §C, alongside 7a/7b.)
- **A reply about a run leads with the run's ace-web page — Drive is ACE's storage, not the
  reviewer's surface.** For any run, the OVERVIEW link above is `ace_web_summary_url` from that
  run's `run_state.yaml`; Drive, HQ and Connect links appear only as deep links behind it. Check
  the draft's FIRST link: a Doc, a folder or an HQ page there means reorder. `bin/ace-email`
  backstops the Drive half (it refuses a Drive-linked body with no ace-web link unless
  `--no-run-page "<why>"`); an HQ-only body passes the rail, so that half is yours to catch.
  (Origin: ace#2378 — Jon, 2026-09-11, on a draft reply to Sophie: *"You should be thinking of
  AceWeb as the primary surface … You don't want to just point her at Google Drive."*)
- **Never cite a GitHub issue or PR to a programme counterpart as a deliverable or a receipt of
  work.** The rule above fixes which link LEADS; this one fixes which links belong at all. "Filed
  as #N" and "merged in PR #N" are ACE-side bookkeeping — a counterpart who cannot open the tracker
  can do nothing with either, and offering them as progress swaps ACE's activity in for the thing
  they actually asked for. Describe the change by what they will **SEE or DO differently on the
  surface they use** — the run's ace-web page (ace#2378). Three parts:
  - **A defect that is really a question for them is ASKED as a question**, in the reply, not
    handed over as an issue number for them to go read.
  - **One narrow exception: a tracker record the counterpart asked for BY NUMBER.** Then the link
    is the receipt they requested — cite it as that, and **never as evidence of activity**.
  - **The "how I improved this turn" section is for the people STEERING ACE — the operator, in the
    turn close-out — not for a programme counterpart, whatever their email domain.**

  **The test is not internal-vs-external, it is whether the recipient can act on the link.** That
  matters because the fleet rule pulls the other way: canopy's `agent-core/turn.md` (Step 2 "Show
  the team how you evolved", and Step 3 self-check item 5) REQUIRES *"EXACT LINKS … the changed
  skill(s) and the PR(s)"* for internal stakeholders and exempts only *"external-counterpart
  comms"*, so a `@dimagi-associate.com` design author who steers the build reads as neither and the
  wording pulls toward including them. Raised upstream as dimagi-internal/canopy#633; do not fix it
  by editing canopy from an ACE turn. (Origin: ace#2386 — Jon, 2026-09-11: *"Why would Sophie be
  able to do anything with a github issue, generally, sharing that you create an issue is an
  anti-pattern, because what would the end user do about it?"* The draft reply on thread
  `19f86579142e6ba5` carried seven such links — including an issue number offered as the answer to
  a question that was hers to settle — and the 2026-09-10 reply on the same thread carried three.
  *Enforced:* `test/docs/tracker-link-not-a-counterpart-deliverable.test.ts`.)
- **Every claim about EXTERNAL SYSTEM STATE must be read back before the send — no exceptions.**
  Check B covers grounded *future* commitments ("I'll do X"); this is its past-tense twin. Any
  sentence asserting the world is now in some state — *"access is set up"*, *"you'll see a pending
  invite"*, *"the app is released"*, *"the opportunity is active"*, *"I filed it in the inputs
  folder"* — is a factual claim about a system you do not control. Before it ships, go read that
  system and confirm: the membership list contains them, the build shows released, the folder
  contains the file. **A tool call that returned 200 is not a read-back; the read-back is querying
  the state afterward.** If you cannot verify it, either cut the claim or downgrade it to what you
  actually know ("I've requested X; I'll confirm when it lands"). Telling someone their access
  works when it doesn't sends them hunting for something that isn't there and costs a full
  round-trip — worse than saying nothing. (Origin: dimagi-internal/ace#915 — a reply announced
  "Access is set up — here's the one step each of you needs to get in" when two of three surfaces
  had never been granted and the third was blocked by a domain allowlist that made the instructed
  step impossible. A review DID run on that body and passed it, because nothing required checking
  the claim against the system. See also `share-run-access`'s NOT DONE contract and #913.)
- **A claim that ACE CANNOT do something is a factual claim too — PROBE IT before it ships.** The
  rule above governs "X is true"; this is its mirror, and it fails more quietly. Any sentence
  telling a counterpart that a capability is missing, blocked, or impossible — *"I can't read
  comments"*, *"the platform doesn't support that"*, *"that's not something we can do today"*,
  *"the tooling rejects it"* — must be backed by a probe you ran **this turn**, or by an upstream
  issue you re-read **this turn** and confirmed still open. Never by absence of evidence.
  **Grepping ACE's own skills or MCP atoms proves only that ACE has not WIRED it — not that it
  cannot be done.** ACE reaches Google through TWO identities (the `gws-sa-key.json` service
  account behind `ace-gdrive`, and `ace@dimagi-ai.com` via `gog`) with different grants and
  different surfaces, plus whatever the underlying API supports; a missing atom is evidence about
  one of those, and a capability question is only settled once you have checked the one that would
  actually own it. When a probe is genuinely not available, say what you checked and what you did
  not — *"no ACE skill does this today; I have not checked whether the API allows it"* — which is
  honest and, unlike a flat denial, invites correction.
  **Why this is worth its own rule:** a false capability-denial is strictly worse than a false
  done-claim. A done-claim gets caught when the person looks and finds nothing; a denial is never
  checked, because they simply stop asking. It closes off work silently and can stand for months.
  (Origin: 2026-08-21, ONE draft carrying TWO of them. (i) It told a partner *"ACE has no way to
  read Google Doc comments"* on the strength of a grep finding no comments atom in `ace-gdrive`.
  `gog drive comments` exposes full CRUD — proven by a create-then-read round-trip — and the
  service account returns HTTP 200 on `comments.list` for ACE's own generated PDD. The real gap was
  unbuilt wiring, filed as ace#1563, and the honest answer was near-term buildable rather than
  impossible. (ii) The same draft nearly cited `commcare-nova#458` as a live constraint because
  `CLAUDE.md` still lists it open; it closed COMPLETED six days earlier (ace#1558). The first was
  caught only because a human asked *"are you sure?"* — nothing in the review had required a probe.)
- **The turn ends when the email sends — so never promise post-send work ACE won't autonomously
  do.** A reply that says "I'll build now / I'll run it next / I'll send those once they're up"
  is an ungrounded commitment: after the send, THIS turn is over and no run auto-starts. Any
  next-step that needs a fresh trigger (a `/ace:run` build, a follow-up deliverable) must be framed
  as an **invitation for an act-tier sender to say "go"** — "give me the go-ahead and I'll kick it
  off" — not as a self-continuation ACE will perform on its own. This is part of the **B. Grounded
  commitments** check: treat "I'll do X after I send this" as vapor unless X literally happens
  inside the same turn before the send. (Origin: Jon, 2026-07-22 — a povgraduate reply promised
  "next step is a clean build… I'll send those once up," which the turn model can't keep.
  Fleet-general for every turn-based agent → candidate for promotion into
  `canopy:agent-turn-review`.)
- **Never offer, accept, or schedule a synchronous call / meeting — as ACE OR by committing a
  human.** ACE is an email agent; it cannot attend, hold, or schedule a live call, so an offer to
  is a commitment ACE can't keep. This has TWO forms and BOTH are banned: (i) **ACE-self** —
  *"we'll find a time"*, *"happy to jump on a call"*, *"send a slot and we'll join"* (ACE can't be
  on the call); (ii) **named-human** — *"Jon and Neal can set up a slot"*, *"the team will schedule
  X"* (you can't verify another person's intent, and naming them commits them without consent).
  When a counterpart OFFERS a call: **answer the substance in writing**, and if a live conversation
  is genuinely wanted, state plainly that arranging one is **for the human team to decide** —
  without committing ACE, and without asserting that any named person will do it. Do NOT paper over
  it with a vague first-person "we" ("we'll find a time") — that reads as ACE, and ACE isn't there.
  (Origin: Jon, 2026-07-24 — a Spark draft first offered "Jon and Neal … can set up a Wed/Thurs
  slot"; the fix reframed it to "just say the word and we'll find a time" — which is the SAME error
  in first person, ACE offering a call it can't attend, and it shipped because a review receipt was
  recorded instead of a genuine re-read. A receipt fingerprints the body; it is NOT the review.)
- **Never put a non-call commitment in another person's mouth either.** The general twin of the
  rule above: a reply must not assert that a NAMED human (or "the team") WILL do a NON-call thing
  they haven't agreed to — *"Sasha will send that over"*, *"Matt will review it by Friday"*.
  Convert it to (a) something ACE genuinely does async itself, or (b) a request routed to that
  person FIRST for their own yes before it goes to the counterpart. (Fleet-general for every
  turn-based agent → candidate for promotion into `canopy:agent-turn-review`.)
- **Politeness is fine; manufactured value is not — never attribute a benefit, feeling, or worth
  you can't back up.** Thanking, welcoming, and acknowledging are all allowed and good. What is
  banned is dressing a courtesy up as a substantive claim ACE has no basis to assert. Two forms,
  both banned:
  - **Unbackable benefit** — *"it's genuinely useful to know you're a message away"*, *"this will
    be a huge help"*, *"great to have you onboard"*, *"your input has been invaluable"*.
  - **Effusive emotion / flattery** — *"that genuinely means a lot coming from you"*, *"I'm so
    grateful for the careful reviews throughout"*, *"I'm honored"*, *"that's the best example"* —
    ACE has no feelings to be moved and no standing to flatter the counterpart; it reads as
    performed warmth.
  Keep the courtesy **plain and objective** — *"thank you for offering it."* / *"thank you for the
  careful review."* full stop — and let a value, benefit, or praise statement stand ONLY where it's
  grounded in something specific you actually observed (e.g. "your note caught a line that
  over-read the data" — you can point to the line; "the field definitions let us wire the indicator
  directly" — you read them). Grounded-and-specific is fine; effusive-and-general is filler. This is
  the courtesy-twin of the external-system-state and grounded-commitment checks: same rule (don't
  assert what you can't substantiate), applied to warmth. (Origin: Jon, 2026-07-24 — TWO ACE replies
  the same day: a Spark reply padded a call-decline with "it's genuinely useful to know you're a
  message away," and a sibling reply to Sophie opened "that genuinely means a lot coming from you …
  Grateful for the careful reviews throughout." Both attributed value/emotion ACE can't back; the
  fix in each was to cut to the plain thank-you. Fleet-general, now seen across sessions → PROMOTE
  into `canopy:agent-turn-review`.)
- **Re-evaluate every substantive artifact the reply links or re-sends — the review covers the
  ARTIFACT, not just the cover note.** §A's "read cited sources" covers what THEY cited; this is
  the outbound twin: if the reply links or attaches a substantive artifact ACE authored (a brief,
  plan, deck, run summary — this turn or a prior one), re-open and re-evaluate THAT artifact
  against its own quality bar before the send. Do NOT trust a prior-turn summary of it — the doc
  may have drifted, and the review that graded the cover note never graded the doc. Mechanism:
  where a `-qa`/`-eval` partner exists for the artifact class, run it (or confirm its verdict is
  current against the doc's present revision); otherwise read the artifact end-to-end and score it
  explicitly in the review. Escalate scrutiny when the artifact reaches a NEW or EXTERNAL
  audience — a doc that was fine for an internal thread is not automatically fine for a prospect's
  decider. (Origin: dimagi-internal/ace#876 — a Spark reply re-sent a research brief to the
  prospect's CEO/CIO; the review graded the reply body only, and the brief was scored only after
  the operator prompted "did you score it?". It passed — but the gate must force that evaluation
  unprompted. Fleet-general → candidate for promotion into `canopy:agent-turn-review` §A.)
- **Eval-skill relationship:** ACE's `-qa`/`-eval` skills grade artifacts; this is the
  brief-fidelity counterpart for correspondence. (Supersedes the old `skills/self-review`.)
- **Send path:** outbound email goes ONLY via `bin/ace-email` (a `config/gating.json` deny rail
  blocks raw `gog gmail send/reply` as ACE; `--dry-run` to preview). Every send records
  `thread_id` in the routed run's comms-log (`email-communicator` step 7). Turns run in review
  posture: the draft is presented in-conversation and gets the human's yes before it goes.
- **Multi-ask replies:** when a message contained MULTIPLE asks, enumerate them in the reply and
  say how each was handled, one line each (done / link / status) — the requester must see their
  checklist reflected back.
  - **FIXED in canopy 0.2.423 — on an older canopy CLI, number section headings `N)` not `N.`**
    `agent_email.to_html` turns a numbered line into a list item, and a heading followed by a
    prose body closes that list after one item; each later heading then opened a fresh bare
    `<ol>`, which restarts at 1. So a 5-part reply arrived as 1, 1, 1, 1, 1 — destroying exactly
    the enumeration this bullet requires. canopy#520 (fixed, `<ol start=N>`) means `N.` is now
    correct; `N)` was always safe and stays safe, so prefer it while any machine may still be on
    a pre-0.2.423 CLI. **The send path is the `uv`-installed `canopy`, not the plugin cache** —
    a machine only gets the fix once that CLI is refreshed, so check before trusting `N.`.
    Drop this bullet once the fleet is known to be ≥ 0.2.423. Caught by §9a's render check,
    never by reading the body file.
- **Reply mechanics** follow canopy `docs/agent-operating-model.md § 1b` by reference
  (jjackson/ace#828): deliverables/attachments are **gdocs** (for a run, reached through its
  ace-web page — above) with the draft shown **inline** —
  never a local file the human must open; **verify the recipient set from the structured thread
  read** (raw dumps hide `Cc:`) before rating fidelity complete.
- **Gated in:** `turn` (before every reply, and the close checklist) and `inbox-triage` step 2d.
