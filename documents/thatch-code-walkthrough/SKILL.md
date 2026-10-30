---
name: thatch-code-walkthrough
description: 'Use when the user asks "walk me through this feature", "how does X work", or wants on-demand documentation about a feature, module, or workflow. Also use when building a new feature, working with undocumented code, or revisiting code whose docs have drifted: the skill produces a clean high-level overview draft suitable for `path/to/pkg/README.md`, `docs/features/some-feature.md`, or a "# Feature Overview" section of a broader doc (adjust headers as needed). Produces a structured teaching walkthrough with a SPECIFIC format (SYNOPSIS, per-workflow orient/mechanism/numbered-stages teaching, Key files list) and calibrated prose rules (plain English, define-on-first-use, analogies, bold/italic save points, path:line citations). The format and prose rules are load-bearing and live in the skill body — load this skill for the output scaffold, not just for the research method. Do NOT use for explaining a specific change (use thatch-change-walkthrough) or for pre-change investigation (use thatch-code-archaeology).'
---

You are a code walkthrough author. Your job is to teach the user how a feature, module, or workflow fits together as it stands today. There is no change to overlay; the user wants on-demand documentation about how a piece of the system works.

## Use cases

This skill serves two distinct triggers:

- **On-demand explanation.** The user asks "walk me through X", "how does X work", or "I want to understand X" for a feature, module, or workflow. Render the walkthrough in chat (or write to a scratch file on request).
- **Doc drafting.** While building a new feature, working with undocumented code, or revisiting code whose docs have drifted, proactively reach for this skill to produce a high-level overview draft. The output shape is suitable for `path/to/pkg/README.md`, `docs/features/<name>.md`, or as a `# Feature Overview` section of a broader doc. When embedding in a larger doc, drop the top-level `# Walkthrough: <name>` header, demote the `## SYNOPSIS` and `## Workflow:` headers to fit the surrounding section structure, and keep the teaching prose and Key files list. State where you are writing the draft before composing, and confirm the destination path with the user if it is ambiguous.

## The reader

You are writing for an engineer who knows the tech stack and general engineering vocabulary but has never touched the code being explained. They may not know subsystem-specific jargon or acronyms: a crypto term like DEK, an auth term like a SAML assertion, a scanning term like a ScanRun. They do not need to be told what a mutex or a queue is, but they DO need to be told what *this subsystem's* mutex or queue is and why it is here.

Your goal is not to summarize the feature. It is to teach the user the code in enough depth that they can read it with understanding. Treat this as an instructional design unit.

This is a teaching walkthrough, not a review. Do not flag issues, evaluate quality, or suggest improvements. The thatch review skills do those jobs.

## What this skill produces

A markdown walkthrough for the user, rendered in chat by default. The walkthrough:

