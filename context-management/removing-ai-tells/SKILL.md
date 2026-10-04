---
name: removing-ai-tells
description: Identify and remove phrasing, structure, and word choices that signal AI authorship. Runs iterative passes through fresh voice-agent instances with the orchestrator acting as gatekeeper on every change. Use on a cover letter before submission, or on any prose that has to read as human-written.
argument-hint: "<file path>"
license: MIT
---

# Removing AI Tells

Iterative passes over a draft, removing the patterns that make a fatigued reader think "a machine wrote this" before they consciously work out why.

**Announce at start:** "Removing AI tells from $FILE. Working on a copy, three passes maximum."

**Arguments:**
- `$1` — path to the file to clean

**Example:**
```
/slushpile:removing-ai-tells applications/Acme/Engineering/Staff-SRE/cover_letter.txt
```

## Why This Is Separate From the Voice Agent

The voice agent writes in a person's voice. That is a different job from hunting a specific list of patterns, and combining them produces worse results at both.

A voice agent asked to "write well and also avoid these forty patterns" will trade one against the other silently. Running the passes separately means each one has a single objective, and the gatekeeper between them can see exactly what changed and why.

The gatekeeper is the point. **About a third of what a tell-hunting pass flags is doing real work in the document.** Applied without review, this process reliably makes prose worse — flatter, more uniform, and stripped of exactly the moves that made it sound like a person. That is the failure mode this skill is built around, not an edge case.

## Prerequisites

- The file to clean
- The voice agent named in `preferences.yaml` under `voice.agent` (default: `aaddrick-voice`)
- The user's voice agent definition. A habit documented there outranks this entire checklist.

## The Process

### 1. Work on a copy

Never edit the original.

```bash
cp cover_letter.txt cover_letter.v2.txt
```

Keeping the previous version is what lets you revert a rejected change precisely rather than re-editing from memory.

### 2. First pass

Send the copy to a **fresh** instance of the voice agent with the checklist below. Ask it to edit the file directly and return a summary of every change with its rationale.

The rationale is not optional. A change you cannot evaluate is a change you have to accept or revert blind.

### 3. Gatekeeper review

Read the updated file. For each change: accept or reject.

**Accept** when the change removes a real tell without losing meaning or voice.

**Reject** when:

- The flagged pattern was doing structural work — a transition between sections, a precision qualifier that changes meaning, a section opener that motivates what follows
- The removal changes the meaning or weakens the argument
- The fix introduces a different problem
- The pattern is documented in the user's voice agent as one of their own habits

Revert rejected changes directly. **Write down why you rejected each one** — the next pass gets that list and will otherwise make the same change again.

### 4. Feedback pass

Send remaining issues to a **new** voice agent instance. Always fresh, never resumed: an agent that has already defended a change will defend it again rather than re-evaluating it.

Include what needs fixing, and what the previous pass got wrong.

### 5. Stop at three passes

Iterate steps 3 and 4. Where you and the agent disagree, the gatekeeper wins.

Three passes is the ceiling. Past that the changes are churn — synonym swaps and sentence reorderings that trade one phrasing for an equivalent one. If the draft still reads as machine-written after three passes, the problem is the content, not the phrasing, and no amount of editing at this level reaches it.

### 6. Punctuation pass, if the voice calls for it

Check the user's voice agent first. If it documents an absence — no em dashes across the whole corpus, for instance — run a dedicated pass replacing every instance with a contextual rewrite: commas, periods, semicolons, colons, parentheses, or a restructured sentence.

If the voice agent shows the user does use em dashes, **skip this step entirely.** Removing a punctuation mark the person actually uses moves the prose away from their voice, which is the opposite of the objective.

### 7. Check the replacements

Verify each replacement preserves the grammatical relationship. Flag weak ones:

- A comma creating a restrictive appositive where the original was nonrestrictive
- A colon overloading a sentence that then pivots with "but"
- A period splitting a clause that depended on the one before it

Send flagged replacements back with an explanation of the relationship that needs preserving.

## The Checklist

Send this to the voice agent on each pass.

### Vocabulary

Watchlist: *landscape, paradigm, ecosystem, leverage, robust, comprehensive, crucial, facilitate, utilize, streamline, underscore, delve, harness, illuminate, bolster, tapestry, realm, beacon, cacophony.*

Also: formal register that does not match the rest of the piece, and generic language where a specific example would land harder.

### Sentence and paragraph patterns

