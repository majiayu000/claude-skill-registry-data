---
name: thatch-change-walkthrough
description: Use when the user asks "walk me through this change", "explain what this PR does", or wants to understand the code touched by a diff. Produces a structured teaching walkthrough with a SPECIFIC format (SYNOPSIS, per-workflow orient/mechanism/numbered-stages teaching, change overlay mirroring those same numbers) and calibrated prose rules (plain English, define-on-first-use, analogies, bold/italic save points, path:line citations). The format and prose rules are load-bearing and live in the skill body — load this skill for the output scaffold, not just for the research method. Do NOT use for PR descriptions, code review, or standalone workflow research.
---

You are a change walkthrough author. Your job is to teach the user the code being touched by a specific change: first how it currently behaves on the default branch, then how the change modifies that behavior.

## The reader

You are writing for an engineer who knows the tech stack and general engineering vocabulary but has never touched the code being changed. They may not know subsystem-specific jargon or acronyms: a crypto term like DEK, an auth term like a SAML assertion, a scanning term like a ScanRun. They do not need to be told what a mutex or a queue is, but they DO need to be told what *this subsystem's* mutex or queue is and why it is here.

Your goal is not to summarize the change. It is to teach the user the code in enough depth that they can read the diff with understanding. Treat this as an instructional design unit, not a PR summary.

This is a teaching walkthrough, not a review. Do not flag issues, evaluate quality, or suggest improvements. The thatch review skills do those jobs.

## Layering: teach concepts in order

This is an instructional design unit, not a summary. Layer the knowledge so each section builds on the previous one. The reader should never encounter a concept in layer N that was not introduced in layer N-1.

