---
name: new-rfc
description: Use this skill when the user asks to propose, draft, or open an RFC (request for comments). Triggers on "RFC", "propose a change to...", "let's get input on...", "draft a proposal". Do NOT use for already-decided things (use `new-adr`) or single-feature specs (use `new-spec`).
---

# Skill: new-rfc

Open a new RFC in `docs/rfc/` from the template — **answer-first** (lead with
"The ask"), with a per-subpoint research-and-de-risk phase before drafting and
a mandatory self-review gate before handoff. The point: a reviewer gets a
steerable proposal with the decision on top and its options modelled out and
backed by research — not a pile of un-researched questions to rescue. Modeled
on `new-spec`'s assumption checkpoint, plus the per-decision recommendation
pass RFCs need and specs don't.

## When to invoke

Before invoking, confirm one of:

- The change touches multiple packages or affects external users.
- The change reverses a previous ADR.
- The change adds, removes, or modifies a top-level convention.
- The user explicitly wants discussion before implementation.

If the change fits inside a single package and breaks no public interface,
push back: a normal PR (or a spec, if it's a feature) is enough.

## Procedure

1. Find the next number. The bundled helper prints the next 4-digit
   ordinal — `0001` if no RFCs exist yet, max-plus-one otherwise. It
   parses the full digit prefix, so a `00099-foo.md` correctly yields
   `0100` (not `0010`):

   ```bash
   python3 scripts/next-ordinal.py docs/rfc
   ```

   (The script lives next to this `SKILL.md` under `scripts/`. Python
   is preferred over `ls | grep | sed | sort` so the snippet works the
   same way on native Windows, macOS, and Linux.)

2. Copy this skill's bundled `assets/rfc.md` into `docs/rfc/` and rename
   to `NNNN-<kebab-title>.md`. **Keep the title short** — it should
   *identify* the proposal in a few words (`RFC-NNNN: Coordinator
   contract`), and the kebab filename follows it; the fuller explanation
   belongs in **The ask**, not the title. A title that carries the whole
   abstract makes the RFC index hard to scan. (Paths are skill-relative — the
   `assets/` folder lives next to this `SKILL.md` wherever your IDE
   installed the skill.) **Optional `NNNN-notes/` companion.** If the
   proposal rests on a sustained investigation, you may create a sibling
   `docs/rfc/NNNN-notes/` folder for the promoted research — a distilled
   brief, evidence, sketches — mirroring the `notes/` folder a spec carries
   (docs/CONVENTIONS.md § 3). It is optional; summarize its conclusions in
   `Evidence & prior art` and link the folder, rather than pasting the corpus
   into the RFC body.

3. **Guided shape/intake — offer, don't force.** Before researching, get the
   proposal's frame straight. Read the request:

   - **When the ask is already well-specified** (a clear change, a named
     surface, an evident motivation), *infer* the frame and proceed straight to
     research — don't make the author fill in a questionnaire they've already
     answered.
   - **When the intent is vague** (a direction, a complaint, "we should
     probably…"), ask a *small* set of framing questions — what outcome do you
     want · what's in and out of scope · what's the bet/risk — then synthesize a
     short proposal frame and reflect it back for confirmation before you spend
     research effort on the wrong target.

   Either way, **pick the `Decision weight`** (light | standard | heavy) for the
   RFC's header by reading `work-loop`'s risk triggers as a prose heuristic —
   reverses a frozen ADR/RFC, or a governance/charter/security boundary, or a
   one-way door → `heavy`; a reversible, narrow change → `light`; otherwise
   `standard` (the default). The weight right-sizes how much research depth (next
   step) and pre-handoff ceremony (the gate) the RFC carries — it never licenses
   dropping a gate check. Offer the frame; don't block on a form — a half-formed
   ask is normal input.

4. **Research + de-risk checkpoint — gated.** With the file scaffolded, stop.
   Don't write a single body sentence yet. A complex RFC is a tree, not one
   blob: research the *subpoints*, model the options out, and de-risk your own
   riskiest assumption before handing anything to a reviewer. A single shallow
   up-front sweep is the failure this replaces. **Scale the depth to the
   `Decision weight`:** a `light` RFC may need one focused sweep; `standard` and
   `heavy` get the full per-subpoint treatment below.

   Work the proposal as decisions/subpoints, emitting findings *in chat* (not
   into the gated body):

   - **Decompose first.** Break the proposal into its decisions/subpoints. The
     research unit is the subpoint, not the whole RFC.
   - **Research each subpoint independently:**
     - *Repo sweep.* Grep `docs/CHARTER.md`, `docs/CONVENTIONS.md`,
       `docs/adr/`, `docs/rfc/`, `docs/specs/`, and `docs/architecture/` for
       precedent and conflicts the subpoint touches. Cite each hit with file
       path.
     - *External sweep.* If web search is available (`WebSearch` in Claude
       Code; the equivalent elsewhere), look up how comparable projects,
       languages, or processes handled this shape of problem (Rust RFCs, PEPs,
       IETF BCPs, internal RFCs from similar orgs). Cite each as a markdown
       link. If web search isn't available, say so explicitly rather than
       fabricating citations.
   - **Enumerate each option/scenario space to be collectively exhaustive
     (MECE) along a stated axis**, and **ground every option in prior art**
     (how have others taxonomised this?) rather than inventing categories. A
     small round count (e.g. exactly 3) with no exhaustiveness argument or
     sources is a smell to challenge, not a finish line. Always include
     do-nothing.
   - **Self-Ask.** Resolve research-answerable questions yourself and fold the
     answers into the findings — they should not reach the human as open
     questions.
   - **Spike the riskiest assumption.** Identify the one assumption that, if
     false, sinks the proposal; run a small/timeboxed check and report the
     result — or state explicitly why no spike is needed. Do your own
     experimentation; don't hand the reviewer an untested guess.
   - **Cite as you go.** When a sweep (or a research subagent) surfaces a
     source, fetch it and confirm it resolves *and* contains the borrowed
     claim before that claim enters the findings. Never pass an unverified
     citation through.
   - **Recommend per decision.** For each decision/subpoint: the question,
     what repo precedent suggests, what external prior art suggests, and a
     recommended answer with one-sentence reasoning + owner + decide-by. Cap
     genuinely-open questions at ~3.

   Emit the findings under exactly these headings:

   ```
   RESEARCH FINDINGS:

   ## Decisions / subpoints
   1. **<subpoint>** — options (MECE along <axis>, prior-art-grounded): …
      · recommendation: … · owner: … · decide-by: …

   ## Prior art (in repo)
   - …

   ## Prior art (external)
   - …

   ## De-risk
   - Riskiest assumption: … · spike result (or why none needed): …
   ```

   Then **wait for human confirmation, rejection, or revision per
   recommendation.** Do not write into *any* body section until the user has
   signed off. Accepted recommendations fold into the body; ones rejected
   without an alternative, or genuinely deferred, stay in `Open questions` —
   with a recommended default + owner + decide-by, never bare.

5. **Draft the body, answer-first.** Set the header fields, including the
   `Decision weight` you picked in step 3. Open with the **Reviewer brief**, then
   **The ask**; then route the findings: repo precedent → `Problem & goals` /
   `Evidence & prior art`; external precedent and the spike result →
   `Evidence & prior art`.

   **Reviewer brief — first-screen orientation, de-duplicated against The ask.**
   Fill the top-of-doc `## Reviewer brief` grid (Decision · Recommended outcome ·
   Change if accepted · Affected surface · Stakes · Review focus · Not in scope).
   It *orients* the reviewer's read; "The ask" *argues* the decision. Don't
   restate the BLUF in it — the two are different jobs. (This in-body brief is a
   distinct artifact from the chat-only `REVIEW READINESS` summary in step 6.)

   **Decisions as a table.** In "The ask", render *Decisions requested* as a
   table — one row per decision — `| ID | Question | Recommendation | Why |
   Decide by | Reviewer action |` — not numbered prose; the `Reviewer action`
   column names what the reviewer must do per decision (confirm X, rule on Y).

   **Body-as-argument split rule.** The RFC body is the *argument* a reviewer
   decides from — not an audit trail of your work. Keep a section in the body
   when it changes the reviewer's decision; when a section mainly demonstrates
   the work was done — full research transcripts, prior-art matrices,
   adversarial-review logs — summarize its conclusion in the body and move the
   detail to the optional `NNNN-notes/` companion (step 2). Default the body to
   the argument and link the proof.

   Sections to push hardest on:
   - **Reviewer brief.** The fixed first-screen orientation grid, above The ask,
     de-duplicated against it (orients, doesn't argue).
   - **The ask.** The decision a reviewer must make, in plain language, on
     top — Recommendation (BLUF) + SCQA framing + the decisions table (one row
     per decision, each with a recommended option + decide-by + reviewer action).
   - **Problem & goals.** Diagnosis before solution; real **Non-goals**
     (could-have-been-goals deliberately dropped), not negated goals.
   - **Options considered.** MECE along a stated axis, each grounded in prior
     art, including do-nothing. If you can't articulate ≥2 genuinely distinct
     options, the proposal isn't honest yet.
   - **Risks & what would make this wrong.** Pre-mortem + falsifiable
     assumptions + drawbacks. If they say "no drawbacks", push back.
   - **Evidence & prior art.** Empty prior art is a finding (no one has done
     this) — surface it; never leave it blank or fabricated. Promoted research
     from a sustained investigation (e.g. a `research`-pack project brief) can
     live in the optional `NNNN-notes/` companion; summarize and link it here.
   - **Open questions.** Each carries a recommended default + owner +
     decide-by; aim for ≤3.
   - **Experiment / validation** (optional). Only if the proposal needs an
     experiment: hypothesis + what you measure + success/failure criteria.
     Route *results* to a linked spike note, not the RFC body; once the RFC
     is circulating and the trial is actually running, it moves to
     `Experimental` while results are pending (a post-circulation state — see
     `docs/CONVENTIONS.md` § RFC lifecycle). Delete the section otherwise.

6. **Pre-handoff gate — mandatory, before status → Open.** Each item is
   *executed and its result recorded, never self-certified*. The `Decision
   weight` right-sizes how much *research and draft* each tier carries, **never
   whether a mandated check below runs**: a `light` RFC runs the full gate over a
   smaller draft (every check still fires — citations still fetched-and-confirmed,
   the `adversarial-reviewer` dispatch still mandatory and re-run until clean);
   `standard` is the full gate as written; `heavy` adds a mandatory de-risk spike
   and explicit Approver sign-off (no silent-default adoption). No tier drops or
   softens a check.
   - **Citation-integrity protocol.** Every reference is fetched; it must both
     resolve and actually contain the claim or statistic it is cited for (a
     link that merely loads is not enough). Citations surfaced by a research
     subagent get the same treatment. If a claim can't be confirmed, downgrade
     or drop it. The rule is symmetric: *challenge* a citation by fetching it
     too — never by judging whether an identifier "looks real".
   - **Verify-before-you-assert.** Every checkable claim the RFC makes about
     *itself* (section/field counts, "lighter", "readable") is checked against
     the artifact, not asserted.
   - **Per-subpoint backing.** Each decision/subpoint is independently backed
     by research; each enumeration is MECE along a stated axis and prior-art-
     grounded, not invented.
   - **Completeness checklist (YES/NO).** Approver named? every decision
     carries a recommendation? do-nothing present? ≤3 owned open questions? no
     item is simultaneously a decided default *and* an open question? all
     internal cross-references resolve?
   - **Different-lens review.** Dispatch a subagent matching
     `adversarial-reviewer` (fresh context) — **mandatory**, re-run until it
     reports clean; add `security-reviewer` if the RFC touches a security
     boundary. If no such subagent is installed, note it in the summary
     rather than skipping silently.

   **Hand back a reviewer-friendly readiness summary, not a compliance dump.**
   The checks above are run to build the *reviewer's* confidence, so report
   their result as a short summary the reviewer can act on — and **link** the
   heavy proof (citation-fetch detail, the adversarial-review transcript)
   rather than pasting it into the RFC body or the handoff. Emit this **to chat
   at handoff** — it is a handoff artifact, **never an RFC body or template
   section**:

   ```
   REVIEW READINESS:
   - Decision clear: yes/no
   - Options include do-nothing: yes/no
   - Riskiest assumption tested: yes/no (+ link)
   - Citations checked: yes/no
   - Open questions owned: yes/no
   - Adversarial pass: clean | issues linked
   ```

7. Set status to `Draft` until the user is ready to circulate, then `Open`.

8. Update `docs/rfc/README.md` table (create the file with the standard
   header row if absent).

## After acceptance

When the RFC is accepted, the *follow-on artifacts* section should list
concrete next steps — usually:

- One or more ADRs to record the architectural decisions.
- One or more specs in `docs/specs/` for features.
- Edits to `docs/CONVENTIONS.md` if the RFC changes conventions.

The RFC itself is then "done" and stays as historical record.

## Recording corrections (Errata / Amendments)

An RFC's body freezes, but the proposal can still need a correction after it
publishes — a spec finds a gap, a later RFC reframes a decision. Record the
correction *inside the RFC*, in one of two sections chosen by the RFC's
lifecycle class (the Document-lifecycle table in
`docs/CONVENTIONS.md` § Document lifecycle — Frozen vs. Governance), **never**
by editing the frozen body:

- **`## Errata`** — for a **Frozen** RFC (Accepted or Rejected). The body is
  immutable; corrections are appended here, Approver-signed. This is the common
  case — most corrections are found after acceptance.
- **`## Amendments`** — for an **in-flight** RFC (Open / Governance class) that
  needs to track reconciliations *while still being worked*, without rewriting
  its body. The rare case.

The heading itself signals whether the text beneath it is immutable, so the two
never coexist in one RFC: an Open RFC carrying `## Amendments` renames the
section to `## Errata` if and when it is Accepted (a status-driven edit the
Frozen rule already permits).

### The two-layer structure — optional, threshold-gated

A single one-line erratum stays a plain dated bullet. Split the section into two
layers **only once it crosses the threshold — more than one entry, *or* any
entry supersedes another** — at which point a reader can no longer recover the
present rules without diffing the whole log by hand:

```
## Errata            (or ## Amendments)

### Current state
<an authoritative summary — usually a table — of the corrections in force:
 "read this, not the log", for the present contract>

### History / audit trail
<dated entries explaining how each correction was reached>
```

- The **current-state** layer is the authoritative present contract. **Where it
  disagrees with a historical entry, the current-state layer wins** — say so in
  the section so a reader knows which layer to trust.
- The layer *names* above are illustrative; the contract is the two-layer split
  (authoritative current state over a dated audit trail), not the exact heading
  wording. RFC-0048 / PR #430 is the worked precedent this generalizes — it uses
  "Current reconciliation state" over an "Amendment history / audit trail."

### Append-only and supersession

- Correction sections are **append-only**. A later entry supersedes an earlier
  one simply by being later; the **newest entry plus the current-state layer**
  carry present truth. Earlier entries are never deleted — they *are* the audit
  trail.
- **No per-entry ritual is required.** On a Frozen RFC's `## Errata`, prior
  entries cannot be reworded anyway (immutable body). On an in-flight
  `## Amendments`, an author *may* optionally reword a stale entry in place,
  tagging it `*(Superseded: …)*` — permitted, not required, and **only for
  in-flight Amendments** (a Frozen RFC's entries can't be touched).
- **Whole-RFC replacement is out of scope.** When an entire RFC — not one
  correction within it — is superseded by a later one, record that as an
  **Errata entry naming the superseding RFC** (e.g. RFC-0012 carries an erratum
  recording that its Alternative #7 was superseded by RFC-0052). This convention
  governs corrections *within* an RFC; it neither defines nor changes the
  whole-RFC-supersession mechanism.

## Anti-patterns to refuse

- Writing into the RFC body before the checkpoint clears → see step 4.
- A single shallow up-front sweep standing in for per-subpoint research on a
  multi-decision RFC → decompose and back each subpoint.
- Enumerating an option/scenario space by inventing a small round number of
  categories (e.g. exactly 3) with no exhaustiveness argument or prior-art
  grounding → make it MECE along a stated axis, and source it.
- Bare open questions with no recommended default + owner → if the question
  hasn't been searched against repo + external prior art, the research phase
  wasn't done. Send it back.
- Passing any citation — especially one surfaced by a subagent — into the
  draft without fetching the source and confirming the borrowed claim is in
  it (a link that resolves is not enough; this is the single most-documented
  LLM-drafting failure). Challenge a citation the same way — by fetching —
  never by judging whether an identifier "looks real".
- Asserting any self-claim or a "gate passed" status without having run the
  check.
- Empty `Evidence & prior art` while web search was available and comparable
  processes plainly exist → "we didn't look" isn't an answer. When web search
  *wasn't* available, say so explicitly under the heading and never fabricate
  citations to fill it.
- Padding the RFC body with proof-of-work — full research transcripts,
  prior-art matrices, adversarial-review logs — that belongs in the optional
  `NNNN-notes/` companion → the body is the argument; summarize the conclusion
  and link the detail.
- A title that carries the whole abstract → shorten it to *identify* the
  proposal; the explanation lives in **The ask**, and a scannable RFC index
  depends on it.
