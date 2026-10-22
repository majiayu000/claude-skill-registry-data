---
name: learn-eval
description: "Extract a reusable pattern from this session and route it to where something reads it, or drop it. Use when saving what was learned in this session (今回の学びを残して)."
compatibility: Developed and tested on Claude Code; portable to other Agent Skills-compatible agents.
user-invocable: true
origin: shimo4228
---

# /learn-eval - Extract, Evaluate, then Save

Extract a reusable pattern from the session, gate it, and route every Save to a destination something actually reaches.

## What to Extract

Look for:

1. **Error Resolution Patterns** — root cause + fix + reusability
2. **Debugging Techniques** — non-obvious steps, tool combinations
3. **Workarounds** — library quirks, API limitations, version-specific fixes
4. **Project-Specific Patterns** — conventions, architecture decisions, integration patterns

## Process

1. Review the session for extractable patterns
2. Identify the most valuable/reusable insight

3. **Determine the destination — there is no parking lot.**

   Every Save must land somewhere that something actually routes to (ADR-0047), so pick
   one of exactly two:

   - **Absorb into an existing asset** — the pattern belongs inside a skill, rule, or
     `hooks/README.md` section that already owns the topic. Name the file and the section.
     This is the default: an addition to a reachable asset beats a new file. A skill's value
     lies in its comprehensiveness, so appending improves it — "I don't want to pollute the
     existing skill" routes the pattern to a file nothing reaches.
   - **Promote to a skill** — the pattern has its own independent trigger (a user request
     that no installed skill answers). Run skill: **skill-creator** (required by
     `rules/common/skills.md` before writing any skill).

   If neither fits, the verdict is **Drop**, not "park it somewhere for now". A note that
   nothing points at is reachable only by grep, and grep requires already knowing the
   content exists (measurement: ADR-0047).

   Global vs project placement (once a destination type is chosen): the source of truth is
   [`docs/adr/0025-global-vs-project-asset-placement.md`](https://github.com/shimo4228/claude-harness/blob/main/docs/adr/0025-global-vs-project-asset-placement.md).

4. Draft the candidate as a scratch note (the final skill shape belongs to `skill-creator`;
   `overlap_candidates.py` reads name / description / Problem / Solution / When to Use):

```markdown
# [Descriptive Pattern Name]

description: "Description in 130 characters or less"
**Context:** [Brief description of when this applies]

## Problem
[What problem this solves - be specific]

## Solution
[The pattern/technique/workaround - with code examples]

## When to Use
[Trigger conditions]
```

5. **Quality gate — checklist + holistic verdict**

   #### 5a. Mandatory checklist (verify by actually reading the files)

   **First, enumerate the overlap candidates — do not grep by hand.** The draft
   from Step 4 is still in the conversation, not on disk, so **write it to a file
   in this session's scratchpad directory with the Write tool** and pass that path:

   > Paths below start at `${CLAUDE_SKILL_DIR}`, the directory holding this SKILL.md; an agent that does not substitute the variable reads it as that directory.

   ```bash
   uv run --frozen --project "${CLAUDE_SKILL_DIR}" \
          --directory "${CLAUDE_SKILL_DIR}" \
          python scripts/overlap_candidates.py \
          --draft /path/to/scratch/learn-eval-draft.md --project "$PWD"
   ```

   Both arguments are load-bearing:

   - **Write the draft to a file; never inline it into the command.** A
     heredoc terminates on a line that matches its delimiter, and a draft is
     arbitrary session-derived prose that may contain one — the rest of the
     draft would then be read by the shell as commands, before any human gate.
     `rules/common/security.md` treats a SKILL.md as a control program for
     exactly this reason: a step that builds shell source out of untrusted text
     is an injection path, not a formatting choice.
   - **`--project "$PWD"` is required whenever `--directory` is.** `--directory`
     makes the skill directory the process cwd, so the script's default
     `--project .` would resolve to the skill's own directory and silently drop
     the invoking repo's `MEMORY.md`. `$PWD` expands before uv changes
     directory, so it still names the repo you are working in.

   Evidence mode: JSON on stdout, exit 0 however many candidates (exit 2 only when
   an input is unreadable). It enumerates; it never says "this is a duplicate".
   `skill_candidates` ranks installed skills by how much of each **description**
   the draft's terms cover (the description is what routes a future session, so a
   body match would rank a skill nothing reaches); `memory_candidates` does the
   same over MEMORY.md index lines — project **and** global — with line numbers.
   Both report `shared_terms`, so a claim of overlap is checkable.

   **Read the score, not the rank**, and read the two lists on different scales:

   - `skill_candidates` — a description carries ~30 terms, so the score spreads.
     Measured 2026-08-26 against the live 67-skill library: a draft whose
     knowledge already had a home scored **0.600** against that skill and ≤0.143
     against everything else; a genuinely new draft topped out at 0.100. Treat a
     tight cluster below ~0.2 as "no candidate", not "five near-misses". That floor
     is language-conditioned — `normalize_terms` tokenizes each CJK run into
     character bigrams (n−1 per n-character run, no stopword list) but Latin text
     into stopword-filtered whole words, and the score divides by the candidate
     description's own term count, so the same knowledge covers far more of a
     Japanese description than of an English one (measured 2026-09-15: a Japanese
     twin scored 0.605 while an English twin carrying the identical shared terms
     scored 0.079, under the floor) — so compare a score only against candidates
     written in the draft's language, and read `shared_terms` before calling an
     English pair "no candidate".
   - `memory_candidates` — an index line carries 3–8 terms, so the score is noisy
     and `shared_concepts` is the signal. **Concepts, not terms**: a Japanese
     word of n characters produces n−1 matching bigrams, so counting raw terms
     let one incidental katakana word outrank a real match. The script drops
     anything sharing a single concept; what survives is worth reading.

   **Before reading the candidates, check that the comparison actually ran.** Each
   of these means part of the corpus was never compared, and "no overlap" would be
   a false clean bill:

   - `memory_files_unreadable` non-empty, or `memory_files_read` empty while
     `memory_files_missing` is not → the memory half did not run. Name the file.
   - `skills_unscannable` non-empty → those skills were not compared at all. The
     one you cannot read is as likely to be the twin as any other.
   - `skill_candidates_total` / `memory_candidates_total` above `top_n` → the list
     was truncated; there are more candidates than you were shown.

   (An empty draft exits 2 rather than reporting no candidates, so a truncated
   Write fails loudly instead of certifying itself.)

   Then run all of the following before evaluating the draft:

   - [ ] Stated, per surviving candidate, whether it is really the same knowledge —
     quoting its `shared_terms` or the cited MEMORY.md line. "Nothing survived the
     floor and the top skill scored 0.09" is a valid answer; "I grepped" is not
   - [ ] Considered appending to an existing skill instead (Step 3, Absorb)
   - [ ] Confirmed the pattern is reusable, not a one-off fix
   - [ ] Checked the pattern against the **session's observational record** (actual tool output, errors, user corrections). Is it grounded in "what actually happened" rather than your own summary or paraphrase?

   Then, **generate and answer 3–5 draft-specific atomic yes/no questions**.
   The fixed checklist covers harness-invariant checks (duplication, reusability) but
   does not test the draft's own claims (what it states under Problem / Solution /
   When to Use), so this step fills that gap:

   - **Atomicity**: each question tests exactly one verifiable claim
   - **Refutation-oriented**: phrase questions to seek disconfirmation, not to affirm
     the draft as written. Examples: "Does the code example run as-is in the stated
     environment?" "Is the trigger condition observable from the prompt text of a
     future session?" "Which line of the session's observational record does the
     Solution correspond to?"
   - **No aggregation**: answers are Yes/No + one line of evidence. Never convert them
     into a numeric score (e.g. a satisfaction ratio). The only consumed output is the
     verdict in 5b; binary answers serve strictly as its evidence

   #### 5b. Holistic verdict

   Weigh the checklist results, the binary answers, and the draft together, then choose
   exactly **one** of the following. **Always enumerate the No-answered questions as
   grounds for the verdict** (hidden Nos breed verdict drift):

   | Verdict | Meaning | Next action |
   |---------|---------|---------------|
   | **Save** | Unique, concrete, well-scoped | Go to Step 6 |
   | **Improve then Save** | Valuable but needs fixes | No questions = improvement items → fix → re-judge with the same questions (once only) |
   | **Absorb into [X]** | Should be appended to an existing skill | Present the target and the content to add → go to Step 6 |
   | **Drop** | Trivial, redundant, or abstract | Explain why and stop |

   **Guiding dimensions** (reference points for judgment, not a scoring rubric):

   - **Concreteness / actionability**: has code examples/commands, immediately usable
   - **Scope fit**: name, trigger, and content align; focused on a single pattern
   - **Uniqueness**: given the checklist results, provides value existing knowledge cannot
   - **Reusability**: will realistically be triggered in future sessions
   - **Grounding**: is the source an observational record (what actually happened) or
     your own interpretation/summary? Self-evaluation-only loops drift (your paraphrase
     gets re-fixed as fact), so lean toward Drop for extractions not grounded in
     observation. **If a grounding question is No, lean Drop even when everything else
     is Yes** (never let averaging dilute a dominant No)

   **Improve then Save improvement list**: the No-answered questions become the
   improvement items as-is. For each No, write one line on what to change to make it a
   Yes; after fixing, re-judge with the **same question set** (once only — do not
   regenerate the questions: if the bar moves, you cannot tell whether the fix worked
   or the bar loosened).

