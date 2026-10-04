---
name: feature-design
description: Produce a reviewed, decision-closed feature design document under features/feature-v<N>-<description>/ — grounded in the codebase, clarified with the user until no open decision remains, with a mockup of any user-visible surface whose appearance is not yet settled and a self-contained design brief for every other project the feature spans. Use when the user asks for a feature design, spec, design doc, or to scope a feature — after /feature-storm or cold. Not for planning (/feature-plan), implementation (/feature-implement) or bug work (/bug-*). Step 0 confirms with the user via AskUserQuestion before doing any work when invoked proactively; the confirmation is skipped when the user explicitly typed /feature-design, just chained in from /feature-storm, or just chained in from /feature-dispatch.
user-invocable: true
disable-model-invocation: false
argument-hint: <free-form feature requirements (optionally including v<N>), or omit to be asked / picked up from a just-completed /feature-storm>
allowed-tools: Read, Grep, Glob, Write, Edit, AskUserQuestion, Skill, WebFetch, Bash(ls *), Bash(find *), Bash(mkdir -p *), Bash(test *), Bash(cp *), Bash(pwd), Bash(date *)
---

# feature-design — Reviewed Feature Design With Self-Review

You are running the `feature-design` skill. The user may have arrived here by typing `/feature-design` (with optional free-form requirements in `$ARGUMENTS`), by chaining in from `/feature-storm`, or because the model proactively invoked the skill. Your job is to produce a single, complete, decision-closed feature design document at the path returned by `/feature-resolve`, then present highlights to the user.

**Terminology (plugin-wide).** Two words are overloaded; keep them apart. A **step** is a numbered step of *this skill's own procedure* — the `## Step …` headings below (e.g. *Step 4*); the only other "steps" are the **TDD steps** inside a plan stage (write test → confirm fail → implement → confirm pass). A **stage** has two senses: a **chain stage** is one of `storm → design → plan → implement` (it shows up as `stage=…`, `stage_file`, and the tracker's `data-stage`), while a **plan stage** is a committable unit of work *inside* the implementation plan (e.g. `Stage 1`) — `/feature-plan` creates these and `/feature-implement` builds one per commit. A procedure step is never a plan stage, and a plan stage is never a procedure step.