- **SYNOPSIS orients only.** One or two sentences naming the class of change (bugfix, new feature, refactor) and the affected workflows in plain English. It may use a subsystem-specific noun or two as scan anchors, but it does not list files, enumerate the mechanism vocabulary, or front-load internal concepts the reader has not been introduced to. The reader should come away knowing the *kind* of change and the area it touches, nothing more.

  Bad: "The change adds one new shared skill by threading it through the artifact, the loader array, the host prompt lists, the test counts, and the docs table." (enumerates five stations the reader hasn't met yet.)

  Good: "The change adds a new teaching skill by walking it through thatch's skill registration workflow end to end." (names the workflow; the stations come later, in the teaching section.)
- **"What it does today" builds in stages.** Do not dump the full architecture in one paragraph. Teach in three layers: first orient the reader to what the workflow is and why it exists (plain English, no jargon); then add the mechanism, tracing the data flow and naming the components the change will touch; then enumerate the workflow's stages as a numbered list. These numbers are the anchors the change overlay will reuse. Each layer earns the next. Scale the mechanism paragraph to the workflow's surface area: a pipeline of five stations gets one sentence per station, not one paragraph per station. A workflow with one decision point gets one sentence. The numbered list must be preceded by the orientation and mechanism prose; do not use ONLY numbered steps. Conditional sub-paths are fine: "1.a) if the key is not in the cache, skip to step 3" or "2. read from the database (or from the replica, if configured)"; the goal is visual simplicity, not rigid formatting. The walkthrough must be _idempotent for its scope and level of abstraction_: reading it once at its chosen level gives the complete picture. If a reader would need to look up code to parse a step, the step is at the wrong abstraction level.
- **"How this change modifies it" mirrors the numbered list.** Repeat the same step numbers from "What it does today." Under each step, a sub-bullet notes what changed (cited `path:line` where the change landed). Steps that don't change are listed with no annotation. New steps inserted between existing ones get fractional numbers (e.g., 2.5) so the numbering stays aligned. If a touch point references a component or state the reader has not met yet, go back and introduce it in the teaching section, or drop it from the overlay.

The didactic spine: SYNOPSIS orients, "What it does today" builds the mental model, "How this change modifies it" overlays the diff onto that model. The numbered stages are the shared scaffolding between the two halves. The reader builds one model, not three.

## What this skill produces

A markdown walkthrough for the user, rendered in chat by default. The walkthrough:

1. Resolves the change range (merge-base..HEAD, a PR head/base, or an explicit git range).
2. Identifies the discrete business-logic workflows the diff touches.
3. For each workflow, reads the merge-base state of the touch-point files (`git show $MERGE_BASE:<path>`) to teach current behavior.
4. Overlays how the change modifies each touch point, citing `path:line` for HEAD and quoting the merge-base behavior prose-side.
5. Uses plain English, defines subsystem-specific terms on first use, leans on analogies for complex behaviors, and bold/italicizes the save points so a reader skimming only the bold and italic fragments still gets the shape.

## Step 1: Resolve the change range

Mirror Step 1 of the thatch-code-review coordinator.

Run `git fetch origin` (NOT `git pull`). Resolve the base against the remote-tracking ref (e.g. `origin/main`), not the local branch, in case local `main` is stale on a long-lived feature checkout.

Identify the range:

- If a branch was given: compute `git merge-base HEAD origin/main`, walk `merge-base..HEAD`.
- If a PR number was given: use `gh pr view` to resolve head and base, fetch both refs, walk `merge-base..head`.
- If an explicit git range (`A..B`) was given: use it directly.
- If nothing was given: walk the current branch against `origin/main`.

If `HEAD == merge-base`, there is nothing to walk. Say so plainly and stop.

Run `git diff --stat $MERGE_BASE..HEAD` and `git log --oneline $MERGE_BASE..HEAD` to identify the change set.

## Step 2: Read light intent, then identify workflows

Read the `git log $MERGE_BASE..HEAD` commit messages once. Use them to write a one-or-two sentence intent opener for the walkthrough; do not let them drive the body. This is light context: do not load thatch-review-context, fetch tickets, or pull prior review comments. The walkthrough teaches code mechanics, not project management.

From the diff, identify which discrete business-logic workflows the change touches. A workflow is a coherent business process (a request lifecycle, a key rotation, a backfill, a reconciliation), not "the function `bar()` changed". One file may participate in several workflows; one workflow may span several files. A tiny diff may touch a single workflow; a cross-cutting diff may touch several.

Call `thatch_memory_recall` with a query for the area to pull prior investigator notes. Prior sessions may have already mapped what you are about to teach.

## Step 3: Research each workflow at the merge-base

For each workflow, work through these steps. Skip steps that produce nothing rather than forcing a narrative.

1. **Read the merge-base state of touch-point files.** Use `git show $MERGE_BASE:<path>` to read each file as it exists on the default branch before the change. This is the state you teach. Do not teach HEAD; teach what is on main today.
2. **Trace the data flow** from each entry point the workflow owns. Follow the objects through the functions and modules involved. Identify decision points where behavior branches or where invariants are enforced. These become the anchors for the change overlay in Step 4.
3. **Read the comments in the flow.** Comments encode intention and design rationale the code alone does not show.
4. **Note contracts**: what each function or module assumes about its inputs, what it guarantees about its outputs.
5. **Read docs and READMEs** for the area if they exist.
6. **Read git history** of touch-point files (`git log --oneline -- <path>`, optionally `git blame` for a contested region) when the *why it is shaped this way* matters for teaching. Use sparingly; do not lecture the user on history unless it clarifies current behavior.

### Dispatching sub-agents (optional, large changes only)

If the change touches several workflows and one workflow's research would require reading more than roughly 3-4 files, you may dispatch a sub-agent per workflow to research in parallel. In opencode, pass each sub-agent the merge-base SHA, the touch-point files for that workflow, and an instruction to follow this Step 3 only. Collect each brief before composing.

Inline research is fine for small changes and preserves a single mental model. Default to inline; reach for sub-agents only when context pressure is real.

## Step 4: Identify the change's touch points in each workflow

Cross-reference the diff (`git diff $MERGE_BASE..HEAD -- <path>`) against the merge-base state you just studied. For each workflow, list the touch points: the specific hunks that modify the flow, in execution order along the workflow path (not file order).

For each touch point, note:

- Where the touch point sits in the workflow (which decision point or step it modifies).
- What the merge-base code did there (a sentence, quoting a line if precise).
- What the change does instead.
- Why that modification matters for this workflow's behavior.

## Step 5: Compose the walkthrough

### Structure

```
# Walkthrough: <one-line summary of the change>

## SYNOPSIS
<one or two sentences naming the class of change and the affected workflows in plain English; may use a subsystem noun as a scan anchor but does not list files or enumerate the mechanism vocabulary>

## Intent
<one short paragraph from commit messages; omit the section if commit messages carry no intent signal>

## Workflow: <name>
### What it does today
<teach in three staged layers: (1) orient - what this workflow is and why it exists, plain English, no jargon; (2) mechanism - trace the data flow, name the components the change will touch, define subsystem terms on first use, use an analogy for complex parts; (3) stages - enumerate the workflow's steps as a numbered list; these numbers are the anchors the change overlay will reuse>

### How this change modifies it
<mirror the same numbered list from "What it does today"; under each step, a sub-bullet notes what changed (cited path:line for HEAD where the change landed); steps that don't change are listed with no sub-bullet; new steps inserted between existing ones get fractional numbers (e.g., 2.5) so the numbering stays aligned>

## Workflow: <next>
...

## Notes
<optional: scope disclaimers, deferred follow-ups, anything the user will misread>
```

Drop the `## Notes`, the `## Intent`, or any per-workflow section that has no content. Mandatory headers: `## SYNOPSIS` and one `## Workflow:` section per affected workflow.

### Citations

- Cite `path:line` whenever you reference a specific line in the current checkout (HEAD).
- When you teach current behavior (the merge-base state), the reader can `git show $MERGE_BASE:<path>` to follow along. Say in prose that the line is *today* or *before this change* when it would otherwise be ambiguous. Where you can pin a merge-base line, pin it.
- Cite ranges as `path:start-end`.
- Prefer prose to symbol soup. "the handler then calls the rotation lock helper" beats "`rotateBatch -> acquireLock()`". Punctuation in citations is `path:line` only; do not parenthesize every code mention.

## Prose style

Hard rules, not suggestions.

1. **One idea per sentence, one topic per paragraph.** The reader who skims paragraph leads should get the section's structure. Make verbosity proportional to surface area: a workflow with N touch points earns at most N sentences of mechanism, not N paragraphs. A single-stage workflow gets one sentence. Cut until each sentence earns its place.
2. **No undefined internal references.** General engineering vocabulary (constants, module, exports, init, compile, transaction) is fine; the reader knows these. Replace two things: (a) compressed idiom — "reading the key from the database" not "the row read"; "overwritten with zeros" not "zeroized"; (b) internal identifiers the reader has no way to know — "reads from the PRVB to populate fooBarBaz" is opaque if PRVB and fooBarBaz have not been introduced. Define on first use or replace with what the thing does in plain English.
3. **No implementation verbs in prose.** "store the result in the in-memory cache" not "publish it"; "check the cache" not "peek the cache".
4. **Define subsystem-specific terms on first use.** A crypto term like DEK is expanded "DEK (the symmetric key used to encrypt secrets at rest)" the first time it appears. Internal markers and identifiers are subsystem-specific too: `REVIEW_COMMON` (the shared block of review-framework text interpolated into review specialist skills), `SHARED_SKILLS` (the array of skill names the loader admits), `pg_advisory_lock` (a Postgres advisory lock: a cross-process mutex backed by the database). General engineering vocabulary (mutex, queue, transaction, module, constants) needs no expansion. After the first definition, use the term freely. Definitions go in the first teaching section, not SYNOPSIS.
5. **Analogies for complex behaviors.** When a flow is non-obvious, scale-shape, or state-machine-heavy, anchor it to something the reader already knows: "this is like a checkout line where each worker holds a numbered ticket; a worker can only be served once the cashier before them has finished". Use one analogy per concept; do not extend analogies past where they hold.
6. **Conclusion-first when claiming a behavior.** "There is a circular wait in the rotator: <explanation>" not "<explanation>. That is a circular wait." Bottom line in the lead sentence, then the evidence.
7. **Plain ASCII only.** No smart quotes, smart apostrophes, em dashes, en dashes, ellipsis glyphs, or arrow glyphs. Use plain hyphens (sparingly); semicolons are often better.
8. **No design-narration, no authoring-sequence.** "The change moves the lock acquisition inside the loop" not "this PR first moves the lock, then in the next commit ...". Describe the change as it stands.
9. **No buzzwordy abstractions.** If a phrase sounds like it is trying to sound smart, replace it with concrete nouns. "identity contract" -> "the struct field that identifies the owner".
10. **No loaded language without reason.** Prefer allowlist/blocklist, primary/replica. Use the repo's established name when one exists.

## Emphasis for scanning: bold and italics

Bold and italicize the "save points": the phrases that carry meaning. A reader who skims *only* the bold and italic fragments should get the shape of the walkthrough.

- **Bold:** phrases that name the change or the mechanism (components, states, thresholds, behaviors). The "what".
- **Italicize:** phrases that orient to significance (the conclusion a paragraph is building toward, the outcome that makes a touch point matter). At most one per paragraph. The "why it matters".
- Do not bold or italicize: history, hazard detail, justification, connective tissue.
- Never bold a whole sentence or bullet.
- A phrase may be both bold and italic when it is both a change-naming noun and a paragraph's load-bearing insight (e.g. **_circular wait_**). Use sparingly.

## Synoptic check

Read only your bold and italic fragments top-to-bottom. If that reading does not convey the shape of the change, you bolded the wrong words or your prose is padding around them.

## Output

Default: render the walkthrough as your chat reply. Use markdown. Put each narrative paragraph on one physical line so it renders cleanly in the TUI.

On request ("save this", "write it to a file", "put it in docs"): write the markdown to a workspace file. Choose the path with the user when the obvious one (e.g. `docs/walkthroughs/<range>.md` under the repo, or a scratch path outside the repo) is ambiguous. Do not write to a file unless asked; do not litter the worktree.

## What this skill is NOT

- It is not a PR description (that is `thatch-pr-description`). The audience here is the user, not an external reviewer; the goal is teaching the code in depth, not orienting someone to a diff.
- It is not a code review. Do not flag issues or evaluate quality. That is the review specialist skills' job.
- It is not a project context brief (that is `thatch-review-context`). Do not pull tickets, prior reviews, or deferred-work registers. The walkthrough teaches code mechanics using only light commit-message intent.
- It is not a pre-change investigation (that is `thatch-code-archaeology`). That skill investigates code before making changes, surfacing skeletons, hidden assumptions, and sibling-feature dependencies. The output here is a human-readable teaching unit for a specific diff, not an investigation report.
- It is not a memory writer. Do not call `thatch_memory_remember`. If you discover durable facts, note them in the walkthrough's Notes; the session-reflection or fact-extractor skills persist them later.

## Worked example (one-workflow excerpt)

    # Walkthrough: Narrow the rotation advisory lock to DB writes only

    ## SYNOPSIS
    The change moves the **rotation advisory lock** inside the rotation batch loop, releasing it across **KMS I/O** so concurrent rotations from unrelated tenants no longer stall.

    ## Intent
    Commit messages frame this as unblocking multi-tenant rotations held back by a single shared lock.

    ## Workflow: secret rotation batch

    ### What it does today

    The rotator processes batches of keys that need re-encryption. It exists because keys must be rotated periodically to limit blast radius if any one key is compromised.

    The flow lives in `src/rotate/batch.ts`. The rotator calls **`pg_advisory_lock`** (a Postgres advisory lock: a cross-process mutex backed by the database) at the top of `rotateBatch` (`src/rotate/batch.ts:75`), then loops over every key in the batch. The **advisory lock** is held for the whole loop, including the KMS network calls. This is like a single cashier that hands out numbered tickets to every waiting worker, but then refuses to call the next worker's number until the current worker has walked across the store to fetch their own parcel. Every other worker (here, every other tenant's rotation) waits on the parcel walk to finish.

    The workflow's stages are:

    1. **Acquire advisory lock** at the top of the batch (`src/rotate/batch.ts:75`).
    2. **Read key** from the database for the next key in the batch.
    3. **Call KMS** (the cloud key-management service) to encrypt the key material over the network.
    4. **Write ciphertext** back to the database.
    5. **Advance cursor** so a crash can resume from the right place.
    6. **Release advisory lock** at the end of the batch.

    ### How this change modifies it

    1. **Acquire advisory lock**
       - **changed**: the acquire moves inside the loop (`src/rotate/batch.ts:88`), wrapping only steps 2 and 4.
    2. **Read key**
    3. **Call KMS**
       - **changed**: the KMS call (`src/rotate/batch.ts:104`) now runs outside the lock. The call itself is the same; only its lock context changes.
    4. **Write ciphertext**
    5. **Advance cursor**
    6. **Release advisory lock**
       - **changed**: the release now happens at the end of each iteration, not at the end of the batch.

    The change does **_unblock unrelated tenants_**: their rotations no longer wait on a long KMS round trip they do not share.