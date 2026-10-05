---
name: new-spec
description: Use this skill when the user wants to start a new feature with a spec, or wants to write a spec for something they're about to build. Triggers on "new spec", "write a spec for X", "let's spec this out", "start a feature for...". Spec-driven development; the spec drives implementation. Do NOT use for cross-cutting proposals (use `new-rfc`) or recording decisions (use `new-adr`).
---

# Skill: new-spec

Create a new feature spec under `docs/specs/<feature>/` with both `spec.md`
and `plan.md`.

## When to invoke

The spec is the contract; the plan is the strategy. Even a one-day feature
benefits from a one-paragraph spec — it forces the question "what does done
look like?" before any code.

## Procedure

1. Pick a kebab-case feature name from the user's description. Keep it short
   and noun-y: `user-onboarding`, `webhook-retries`, not
   `improve-the-onboarding-experience`.

2. Create the directory and copy this skill's bundled `assets/spec.md`
   and `assets/plan.md` into it as `docs/specs/<feature>/spec.md` and
   `docs/specs/<feature>/plan.md`. (Paths are skill-relative — the
   `assets/` folder lives next to this `SKILL.md` wherever your
   installer placed the skill.)

3. **Surface assumptions before writing any spec body — and run one
   targeted verification check per candidate first.** With the
   directory scaffolded, stop. The load-bearing rule: **one targeted
   check per candidate assumption — a repo read, a web lookup, or a
   read-only probe script — not a sweep.** Then split the result into
   what you confirmed and what still needs the user.

   Draft candidates covering the three categories below, generated
   from this repo's actual context — the template serves multiple
   project types, so don't carry assumptions across features:

   - **Technical** — runtime, data model, persistence, deployment
     target, transport. Canonical sources: package manifests
     (`pyproject.toml`, `package.json`, `Cargo.toml`, `go.mod`, etc.),
     build / orchestration configs (`docker-compose.yml`, CI
     workflows), and the module the feature touches.
   - **Product** — who this serves and where the feature ends. No
     canonical local source; goes straight to Unverified. Don't
     fabricate confirmation.
   - **Process** — review cadence, who signs off on **Boundaries**
     (especially the `Never do` subsection), how the spec moves Draft
     → Approved. Canonical sources: `docs/CHARTER.md`,
     `docs/CONVENTIONS.md`, the bundled `assets/spec.md` template for shape
     + `docs/product/engram.md` for what exists today, prior ADRs / RFCs that
     named the rule.

   See the **Source of truth** table in `AGENTS.md` for the full repo
   map. For assumptions about an external library, standard, service,
   or runtime behavior, the right source is a **web search** (cite
   the URL) or a **read-only probe script** (paste the command and
   its output) — e.g. `python -c "import x; print(x.__version__)"`,
   a `GET` on a list endpoint, `git --version`. **Probes must be
   side-effect-free** against any external service: no writes, no
   mutations, no calls that bill or page. If the only way to verify
   is to write, the assumption stays Unverified. **If web search
   isn't available in the harness**, mark the assumption Unverified
   with `(web search unavailable)` — never guess a URL.

   Emit the result **in chat** (not into `spec.md` — the body is
   gated below), under this shape:

   ```
   ASSUMPTIONS I'M MAKING:

   ## Verified
   - <category>: <fact> (<single-line citation: path | URL | command + one-line summary>)
   - …

   ## Unverified
   - <category>: <open item or reason it couldn't be settled>
   - …
   ```

   Each Verified bullet stays single-line. If a probe's output is too
   long to summarise in one line, paste the full transcript in a
   fenced block *above* the `ASSUMPTIONS I'M MAKING:` heading and
   reference it from the bullet (e.g. `(probe #1 above: returned True)`).

   Example Verified entries:
   `Technical: runtime is Python 3.12 (pyproject.toml)`,
   `Technical: HTTP client is undici 6.x (package.json)`,
   `Process: top-level convention changes need an RFC (docs/CONVENTIONS.md §Living-docs)`.

   Three to seven *candidate* assumptions before verification is the
   usual shape; Verified is whatever subset of those candidates passed
   the check — no floor, no separate cap. Coverage check is across
   the three categories (Technical / Product / Process), not the two
   subsections.

   **Surface the Unverified list and wait** for human confirmation or
   correction before writing into `Objective`, `Boundaries`,
   `Testing Strategy`, or `Acceptance Criteria`. If Unverified is
   empty, surface the Verified list with the highest-stakes item
   called out and ask the user to confirm *that one specifically* — a
   vague "looks good" doesn't count when the user may not have read
   the list.

   Only once Unverified has been signed off (or the highest-stakes
   Verified item confirmed, if Unverified was empty):

   - Copy the now-confirmed assumption list into the spec's
     `## Assumptions` section as a flat list — one bullet per item,
     each citing how it was settled. Verified entries keep their
     canonical source (path / URL / probe summary); previously-
     Unverified entries cite `user confirmation YYYY-MM-DD` with
     today's date. The chat block was the working surface; the spec
     section is the audit trail.
   - Write the spec's `Constrained by:` header from any Verified
     items that name an ADR or RFC the feature must cite. The header
     lands before any body section; Verified items don't gate the
     Unverified loop but they do gate `Constrained by:`.
   - Stamp the optional `Brief:` header **only** when this spec is
     derived from a product brief — i.e. you arrived here from
     `receive-brief`, which decomposes a received brief into specs. Set
     it to the brief's slug (`docs/product/briefs/<slug>.md`); leave it
     blank or `none` for a spec authored directly. It records *product
     provenance* and is distinct from `Constrained by:` (governance).
     A spec without it stays valid — the field is additive.