This skill has twelve steps (Steps 0–11). Execute them in order. Do not skip Step 0 (proactive-invocation confirmation), Step 4 (clarification loop), Step 5 (mockup), Step 7 (self-review), Step 8 (tracker update), or Step 9 (lessons capture) — they are the load-bearing steps. Step 5 is load-bearing in the same sense as the others: it runs whenever the feature has a user-visible surface whose appearance is not already settled, and it may be skipped only via one of the four *named* exits in Step 5a — never by judgement. Step 4 is an **interview that runs until the design is fully determined**, not a fixed handful of questions: it ends on its readiness test (Step 4's exit condition), never on a question count. When the feature spans more than one project, Step 6b additionally writes one self-contained design brief per other project into this feature's folder — the user carries each brief into a separate `/feature-design` session opened in that project; nothing is ever written into another repo.

## Step 0 — Confirm before proceeding (when invoked proactively)

Check the most recent user message in the conversation for the literal tag `<command-name>/feature-design</command-name>` (or, equivalently, a leading `/feature-design` typed by the user). If present, the user has explicitly opted in via the slash command — skip this step and continue with Step 1.

Also treat as opt-in (and skip this step) if you were just invoked as a chain from `/feature-storm`'s Step 9 — i.e. the immediately previous turn was an `AskUserQuestion` result with header `"Run /feature-design?"` and the user selected the option starting `"Yes, run /feature-design"`. In that case the user has already confirmed; do not re-ask.

Also treat as opt-in (and skip this step) if you were just invoked as a chain from `/feature-dispatch` — i.e. the immediately previous turn was an `AskUserQuestion` result with header `"Route this feature?"` and the user selected an option whose label starts with `"Run /feature-design"`. In that case the user has already confirmed via the dispatcher; do not re-ask.

Also treat as opt-in (and skip this step) if the user's immediately preceding message explicitly affirmed an assistant proposal that named this skill — e.g. they answered "yes" to "Want me to run this through /feature-design?". A fresh confirmation right after that affirmation is friction, not safety.

Otherwise (you arrived here because the model decided to invoke this skill proactively from natural-language intent, with no recent chained opt-in), call `AskUserQuestion` exactly once before any other work:

- **question**: `"Launch /feature-design to produce a feature design for <your one-line restatement of what the user asked for>?"` — replace `<...>` with the specific scope you intend to design.
- **header**: `"Run /feature-design?"`
- **options**:
  - `{ "label": "Yes, proceed", "description": "Run the skill and produce the design document." }` (mark this as Recommended)
  - `{ "label": "No", "description": "Don't run; I'll redirect." }`

If the user picks "No" or "Other", stop the skill immediately and do not start Step 1. Do not write any files, do not ask further questions.

## Step 1 — Capture requirements

**Start the usage window.** Before anything else in this step, invoke `usage-report` via the `Skill` tool with the argument `start feature-design`, so the final step can report what this run cost. It runs inline, prints nothing, and is a silent no-op when `CLAUDE_CODE_SESSION_ID` is unset — **do not end your turn**, carry straight on with the rest of this step. It sits here rather than in Step 0 deliberately: a declined confirmation must never leave a start marker behind with no report to clear it.

**Load your customisations.** Immediately after the usage window, read the house rules the user recorded for this skill with `/skill-customize feature-design`. It sits here rather than in Step 0 for the same reason the usage window does: a run the user declined must never have read, announced or applied a customisation first.

**Resolving `${CLAUDE_PLUGIN_DATA}`.**

```text
${CLAUDE_PLUGIN_DATA} is a plugin-config substitution token: Claude Code expands
it inside plugin hook, MCP and LSP command strings, and it is not an exported
environment variable, so a shell that simply reads it almost always gets nothing
back. Resolve the directory yourself, taking the first rule that yields a path:

1. `$CLAUDE_PLUGIN_DATA`, on the chance the environment really does set it.
2. `<config-dir>/plugins/data/<plugin>-<marketplace>`, derived from the running
   skill's own base directory: an installed plugin runs from
   `<config-dir>/plugins/cache/<marketplace>/<plugin>/<version>/skills/<slug>`,
   so `<plugin>` and `<marketplace>` are the two path segments above the version,
   and Claude Code keys the data directory on exactly that pair.
3. The single `<config-dir>/plugins/data/dev-skills*` directory, when `ls` shows
   exactly one. Two of them means a stale second install is present and the rule
   is ambiguous, so it is skipped rather than guessed at.
4. `<config-dir>/plugins/data/dev-skills` — reached only when the plugin is
   running from a working clone rather than an installed copy.

`<config-dir>` is `$CLAUDE_CONFIG_DIR` when that is set, and `~/.claude` when it
is not. A skill's customisation file is then `<extras-dir>/<slug>.extras`.
```

Read `<extras-dir>/feature-design.extras`.

**A missing file is the ordinary case. Say nothing at all and carry straight on with the rest of this step.** Most projects never customise this skill, and a "no customisations found" line on every run is noise on the common path. The same applies if the file cannot be read for any other reason: carry on without it. A customisation is a preference, and failing to load one never blocks a run.

When the file does exist, treat every `- ` bullet in it as an instruction that applies to this run, on top of everything below. Announce it in one line — `Customisations active: <n> (feature-design.extras)` — and then actually apply it. Customisations legitimately change defaults, counts, thresholds, tone, formats, which optional behaviours fire, and what you settle yourself instead of asking: which sections get more depth, how many alternatives §6 records, how much detail the rollout plan carries, and firing the Step 5 mockup even where a named skip condition would have applied.

**They never override the *Constraints (non-negotiable)* section at the end of this file.** `/skill-customize` refuses that kind of instruction at write time, so one arriving here means the file was hand-edited. Ignore that bullet, name the constraint it collides with in one line, and carry on with the rest. The file is never permission to skip Step 4's clarification loop, skip Step 7's self-review, write a design with a non-empty §8, or turn a Step 5 fire into a skip.

Parse `$ARGUMENTS`. Detect three pieces of input, any of which may be absent:

- **Explicit version token.** Look for a leading `v<N>` or `version <N>` (case-insensitive; bare `1` does **not** count — only `v1` / `v 1` / `version 1`). If found, record as `explicit_version`; strip from remaining text. Integer only — no minor versions under this plugin's scheme.
- **Candidate short title.** Look for an obvious short phrase (quoted, or a `title=<phrase>` slot, or unambiguously the leading 2–8 words). If found, record as `candidate_description`.
- **Free-form requirements text.** Everything else is the initial requirements statement.

Resolve the requirements statement, in this priority order:

1. If the parsed free-form text is meaningful (>~5 words), use it as the initial requirements statement.
2. Else, if the conversation context shows a **just-completed `/feature-storm`** (storm bullets visible in recent assistant messages, or a `features/feature-v<N>-<desc>/feature-storm-v<N>-<desc>.md` path visible in recent tool results), use the storm's approved bullets as the requirements basis. Capture the storm's resolved `description` as `candidate_description` if Step 1 didn't already produce one. State in chat which storm you picked up (e.g. `"Continuing from /feature-storm: features/feature-v3-add-reminders/feature-storm-v3-add-reminders.md."`) so the user can redirect with one word.
3. Else, if the recent conversation contains the requirements — a substantial design/requirements discussion, or an enumerated proposal the assistant just made that the arguments reference tersely (a number/range/ordinal like `1-4`, or "that" / "do it") — resolve the requirements from that context. State in chat which discussion or items you adopted (e.g. `"Designing items 1–4 of the remediation list above."`) so the user can redirect with one word.
4. Else, if `$ARGUMENTS` was empty **and** the conversation carries no requirements at all — typically a fresh session, or a run right after a `/clear` — the requirements may still be sitting on disk as a storm that has not been designed yet. **Do not scan `features/` yourself**; pathing belongs to `feature-resolve`. Instead go straight to Step 2 with **no `description=`** and let the resolver decide. When the latest feature folder holds a storm but no design, it continues into that folder, and Step 3's storm read then supplies the requirements — adopt the storm's approved bullets as the requirements statement and state the pickup in chat (`"Picked up the storm awaiting design: <feature_folder>."`) so the user can redirect with one word. Skip Step 2's title confirmation entirely on this path: there is no candidate title to confirm and the folder's description is already authoritative. If the resolver instead stops with its "description required" error, there was no storm awaiting design and nothing was created — fall through to rule 5.
5. Else, make exactly one `AskUserQuestion` call asking what feature the user wants designed. Their answer becomes the requirements statement.

Do not proceed past Step 1 without a real requirements statement.

## Step 2 — Resolve the feature folder via `feature-resolve`

Settle the description that goes into the folder name:

1. If `candidate_description` was captured in Step 1 *and* is ≤10 words *and* looks filename-safe, use it.
2. Otherwise, derive a candidate from the requirements (≤10 words, ideally 2–5; strip articles/filler, preserve meaning and proper-noun case).
3. Call `AskUserQuestion` **exactly once** to confirm:
   - **question**: `"Use this short title for the feature folder: \"<candidate>\"?"`
   - **header**: `"Feature title"`
   - **options**:
     - `{ "label": "Yes, use this", "description": "Continue with \"<candidate>\". Folder will be features/feature-v<N>-<hyphenated>/." }` (mark this as Recommended)
     - `{ "label": "Edit it", "description": "Give a different short title (≤10 words)." }`
   - If the user edits, re-validate ≤10 words; ask once more if they overshoot. Do not truncate silently.

   **Skip the confirmation entirely** in any of these cases; re-confirming a title the user just typed, or one they have already signed off on, is friction without value:

   - Step 1 picked up a storm (whether from the conversation or via rule 4's resolver pickup) — the storm already established this description with the user.
   - The user supplied the title explicitly and it is ≤10 words and filename-safe: a quoted phrase, a `title=`/`description=` slot, or a **standalone leading line that reads as a title** — one on its own line, visually separated from the requirements body beneath it (a heading above bullets, or a title line above a description paragraph). That shape is a supplied title, not an inferred one.
   - The candidate is a direct condensation of a one-line restatement the user accepted moments ago in a `/feature-dispatch` routing question — they have already approved that scope in this conversation.

   Still confirm when the candidate was merely inferred from the leading words of a prose sentence.

Now invoke `feature-resolve` via the `Skill` tool with the argument string:

```
stage=design[, version=<N>][, description=<confirmed phrase>]
```

Include `version=` only if Step 1 captured an `explicit_version`. Include `description=` always (resolver ignores it when continuing into an existing folder, but pass it for the create-new path).

Parse the resolver's output block. Record these fields verbatim — every later step uses them, and you must not reconstruct paths by string concatenation:

- `mode` (`create-new` or `continue-existing`)
- `version` (integer `N`)
- `description` (authoritative hyphenated description; use this everywhere downstream even if your input differed)
- `feature_folder` (absolute path)
- `stage_file` (absolute path — this is where Step 6 writes)
- `tracker_file` (absolute path — Step 8 edits this)
- `notes` (surface to the user only if non-trivial — e.g. description conflict, tracker seed skipped)

If the resolver stops with an error, pass the message to the user verbatim and stop. Do not retry with invented arguments. **One carve-out:** if you arrived here via Step 1's rule 4 (no arguments, no context, probing for a storm awaiting design) and the error is the resolver's "description required" exit, nothing was created and this is the expected negative result — do not surface it as a failure. Fall back to Step 1 rule 5, ask the user what they want designed, and then re-enter Step 2 normally with the description that produces.

**`feature-resolve` runs inline in this turn — do not end your turn when its result block appears.** The `Skill` tool loads it into your own context rather than delegating to a subagent, so the block is a checkpoint in the middle of *your* run, not a hand-off that returns control anywhere. Once you've recorded the fields above, continue straight into Step 3 in the same turn. Stopping here strands the user with a seeded folder, an empty tracker, and no design.

## Step 3 — Ground the design in the codebase

**Do this before the first `AskUserQuestion` in Step 4.** Clarifying questions written without grounding are vague and force extra rounds; reading the modules the feature will most likely extend first makes the questions concrete and lets you offer specific options.

**Read the storm first, if one exists for this feature.** Check the resolver-returned `feature_folder` for a file named `feature-storm-v<version>-<description>.md`. If it exists, `Read` it now, before any codebase exploration — it captures the product intent (§1–§6) and, crucially, the open questions §7 that **Step 4's clarification loop must close**; the storm's §6 (Risks) also seeds this design's own risks section. If no storm exists, that's fine — the user chose to design cold; proceed without it. Do not warn or prompt; cold design is a supported path. This mirrors the convention `/feature-plan` and `/feature-implement` use to read sibling artefacts from the same feature folder.

Use `Read`, `Grep`, and `Glob` only to understand the parts of the project the feature interacts with — entry points, existing modules the feature must integrate with, data models it must extend, tests that establish current behavior. Cite findings by `path:line` when relevant.

**Legacy `docs/` is fair game for grounding.** If the repo has older `docs/<prefix>-v<X>.<Y>.md` files (the previous-generation design convention), read them for context — they capture prior decisions and architectural intent. Do **not** continue their version numbering and do **not** write into `docs/`; the new artefact lives under the resolved `feature_folder`. The `notes` field from the resolver will mention if you're in a repo that has legacy docs.

Two more grounding sources are load-bearing when they exist: (a) if the feature supersedes or remediates an area covered by an earlier feature, read the most recent prior `features/feature-v<M>-*` design for that area — it records the prior approach and decisions your §6 *Alternatives considered* should contrast; (b) if the requirements come from a multi-item review/spec document, also read its corrections / caveats / "deliberately not recommended" sections and reconcile the target item's stated mechanism against them and the actual code path before designing to it — review docs regularly contain a rationale that a later section (or the code) contradicts.

**Inherited claims are leads, not facts.** The storm, prior designs, and supplied spec or review documents all carry claims that were true when written, true somewhere else, or never true — re-verify them before the interview builds on them:

- Re-derive every `path:line` citation you carry into this document with `Grep`/`Read` — files grow, and inherited line numbers are stale by default.
- For every existing field, carrier or mechanism such a document proposes to reuse, read its validation, caps and call sites first — a named carrier is a claim, not a fact, and a mechanism cited at one site may live at three.
- Cross-check the storm's technical-direction and risk claims against the repo's own committed docs/wiki, and resolve any contradiction against the vendor's primary documentation before writing a single clarifying question — designing on a premise the repo already contradicts is the one error a later self-review cannot catch, because the design stays internally consistent.
- Run a directed pass over the storm's in-scope list: confirm each item is neither already satisfied by the codebase nor blocked by an existing constraint, and open Step 4 with any item that fails — dead scope surfaces in the first round, not mid-design.

**Notice when the feature crosses a project boundary.** While grounding, check whether the requirements can actually be met inside this repo alone. The signs that they cannot: the feature names two sides (client and server, app and API, plugin and host, producer and consumer); it depends on a system whose source is not in this working tree; the code path it extends stops at an HTTP call, a queue, an SDK, or a schema owned elsewhere. Name each other project you find — Step 4 closes the split with the user and Step 6b writes that project's brief. Grounding in a sibling clone is fine when the user points you at one, and so is reading the other side's published API docs; **writing there never is**, at any step.

The goal is twofold: (a) ask better clarifying questions in Step 4, and (b) ensure the design references real, existing structures rather than invented ones. Do not embark on a wide codebase audit — bound the exploration to what the feature touches.

If the working directory is unfamiliar, a single top-level listing plus reading the obvious entry points (README, package manifests, main module) is usually sufficient before moving on.

If the feature integrates with a third-party platform (cloud provider, API, framework, library), also ground in that platform's official documentation. **Prefer docs-MCP servers first**, with `context7` as the default for library and framework documentation; use vendor-specific MCP servers (e.g. Microsoft Learn) for those vendors' surfaces. Fall back to `WebFetch` against the platform's official documentation URL **only when no MCP server covers the topic**. Invent nothing about the external surface.

## Step 4 — Clarify until all material decisions are closed

**This step is mandatory even in auto / non-interactive mode.** If the user or the harness has told you to "work without stopping", "skip clarifying questions", or otherwise run autonomously, that instruction does **not** apply here — closing material ambiguity before the design is written is the entire purpose of this skill. Ask the questions anyway; a design produced from guesses is worse than a brief pause.

**This is an interview, not a quiz.** One `AskUserQuestion` call of four questions closes a genuinely trivial feature and nothing else. Anything with a data model, an integration, a user flow, or a migration takes **several rounds**, and that is the expected shape of this step — treat your first round as the opening of the interview rather than the whole of it. The loop ends on the readiness test below, never on a question count and never on a feeling that you have asked enough.

Iteratively use `AskUserQuestion` (1–4 questions per call) to resolve every material ambiguity. Every area below must be **resolved** before the loop ends — by a user answer where the choice is theirs, or by a grounded decision you record with rationale where it is not:

- **Scope** — what is explicitly in and out of scope for this feature.
- **Acceptance criteria** — what "done" concretely means; how the user verifies the feature works.
- **Behaviour per requirement** — for each numbered requirement that will land in §3, the specific observable behaviour, including what happens at its boundaries. A requirement two engineers could implement differently is not yet closed.
- **Approach choices** — when multiple viable paths exist, present them as options for the user to pick. When an option differs from the others on a **measurable dimension** (cost, latency, storage, memory, quota/request usage), compute that quantity from the Step 3 grounding and state it inside the option description rather than offering an abstract trade-off — quantified options close the decision in one round and ground your recommendation in numbers the user can verify.
- **Constraints** — performance, security, dependencies, deadlines, compatibility, platform.
- **Data and state** — what is stored, where, with what lifetime, with what migration path if any.
- **Interfaces and integration points** — the contract with existing code and with anything external: what this feature calls, what calls it, what it must not break, and what happens to existing callers and existing data.
- **Cross-project split** — whether delivering this feature requires changes in another project or repo (a frontend, a backend, a shared library, an SDK, an infrastructure repo). When it does, close: which projects are involved, what each side owns, the exact contract between them (endpoints or messages, payload shapes and field types, error codes, auth, versioning), which side changes first, and **whether the two sides are built step by step with cross dependencies** (each blocked at points by the other) or independently once the contract is agreed. These answers are what makes Step 6b's brief implementable — a brief written over a guessed contract is worse than no brief at all.
- **Failure behavior** — how the feature behaves on bad input, partial failure, network errors, race conditions.
- **Scale and concurrency** — expected volumes and rates, what happens at the top of that range, and whether concurrent use is possible.
- **Permissions and trust boundaries** — who may do this, what is untrusted input, what secrets or credentials are involved. Skip only when the feature genuinely has no trust boundary, and record that as the finding.
- **Operability** — how anyone will know it is working or broken (logging, metrics, user-visible errors), and whether it needs a flag or staged rollout.

**Ask, or decide and record — but never guess.** Route each open item deliberately:

- **Ask the user** when the choice is theirs to make: product behaviour, anything they would notice or care about, anything trading cost / risk / effort against value, anything irreversible, and anything where your grounding gives two defensible answers.
- **Decide yourself** when the answer follows from the Step 3 grounding, an existing convention in the repo, or a plain best practice with no user-visible consequence — then record it in §5/§6 with its rationale, which is what makes it a closed decision rather than an assumption.
- Never self-decide something merely to save a round-trip. If you would feel the need to write "assuming …" in the design, that is a question you have not asked.
- Bundle up to four questions per call so depth costs rounds, not round-trips — thoroughness is measured in decisions closed, not in messages sent.

If a `/feature-storm` ran first, its §7 (Open questions for design) is the seed list — explicitly close every item there. Do not skip them on the assumption that "the design will figure it out". An item is *closed* either by a user answer **or** by a grounded decision you record in §5/§6 with rationale; reserve `AskUserQuestion` for items with a genuine user-facing trade-off.

**Appearance is not closed here — it routes to Step 5.** When the feature has a user-visible surface, this loop closes *behaviour* — everything on the coverage list above, including the surface's flows, states and error handling. It does **not** close how the surface looks — placement, hierarchy, information density, which components carry it, type or colour treatment. Those are Step 5's decisions, and they are settled by a rendered mockup the user can accept or redirect, not by prose options in an `AskUserQuestion`. This carve-out exists because closing them here inverts the mockup rule: the more visual unknowns a feature has, the more of them this loop would absorb, and the more Step 5a's *Appearance already settled* exit would (wrongly) appear to apply. Concretely:

- A storm §7 item that is a **visual** question is closed *by Step 5*, not by an answer collected here. Record it as routed-to-mockup and carry it into Step 5b's `feature=` statement; it is still closed before the design is written, just one step later.
- Ask here only the visual questions that **bound** the mockup rather than decide it — which platform or breakpoint it targets, whether an existing surface is being modified or a new one added, whether the user already has a reference to follow. Those shape the `kind=` and `references=` slots.
- The one exception is the ambiguity question named in Step 5a (whether to mock up at all); fold that in here when it applies.

### The readiness test — the exit condition

After each round, restate your working understanding internally, then run this test. **The loop ends only when every check passes; a single failure means another round.**

1. **Dry-draft §5.** Sketch the design document's §5 in note form — data model, interfaces, control flow, failure and edge cases, security at trust boundaries, user-facing flows and states (*behaviour*, not appearance), per-component test plan. Every place you would write a guess, a hedge, or "assuming X" is an unclosed decision.
2. **No hedge language survives.** Nothing you intend to write contains "TBD", "TODO", "to be decided during implementation", "either … or …", "as appropriate", "something like", or a list of options presented as if it were a decision.
3. **§8 would be empty.** The design's *Open questions* section would read "None — all decisions closed." Any item you would otherwise park in §8 is a question you have not asked yet — `/feature-plan` refuses to plan against a non-empty §8, so parking it does not defer the cost, it stalls the chain.
4. **Every storm §7 item is closed** — by a user answer, by a recorded grounded decision, or (for visual items only) by routing to Step 5.
5. **Two-engineer test.** Two competent engineers implementing from this design without access to you would produce functionally equivalent behaviour — same data written, same failure handling, same contract with existing code.
6. **A dry round.** The most recent round surfaced nothing that changed the design. If your last round moved something, there is at least one more round to run.

The only uncertainty permitted past this test is **appearance**, which Step 5 closes with a rendered mockup, per the carve-out above.

Three rules keep the rounds efficient and honest:

- **Sequence by dependency.** When the design inherits a load-bearing premise that was flagged high-risk or uncertain (e.g. an external integration whose feasibility was in doubt), re-confirm that premise in the first question — detail questions that silently depend on it are wasted if the premise falls. The same applies *within* a round: when two questions in one call are mutually determining — either answer could change the right answer to the other — merge them into a single question over the combined options rather than asking both and reversing one later.
- **Verified claims only.** Before presenting options whose descriptions or previews assert a specific technical or behavioural outcome, validate the claim against the Step 3 grounding (or a throwaway prototype). Never put an unverified behavioural guarantee in an option. Several classes are easy to miss because they do not read as claims at all, yet the user picks an option *because* of them — so each must be verified before it appears in a question, option description, or preview:
  - **Load-bearing background facts** — regional or service availability, data residency, quota and rate limits, pricing tiers, version support. They read as context rather than as a promise, but they are the reason the user chooses.
  - **Numbers inherited from before the skill ran** — any measured quantity that arrived from the pre-skill conversation, whoever produced it, must be re-derived during Step 3 grounding before it may frame a decision. A figure from a truncated sample or a stale run silently frames the wrong one, and correcting it mid-loop costs the round it was meant to save.
  - **Assumptions about the user's environment** — instance, window or display counts, installed tool versions, what is already running. Where the grounding only *assumed* one, ask it as its own question in the same round rather than baking it into an option description: if the assumption is wrong, the recommendation usually flips. Before asking, attempt to verify it locally with read-only probes (a certificate check, a DNS query, a CLI status call) and ask only what cannot be probed.
  - **Enumerations of a third-party product's current offerings** — model identifiers, SKUs, tiers, plan names, API versions. These are the fastest-rotting facts you hold, and they read as data rather than as claims, so they bypass the verification instinct. Look them up live before they appear in an option, even when Step 3 already covered that platform's API shape.
  - **Cost and blast-radius claims** — before an option asserts a change is cheap, self-contained, or touches N call sites or tests, grep for the tests that pin the behaviour and the prior designs that decided it, and state the real counts inside the option description. And when an option changes a rate, interval, cadence or retry count, read the failure and side-effect contract of everything that fires per tick before recommending it — the amplified downstream side effect, not the tick cost, is what decides.
- **Cross-check the answers — every round, not only at the end.** After each `AskUserQuestion` result, before composing the next round, test the new answers against each other, against earlier rounds, and against the Step 3 grounding for a combination that is contradictory, a no-op, or self-defeating given what the code actually does — and re-ask immediately with the collapsed option set rather than carrying the conflict forward: the user should re-decide in the round that created it, not discover a round later that their earlier choice was empty. After the loop ends, do one final re-scan of all collected answers, resolve anything remaining before writing the design, and note the reconciliation in the doc.

Do not pad with questions for their own sake — a question whose answer cannot change the design is noise, and the ask-or-decide rule above keeps mechanical detail off the user's plate. But when the two failure modes are weighed against each other, **under-clarification is the far more expensive one and the one this skill exists to prevent**: a padded round costs the user thirty seconds, while a design written over a guess costs a plan and an implementation built on it. Never stop early to avoid friction, to seem efficient, or because the user has answered several rounds already — the user asked for a design they can build from, and rounds are the price of one. The final design must have **no points that require further decisions**.

## Step 5 — Mock up the user-visible surface

Run this after the clarification loop has closed and **before** the design document is written — a UI decision settled in prose is a decision nobody actually took, and re-deciding it after §5 is drafted means rewriting the design.

### 5a. Decide whether to mock up at all

A mockup costs the user a round of attention, so this is a rule with named exits, not a matter of taste. Fire `feature-mockup` when **both** hold:

1. The feature has a **user-visible surface** — a GUI screen or component, a web page, a terminal UI, the shape of CLI output, a report or document layout, a notification / email template.
2. That surface's **appearance is not already settled** — there is at least one real visual decision left (placement, hierarchy, density, which components carry it, type or colour treatment).

Skip when any of these four conditions is met. Each is a *named* exit: record which one applied in one line of chat and in §5 of the design, so the absence of a mockup is a visible decision rather than a silent omission.

- **No user-visible surface** — a library or API-only change, a background job, a schema migration, an infrastructure, CI or tooling change, a pure refactor. Nothing to draw.
- **Appearance already settled** — the user supplied the surface *of their own accord, independently of this skill's clarification round*: a screenshot, image, wireframe, design-tool link or existing page to copy; a field-by-field / label-by-label / value-by-value description precise enough to implement without a visual decision; or an accepted mockup already exists for this exact surface (in this feature's `mockups/`, or in a prior feature version's whose surface this feature does not change). Their artefact **is** the accepted direction — cite it in §5 by path or URL instead of drawing over it. Do not "confirm" a decision the user has already made.

  **Answers you collected in Step 4 do not settle appearance.** This exit is about material the user brought — in `$ARGUMENTS`, in the conversation before this skill ran, or in the storm — not about visual choices you elicited yourself a few minutes ago by listing options in an `AskUserQuestion`. A picked option is a direction, not a rendered surface, and Step 4 is explicitly carved out from closing appearance for exactly this reason. If the only thing making the surface "settled" is your own Step 4 round, this exit does not apply — fire the mockup and pass what the user said through as the direction to render.
- **Mechanical delta** — the change follows an existing pattern one-for-one with no visual decision inside it: a label or copy fix, one more field on an existing form, one more column in an existing table, one more row in an existing settings list, a value swap the user already specified exactly.
- **User declined** — the user said, in this conversation, that they don't want a mockup, or asked to go straight to the design or the code for this feature.

**The fire trip-wire — checked before any exit.** The four exits are a filter on a decision that defaults to *fire*, so run this check first and let it win. If the feature has a user-visible surface **and** either of the following holds, Step 5 fires and **no exit applies**:

- the storm's §7 contained a visual question (one you routed to Step 5 under the Step 4 carve-out), or
- Step 4 touched appearance at all — any question, option or answer about placement, hierarchy, density, which components carry the surface, or type/colour treatment.

Both are positive evidence that a real visual decision exists and that the user has opinions about it — which is the fire condition, not the skip condition. The trip-wire is deliberately one-way: it can force a fire, never a skip. Note what it rules out — a feature with many UI unknowns cannot reach *Appearance already settled*, because the unknowns are what tripped it.

Two rules keep this cheap and honest:

- **Don't skip because the UI "seems obvious" to you.** Obvious-to-you is exactly where your picture and the user's diverge. Only the four conditions above license a skip.
- **When it's genuinely ambiguous — the surface exists, the trip-wire did not fire, and you can't tell whether the appearance is settled — fold one question into the Step 4 clarification round** rather than spending a standalone round-trip on it or drawing speculatively. Ask it as a single choice, not as a bundled either/or: question `"Mock up <the surface> before writing the design?"`, options `"Yes, mock it up first"` (Recommended — a rendered page settles placement and density in one round) and `"No, my description is enough"`. If Step 4 has already closed and the ambiguity remains, ask that same question here via `AskUserQuestion`.

**Partially supplied references are a fire, not a skip.** When the user gave a reference that covers only part of the surface (one screen of three, the desktop layout but not the mobile one, the palette but not the layout), fire the mockup and pass the reference through — the mockup's job is then to extend the user's own direction, not to reinvent it.

### 5b. Invoke `feature-mockup`

`feature-mockup` writes each page under `<feature_folder>/mockups/` and publishes it as a Claude Artifact, so the user reviews a hosted page by link instead of a `file://` path. The `Artifact` tool asks that the `artifact-design` skill be loaded before any artifact page is written, and `feature-mockup` holds no `Skill` tool of its own — so **when this session offers both an `Artifact` tool and an `artifact-design` skill, load `artifact-design` via the `Skill` tool now**, immediately before the invocation below. It runs inline and writes nothing: do not end your turn, carry straight on. When either is absent, skip this and invoke the mockup directly — it falls back to presenting local files.

Invoke it via the `Skill` tool with the argument string:

```
feature_folder=<feature_folder>, version=<version>, feature=<one-line statement of what the user will see>[, kind=<new|modify>][, references=<path-or-URL>[; <path-or-URL>…]]
```

Use the `feature_folder` and `version` recorded in Step 2 verbatim. Pass `kind=modify` when the Step 3 grounding shows the surface already exists in the codebase, `kind=new` when it does not, and omit the slot when you are unsure — the mockup skill classifies it. Pass `references=` whenever the user supplied a partial visual reference (an image path from the conversation, a design-tool or documentation URL, or a path to an existing page in the repo to follow); omit it otherwise.

Three surface shapes need one more line in the invocation:

- When the surface *is* an interaction (drag, swipe, gesture, animation), say so in the `feature=` statement and ask for the interaction to be simulated live in the page (throwaway inline script, nothing persisted) — a frozen frame of a gesture tells the user nothing, and retrofitting the live behaviour costs a revision round.
- When the feature spans two or more distinct surfaces, ask for the choice question to be posed per surface rather than over whole-page composites, so a hybrid preference ("this tab from A, that tab from B") lands in the first choice round instead of forcing one.
- When an accepted mockup already exists for this feature's surface and only new states or sub-surfaces remain, pass `kind=modify` with `references=<the accepted mockup's path>`, so the alternatives explore only what it leaves open rather than re-litigating the accepted direction.

### 5c. Fold the outcome into the design

Parse the returned result block and record `status`, `kind`, `mockup_dir`, `chosen_mockup`, `artifact_urls`, `alternatives`, `design_language`, `decisions`, and `open_ui_questions`. Then:

- **`status: accepted`** — carry `decisions` into the design: each item becomes concrete content in §5 (*Interfaces* for the surface itself, *Architecture / components* for the components it reuses or adds), and the accepted mockup is referenced from §5 by relative path (`./mockups/<chosen_mockup>`) plus, when `artifact_urls` holds a link for that filename, its artifact URL alongside. Cite both: the URL is what a reader clicks, the relative path is what still resolves in a clone with no network. Record each rejected entry in `alternatives` in §6 as one line plus why it lost, with its own artifact URL when there is one. Any `open_ui_questions` must be closed by looping back to Step 4 for one more round — they may **not** be parked in §8, which has to stay empty.
- **`status: declined` or `not-applicable`** — note it in one line and continue to Step 6. Neither blocks the design; §5 then describes the surface in prose as it always did.
- **Skipped at 5a** — §5 records which named condition applied in one line, and for *Appearance already settled* also cites the user's artefact (path, URL, or the prior feature's accepted mockup) as the source of the surface's appearance. A skipped mockup is not an excuse for a vaguer §5: the surface still gets flows, states and placement specified.

**`feature-mockup` runs inline in this turn — do not end your turn when its result block appears.** The `Skill` tool loads it into your own context rather than delegating to a subagent, so the block is a checkpoint in the middle of *your* run. Continue straight into Step 6 in the same turn.

## Step 6 — Write the design document

### 6a. The design document

**Guiding principle:** the design must always prefer a **modular, separately testable** structure over a monolithic one. Decompose the feature into small components with clear single responsibilities and explicit interfaces. Each component should be unit-testable in isolation (no hidden global state, no implicit coupling, no requirement to spin up the whole feature to test one piece). When there is a viable modular approach, choose it over the monolithic one even if the modular approach takes more files. If a monolithic approach is genuinely warranted (e.g. the seam would be artificial and add no testability), record the rationale explicitly under §6 *Alternatives considered*.

Write the file at the `stage_file` path returned by Step 2. Use this structure exactly. Every section is required; if a section has no content for this feature, write a brief explicit "Not applicable — <reason>" rather than omitting it.

```markdown
# <Feature Name> — Design v<N>

**Status:** Draft
**Date:** <YYYY-MM-DD>
**Storm:** [feature-storm-v<N>-<description>.md](./feature-storm-v<N>-<description>.md)  ← include this line only if the storm file exists in the same feature folder; omit otherwise.

## 1. Summary
One paragraph: what the feature is, who it is for, what problem it solves.

## 2. Goals and non-goals
- **Goals:** bulleted, concrete outcomes.
- **Non-goals:** what this design explicitly does not address (and why, briefly). When the feature spans more than one project, the other projects' implementation is a non-goal *here* — name it and point at its brief under `./briefs/`, so nothing downstream plans work this repo does not own.

## 3. Requirements
Numbered functional and non-functional requirements derived from Steps 1 and 4. Each requirement must be testable.

## 4. Background and context
Relevant existing code, modules, data models, prior designs. Cite by `path:line` where applicable. Note what currently exists and what is missing. If a brainstorm document exists at `features/feature-v<N>-<desc>/feature-storm-v<N>-<desc>.md`, reference it.

## 5. Design
The single recommended approach, in enough detail that a competent engineer can implement it without re-deriving decisions.

Sub-sections as needed:
- **Architecture / components** — what is added, modified, removed. Show the modular decomposition: each component's single responsibility, its public interface, and which other components it depends on. If the feature is implemented as one cohesive unit rather than several, explain why splitting would be artificial.
- **Data model** — schemas, migrations, storage, lifetimes.
- **Interfaces** — APIs, function signatures, message shapes, CLI flags, UI surfaces. When Step 5 produced an accepted mockup, describe the surface as that mockup shows it and link it: `[<name>](./mockups/<chosen_mockup>)`.
- **Cross-project contract** — only when the feature spans more than one project: what this repo owns, what each other project owns, and the exact contract between them (endpoints or messages, payload shapes with field names, types, optionality and units, status and error codes, auth, idempotency, limits, versioning and what happens to existing callers). This section and the briefs written in Step 6b must state the same contract, field for field.
- **Control flow** — happy path step-by-step; key alternative flows.
- **Failure and edge cases** — concrete behavior for each.
- **Security** — authn/authz, input validation, secret handling, trust boundaries.
- **Performance** — expected load, hot paths, caching, indexes, limits.
- **Observability** — logs, metrics, traces; what is alertable.
- **Compatibility / migration** — backwards compat strategy; data migration steps.
- **Testing strategy** — unit, integration, end-to-end coverage; how acceptance criteria are verified. Each component identified in *Architecture / components* must have a corresponding unit-test plan that does not require the rest of the feature to be running.

## 6. Alternatives considered
Only include alternatives that were actively evaluated and rejected. For each: one sentence on the alternative and one sentence on why it was rejected. If none were actively evaluated, write "None — <reason>" rather than omitting the section.

## 7. Risks and issues
Concrete risks with likelihood/impact and mitigation. Include known issues with the current codebase that this design must work around.

## 8. Open questions
This section **must** be empty or contain only the literal text "None — all decisions closed." If you find yourself listing real open questions here, return to Step 4 and resolve them before saving.

## 9. Rollout plan
Phasing, feature flags, dark launches, rollback strategy, communication. When the feature spans projects that are built step by step with cross dependencies, state here that a **single implementation plan spanning both projects is required** — neither side can be planned in isolation — and name the checkpoints that must line up.
```

Compute `<YYYY-MM-DD>` from `date -u +%Y-%m-%d`. Use `v<N>` (integer) in the header — never `v<N>.<M>`.

### 6b. Design briefs for the other projects

Run this whenever Step 4 closed the *Cross-project split* with **more than one project involved**. When the feature lives entirely inside this repo, skip it — no folder, no file, one line in Step 10.

The user cannot run `/feature-design` in the other project from this session, and this skill must never reach into that repo. So write one **design brief per other project** into this feature's own folder, hand the paths over in Step 10, and let the user feed each brief to `/feature-design` in a separate session opened in that project.

Write each brief to:

```
<feature_folder>/briefs/brief-v<N>-<project-slug>.md
```

`<project-slug>` is the other project's repo or product name, lower-cased and hyphenated (`payments-api`, `web-client`). Create `briefs/` with `mkdir -p` on first use. One file per project — never one combined brief covering several.

**Write each brief for a reader with no access to this repo, this conversation, or this design.** Whatever the brief omits, the other side will re-derive by guessing, and a guessed contract is a broken integration that surfaces in neither project's tests. Use this structure; every section is required, and a section with nothing to say gets an explicit "Not applicable — <reason>":

```markdown
# <Feature Name> — Design brief for <Other Project>

**Status:** Brief — input for `/feature-design` in <Other Project>
**Date:** <YYYY-MM-DD>
**Source:** <this repo name> — features/feature-v<N>-<description>/feature-design-v<N>-<description>.md (v<N>)

## Context
What the feature is, who it is for, why this project is involved, and what the other side is building. Enough for a reader who has never seen this feature.

## What this project must implement
Numbered, testable requirements for *this* project — observable behaviour, not internal implementation. Each stands on its own; never "as described in the source design".

## The contract between us
The exact interface between the two sides, in enough detail to build and test against without asking us: endpoints or messages with methods and paths, request and response shapes with field names, types, optionality and units, status and error codes with their meaning, auth and identity, idempotency, pagination, limits, timeouts, versioning, and what happens to existing callers and existing data. Give a concrete example of every payload. This section is the reason the brief exists.

## What the other side does
The counterpart behaviour this project can rely on, what it must not assume, and which parts of it already exist versus are being built alongside.

## Constraints and non-functional requirements
Performance, expected scale and concurrency, security and trust boundaries, data handling and retention, compatibility, platform, deadlines.

## Failure behaviour
What each side does when the other fails — errors, timeouts, retries and whether they are safe, partial failure, and the degraded behaviour the end user should see.

## Acceptance criteria
How this project verifies its half is done, including what it can test in isolation with the other side stubbed.

## Sequencing
Whether this project can be built independently once the contract is agreed, or in lockstep with the other side. If in lockstep: the cross dependencies, the order they force, and the plain statement that **a single implementation plan spanning both projects is required** — neither side may be planned in isolation.

## Open questions for the receiving design
Decisions deliberately left to this project — its internal architecture, its own storage, its own UI. Anything about the *contract* belongs above, decided; it may never be parked here.
```

Three rules make a brief usable on the other side:

- **Self-contained.** No `path:line` citations into this repo, no "see §5", no links to files the reader cannot open. If a detail matters, restate it in full.
- **Contract-complete.** Every field, code, unit and edge the two sides exchange is named. "The usual error envelope" is a failure.
- **Our internals stay here.** The brief carries the contract and the expectations, never this repo's module layout, test names, or decisions the other side cannot observe.

**Lockstep delivery needs a joint plan, stated on both sides.** When Step 4 established that the two sides are built step by step with cross dependencies, the need for a single implementation plan spanning both projects must appear **in this design's §9** *and* **in every brief's *Sequencing*** — the same statement in both places, so whichever session reads first sees it. Neither project's `/feature-plan` run can sequence the other's stages, so the coordination only exists if the user is told to carry it.

**Never write outside this repo.** Briefs live in `<feature_folder>/briefs/` and nowhere else. Do not create, edit or copy files in the other project — not its `features/` folder, not its docs, not a shared location — even when a local clone is sitting right there. Moving the brief is the user's step, not this skill's.

## Step 7 — Self-review and fix

Re-read the draft critically through these lenses, and fix what you find via `Edit` directly in the design file. Do not produce a separate review document.

- **Functional correctness** — does every numbered requirement in §3 map to concrete design content in §5? Any requirement without a corresponding design element is a gap to fix.
- **Decision closure** — is §8 truly empty / "None"? Any hand-wave ("we'll just…", "should be straightforward…", "TBD", "TODO", "to be decided") must be replaced with a concrete decision or moved to §7 as an explicit accepted risk with rationale.
- **Security gaps** — injection (SQL/command/template/prompt), authn/authz holes, secret handling, input validation at trust boundaries, unsafe deserialization, SSRF, path traversal, crypto misuse, logging of secrets/PII. Fix or document with mitigation.
- **Inefficiencies** — blocking I/O on hot paths, unbounded scans / buffers / retries, cache misuse, redundant computation, premature abstraction, shotgun surgery; *for data-backed features also*: N+1 queries, missing indexes. Skip lenses that do not apply to the feature's domain — do not invent database concerns for features that touch no database. Fix or justify what remains.
- **Modularity and testability** — is the feature decomposed into small components with single responsibilities and explicit interfaces? Can each component be unit-tested in isolation without standing up the rest of the feature? Flag any "god module" / monolithic blob that mixes responsibilities, and split it (or record an explicit rationale in §6 if the split would be artificial). Modularity for its own sake is not the goal — testability and clear seams are.
- **Reference integrity** — every `path:line` citation, function name, library, or API named in the design must actually exist. Verify the non-obvious ones with `Read`/`Grep`. Remove or correct anything invented.
- **Grounded-behaviour integrity** — existence is not enough: verify the design's *claims about* existing code against the Step 3 grounding. For any function the design leans on for an error-handling or degradation path, read its failure contract (raises vs returns empty vs no-op) rather than assuming graceful degradation. Confirm the proposed flow honours the documented preconditions and ordering/state invariants of any function or data structure it reuses or sits adjacent to. Every field or distinction the design derives must be obtainable from the grounded interface/response shapes — never promise data the integrated system cannot provide. If the feature touches a path served by an existing incremental-redraw, diff, cache, or index optimization, state whether the design preserves or consciously replaces it (with the cost). And for any requirement that changes a constant, default, or config value, confirm the current value from the codebase and flag already-satisfied no-op changes explicitly.
- **Extension completeness** — when the design *extends* something that already exists rather than adding something standalone, the failure mode is partial wiring: the design covers one site while the mechanism has several, and the gap surfaces as missing wiring during implementation. Enumerate the sites and confirm the design names each. Three shapes recur:
  - **A new value on an existing type, enum or discriminated union** — every dispatch, switch or match site over that field must handle it, including the `else`/default branches that would otherwise raise on an unrecognised value.
  - **A mechanism already wired at several sites** — grep for every call site *and* every intermediate carrier between the mechanism's origin and its endpoint. A mechanism wired at N sites must be extended at N sites; naming the origin and the endpoint while omitting the carrier in between is the common miss.
  - **A new branch or early return inserted inside an existing function** — enumerate every side effect that function performs *after* the branch point (validation, sanitisation, normalisation, metric or log emission, state mutation) and confirm each still executes on the new path or is explicitly re-invoked; where one must be shared, the design names the extraction as its own behaviour-preserving step. This shape is the costliest of the three: a sanitisation step sitting inside the bypassed leg silently unmeets a security requirement, and nothing downstream reports it.
- **Mockup fidelity** — if Step 5 returned `status: accepted`, every item in its `decisions` list must appear as concrete design content (placement, reused components, states, palette/typography deltas), the accepted mockup must be cited by relative path, and no section may describe a surface that contradicts it. A design that quietly drifts from the mockup the user approved is the failure this lens exists to catch. Skip the lens when Step 5 was skipped or returned `declined` / `not-applicable`.
- **Cross-project brief completeness** — when Step 6b wrote briefs: each brief is implementable by a reader with no access to this repo (no dangling citations, no "see the design", no unstated field), the contract it states matches §5's *Cross-project contract* field for field — same names, types, codes, units and directions — and every requirement this design assigns to another project appears in that project's brief. Where the sides are in lockstep, the joint-plan statement appears in both §9 and each brief's *Sequencing*. Verify by re-reading each brief on its own, as the other side will. Skip the lens when the feature is single-project.
- **Cross-section consistency** — for any scenario the design describes in more than one place (§5.4 + §5.5 + §5.9), trace it through ALL sections and check they agree on the same outcome. Contradictions between sections are the most common review failure.

Update §1–§9 in place. Do not append a "review notes" section — the design is the artifact, not the review.

After the edits, do a final read-through to confirm:

1. §8 is empty / "None — all decisions closed."
2. No "TBD", "TODO", "FIXME", or hand-wave language remains.
3. Every requirement is addressed.
4. Risks in §7 each have a mitigation.

If any of these still fail, loop on Step 7 until they pass. Do not proceed to Step 8 with an unresolved design.

## Step 8 — Update the tracker

The tracker file at `tracker_file` already exists (seeded by `feature-resolve` in Step 2; its stepper has only two states — `pending` and `complete` — and the design step stays `pending` until this step flips it). If the file is somehow missing (resolver `notes` flagged `tracker_seed: skipped`), defensively copy the plugin template:

```bash
# 1. Prefer the running plugin's own copy: this skill's announced base directory is
#    .../dev-skills/<version>/skills/<slug>, so the template is at <base>/../../templates/.
# 2. Else search — the *dev-skills* form is deliberate, since installed plugins live at
#    .../dev-skills/<version>/templates/ which "*/dev-skills/templates/*" silently misses.
find ~ -path "*dev-skills*/templates/feature-tracker.html" 2>/dev/null
# cp the winner (base-dir copy first; else a plugins/cache/ match at the highest version;
# else a working clone) to <tracker_file>. Copy, never symlink.
```

If no template can be located, skip the tracker update and note it in Step 10 — do **not** fail the whole skill.

First `Read` the tracker file once — `feature-resolve` seeded it via a shell copy, so the `Edit` tool has no read-state for it and every edit below would otherwise fail its first attempt. Then apply these edits via the `Edit` tool. For each `{{TOKEN}}`, check it is still literal text in the file (so you never overwrite content from `/feature-storm` or any other prior stage). If a token is already substituted, skip that edit silently. Note: the seeded tracker opens with an HTML documentation comment that lists every token name literally, so a bare `{{TOKEN}}` match is non-unique — scope each Edit to the rendered body occurrence (the chip span, bullets `<ul>`, details block, or `<h1>` title), never the comment-block token. **Never use `replace_all` on a tracker token.** The two-match failure is the *safe* outcome — it errors and you fix the scope. `replace_all` instead succeeds silently and rewrites the token name inside the opening documentation comment as well, corrupting the template's own self-documentation with no error and no gate to catch it. The reliable technique: grep the tracker for each token name first to locate the body occurrence (the second hit — the first is the doc comment), anchor the Edit with surrounding context taken from that spot, and treat a missing match as a loud failure to investigate — never as a silent skip of a token this skill owns.

**Header tokens** (only edit if still literal):

- `{{FEATURE_VERSION}}` → `<N>` (integer).
- `{{FEATURE_TITLE}}` → human-readable title: take `description`, replace hyphens with spaces, then title-case each word while preserving any existing capitalization and upper-casing well-known acronyms (REST, API, CLI, HTTP, URL, SQL) (`Add-Reminders` → `Add Reminders`; `python-rest-server` → `Python REST Server`).
- `{{FEATURE_SLUG}}` → `feature-v<N>-<description>`.
- `{{GENERATED_AT}}` → today's UTC date (`YYYY-MM-DD`).

**Design section tokens** (this skill owns these — always fill them with real content). Compute the timestamp once via `date -u +"%Y-%m-%d %H:%M UTC"` and reuse the same value for the chip. **If `/feature-storm` ran first, these are no longer the literal `{{DESIGN_*}}` tokens — the storm rendered them as the placeholder prose `Awaiting /feature-design` (the chip) and two `<p class="empty">Not yet filled — pending /feature-design.</p>` blocks (bullets + details). Overwrite those placeholder strings with the real design content; the skip-if-substituted rule above protects only *other* skills' tokens, never your own Design panel.**

- `{{DESIGN_AT}}` → `Updated <YYYY-MM-DD HH:MM UTC>` (the timestamp chip text — no surrounding HTML).
- `{{DESIGN_BULLETS}}` → an `<ul>` of 5–10 design highlights, one `<li>` per bullet, plain text content (no markdown — convert any markdown to HTML).
- `{{DESIGN_DETAILS}}` → free-form HTML rendering the design in increasing detail, drawn from the design file written in Step 6. When Step 5 produced an accepted mockup, include a relative-path `<a href="./mockups/<chosen_mockup>">` link to it near the top of this block so the tracker doubles as the way back to the approved visual — and, when `artifact_urls` holds a link for that filename, a second `<a>` to the published artifact beside it, which is the one that still works when the tracker is shared. Cover §1 (Summary) → §2 (Goals & Non-goals) → §5 (Architecture / data / interfaces / failure / security / performance / testing — pick the sub-sections that matter most for this feature) → §7 (Risks) → §9 (Rollout). Use `<h3>` for top-level section titles, `<h4>` for sub-sections, `<p>` / `<ul>` / `<table>` for content. Order content from highest-level to most detailed so a reader can stop reading at any depth. Skip §6 if empty and skip §8 (it's always "None"). When Step 6b wrote briefs, list each one near the top as a relative-path `<a href="./briefs/<file>">` link naming the project it targets, so the tracker shows the feature's other halves and where they are handed off.

**Storm and future-stage placeholders** — substitute with the empty placeholder *only if still literal*. If `/feature-storm` ran, `{{BRAINSTORMING_*}}` will already be content and you skip them:

- `{{BRAINSTORMING_AT}}` → `Awaiting /feature-storm`
- `{{BRAINSTORMING_BULLETS}}` → `<p class="empty">Not yet filled — pending /feature-storm.</p>`
- `{{BRAINSTORMING_DETAILS}}` → `<p class="empty">Not yet filled — pending /feature-storm.</p>`
- `{{PLAN_AT}}` → `Awaiting /feature-plan`
- `{{PLAN_BULLETS}}` → `<p class="empty">Not yet filled — pending /feature-plan.</p>`
- `{{PLAN_DETAILS}}` → `<p class="empty">Not yet filled — pending /feature-plan.</p>`
- `{{IMPLEMENTATION_AT}}` → `Awaiting /feature-implement`
- `{{IMPLEMENTATION_BULLETS}}` → `<p class="empty">Not yet filled — pending /feature-implement.</p>`
- `{{IMPLEMENTATION_DETAILS}}` → `<p class="empty">Not yet filled — pending /feature-implement.</p>`

**Progress bar** (mandatory transition — only fired in this step, after the design document is written and self-reviewed):

- old_string: `<li class="step" data-stage="design" data-state="pending">`
- new_string: `<li class="step" data-stage="design" data-state="complete">`

Scope the match to the full stepper `<li>` opening tag as above — the bare `data-stage="design" data-state="pending"` attribute pair also appears in the template's documentation comment as its worked example, so the shorter old_string fails with two matches on every fresh tracker.

If the Edit fails because no `pending` match exists, the design step is already `complete` (backfill on a fully tracked feature) — leave it alone.

Do **not** touch other skills' tokens (storm content, plan, implementation) beyond the empty-placeholder fallback above. Do **not** touch other skills' progress steps.

## Step 9 — Capture lessons

Invoke the `lessons-capture` skill in this plugin via the `Skill` tool with the single argument `feature-design`. It runs the reflection protocol, appends a dated entry to `~/.claude/dev-skills/lessons/feature-design.md`, and returns the entry body (a single recommendation in three lines, or the "No skill-improvement recommendations from this run." line) for you to paste under the *Skill-improvement recommendations* heading in Step 10.

Do not run the reflection inline — `lessons-capture` is the single source of the protocol for all skills in this plugin.

## Step 10 — Present highlights

In chat, output a short, scannable summary so the user does not need to open the file to get the gist:

```
Saved: <stage_file path>
Tracker: <tracker_file path>
Mockup: <artifact URL of the accepted mockup, when published> — <path to the accepted mockup> (<its name>)   ← omit this line when Step 5 was skipped or returned declined / not-applicable
Briefs: <path to each brief> → <Other Project>   ← one line per brief; omit when the feature is single-project

**Feature:** v<N> — <human-readable title>

**Highlights**
- <Approach in one bullet>
- <Key data/interface decision>
- <Key security or performance decision>
- <Any notable trade-off the user should know>

**Risks**
- <Top 1–3 risks from §7, each one line>

**Acceptance**
- <How the user will verify the feature works, one or two bullets>

**Cross-project hand-off**   ← omit this whole section when the feature is single-project
- <Other Project> — `<brief path>`: open a separate session in that project and run `/feature-design` with this brief as the requirements. The brief is self-contained; that session needs nothing from this one.
- <Either "Both sides can be planned independently once the contract is agreed." or "Both sides are built with cross dependencies — they need one implementation plan spanning both projects, not two independent ones.">

**Skill-improvement recommendations**
- <single item from Step 9, or the line "No skill-improvement recommendations from this run.">
```

Keep the chat output under ~30 lines. The file is the artifact; the chat is the pointer.

## Step 11 — Offer to chain into /feature-plan

**Report the run usage.** Invoke `usage-report` via the `Skill` tool with the argument `report feature-design, tracker_file=<tracker_file>, feature_version=<version>`, taking both values from this skill's `feature-resolve` block. It prints the run's usage table, appends one line to the usage log and fills this stage's tracker panel. Do this *before* the offer below: on the chain-in branch this skill hands over through the `Skill` tool and never returns to the step, so a report placed afterwards would silently never run. It runs inline — **do not end your turn**, carry straight on.

After presenting the highlights, give the user a one-click way to continue into the planning skill. Call `AskUserQuestion` exactly once:

- **question**: `"Continue with /feature-plan to produce a TDD-staged implementation plan for this design?"`
- **header**: `"Run /feature-plan?"`
- **options**:
  - `{ "label": "Yes, run /feature-plan", "description": "Launch the plan skill against the design just saved." }` (mark this as Recommended)
  - `{ "label": "Not now", "description": "Stop here; the design is saved." }`

If the user picks "Yes, run /feature-plan", invoke the `feature-plan` skill via the `Skill` tool with the single argument `v<version>` (the integer feature version resolved in Step 2). The plan skill's Step 1 parses the version token and delegates to `feature-resolve`, which continues into the same feature folder — no conversation-context lookup involved.

If the user picks "Not now" or "Other", emit exactly one line before stopping:

```
**Next step:** when you're ready, run `/feature-plan v<version>`.
```

Do not skip this step or substitute the AskUserQuestion with prose. The offer is the affordance; rendering it as a question is what makes it one-click. The "Next step" hint is only emitted on decline.

## Constraints (non-negotiable)

- **Output path comes from `feature-resolve` only.** Never write to `docs/`, never construct `features/...` paths by hand. Step 2 is the single source of pathing.
- **Integer versions only.** `v<N>` everywhere — no `v<N>.<M>` minor versions. No "next available version" math in this skill; the resolver decides.
- **No open decisions.** §8 must be empty or "None — all decisions closed." before Step 8 begins.
- **Clarify to exhaustion, not to a quota.** Step 4 is an interview that runs until the readiness test passes — a dry-drafted §5 with no guesses, no hedge language, an empty §8, every storm §7 item closed, the two-engineer test met, and a round that surfaced nothing new. Question count, elapsed rounds, and the user having already answered a few are not exit conditions. The one uncertainty allowed past it is appearance, which Step 5 closes with a rendered mockup.
- **Report the run usage before you stop.** However this run ends — normal completion, a halt, a refusal, a stop condition, or an error surfaced to the user — invoke `usage-report` with `report feature-design, outcome=halted` before you stop (Step 11's normal path passes `outcome=completed` instead). This covers every exit Step 11 does not. A halted run still cost tokens, and one that never reports vanishes from the log and skews every average drawn from it.
- **Self-review is mandatory.** Step 7 must run even if the draft looks clean — security and efficiency gaps are usually invisible on the first pass.
- **UI decisions come from the user, via the mockup.** When the feature has a user-visible surface, Step 5 runs and the design records the direction the user accepted — never a surface you invented and never one the user has not seen. `feature-mockup` owns the mockup files under `<feature_folder>/mockups/` and their published artifacts; this skill only reads them and cites them, by URL and relative path both.
- **Briefs never leave this repo.** When the feature spans projects, Step 6b writes one self-contained brief per other project under `<feature_folder>/briefs/` and stops there. This skill never writes, edits or copies anything into another repository, never runs the chain on the other side's behalf, and never treats a brief as a substitute for closing the contract: what the brief states was decided in Step 4 and is recorded in §5.
- **Tracker edits are defensive.** Substitute only tokens still literal `{{...}}`; never overwrite content placed by `/feature-storm` or any other skill. The progress bar's `data-stage="design"` entry is this skill's alone to touch.
- **`docs/` is read-only legacy.** Step 3 may read legacy designs for context but never writes there. The empty-placeholder pattern in `feature-resolve` + Step 8 ensures the tracker renders cleanly regardless of whether prior stages ran.
- **No symlinks.** If a defensive tracker template copy is needed in Step 8, always copy — never link.
- **Lessons capture runs every time.** Step 9 always invokes `lessons-capture`; whether it produces a recommendation or "none this run" is decided by that skill.
- **Never paste the entire design into chat.** Step 10 is highlights only; the user opens the file for full content.
