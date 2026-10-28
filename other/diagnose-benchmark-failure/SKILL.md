---
name: diagnose-benchmark-failure
description: >-
  Use when a judged benchmark or acceptance scenario fails and you need the
  cause before editing. Reads the judge's rendering, the raw transcript, the
  primitive the agent saw and the scenario, then reports a classified diagnosis
  without fixing.
argument-hint: 'scenario id, or the path of the failed run directory'
effort: medium
---

# Diagnose Benchmark Failure

## Why this skill exists

When a scenario fails, the natural reflex is to edit the primitive and re-run.
That is guessing. A judged run leaves four artefacts behind — the judge's
rendering, the raw transcript the agent's CLI wrote for itself, the snapshot of
the primitive the agent read, and the scenario definition — and together they
carry the actual chain of cause and effect: what the agent saw, what it did,
what it emitted, what the judge measured. This skill enforces an evidence-first
diagnosis so each iteration moves on facts, not hopes.

Harnesses differ. Names and paths in this file are examples; the four artefact
kinds are the constant. Match by kind, never by file name.

## Rules

<rules>
1. **Evidence before hypothesis**: you MUST read all four artefacts — the
   judge's rendering, the raw agent transcript, the snapshot of the primitive
   the failing agent read, and the scenario definition — BEFORE you state any
   cause or propose any fix. If you propose a cause without quoting from these
   files, the diagnosis is invalid.
2. **No fixes**: this skill produces a *report*. It MUST NOT edit the
   primitive, the scenario, or any other source file. Edits happen in the next
   step, owned by whoever called this skill.
3. **Quote, don't paraphrase**: every claim in the report must cite a quoted
   line (or line-range) from one of the four artefacts, plus the file path. A
   transcript citation is a quoted line of the transcript or a tool-call count
   produced by the command in step 3.
4. **Fail closed on a missing KIND, not on a missing NAME**: an artefact that
   exists under a name you did not expect is not missing. Search for each kind
   before concluding anything. Only when a kind is genuinely absent do you
   STOP and report the gap, naming every path you searched; do not proceed
   with partial data.
5. **The transcript beats the judge's rendering**: the rendering is the judge's
   summary of the session; the transcript is ground truth. Where the two
   disagree, the transcript wins. A claim the failing agent made about its own
   environment ("no subagent tool here", "parallel execution is unavailable",
   "the file does not exist") is a hypothesis to test against the tool-call
   histogram, never a finding: a tool the transcript shows invoked was
   available, whatever the agent said afterwards. "Cannot" and "did not" are
   different failures with different fixes.
</rules>

## Inputs

- A scenario ID, or the path of the run directory.
  Inferred from the user prompt or from the most recent failure in the
  harness's output.

## Step-by-step

<step_by_step>

1. **Locate the run and its four artefacts**
   - If this project ships an addendum that states its own layout — a
     project-level skill, or a section of the project instructions naming the
     run directory and the artefact file names — read it first and use its
     paths. It saves the search and it is authoritative where it applies.
   - Otherwise search. Find the directory holding the run for this scenario
     (usually the most recently modified one whose path carries the scenario
     ID), then identify inside it:
     - **(a) the judge's rendering** — a text or Markdown file holding the
       prompt the agent received, a log of the session, and the file diffs.
     - **(b) the raw transcript** — the JSON-lines file the sandboxed CLI
       wrote for itself: `find <run-dir> -name '*.jsonl'`.
     - **(c) the primitive snapshot** — the copy of the failing primitive
       inside the run's workspace, under the IDE's config directory
       (`.claude/skills/`, `.codex/skills/`, `.cursor/skills/`,
       `.opencode/skills/`).
     - **(d) the scenario definition** — the source file declaring the
       prompt, the simulated user and the checklist.
   - A run may hold several attempts (`run-1`, `run-2`, `attempt-1`).
     Diagnose each failed attempt, not only the first.
   - A kind you cannot find after searching → fail closed (rule 4).

