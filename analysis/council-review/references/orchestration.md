# Orchestration - which skill to call, and when

This skill is the conductor. The gates and seats decide *what evidence is missing*;
the skills below *go get it*. The rule of thumb: invoke a supporting skill only
when a specific gate or seat needs evidence you don't already have. Don't run them
reflexively - each one costs context and time, and a clean gate needs no help.

## Routing table

| Trigger (a gate/seat needs...) | Skill to invoke | What it returns to the review |
|---|---|---|
| Novelty / "has this been done" / prior-art map (Legolas, Gate 6) | `literature-review` | Screened sources, synthesis, novelty assessment, citation-support check |
| Broad web search beyond academic lit (Legolas) | `deep-research` | Cited multi-source report with attribution |
| Biomedical claim, MeSH terms, PMID/citation verification (Legolas, Aragorn) | `pubmed-database` | Verified PubMed records, MeSH-precise hits, citation confirmation |
| General scholarly-writing quality: structure, argument rigor, framing (Boromir, Elrond) | `scholar-evaluation` | Structured scholarly critique to fold into findings |
| Recompute / sanity-check the actual code+results in artifact mode (Aragorn, Gandalf, Elrond) | `verification-loop` | Re-run numbers, reproducibility check, discrepancy report |
| Capture the finished review into the knowledge base / graph | `knowledge-ops` or `graphify` | Persisted review node, linked to the project |
| Non in-silico empirical work (clinical/biomedical/observational/meta-analysis) | consult `references/domain-adaptation.md` directly | Reporting-standard mapping (CONSORT/STROBE/PRISMA/ARRIVE) onto the gate ladder |

## Sequencing within a review

1. **Read first, orchestrate second.** Establish mode, extract claims, build the
   Claim Ledger, and walk the gates on the evidence already in front of you.
   Note where a gate is *blocked for lack of external evidence* rather than
   guessing.
2. **Batch the lookups.** When several gates need external evidence (e.g., Legolas
   needs a novelty check *and* Aragorn wants citations verified), fire the
   supporting skills together rather than serially.
3. **Verify, don't assume, in artifact mode.** If the repo is present, prefer
   `verification-loop` to actually re-run a headline number over trusting the
   prose. A recomputed number that disagrees with the text is one of the strongest
   findings a review can produce.
4. **Fold results back into the gate ladder.** Every orchestrated result becomes a
   line in the Evidence log and updates a gate's PASS/FAIL with a concrete number
   or citation.

## When NOT to orchestrate

- The work is a short proposal with no code and no empirical claims yet - the gate
  ladder runs on reasoning alone; literature lookups may still help Legolas, but
  `verification-loop` has nothing to verify.
- The user explicitly wants a *fast* read ("quick gut check, don't go research
  it") - run the gates and seats from what's present and say which gates you left
  evidence-blocked.
- You already have the evidence in context (the user pasted the prior-art, or the
  results were recomputed earlier this session). Re-running a skill to confirm what
  you already know is wasted motion.

## Note on subagents

If supporting skills are run via subagents, remember the parent rule for this
environment: spawn agents only when the user has asked for that depth of work. For
a normal review, invoking the supporting skills inline (reading their guidance and
executing) is usually the right call. Reserve fan-out subagents for when the user
explicitly wants an exhaustive, multi-front audit.