4. Fill in the spec — including the **Testing Strategy** section. Push
   back hard on these failure modes:
   - **Objective is vague.** "It should be fast" is not an objective.
     "Returns within 200ms at p99 for payloads under 1KB" is. Every
     user-visible outcome named in the Objective must be precise
     enough that a test could be derived from it.
   - **Testing Strategy left as the template's mode list.** The
     template shows three modes (TDD, goal-based, manual QA); naming
     them without pairing each user-visible outcome from the Objective
     with a mode and a one-sentence why isn't a strategy.
   - **Boundaries left empty.** The three subsections — `Always do`,
     `Ask first`, `Never do` — keep an implementing agent inside the
     lines. Make the user name at least one entry per subsection, and
     at least one *structural* entry under `Never do` (no new top-level
     dependency, no new module boundary) so the diff can't sprawl into
     hypothetical futures.
   - **No Acceptance Criteria.** Without a checklist, "done" is opinion.
   - **Body narrates history or the future.** Write the spec in the
     present tense, as if the feature already exists and always worked
     this way — the *retcon* discipline. No "will be implemented", no
     "previously X, now Y", no deprecation timelines, no version-stamped
     history in the body. Mixed tenses make an agent reading the spec
     guess wrong about what is current; a present-tense body reads as a
     clean description of the contract as it stands. Decision history
     lives in ADRs and the changelog, not the spec body — the plan
     (`plan.md`) is the one exception, since it carries its own changelog
     of how the approach evolved.

   While writing Testing Strategy, sanity-check that each TDD-mode AC is
   concrete enough to *stub* — see `work-loop`'s
   [`references/tdd-stubs.md`](../work-loop/references/tdd-stubs.md). This
   is a **self-check only**: do **not** commit stubs at spec-authoring time —
   the stack and `Contract:` may not be settled yet, so committed stubs are
   generated later, in `work-loop` PLAN. An AC you can't imagine typing a test
   against is the signal to sharpen it now.