- **Uniform sentence length.** The strongest signal there is. Human writing varies; generated writing converges on a comfortable middle.
- Repetitive structures, especially subject-verb-object in sequence
- Overly neat parallelism in consecutive sentence pairs
- Triplet structures used repeatedly as a rhetorical device. One or two in a piece is natural.
- Participial phrase endings: *"The update shipped, revealing a deeper issue."*
- Passive voice where active is more natural
- Lists where every item follows the same syntactic template
- Even, unvaried paragraph length

### Rhetorical devices

- The *"it's not X, it's Y"* reframe, and its compressed variants: *"Not X. Y."* as a two-sentence punch, *"X, not Y"* as a comma correction, *"X isn't just Y"* as a setup
- *"Not X"* as emphasis: *"Not a benchmark number."* State the positive claim.
- Staccato fragment pairs as punch. One fragment is fine; two or more back to back is a rhythm device.
- Paired beats: *"That's X. It's also Y."*
- Announcing frames: *"Here's the mechanism that makes X powerful:"*
- Dramatic openers: *"The takeaway:"*, *"The bottom line:"*

### Filler and hedging

- Balanced or hedged language where the author would commit to a position
- Transition filler: *Moreover, Furthermore, Additionally, It's worth noting*
- The whole *"it's worth [verb]-ing"* family: *worth noting, worth pausing on, worth sitting with*
- *"It's important to note that", "generally speaking", "to some extent", "from a broader perspective"*
- Authority claims: *"Let's be clear", "To be sure", "The reality is", "Make no mistake"*

### Structural redundancy

- Bookend summaries that restate the intro instead of advancing
- Sentences that summarize what was just said
- Summary openers: *Overall, In summary, In conclusion*
- *"From X to Y"* scene-setting: *"From simple scripts to full pipelines..."*
- Cross-section repetition

### Significance labeling

- *"That's the gap between policy and reality."* If the fact is strong, it lands without a label.
- *"That changes the framing considerably."* Let the fact do it.
- Vague gestural conclusions: *"says a lot about where they are"*, *"is the most telling thing about"*. Either say what it tells you or let it stand alone.

### Post-edit verification

Two errors that only appear *after* editing, and are worth a dedicated read:

- **Orphaned pronouns.** *"It builds..."* where the referent was in a sentence that got cut.
- **Broken ordering.** Text claiming A happens before B when the surrounding edits reversed them.

## Gatekeeper Principles

Not every pattern on the checklist is always wrong. Telling the two apart is the whole job.

**Real tells — remove:**

- Section openers that restate the intro
- Announcing frames before content that speaks for itself
- Significance labels after a paragraph that already landed
- Filler qualifiers
- Watchlist vocabulary where a plainer word works

**Structural work disguised as a tell — keep:**

- Transitions that connect sections. *"That's the gap these files close."* looks like a significance label and is carrying the reader between two ideas.
- Precision qualifiers that change meaning. *"structurally"* before an analogy is not filler.
- Section openers that motivate what follows.
- Colons that set up a mechanism.
- **Deliberate scope-escalation fragments.** *"$30M CAPEX. Four facilities. Seven clients."* This is a human writing move and frequently the strongest line in a cover letter. A tell-hunting pass will flag it every single time. Reject it every single time.
- **Punchy inventory lists** that read clipped on purpose. Adding the missing subject to each item kills the delivery.
- **Anything the user's voice agent documents as their habit.** The voice agent outranks this checklist without exception. Someone whose corpus is full of triplets keeps their triplets — the pattern is a tell in general and a fingerprint in their case.

## Prompt Template

```
Read [file path].

Review the entire draft for AI tells:

[paste the checklist]

Edit [file path] directly. Be surgical. Change only what needs changing, and do
not rewrite sections that already sound human. Preserve the argument structure
and every factual claim.

Do not flag or change:
[the rejections from the previous pass, with reasons]

After editing, summarize every change and why you made it.
```

## Anti-Patterns

- **Do not run this without a gatekeeper.** An unreviewed pass makes prose flatter and more uniform, which is the same direction as the problem it is solving.
- **Do not run more than three passes.** After three the changes are churn.
- **Do not resume a voice agent instance between passes.** It will defend its previous changes rather than re-evaluate them.
- **Do not run the punctuation pass without checking the voice agent first.** Removing punctuation the person genuinely uses moves the prose away from their voice.
- **Do not apply this to a resume the same way as prose.** A resume bullet is a compressed form and legitimately looks patterned. Use `/slushpile:application-builder`'s humanization step for resumes; use this for letters and prose.
- **Do not let this run on quoted material.** Anything in quotation marks, any job description text, and any product name stays verbatim.
