---
name: capturing-meeting-intelligence
version: "1.1.1"
description: >
  Connects Otter.ai (transcription), Granola (structured meeting notes), and
  Mem (knowledge storage) into a unified meeting intelligence workflow for
  Loxihart and FlashFusion. Routes each meeting to the right capture tool, runs a
  post-meeting processing protocol within 24 hours, and stores distilled
  context where it can be retrieved. Activates when the user mentions: meeting
  notes, capture this meeting, Otter, Granola, Mem, PKM, after a call, after
  a workshop, what did we decide, what was discussed, meeting recap, log this
  conversation, store this context, note from today, or any request to capture
  or retrieve context from a meeting or conversation.
---

<!-- ─────────────────────────────────────────────────────────────────────── -->
## DEPENDENCY_DECLARATION

| Tool | MCP Status | Required / Optional | Role in Workflow |
|------|------------|---------------------|-----------------|
| Otter.ai | ✅ Connected | Required — primary transcript source for long/recorded meetings (30+ min) | Live transcription, highlight capture, searchable audio archive |
| Granola | ✅ Connected | Required — primary structured notes source for 1-on-1s and short meetings | AI-structured note generation, automatic meeting summary |
| Mem | ✅ Connected | Required — distilled knowledge storage and retrieval | Semantic PKM storage; destination for three-item extract |
| Notion | ✅ Connected | Required — project and client record routing destination | Structured record-keeping per meeting type (FlashFusion clients, Loxihart, workshops) |

<!-- ─────────────────────────────────────────────────────────────────────── -->

# Meeting Intelligence Capture

Three tools, one workflow. Raw capture lives in Otter or Granola.
Distilled context lives in Mem. Nothing useful lives only in your head.

---

## Evals

**Should trigger:**
1. "I just got off a call with a FlashFusion client — help me process the notes"
2. "Pull up what we decided in the last workshop I ran at Loxihart"
3. "Start Otter for this — it's going to be a long one"

**Should NOT trigger:**
1. "Write a meeting agenda" — pre-meeting prep, not capture
2. "Draft a follow-up email from these notes" — use message_compose or drafting skill

---

## Decision Tree: Which Tool to Use

```
What kind of meeting is this?
  │
  ├─ Workshop / training / recorded call / 30+ minutes
  │    → Otter.ai (full transcript, searchable, AI summary)
  │
  ├─ 1-on-1 / project call / structured agenda / under 30 minutes
  │    → Granola (AI-structured notes, less noise than full transcript)
  │
  ├─ Quick sync / hallway conversation / ad hoc decision
  │    → Mem directly (capture the decision or context only, no transcript)
  │
  └─ Already have transcript or notes from another tool
       → Skip to Post-Processing (Section 3)
```

Full routing rationale in `references/tool-routing.md`.

---

## Section 1: Before the Meeting (2 minutes)

1. Determine tool (decision tree above)
2. Start the tool before the meeting begins — not after
3. Set a Mem reminder or calendar note: "Process [meeting name] by EOD"
4. If FlashFusion client call: open the client's Notion record in another tab

---

## Section 2: During the Meeting

**Otter.ai:** let it run. Add highlights (⭐ button) at: decisions made,
action items committed to, important context shared by the other party.
You don't need to take separate notes — highlights are enough.

**Granola:** let it run in the background. Granola structures notes
automatically. Add a quick typed note for anything the AI is likely to
miss: proper nouns, unusual terms, decisions stated informally.

**Mem:** if the meeting is a quick sync, open a Mem note immediately and
type the key point(s) as they happen. One sentence per decision or action.

---

## Section 3: Post-Processing Protocol

**Run within 24 hours.** Context degrades fast. A transcript you process
24 hours later is twice as useful as one you process a week later.

### Step 1: Review the capture

- Otter: scan the AI summary + your highlights. Are the highlights complete?
  Did Otter miss any key decisions?
- Granola: read the structured notes. Add any context Granola structured
  incorrectly or missed.

### Step 2: Extract the three things that matter

From any meeting, extract exactly three things:

```
DECISIONS: [What was decided — specific, not "discussed X"]
ACTIONS: [Who does what by when — named, not "someone will"]
CONTEXT: [Background knowledge that makes future interactions smarter]
```

If you can't identify at least one item in each category, the meeting
may not have needed to happen. Note that for your own future scheduling.

### Step 3: Store in Mem

Create or update a Mem note. Title format: `{{Meeting type}} — {{Other party}} — {{YYYY-MM-DD}}`