4b. **Author the interface contract — only if this feature exposes an interface
   surface.** This conditional step sits between the spec body and the plan, and
   is **contract-type-agnostic** — it handles any interface, not just REST APIs.
   If the feature exposes **no** interface surface, skip it: the spec→plan path
   runs unchanged.

   - **Detect & confirm the type.** From the Objective's interface-facing
     Acceptance Criteria, auto-detect whether the feature exposes a contract
     surface and of **which type** — a synchronous REST API (`openapi`), an
     **event interface** (`asyncapi`), an RPC service (`proto`), a GraphQL schema
     (`graphql`), a standalone schema (`jsonschema`), … The type drives
     everything below. Confirm with the user — it's a judgment, not a flag.
   - **Locate or create** the contract at its type's conventional path
     `contracts/<type>/<domain>.<ext>` (CONVENTIONS § 4 *Contracts*;
     [`references/contract-types.md`](references/contract-types.md) maps every
     type to its location) — a new file for a new interface, the existing file
     when this spec modifies a known one. The **location convention is the
     anchor**: anyone finds contracts by globbing `contracts/<type>/`, no
     installed skill required, so *any* type (events included) lands in its
     canonical place.
   - **Author it.** Look up the type's authoring skill in
     [`references/contract-types.md`](references/contract-types.md) and check your
     available-skills roster (the same roster step 6 uses). **If a skill is
     present** (today: `api-contract` for `openapi`), invoke it to author/modify
     the contract against the active standard. **If absent** (today: every
     non-OpenAPI type, e.g. events), **edit the file directly and note** it was
     authored without rule-enforcement — a serviceable file for YAML-shaped types
     (AsyncAPI, JSON Schema), a **stub + note** for formats you can't reliably
     hand-author unaided (proto, GraphQL). A missing skill degrades *enforcement*,
     never the *integration*, and **never blocks** the spec.
   - **Link it (both ways).** Fill the spec's `- **Contract:**` header with the
     contract file(s) this spec defines or touches, and add the backward pointer
     in the contract (an `x-spec` extension, or a `contracts/REGISTRY.md` row for
     extensionless formats) — CONVENTIONS § 4 *Contracts*.
   - **Point the plan at it.** The plan's construction tests reference the
     contract as the artifact the implementation is verified against.

4c. **Derive the spec's `Shape:` and the implementation stack — this primes the
   plan's `## Design (LLD)`.** Between the spec body and the plan, settle two
   things so the design scaffolds at the right size and against the right stack:

   - **Shape.** Pick the spec's `Shape:` — `ui | service | data | integration |
     mixed` — from the feature itself: a screen or flow is `ui`, a backend
     endpoint or worker is `service`, a schema/model change is `data`, a wiring
     of external systems is `integration`, anything spanning several is `mixed`.
     If you arrived here from `receive-brief`, the brief's framing usually
     decides it; otherwise **ask the user**. The shape selects which
     `## Design (LLD)` sub-sections the plan scaffolds — a narrower shape keeps
     the plan thin. Stamp the resolved value on the spec's `Shape:` header.
   - **Stack.** Determine the stack the `## Design (LLD)` sub-sections will name:
     - **When `docs/architecture/reference.md` is present**, read it and
       **conform** the design to it — reference its named components,
       stereotypes, layers, and standards *by name* rather than inventing
       parallel ones. The reference architecture is the source of truth for the
       stack; the LLD is an instance of it.
     - **When it is absent**, **degrade** to detecting the established stack from
       the repo — lockfiles (`package.json`, `pyproject.toml`, `go.mod`,
       `Cargo.toml`, …), build / orchestration files, and the imports in the
       module the feature touches — plus any stack context a brief carried.
     - **Elicit, don't invent.** When detection is ambiguous or the repo is
       greenfield, **ask** which stack to target. Never guess a framework into
       the design — an invented stack is worse than one asked question.

   The headings in `## Design (LLD)` stay universal; the prose under them is the
   stack-specific instance you resolved here.

