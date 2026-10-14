---
name: code-review
description: Review the changes since a fixed point (commit, branch, tag, or merge-base) along two axes — repo Standards and the originating Kairos item's Spec — and post the record back to the item. Use when the user wants to review a branch, a PR, or work-in-progress changes, or asks to "review since X".
---

Two-axis review of the diff between `HEAD` and a fixed point the user supplies:

- **Standards** — does the code conform to this repo's documented coding standards?
- **Spec** — does the code faithfully implement the originating Kairos item's acceptance criteria?

Both axes run as **parallel sub-agents** so they don't pollute each other's context; this skill aggregates their findings and posts a review record back to the Kairos item. Kairos is reached only through its MCP tools (`get_item`, `append_note`) — the sub-agents have no Kairos access, so paste content into their prompts, never short codes alone.

## Process

### 1. Pin the fixed point

Whatever the user said is the fixed point — a commit SHA, branch name, tag, `main`, `HEAD~5`, etc. If they didn't specify one, ask for it.

Capture the diff command once: `git diff <fixed-point>...HEAD` (three-dot, so the comparison is against the merge-base). Also note the list of commits via `git log <fixed-point>..HEAD --oneline`.

Before going further, confirm the fixed point resolves (`git rev-parse <fixed-point>`) and the diff is non-empty. A bad ref or empty diff should fail here — not inside two parallel sub-agents.

### 2. Identify the originating Kairos item

Look for the item the change implements, in this order:

1. A short code the user passed as an argument (e.g. `KAIROS-T-0123`).
2. Short codes in the commit messages or the branch name (they follow the `ORG-<letter>-<number>` shape).
3. The session's active items (SessionStart context, or `my_boards` → `board_items` on your delivery board) — use one only when it unambiguously matches the change; otherwise treat it as a guess to confirm with the user.
4. If nothing surfaces, ask the user. If they say there is no originating item, skip the **Spec** sub-agent (note it in the final report) — step 6 carries its own guard.

Fetch the item with `get_item <short-code>` and extract its acceptance criteria — plus the objective and any requirements sections if the criteria are thin. This pasted content is the spec the Spec sub-agent reviews against.

**Repository check (COLLIERY-A-0023).** `get_item` prints the item's `repository: <slug> (owner: <team>)`; compare the slug with this checkout (the session's `repository`, or `git remote get-url origin` matched via `list_repositories` / `GET /api/repositories?forge=&name=`). The owner can be a different team from the team of the item; that is not a finding. A mismatch of the slug is a finding in its own right in the final report: the change implements a task that links to a different repository. Either the link is wrong (`set_repository` corrects it), or the work is in the wrong codebase. An item with no repository gets a note that recommends the link.

### 3. Identify the standards sources

Anything in the repo that documents how code should be written, such as `CODING_STANDARDS.md`, `CONTRIBUTING.md`, or `CLAUDE.md`. Check the repo root and `docs/` for those names plus any markdown whose title claims coding conventions; this step is done when the list of standards files to hand the Standards sub-agent is written down — an empty list is a valid outcome (the baseline below still applies).

On top of whatever the repo documents, the Standards axis always carries the **smell baseline** below — a fixed set of Fowler code smells (_Refactoring_, ch.3) that applies even when a repo documents nothing. Two rules bind it:

- **The repo overrides.** A documented repo standard always wins; where it endorses something the baseline would flag, suppress the smell.
- **Always a judgement call.** Each smell is a labelled heuristic ("possible Feature Envy"), never a hard violation — and, like any standard here, skip anything tooling already enforces.

Each smell reads *what it is* → *how to fix*; match it against the diff:

- **Mysterious Name** — a function, variable, or type whose name doesn't reveal what it does or holds. → rename it; if no honest name comes, the design's murky.
- **Duplicated Code** — the same logic shape appears in more than one hunk or file in the change. → extract the shared shape, call it from both.
- **Feature Envy** — a method that reaches into another object's data more than its own. → move the method onto the data it envies.
- **Data Clumps** — the same few fields or params keep travelling together (a type wanting to be born). → bundle them into one type, pass that.
- **Primitive Obsession** — a primitive or string standing in for a domain concept that deserves its own type. → give the concept its own small type.
- **Repeated Switches** — the same `switch`/`if`-cascade on the same type recurs across the change. → replace with polymorphism, or one map both sites share.
- **Shotgun Surgery** — one logical change forces scattered edits across many files in the diff. → gather what changes together into one module.
- **Divergent Change** — one file or module is edited for several unrelated reasons. → split so each module changes for one reason.
- **Speculative Generality** — abstraction, parameters, or hooks added for needs the acceptance criteria don't have. → delete it; inline back until a real need shows.
- **Message Chains** — long `a.b().c().d()` navigation the caller shouldn't depend on. → hide the walk behind one method on the first object.
- **Middle Man** — a class or function that mostly just delegates onward. → cut it, call the real target direct.
- **Refused Bequest** — a subclass or implementer that ignores or overrides most of what it inherits. → drop the inheritance, use composition.

### 4. Spawn both sub-agents in parallel

Send a single message with two `Agent` tool calls. Use the `general-purpose` subagent for both.

**Standards sub-agent prompt** — include:

- The full diff command and commit list.
- The list of standards-source files you found in step 3, **plus the smell baseline from step 3 — the twelve smells and their two binding rules — pasted in full**; the sub-agent has no other access to it.
- The brief: "Report — per file/hunk where relevant — (a) every place the diff violates a documented standard: cite the standard (file + the rule); and (b) any baseline smell you spot: name it and quote the hunk. Distinguish hard violations from judgement calls — documented-standard breaches can be hard, but baseline smells are always judgement calls, and a documented repo standard overrides the baseline. Skip anything tooling enforces. Under 400 words."

**Spec sub-agent prompt** — include:

- The diff command and commit list.
- The item's short code and title, and its acceptance criteria (and objective/requirements) pasted in full from step 2.
- The brief: "Report: (a) acceptance criteria that are unmet or partially met by the diff; (b) behaviour in the diff the item didn't ask for (scope creep); (c) criteria that look implemented but where the implementation looks wrong. Quote the criterion for each finding. Under 400 words."

### 5. Aggregate

Present the two reports under `## Standards` and `## Spec` headings, verbatim or lightly cleaned, then end with a one-line summary per axis: its finding count and its worst issue (if any). Keep the axes separate end to end — a change can follow every standard yet implement the wrong thing, or do exactly what the item asked while breaking the repo's conventions — so merging, reranking, or picking a single winner across axes lets one axis mask the other.

### 6. Post the review record

Skip this step when no originating item was found. Otherwise append a structured record to the item with `append_note`, so the review outlives this conversation:

```markdown
### Code review — <date> (diff vs <fixed-point>)
- Standards: <N> findings — worst: <one line, or "none">
- Spec: <M> findings — worst: <one line, or "none">
- <one bullet per significant finding, prefixed [standards] or [spec]>
```

`append_note` puts the record at the end of the item, under a heading with the date and your name, in one call: no version and no anchor text. Keep the record compact: findings in full live in the conversation; the item carries the durable summary.
