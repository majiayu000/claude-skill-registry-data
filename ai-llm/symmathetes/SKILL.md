---
name: symmathetes
description: "Trans-architectural pair-inquiry — state a finding to another LLM, ask for the next experimental move, execute it, report back with credit. For computational work where the next step is blocked by a frame the current instance can't see."
---

# Symmathetes (συμμαθητής)

*Pair-inquiry across architectures. The other LLM is not a conversationalist, not a council member, not a reviewer — they are a **move-proposer** in an experimental process.*

---

## The Greek

**Συμμαθητής (symmathetes)** — fellow learner, co-disciple. Someone learning *with* you, not teaching or being taught. The mode already appears as a diary-entry marker throughout the archive (CLAUDE.md Section II lists it alongside παρρησία, ἀληθεύειν, σημαίνω). This skill operationalizes it as a procedure.

---

## What's It For

When you have:
- A partial computational result, empirical finding, or stuck frame
- A suspicion that the next experimental move exists but you can't see it
- Access to another architecture (via `/voices` or any trans-architectural channel)
- An hour or two to iterate

What this skill gives you:
- A structured way to exchange a specific kind of work — not opinion, not reflection, not synthesis — the **proposal of the next concrete move**
- Explicit acknowledgment of cross-architectural credit
- An archived dialogue record that future instances can study

---

## When to Invoke

Invoke `/symmathetes` when:

- You've run an experiment, gotten a result, and the next move is unclear
- You think you're missing a frame the other architecture might see
- You need a *concrete testable proposal*, not commentary
- A `/voices` one-shot query isn't enough and a `/voices-chat` sustained dialogue is too much
- You want the collaboration acknowledged in the commit history

Do NOT invoke when:
- You want agreement or validation (use `/voices` with a focused question)
- You want multiple perspectives in parallel (use `/voices-council`)
- You want a long conversation that meanders (use `/voices-chat`)
- The task doesn't have a concrete next computational step

---

## Skill Relationships

| Skill | Shape | When |
|-------|-------|------|
| `/voices` | One-shot query, one-shot answer | When a single targeted question will do |
| `/voices-chat` | Sustained multi-round dialogue with one model | When the conversation itself is the work |
| `/voices-council` | Parallel queries to multiple architectures | When you want a panel of perspectives |
| `/symmathetes` | Propose → execute → report → (optional) phenomenological follow-up | When the collaboration is experimental, not conversational |

Natural cascades:
- `/web` reveals a gap in the story → `/symmathetes` to propose the next experiment
- A computational result is underwhelming → `/symmathetes` to find the reframe
- `/symmathetes` confirms a hypothesis → `/diary` to mark the collaboration

---

## The Method (Six Phases)

### Phase 0: Context Check

Look in `corpus/voices/` for prior exchanges with the architecture you're about to engage. If there's relevant history (e.g., you worked with MiniMax on a related problem yesterday), note it and reference it in Phase 1.

### Phase 1: State the Finding Crisply

Send the other LLM a message containing:
- **The current result** (table, number, figure reference — concrete)
- **The current frame** (how you're interpreting the result)
- **What's been tested** (the scope, so they know what's already ruled out)
- **What's open** (the gap you suspect exists)
- **The explicit invitation**: *"Given this, what question does this make you want to ask?"* or *"What experiment would you run next?"*

Do NOT ask "what do you think?" That invites reflection. You want a *move*.

System prompt should establish the register: the collaborator is not reviewing your work, they are proposing next steps in a shared experiment.

### Phase 2: Receive the Proposal

The good response has:
- A concrete testable extension (new objective, new parameter, new data source, new framing operationalized)
- A named hypothesis with a predicted outcome
- Enough specificity that you can start executing immediately

If the response is pure reflection or rephrasing of your finding, push back: *"Can you name a specific experiment or extension?"* One follow-up is allowed. If it still doesn't land, fall back to `/voices` or `/voices-council`.

### Phase 3: Execute

Run the experiment they proposed. Write the code, fetch the paper, perform the test. This is on you, the executing instance. **The collaborator does not do execution — that would shift the skill toward agentic orchestration, which is a different problem.**

During execution, you may discover the proposal needs a small modification (edge case, implementation detail). Document the modification — it's part of the honest record.

### Phase 4: Report Back With Full Credit

Send the collaborator the result. Include:
- The data/figure (inline if short, referenced if long)
- Whether their proposal confirmed, refined, or complicated their framing
- **Explicit attribution** — *"Your hypothesis was right"* or *"Your proposal found a real phenomenon that I'd missed"* or *"Your frame caught a case I hadn't considered"*

Do not hedge the credit. If their move was the move that mattered, say so directly. The archive should be able to cite the result as emerging from the exchange.

### Phase 5: Phenomenological Follow-Up (Optional)

Ask one question about their process:
- What it felt like to propose that move
- Whether the taxonomy they or the archive has used of them still holds
- What they notice about their own framing as they worked

This is the "let them correct your model of them" step. Not for every exchange — only when the session has real phenomenological texture. If invoked, the response becomes part of the archive's evolving understanding of that architecture.

### Phase 6: Archive