5. Fill in the plan second. The plan should:
   - Cite any ADRs or RFCs it follows from.
   - Break the work into tasks small enough to be a single PR each.
   - Carry **construction tests** per task — `Tests:` before `Approach:`
     in each task, designed up front. "We'll test it" is not a strategy.

   Push back hard on these plan-stage failure modes (mirror of step 4):
   - **Task too big.** "Implement the feature" is not a task; "add the
     validation function for X" is. Each task should fit a single PR
     and a single context window. Split coarse tasks until they do.
   - **`Depends on:` omitted.** Every task must state `Depends on:`
     explicitly — prior task IDs or `none`. Don't let authors lean on
     task order to imply dependency; that hides serial-by-default
     thinking and makes the plan unparseable.
   - **Verification mode unstated.** Every task must declare its mode —
     TDD, goal-based check, or visual / manual QA. Silent defaults
     produce mock-shape tests on config-shape tasks and untested
     invariants on logic-shape tasks.
   - **Tasks without spec mapping.** Each task should reference which
     behavior from the spec's Objective it implements, and the Testing
     Strategy mode for that behavior. Orphan tasks are scope creep in
     disguise; behaviors with no implementing task are gaps.
   - **Specificity miss.** Task descriptions should reference exact
     file paths and function or symbol names where they're known.
     "Update the parser" is too coarse to verify; "add a null-check
     in `parser/lex.ts:Lexer.next`" is the right level.

6. Spec-mode adversarial review. Before announcing the spec in the README,
   select a subagent matching `adversarial-reviewer` and ask it to review
   the freshly drafted `spec.md` + `plan.md` in spec mode — the role
   supports this explicitly. Iterate on findings until the reviewer returns
   `Clean — ready to commit.` Spec-mode reviews should converge in 1-2
   passes; if you can't reach clean in 3, the spec has a structural problem
   — surface to a human rather than grinding. Absence of any subagent
   matching this role is a note in the final summary
   (`adversarial-reviewer: no matching subagent installed; review skipped`),
   not a blocker.

7. Update `docs/specs/README.md` to add the feature to the active list.

8. **Keep the spec the single source of truth — drift is a bug.** When
   implementation diverges from the spec, the spec is wrong: update it in
   the same PR. The failure mode this discipline prevents has a name —
   **context poisoning**: an agent loads a stale, duplicated, or
   self-contradicting doc and makes a confident, wrong decision from it,
   because nothing in the document tells it which part is current. Two
   habits are the defense, one for each way a doc poisons: **one canonical
   home per fact** (the *Source of truth* map in `AGENTS.md`) stops a fact
   from living in two places that can drift apart, and the **present-tense
   retcon body** (the failure mode in step 4) stops a single document from
   contradicting itself across tenses. Remind the user of both.

## Anti-patterns to refuse

- Drafting a spec for something already half-built without checking against
  the existing code → ask the user to either align the spec with current
  behavior (and note any divergences) or write a new spec for what should
  change.
- Writing a spec that reads like a design doc (full of implementation) → the
  spec is the contract, not the design. Move implementation detail to
  `plan.md`.
- Skipping Boundaries → mandatory section. Each of the three
  subsections needs at least one entry.
- Writing into the spec body before the Unverified list has been
  confirmed → the headers can stay scaffolded; the bodies are the
  commitment and stay empty until the user has signed off on or
  revised the Unverified entries, even if the original prompt sounded
  definitive.
- Classifying a Technical or Process assumption as Unverified
  without recording the one check you attempted (path read, URL
  fetched, or read-only probe command + output) → attempt and cite
  the check. An attempted check that came back ambiguous is fine; a
  skipped check is not. The user's time is the scarce resource;
  burning a round-trip on a fact a single command would have answered
  is a tax on every spec.
- Fabricating a URL when web search isn't available → mark the
  assumption Unverified with `(web search unavailable)` and let the
  user supply the source. Plausible-looking citations the agent
  didn't actually fetch are worse than honest Unverified items.