Paste the three-item extract. Add any relevant links (ticket, Notion page, SOW).

Do not paste the full transcript into Mem. The transcript lives in Otter/Granola.
Mem gets the distilled version — what you'd tell someone if they asked "what came out of that meeting?"

### Step 4: Route to the right Notion record

| Meeting type | Notion destination |
|---|---|
| FlashFusion client call | `FlashFusion/Clients/{{Name}}/Calls/` |
| Loxihart internal meeting | Loxihart notes space |
| AI coaching conversation | Append to AI adoption coaching log |
| Workshop (Loxihart or FlashFusion) | Session record in workshop folder |
| Strategic/personal | Personal knowledge base |

---

## Section 4: Retrieval

When you need to recall something from a past meeting:

1. **Mem first** — search by person name, topic, or date. Mem's semantic
   search handles "what did we decide about the FlashFusion pricing call"
   better than keyword search.

2. **Otter second** — if you need the verbatim quote or the exact moment
   something was said, search Otter by keyword.

3. **Granola third** — for structured notes from 1-on-1s, Granola's
   organization by meeting makes chronological review fast.

The Mem note should make Otter/Granola lookups rare. If you're frequently
going back to the raw transcript, the distillation step isn't being done.

---

## Self-Verification

After any post-processing session:
- [ ] Three-item extract (decisions, actions, context) is in Mem
- [ ] Mem note is linked to the relevant Notion record
- [ ] Action items are in whatever task system you use (not just in the note)
- [ ] Otter/Granola transcript is accessible but not the primary reference

---

<!-- ─────────────────────────────────────────────────────────────────────── -->
## FAIL_IF CONDITIONS

**Otter.ai unavailable:**
- FAIL_IF Otter.ai MCP returns auth error, connection failure, or recording cannot be started: immediately switch to Granola as the primary capture source regardless of meeting length or type; do not wait or retry Otter during an active meeting.
- DEGRADATION PATH: Granola handles recording and structure. Post-processing follows the same three-item extract protocol using Granola output. Note in the Mem entry: "Otter unavailable — full audio transcript not available for [date]; Granola structured notes are the primary source."

**Granola unavailable:**
- FAIL_IF Granola MCP returns error or structured notes cannot be retrieved after a meeting: use the Otter.ai transcript directly as the primary post-processing source; skip the structured-notes review step; proceed with raw transcript scan to extract decisions, actions, and context.
- DEGRADATION PATH: do not delay the 24-hour post-processing window waiting for Granola to recover. Extract the three-item summary from Otter directly and store in Mem. Note in the Mem entry: "Granola unavailable — distilled from raw Otter transcript; structured notes may be incomplete."

**Mem unavailable:**
- FAIL_IF Mem MCP returns auth error or write failure during the post-processing step: route the three-item extract directly to the relevant Notion record as a fallback storage destination; prepend the note with "⚠️ PENDING MEM SYNC — Mem unavailable on [date]; logged to Notion temporarily."
- DEGRADATION PATH: Notion is the temporary PKM destination. When Mem is restored, sync the Notion-logged entries to Mem, update the Mem title and tags as normal, and remove the PENDING MEM SYNC flag from the Notion entry. Note the affected date range in a Mem entry titled "PKM GAP — [date range]" so future retrieval searches know to check Notion for that window.

**Notion unavailable:**
- FAIL_IF Notion MCP returns connection error or page write failure during the routing step: do not block the Mem distillation step; the Mem note is the primary artifact and stands complete without Notion routing.
- DEGRADATION PATH: log the intended Notion routing destination as a tag directly in the Mem note body (e.g., `[[NOTION-PENDING: FlashFusion/Clients/{{Name}}/Calls/ — route when restored]]`). Create a follow-up task in your task system to complete Notion routing when the connection is restored. The meeting intelligence is fully captured; Notion routing is deferred, not skipped permanently.

<!-- ─────────────────────────────────────────────────────────────────────── -->

## CLAIMS
- Processing capture within 24 hours produces meaningfully better
  distilled notes than waiting; the meeting's context is still active
  in working memory and gaps are fillable
- Distilled Mem notes retrieve faster and more accurately than searching
  raw transcripts for the same information

## COUNTEREXAMPLE
- For legal or compliance-relevant conversations (client disputes, HR
  matters), the raw transcript is the primary artifact — do not rely
  on distillation alone; keep the full Otter recording

## CONTRADICTIONS
- "Use Granola for short meetings" conflicts with situations where a
  30-minute meeting is densely technical; use Otter for technical
  density regardless of length