2. **Read the judge's rendering end to end**
   - Find its three parts, whatever they are labelled: the prompt the agent
     received, the log of the session, the diffs of the files it changed.
   - From the session log, extract the **last assistant turn** the user would
     have seen. This is the agent's actual emitted output.
   - Copy the prompt verbatim.
   - Note any tool calls the rendering shows. Treat this list as provisional:
     a rendering can omit calls, and step 3 replaces it with the count from
     the transcript.

3. **Read the raw agent transcript**
   - Print the tool-call histogram BEFORE forming any hypothesis. Two common
     CLI formats:
     - codex rollout: `jq -r 'select(.type=="response_item") | .payload | select(.type=="function_call" or .type=="custom_tool_call") | .name' <file> | sort | uniq -c | sort -rn`
       (arguments are in `.payload.arguments` / `.payload.input`; the agent's
       own text is in `response_item` lines of type `message` with role
       `assistant`, its reasoning in lines of type `reasoning`).
     - claude transcript: `jq -r 'select(.message.content|type=="array") | .message.content[] | select(.type=="tool_use") | .name' <file> | sort | uniq -c | sort -rn`
       (the agent's own text and thinking are `assistant` lines whose content
       blocks are of type `text` / `thinking`).
     Another CLI needs another selector; read one line of the file and write
     the equivalent query rather than skipping the histogram.
   - Copy the histogram into the report verbatim. Then locate the decisive
     call — the invocation, or the absence of one, that the failing checklist
     item is about — and quote the agent's own text or reasoning around it:
     that is where the agent explains its choice to itself, and that is what
     the judge's rendering never shows.
   - Cross-check every capability claim in the session log against the
     histogram (rule 5). Record each as "claimed X; transcript shows Y".

4. **Read the scenario definition**
   - Extract: the prompt given to the agent, the simulated user's persona, and
     the checklist items with their ids, descriptions and critical flags.
   - Also extract whatever the harness lets a scenario stage before the run:
     its setup step, its template variables, whether the run was interactive.

5. **Read the primitive — BOTH copies, side by side**

   There are two different copies of the same primitive, in two different
   locations. You MUST read both and compare them. Confusing them leads to the
   wrong classification.

   - **(a) The failing agent's view**: the snapshot inside the run's
     workspace. This is the static copy the failing agent read. Read it first.
   - **(b) The current source**: the file in the project tree that the next
     edit would change. It may differ from (a).

   Do NOT read the project's own installed copy — the one the IDE loads for
   your session — and call that the snapshot. It is the current source under
   another path, and it tells you nothing about what the failing agent saw.

   After reading both, diff (a) vs (b):
   - Identical → the failure cannot be a stale-copy issue; eliminate
     STALE-SKILL-IN-SANDBOX from candidates.
   - Significantly different → potential STALE-SKILL-IN-SANDBOX; verify by
     correlating the diff with the failure mode.

   The classification depends on what (a) said vs. what the agent actually
   emitted — not on what (b) currently says.

6. **Re-derive the verdict**
   - Which checklist items failed and why is usually in the harness's output,
     not in the judge's rendering. If you don't have it, re-run the scenario
     with the harness's cache disabled and capture its output. Otherwise,
     check each checklist description against the agent's last turn from
     step 2 and judge yourself before continuing — this catches LLM-judge
     calibration drift.

7. **Match symptoms to the failure-mode taxonomy** (next section). Pick the
   most likely mode based on the quoted evidence. If two modes fit equally,
   list both; do not collapse them.