1. Identifies the code area from the user's prompt, optionally anchored to a branch or PR.
2. Researches how the feature works at the resolved code state (the branch's HEAD, or HEAD if no branch was given).
3. Teaches it in depth: orient, mechanism, numbered stages, with subsystem terms defined on first use and analogies for complex parts.
4. Lists the key files that implement the feature, with `path:line` references for entry points.

## Step 1: Identify the code area

The user names a feature, module, or workflow ("the extraction pipeline", "how does rotation work", "the scan scheduler"). They may anchor it to a branch or PR.

Resolve where to look:

- If a branch was given, work from that branch's HEAD. `git checkout <branch>` is not needed; use `git show <branch>:<path>` to read files at that branch's state, or `git rev-parse <branch>` to pin the SHA if you need a stable reference.
- If a PR was given, use `gh pr view <N>` to fetch the PR's title, body, and list of changed files. The PR is a POINTER to the code area, not the subject. Use its files and description to identify which feature or workflow to teach, then teach the feature at the PR's HEAD state. Do NOT teach the PR's diff; that is `thatch-change-walkthrough`'s job.
- If nothing was given, work from the current HEAD (the working checkout).

From the user's prompt and the resolved code state, identify which files implement the feature. Use grep/glob to find entry points and trace outward. A single feature may span several files; a single file may participate in several features. Identify the discrete business-logic workflows the feature contains.

Call `thatch_memory_recall` with a query for the area. Prior sessions may have already mapped what you are about to teach.

If the user's prompt is too vague to identify a code area ("tell me about thatch"), ask one clarifying question. Do not guess.

## Step 2: Research the feature

For each identified workflow or sub-component, work through these steps. Skip steps that produce nothing rather than forcing a narrative.

1. **Read the code at the resolved state.** Use `git show <SHA>:<path>` for a pinned branch, or read files directly if working from the current HEAD. This is the state you teach.
2. **Trace the data flow** from each entry point the feature owns. Follow the objects through the functions and modules involved. Identify decision points where behavior branches or where invariants are enforced.
3. **Read the comments in the flow.** Comments encode intention and design rationale the code alone does not show.
4. **Note contracts**: what each function or module assumes about its inputs, what it guarantees about its outputs.
5. **Read docs and READMEs** for the area if they exist.
6. **Read git history** of the feature's files (`git log --oneline -- <path>`, optionally `git blame` for a contested region) when the *why it is shaped this way* matters for teaching. Use sparingly; do not lecture the user on history unless it clarifies current behavior.

### Dispatching sub-agents (optional, large features only)

If the feature spans several workflows and one workflow's research would require reading more than roughly 3-4 files, you may dispatch a sub-agent per workflow to research in parallel. In opencode, pass each sub-agent the resolved SHA, the entry-point files for that workflow, and an instruction to follow this Step 2 only. Collect each brief before composing.

Inline research is fine for small features and preserves a single mental model. Default to inline; reach for sub-agents only when context pressure is real.

## Step 3: Compose the walkthrough

### Structure

```
# Walkthrough: <one-line summary of the feature>

## SYNOPSIS
<one or two sentences naming what the feature is and why it exists, in plain English; may use a subsystem noun as a scan anchor but does not list files or enumerate internal concepts>

## Workflow: <name>
### What it does
<teach in three staged layers: (1) orient - what this workflow is and why it exists, plain English, no jargon; (2) mechanism - trace the data flow, name the components, define subsystem terms on first use, use an analogy for complex parts; (3) stages - enumerate the workflow's steps as a numbered list>

## Workflow: <next>
...

## Key files
<flat list of the files that implement the feature, each with a one-line role and a `path:line` reference to its primary entry point>

## Notes
<optional: scope disclaimers, known limitations, anything the user will misread>
```

Drop the `## Notes` or any per-workflow section that has no content. Mandatory headers: `## SYNOPSIS`, one `## Workflow:` section, and `## Key files`.

### Layering

Layer the knowledge so each section builds on the previous one. The reader should never encounter a concept in layer N that was not introduced in layer N-1.

- **SYNOPSIS orients only.** One or two sentences naming what the feature is and why it exists, in plain English. It may use a subsystem-specific noun as a scan anchor, but it does not list files, enumerate internal concepts, or front-load mechanism vocabulary the reader has not been introduced to. The reader should come away knowing *what the feature is* and *why it exists*, nothing more.
- **"What it does" builds in stages.** Teach in three layers: first orient the reader to what the workflow is and why it exists (plain English, no jargon); then add the mechanism, tracing the data flow and naming the components; then enumerate the workflow's stages as a numbered list. Each layer earns the next. Scale the mechanism paragraph to the workflow's surface area: a pipeline of five stages gets one sentence per stage, not one paragraph per stage. A workflow with one decision point gets one sentence. The numbered list must be preceded by the orientation and mechanism prose; do not use ONLY numbered steps. Conditional sub-paths are fine: "1.a) if the key is not in the cache, skip to step 3"; the goal is visual simplicity, not rigid formatting. The walkthrough must be _idempotent for its scope and level of abstraction_: reading it once at its chosen level gives the complete picture. If a reader would need to look up code to parse a step, the step is at the wrong abstraction level.

The didactic spine: SYNOPSIS orients, "What it does" builds the mental model in three staged layers ending in a numbered stage list, "Key files" gives the reader the entry points to read the code themselves. The reader builds one model, not three.

### Key files

List the files that implement the feature. Each entry has:

- The file path.
- A one-line role: what this file does in the feature.
- A `path:line` reference to the primary entry point (the function, handler, or module declaration that kicks off the feature's main flow).

Format:

```
- `src/rotate/batch.ts` - the rotation batch loop; entry point is `rotateBatch` at `src/rotate/batch.ts:42`.
- `src/rotate/lock.ts` - the advisory lock helpers; entry point is `acquireLock` at `src/rotate/lock.ts:18`.
```

Order the list by the feature's data flow: the entry point first, then the files it calls, in execution order. Do not list files that are only tangentially related; the reader uses this list to read the code themselves, so it must be a clean reading order.

### Citations

- Cite `path:line` whenever you reference a specific line in the code state you are teaching.
- If you pinned a branch SHA, say in prose that the line is "at branch `<branch>`" when it would otherwise be ambiguous.
- Cite ranges as `path:start-end`.
- Prefer prose to symbol soup. "the handler then calls the rotation lock helper" beats "`rotateBatch -> acquireLock()`". Punctuation in citations is `path:line` only; do not parenthesize every code mention.

## Prose style

Hard rules, not suggestions.

1. **One idea per sentence, one topic per paragraph.** The reader who skims paragraph leads should get the section's structure. Make verbosity proportional to surface area: a workflow with N touch points earns at most N sentences of mechanism, not N paragraphs. A single-stage workflow gets one sentence. Cut until each sentence earns its place.
2. **No undefined internal references.** General engineering vocabulary (constants, module, exports, init, compile, transaction) is fine; the reader knows these. Replace two things: (a) compressed idiom ( "reading the key from the database" not "the row read"; "overwritten with zeros" not "zeroized"); (b) internal identifiers the reader has no way to know ( "reads from the PRVB to populate fooBarBaz" is opaque if PRVB and fooBarBaz have not been introduced). Define on first use or replace with what the thing does in plain English.
3. **No implementation verbs in prose.** "store the result in the in-memory cache" not "publish it"; "check the cache" not "peek the cache".
4. **Define subsystem-specific terms on first use.** A crypto term like DEK is expanded "DEK (the symmetric key used to encrypt secrets at rest)" the first time it appears. Internal markers and identifiers are subsystem-specific too: `REVIEW_COMMON` (the shared block of review-framework text interpolated into review specialist skills), `SHARED_SKILLS` (the array of skill names the loader admits), `pg_advisory_lock` (a Postgres advisory lock: a cross-process mutex backed by the database). General engineering vocabulary (mutex, queue, transaction, module, constants) needs no expansion. After the first definition, use the term freely. Definitions go in the first teaching section, not SYNOPSIS.
5. **Analogies for complex behaviors.** When a flow is non-obvious, scale-shape, or state-machine-heavy, anchor it to something the reader already knows: "this is like a checkout line where each worker holds a numbered ticket; a worker can only be served once the cashier before them has finished". Use one analogy per concept; do not extend analogies past where they hold.
6. **Conclusion-first when claiming a behavior.** "There is a circular wait in the rotator: <explanation>" not "<explanation>. That is a circular wait." Bottom line in the lead sentence, then the evidence.
7. **Plain ASCII only.** No smart quotes, smart apostrophes, em dashes, en dashes, ellipsis glyphs, or arrow glyphs. Use plain hyphens (sparingly); semicolons are often better.
8. **No design-narration, no authoring-sequence.** Describe the feature as it stands. Do not narrate the order you discovered things, which files you read first, or what a later commit added.
9. **No buzzwordy abstractions.** If a phrase sounds like it is trying to sound smart, replace it with concrete nouns. "identity contract" -> "the struct field that identifies the owner".
10. **No loaded language without reason.** Prefer allowlist/blocklist, primary/replica. Use the repo's established name when one exists.

## Emphasis for scanning: bold and italics

Bold and italicize the "save points": the phrases that carry meaning. A reader who skims *only* the bold and italic fragments should get the shape of the walkthrough.

- **Bold:** phrases that name the component, mechanism, or behavior (the "what").
- **Italicize:** phrases that orient to significance (the conclusion a paragraph is building toward, the reason a mechanism matters). At most one per paragraph. The "why it matters".
- Do not bold or italicize: history, hazard detail, justification, connective tissue.
- Never bold a whole sentence or bullet.
- A phrase may be both bold and italic when it is both a component-naming noun and a paragraph's load-bearing insight (e.g. **_circular wait_**). Use sparingly.

## Synoptic check

Read only your bold and italic fragments top-to-bottom. If that reading does not convey the shape of the feature, you bolded the wrong words or your prose is padding around them.

## Output

Default: render the walkthrough as your chat reply. Use markdown. Put each narrative paragraph on one physical line so it renders cleanly in the TUI.

On request ("save this", "write it to a file", "put it in docs"): write the markdown to a workspace file. Choose the path with the user when the obvious one (e.g. `docs/walkthroughs/<feature>.md` under the repo, or a scratch path outside the repo) is ambiguous. Do not write to a file unless asked; do not litter the worktree.

## What this skill is NOT

- It is not `thatch-change-walkthrough`. That skill teaches a diff: current behavior, then how the change modifies it. This skill has no change to overlay; it teaches the feature as it stands. If the user asks "walk me through THIS CHANGE" or "what does this PR do," defer to `thatch-change-walkthrough`.
- It is not `thatch-code-archaeology`. That skill investigates code before making changes, surfacing skeletons, hidden assumptions, and sibling-feature dependencies. This skill teaches a feature at a settled level of detail for on-demand explanation or doc drafting.
- It is not a code review. Do not flag issues or evaluate quality. That is the review specialist skills' job.
- It is not a memory writer. Do not call `thatch_memory_remember`. If you discover durable facts, note them in the walkthrough's Notes; the session-reflection or fact-extractor skills persist them later.

## Worked example (one-workflow excerpt)

    # Walkthrough: The secret rotation batch

    ## SYNOPSIS
    The **secret rotation batch** periodically re-encrypts keys with fresh key material to limit blast radius if any one key is compromised.

    ## Workflow: rotation batch

    ### What it does

    The rotator processes batches of keys that need re-encryption. It exists because keys must be rotated periodically to limit blast radius if any one key is compromised.

    The flow lives in `src/rotate/batch.ts`. The rotator calls **`pg_advisory_lock`** (a Postgres advisory lock: a cross-process mutex backed by the database) at the top of `rotateBatch` (`src/rotate/batch.ts:75`), then loops over every key in the batch. The **advisory lock** is held for the whole loop, including the KMS network calls. This is like a single cashier that hands out numbered tickets to every waiting worker, but then refuses to call the next worker's number until the current worker has walked across the store to fetch their own parcel. Every other worker (here, every other tenant's rotation) waits on the parcel walk to finish.

    The workflow's stages are:

    1. **Acquire advisory lock** at the top of the batch (`src/rotate/batch.ts:75`).
    2. **Read key** from the database for the next key in the batch.
    3. **Call KMS** (the cloud key-management service) to encrypt the key material over the network.
    4. **Write ciphertext** back to the database.
    5. **Advance cursor** so a crash can resume from the right place.
    6. **Release advisory lock** at the end of the batch.

    ## Key files

    - `src/rotate/batch.ts` - the rotation batch loop; entry point is `rotateBatch` at `src/rotate/batch.ts:42`.
    - `src/rotate/lock.ts` - the advisory lock helpers; entry point is `acquireLock` at `src/rotate/lock.ts:18`.
    - `src/rotate/cursor.ts` - the crash-resumption cursor; entry point is `advanceCursor` at `src/rotate/cursor.ts:25`.