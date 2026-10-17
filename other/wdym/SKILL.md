---
name: wdym
description: "Decode this session's agent output for the supervising user — prose conclusions, raw tool output (logs, diffs, stack traces, query results), or subagent reports — grounded in the session's own evidence. Trigger on self-directed comprehension or verification asks with no named audience: 'wdym', 'what do you mean', 'I don't follow', 'I don't understand', 'what just happened', 'what does this output mean', 'walk me through what you did', mid-task 'what is X', 'why this way', 'how did you verify', 'prove it'. Also 'wdym debrief' for an end-of-task comprehension pass. Do NOT trigger when an audience is named ('explain to my manager', 'ELI5 for my wife' — that is the eli5 skill) or for pure visual requests (show-me)."
user-invocable: true
---

# WDYM — What Do You Mean

Re-explain a stretch of this session's agent work to the person supervising it. The source
material is the session itself: explain what actually happened here, never the general case.

## Step 0: Load the profile

```bash
source "${CLAUDE_PLUGIN_ROOT}/skills/common/get_kb_path.sh" && KB_PATH=$(get_kb_path)
cat "$KB_PATH/rules/comprehension-profile.md"
```

The profile carries the person's calibration that is not already in their always-on
instructions — register, analogy policy, native formats, daily-stack anchors, known confusion
clusters — and overrides the generic defaults below. If the file is missing, use the defaults
and offer once to compile a profile from the knowledge bank's reflections.

## Calibration (generic defaults; the profile overrides)

- Peer register for a working engineer. Never a child's register.
- Prose at "80% of the way to ASD-STE100": short sentences, active voice, one term per
  concept, one idea per sentence. Soften rather than follow the spec strictly — strict STE
  measurably drops facts.
- One brief analogy may open; the in-context example is mandatory: the actual file, log line,
  or command from this session. An analogy without the in-context example is a non-answer.
- Anything with layers, roles, or directions gets a 2-axis table or a decision tree, not prose.
- Close substantial explanations with a trigger list: "you'll know X applies when …".

## The ladder

Follow-ups escalate predictably. Answer the rungs that apply, and never leave the NEXT rung
unaddressed — it is the question you will be asked anyway:

1. What changed?
2. Where does it come from? (file, config, upstream system)
3. What is X? (term, acronym — define once, use it consistently after)
4. Why this way? (the alternative considered, and why not)
5. Prove it. (the verification evidence)

## Format escalation

Start at rung 1; climb only while the point is not landing:

1. **Prose** — 80%-STE, calibrated as above.
2. **Diagram** — when the subject has layers, roles, directions, or flow. After drawing,
   restate every edge as a checkable sentence; a missing arrow silently claims "no dependency".
3. **Interactive HTML** — one focused page, only when a static diagram cannot carry it (state
   spaces, before/after comparisons, things worth poking at). Reuse the show-me grammar.

Explainer videos are out of scope.

## Verification posture

Clarity must not outrun truth: a wrong claim in a clean diagram is MORE convincing, not less.

- Every claim about what happened cites this session's evidence: `file:line`, the actual log
  line, the command and its output.
- Mark **verified** (evidence is in the session) vs **inferred** (reasoning, not yet checked)
  explicitly.
- If a verification gap exists, say so plainly — the "prove it" rung exists because gaps hide.

## Learning loop

When the person's confusion is new, or a known cluster repeats, append one dated line to the
profile's `## Inbox` section:

```
- YYYY-MM-DD: confused by <X> in <context>; <what explanation landed>
```

On "recompile my profile": fold the Inbox and recent reflections into the profile body, then
empty the Inbox.

## Promotion

After a substantial explanation that resolved real confusion, offer once — never auto-write —
to promote it to a knowledge-bank concept doc, preserving the analogy under a
`## The Analogy (from the session's ELI5)` heading. Use the kb-ingest workflow.

## Debrief mode

`wdym debrief` (or asked at task end): walk the ladder over the whole task — what changed,
where it came from, new terms, why this shape, and the verification evidence — pre-answering
the questions the person would otherwise ask one by one.

## Boundaries

- A named audience ("explain this to my manager") → the eli5 skill, not this one.
- A standalone visual with no comprehension question → show-me.
- "How did we handle X before" / service documentation → knowledge-bank-lookup.
- Deliberate multi-session study of a topic → teach.