8. **Decide whether an interview is the next evidence step**
   - The transcript shows what the agent DID; only the agent can say which
     words it justified the act with, and those are the words a fix would
     edit. So when the fix-direction you are about to propose is a change to
     the primitive's wording (a sentence to add, tighten, or remove), the
     report MUST name resuming the failed session and asking it why as the
     next evidence step, before any edit — and give the command for the run's
     CLI. The session's home directory and working directory are the ones the
     run used, both preserved in the run directory:
     - codex: `cd <run workspace> && CODEX_HOME=<run home>/.codex codex exec resume <uuid> "<question>"`
       (`<uuid>` is the tail of the rollout filename; open the question with
       "Do not invoke any skill; answer from memory").
     - claude: `cd <run workspace> && HOME=<run home> claude -p --resume <uuid> "<question>"`
       (`<uuid>` is the transcript filename without its extension).
     Resolve a symlinked run directory with `readlink` before using it as a
     path. The workspace outlives the run, so the session can be resumed in
     place.
   - Draft the question neutrally: describe the situation without accusing;
     ask what made the chosen path better than the alternative, which phrase
     in the rule left room for it, and what the rule would have had to say.
     Say it is to be asked of EVERY failed run of the scenario — agreement
     across runs is what separates a defect in the text from one agent's
     rationalisation.
   - When the fix-direction is not a wording change (a harness defect, a stale
     snapshot, a primitive that was never installed), say so and skip the
     interview.

9. **Write the diagnostic report** (template below). Every claim cites a
   quoted line from step 2/3/4/5.

</step_by_step>
## Failure-mode taxonomy

A symptom-to-cause map. Use the *symptom* column to match what you observed;
the *cause* column gives the most likely root cause; the *fix-direction*
column points the next iteration at a real lever, not a guess. **Do not invent
new modes** unless the evidence rules out every one listed.

- **MD-PRIOR-BULLETS** (markdown-prior-wins-over-instruction)
  - Symptom: the primitive says options must be numbered (`1.`, `2.`, …); the
    agent emits bulleted dashes (`- **X** —`) for option lists with rich
    descriptions.
  - Cause: the model's training prior on bulleted-options-with-descriptions
    overrides plain-prose MUST instructions in the primitive's context.
  - Fix-direction: scope the requirement down to what is enforceable through
    the primitive's text alone, OR add a runtime mechanism (a helper script
    the agent invokes, a post-process hook). Adding more imperative prose has
    been empirically rejected for this mode.

- **HEADING-INSTEAD-OF-ITEM**
  - Symptom: the primitive says the question must be a numbered list item; the
    agent emits `### Variant A`, `### Variant B`, or `**1. Title**` (bold
    heading).
  - Cause: the instruction was read but not internalised at format time; the
    agent reverts to its default for "labelled chunks of related content".
  - Fix-direction: add an explicit anti-pattern example showing that
    `### Variant A` is wrong; demonstrate the correct shape with the EXACT
    surface form expected.

- **STALE-SKILL-IN-SANDBOX**
  - Symptom: the agent's behaviour matches an older version of the primitive;
    the snapshot (c) diffs against the current source.
  - Cause: the harness reused a cached verdict for a scenario whose primitive
    was edited after the cached run, or the cache was not disabled on a quick
    re-run.
  - Fix-direction: re-run with the harness's cache disabled. If the issue
    persists, compare what the cache key covers against what actually changed.

- **SKILL-NOT-MOUNTED**
  - Symptom: the agent exits successfully but took zero steps, or the judge
    reports "Unknown skill" / the agent never invokes the primitive.
  - Cause: the harness did not copy the primitive into the run's workspace
    config directory — most often the scenario names a primitive that does not
    exist, or the set the harness copied does not include it.
  - Fix-direction: fix the harness or the scenario's primitive name, NOT the
    primitive's text.

- **COMPOSITE-DELEGATION-BYPASS**
  - Symptom: a composite primitive (one that inlines the work of several
    others) was invoked, but the session log shows an early delegation call
    re-entering one of the inlined sources, bypassing the composite's gate.
  - Cause: the composite's frontmatter description names the source
    primitives, or its body lacks a "no-delegation" rule.
  - Fix-direction: rename the description so it carries no source names, add
    the no-delegation rule, harden the verdict gate. Follow the project's own
    composite-authoring guidance where it has one.