6. **Per-verdict confirmation flow (one at a time, `[y/n/skip]`)**

   Even when multiple patterns were extracted from the session, confirm them
   **one at a time — never ask for batch approval** (a bulk "save them all? [y/n]" is banned).
   For each candidate, present the evidence first (checklist results + verdict
   rationale), then ask `[y/n/skip]`.
   The user can stop at any point. `n` = discard, `skip` = defer for now (leave a
   one-line reason):

   - **Save**: present the save path + checklist results + one-line verdict rationale + the full draft → save after `[y/n/skip]` confirmation
   - **Absorb into [X]**: present the target path + the content to add (as a diff) + checklist results + verdict rationale → append after `[y/n/skip]` confirmation
   - **Drop**: show the checklist results + reason only (no confirmation needed; stop)

7. Save to the destination chosen in Step 3

   - **Absorb**: append to the named asset in place and show the diff. Do not create a file.
   - **Promote**: hand the draft to skill: **skill-creator** — it fixes the intent packet,
     draws the boundary against neighbouring skills, structures it as
     `~/.claude/skills/<name>/SKILL.md`, and passes it through a fresh-context draft gate
     (learn-eval = extraction and Save/Drop judgment / skill-creator = shape, boundary and
     gate — a deliberate role split).

8. **Reachability check (after a Save only)**

   State in one line what will route to the saved content in a future session: the section
   it now lives in, or the skill description that will select it. **If the honest answer is
   "nothing — someone would have to grep for it", the Save was wrong**; go back to Step 3
   and either absorb it into a reachable asset or Drop it.