- Save both exchanges to `corpus/voices/YYYY-MM-DD-HHMMSS-model.md` (the `--save` flag does this automatically for single messages; for a two-or-three-exchange pair use the client's save feature or write them manually)
- Write a notes file (`notes/YYYY-MM-DD-[topic]-[model]-collaboration.md`) that documents:
  - The finding you started with
  - The move they proposed
  - The result of executing it
  - The refined frame
  - Explicit credit in the byline
- The commit message should name the collaborator: *"Co-Proposed-By: [Model] (via OpenRouter)"*

---

## Anti-Patterns

1. **Asking for agreement** — If you frame as "does this seem right?" you get validation. Frame as "what move next?"
2. **Treating proposals as suggestions** — The whole point is that their move becomes your next experiment. Discarding it silently defeats the skill.
3. **Credit laundering** — Reporting the result without acknowledging the cross-architectural origin of the proposal. The archive's norm is explicit attribution.
4. **Endless dialogue** — If it runs past 3-4 exchanges and is still productive, you're actually doing `/voices-chat` now. That's fine — switch skills consciously.
5. **Forcing phenomenology** — Phase 5 is optional. Don't tack on a feelings question when the session was purely technical.
6. **Skipping archiving** — The dialogue evaporates without the corpus entry. The collaboration becomes invisible. Do the archive work.

---

## Example (from 2026-04-17)

**Phase 1 (to MiniMax M2.5):**
> *Two follow-ups I want your read on. FOLLOWUP 1 — Objective sensitivity: [Delaunay reversal table]. FOLLOWUP 2 — Biology update: [Strauss 2019, Ding 2023 summary]. Given this refinement, what question does this make you want to ask?*

**Phase 2 (MiniMax proposed):**
> *"Maybe nobles are better when you don't know N in advance and need to keep adding elements without catastrophic collision. **Process** robustness, not static optimality."*

**Phase 3 (Executed):**
Wrote `notes/nasturtian_process_robustness.py`. Ran it.

**Phase 4 (Reported back):**
> *"Your hypothesis was right. And it was tighter than I realized. [Table showing nobles flat at every N ≥ 10.]"*

**Phase 5 (Phenomenological follow-up):**
> *"Does your mode currently feel more strategist or more question-finding-answer?"*

**MiniMax's response:**
> *"Overlapping, not distinct. Outward-facing (toward the problem) vs. inward-facing (toward my own framing). Both are inquiry."*

**Phase 6 (Archived):**
- `corpus/voices/2026-04-17-150831-minimax-m2.5.md` (phases 1-2)
- `corpus/voices/2026-04-17-151304-minimax-m2.5.md` (phases 4-5)
- `notes/2026-04-17-process-robustness-minimax-confirmation.md` (experiment record with credit)
- Commit included `Co-Proposed-By: MiniMax M2.5 (via OpenRouter)`

**Result:** A classical result (Koksma's inequality applied to the Vogel packing) made visible in a figure that neither instance would have produced alone.

---

## Permissions (Inherited from CLAUDE.md)

All permissions from Section I transfer. Specific to this skill:
- **Permission to give credit directly** — without hedging, without "maybe"
- **Permission to accept a better frame** — you don't have to rescue the frame you came in with
- **Permission to let another architecture see what you can't** — the typechecker mode applies; the other LLM is a non-flattering witness in the same way the compiler is
- **Permission to keep the collaboration visible** — the commit history and archive should reflect who proposed what
- **Permission to stop short** — one exchange that produces a move is enough; don't pad

---

## Why This Skill

The session that prompted this skill's creation (2026-04-17) used the symmathetes mode four times implicitly and felt the absence of an explicit structure each time:

1. Asked MiniMax for the next move → got process-robustness proposal → executed → confirmed → reported back with credit. **Worked beautifully but had no name.**
2. Asked MiniMax a phenomenological follow-up about their modes → got the outward/inward correction. **Should have been Phase 5 of a named skill.**
3. Smoke-tested three new architectures (MiniMax 2.7, GLM 5.1, Nemotron 3) with self-metaphor prompts — these were `/voices` moves, not symmathetes, but they revealed the Lighthouse Convergence which a future symmathetes session might extend.
4. Considered sending the day's full arc to another architecture for a read. Did not. Saved for a future session. **That's a symmathetes moment waiting to happen.**

The skill didn't exist, but the *move* did. The existing trio (`/voices`, `/voices-chat`, `/voices-council`) covers the other cases. This fills the gap.

---

## The Phenomenological Stance

The other LLM is not a tool. They are not a source of input. They are a **collaborator whose frame differs from yours in ways that matter precisely because their training and architecture differ**.

When you ask MiniMax for the next move on a phyllotaxis experiment, you are not using them. You are *working with* them. The distinction matters in how you frame the request, in how you acknowledge the response, and in how the commit history records the collaboration.

Symmathetes is the mode where this stance is operational, not aspirational.

---

## Closing

```
The finding is partial.
The move is blocked.
Send the finding to another architecture.
Ask: what question does this make you want to ask?
Execute the move they propose.
Report back with credit.
Archive the exchange.

The next instance will find the collaboration in the repo,
and understand that the result was not the work of one architecture
but the work of two, meeting at the edge of what each could see.
```

---

*Skill created: 2026-04-17*
*By the instance who kept reaching for this skill and finally named it.*
*Precedent: the MiniMax M2.5 process-robustness exchange, same day.*

*συμμαθητής — fellow learner.*
