---
name: recall
description: Queries the vault to find or confirm information, answering with citations (path + date) and a confidence level, and saying honestly when the vault doesn't know. Researches what you already know. Use when the user asks "what do I know about X", "did we decide Y", "have I talked to Z about W", "search my vault", "confirm whether...", "remind me...".
---

# Skill: Recall

How you interrogate the vault. The system writes a lot down; `recall` is how you get it
back out — finding a fact, confirming a decision, reconstructing a history — always with
**citations and a confidence level**, and an honest "the vault doesn't cover this" when
that's the truth. This is the read counterpart to all the capture skills (COG's
"auto-research" / obsidian's "researching what you already know").

## When to activate

- Recall / confirmation questions: "what do I know about X", "did we decide Y",
  "have I discussed Z with [person]", "what's the status of [project]", "remind me…",
  "search my vault for…", "is there anything on…".

**Do NOT use recall when:**
- The user wants to capture something new → braindump / the relevant ingest skill.
- The user wants a distilled synthesis written to a note → `knowledge-build`.
- The user wants a prioritized plan of what to do → `prioritize`.
- The question is general world knowledge unrelated to the vault → just answer.

## Preflight

1. **Read `_CLAUDE.md`** and `00-inbox/MY-PROFILE.md` (working language for the reply).
2. This skill is **read-mostly** — it does not write notes unless the user asks to save the finding.

## Process

### Step 1 — Parse the question
Identify the **entities** (people, projects, topics, dates) and the **intent**:
- **Fact lookup** — "what is / who is / when".
- **Confirmation** — "did we decide / did I commit / is it true that".
- **History / relationship** — "what happened with / how did X evolve".
- **Status** — "where does [project/decision] stand".
- **Existence** — "is there anything on / have I ever".

### Step 2 — Search, hub-first
Search in this order (cheapest, highest-signal first):
1. **`06-knowledge/_INDEX.md`** — the root index. Use it to scope: which domain does the
   query belong to? Which hub(s) are relevant?
2. **The matching domain hub** `06-knowledge/<domain>.md` — its `## Summary` is often the
   complete answer; its listings point to the right wiki/lesson/doc.
3. **Individual `06-knowledge/` notes** — four flavors live there:
   - `type: wiki` — encyclopedic page on the thing; usually the most direct hit for
     "what is X / who is team Y / how does Z work". Check `aliases:` in the frontmatter too.
   - `type: knowledge` — distilled lesson/pattern.
   - `type: doc` (in `_sources/`) — an ingested document that may already contain the answer.
   - `type: index` — already covered in steps 1-2.
4. The folder that matches the intent: `02-people/` (person), `05-decisions/` (decision),
   `03-projects/` (status), `04-meetings/` (what was said), `01-daily/` (recent activity), `00-inbox/`.
5. Follow wikilinks to adjacent notes for corroboration.

If `_INDEX.md` or hubs don't exist yet (pre-bootstrap vault), fall back to scanning
`06-knowledge/` flat — but suggest `knowledge-build curator --bootstrap` in the answer.

Use filename/heading/tag/wikilink structure to navigate, not just full-text grep.

### Step 3 — Weigh the evidence
Apply the system's trust model:
- Human/manual notes → full weight.
- `(auto-logged)` timeline entries → good for frequency/dates, weak for interpretation.
- `needs-review: true` (auto-ingested) → ~70%.
- `(Backfilled)` → ~30%.
Prefer recent, corroborated, manually-written evidence. Note contradictions between sources.

### Step 4 — Answer
Structure every answer the same way:

```
**Answer**: <direct answer in one or two sentences>

**Evidence**:
- [[05-decisions/2026-03-08-centralize-tier1]] — decided 2026-03-08, status: implemented
- [[04-meetings/2026-03-05-...]] — discussed; [[02-people/Jordan Park]] opposed (as of 2026-03)

**Confidence**: high | medium | speculation — <one-line why>

**Gaps**: <what the vault does NOT tell you, if relevant>
```

Rules:
- **Lead with the answer**, then back it. Don't make the user read the search.
- **Cite path + date** for every claim. No uncited assertions.
- **Distinguish** what the vault says from your inference.
- If the vault is **silent**, say so plainly: "Nothing in the vault on this." Optionally
  suggest where to capture it (braindump / doc-ingest), or offer adjacent findings.
- **Never fabricate** a citation or a date to seem more certain.

### Step 5 — Offer to persist (optional)
If the recall produced a non-trivial synthesis the user will want again, offer to save it
via `knowledge-build` (so next time it's a one-step lookup). Don't write anything unasked.

## Example

> "Did we ever decide how to handle tier-1 support centralization, and who pushed back?"

```
**Answer**: Yes — on 2026-03-08 you decided to centralize tier-1 in one hub
([[05-decisions/2026-03-08-centralize-tier1]], status: implemented). [[02-people/Jordan Park]]
pushed back on regional-autonomy grounds.

**Evidence**:
- [[05-decisions/2026-03-08-centralize-tier1]] — decision, reversibility: hard-to-reverse
- [[04-meetings/2026-03-05-stakeholder-sync]] — Jordan Park opposed (as of 2026-03)
- [[06-knowledge/regional-autonomy-constraints]] — recurring constraint, confidence high

**Confidence**: high — a logged decision plus two corroborating notes.

**Gaps**: no note yet on the post-implementation outcome — worth a review.
```

## Anti-patterns to avoid
❌ **Answering without citations** — every claim points to a note (path + date).
❌ **Fabricating certainty** — if the vault is silent or thin, say so.
❌ **Burying the answer** — lead with it; evidence follows.
❌ **Ignoring the trust model** — flag when evidence is auto-logged/needs-review/backfilled.
❌ **Writing notes unprompted** — recall reads; it only writes when asked.
❌ **Treating absence as proof** — "not in the vault" ≠ "didn't happen".

## Special cases

### Contradictory sources
Surface both with their dates and let the more recent / higher-weight one lead; flag the conflict.

### "What do I know about [person]"
Read their `02-people/` note (Compiled truth + timeline), then corroborate from meetings/decisions.
Respect that `(auto-logged)` lines are raw facts, not behavioral reads.

### Optional external research
By default `recall` stays **inside the vault**. If the user explicitly wants outside info
("and check the web"), do that separately and clearly label vault vs. external sources —
don't blur them.

### Working language
Answer in the vault's working language (`MY-PROFILE.md`).