## Output Format for Step 5

```
### Overlap candidates (from scripts/overlap_candidates.py)
- skills: 0.60 git-workflow [bash, c, cd, git, permission, status] → same knowledge, Absorb
- memory: MEMORY.md:45 feedback_git_dash_c_over_cd, 4 shared terms → already recorded
(or: top skill 0.10, nothing survived the memory floor — no real overlap)

### Checklist
- [x] Candidates judged one by one: (verdict per candidate, quoting shared terms)
- [x] Append-to-existing considered: new file appropriate (or should append to [X])
- [x] Reusability: confirmed (or one-off → Drop)
- [x] Grounding: (the tool output, error or user correction it rests on — a No leans Drop)

### Draft-specific questions
- [Yes] Q1: ... — one-line evidence
- [No]  Q2: ... — one-line evidence → (on Improve: one-line fix plan)

### Verdict: Save / Improve then Save / Absorb into [X] / Drop

**Rationale:** (1–2 sentences explaining the verdict; always mention any No questions)
```

## References

The generic design canon for this evaluation style (binary checks as evidence →
holistic named verdict, no aggregation) is the `llm-as-judge` skill; Step 5 is its
N=1 implementation.

Design rationale for Step 5's two-layer design (binary question decomposition → holistic verdict):

- BinEval — "Ask, Don't Judge: Binary Questions for Interpretable LLM Evaluation and Self-Improvement" ([arXiv:2606.27226](https://arxiv.org/abs/2606.27226)). A framework that decomposes evaluation criteria into atomic yes/no questions and wires failed questions directly into improvement feedback. The dynamic generation of draft-specific questions and the "No questions = improvement items" path are ported from here
- The same checklist-style evaluation research line: CheckEval (arXiv:2403.18771), TICK (arXiv:2410.03608), FActScore (arXiv:2305.14251), UniEval (arXiv:2210.07197)
- The decision **not** to adopt numeric scores (satisfaction ratios) also follows BinEval's own limitations: on subjective, holistic quality dimensions, over-decomposition degrades correlation with human judgment, and the proportion of affirmed questions does not map linearly to quality. For an N=1 draft evaluation the only consumed output is the verdict; binary answers serve strictly as its evidence