- **PERSONA-MISMATCH**
  - Symptom: the agent asks one question; the simulated user answers something
    the agent did not ask. The session log shows a reply that does not fit —
    whatever marker the harness uses for simulated-user input.
  - Cause: the persona was scripted for an older version of the primitive, or
    for a different question structure.
  - Fix-direction: align the persona with the primitive's current flow — but
    ONLY after confirming the primitive itself is correct. Persona changes
    that smuggle in the right answer ("test-fitting") are forbidden.

- **TEST-FITTING-PERSONA**
  - Symptom: the persona contains the literal target output (for example it
    dictates the exact format). The scenario passes only because the persona
    scripts the answer.
  - Cause: the scenario author worked backwards from a green run.
  - Fix-direction: rewrite the persona to be neutral. The scenario's
    diagnostic value is now suspect — review the checklist items too.

- **CAPABILITY-CLAIMED-UNAVAILABLE**
  - Symptom: the agent's own prose in the session log says a tool or
    capability was missing ("no subagent tool", "parallel execution
    unavailable") and the work was done another way; the transcript histogram
    shows that tool invoked (or installed in the workspace) in the same
    session.
  - Cause: the agent abandoned the approach — a worker's partial output looked
    slower to reconcile than redoing it, or the first call returned something
    awkward — and explained the retreat as an environment limit, licensed by a
    clause in the primitive such as "if X is unavailable, proceed with Y".
  - Fix-direction: interview the failed runs first (step 8); then close the
    clause that licensed the fallback so "unavailable" means "the tool is not
    in the tool list", not "the first attempt was inconvenient". Do NOT fix
    the harness: the capability was there.

- **CROSS-PACK-REFERENCE-MISSING**
  - Symptom: the primitive's text references another primitive by name, but
    that one is not in the workspace. The agent reads the reference and cannot
    act on it.
  - Cause: the referenced primitive ships in a group the scenario does not
    install; the harness's output usually names what it copied.
  - Fix-direction: drop the cross-reference, OR make the scenario install the
    group that carries it (rare; usually drop the reference).

## Output template

Produce exactly this structure. Every bullet ends with a `(<file>:<line-range>)`
citation.

```
# Diagnostic Report: <scenario-id>

## Run inspected
- Run dir: <path>
- Verdict line: "<paste>"
- Failed checklist items (id + critical?): <list>

## Evidence collected (paths)
- judge's rendering — <path>, <bytes>, <line count>
- raw transcript — <path>; tool-call histogram:
  <paste the histogram verbatim>
- primitive snapshot — <path>, <bytes>
- scenario definition — <path>

## Judge's rendering vs transcript
- <each capability or "I did X" claim from the session log: "claimed …; transcript shows …" with the decisive line quoted> (<transcript path>:<line>)

## Agent's last assistant turn (verbatim, ≤30 lines)
```
<paste>
```
(<judge's rendering path>:<L1>-<L2>)

## What the primitive actually said about this point (verbatim, ≤15 lines)
```
<paste>
```
(<snapshot path>:<L1>-<L2>)

## Diff: primitive snapshot vs current source
- <"identical" or summary of significant diffs with line refs>

## Failure-mode classification
- Primary: <TAXONOMY-CODE>
- Why this code: <one-sentence reason citing two of the four artefacts, the transcript among them when a capability claim is involved>
- Alternatives ruled out: <code(s) considered + the evidence that rules them out>

## Proposed next iteration
- <one-sentence fix-direction action, drawn from the taxonomy fix-direction column>
- Files to edit: <paths>
- Interview: <"required — wording change" + the resume command with this run's uuid + the question, to be asked of every failed run | "not needed — <reason>">
- Anti-actions (do NOT try): <bullets, each with the prior failure that disqualified it if applicable>

## Confidence
- <High|Medium|Low> — <one-sentence reason>
```
