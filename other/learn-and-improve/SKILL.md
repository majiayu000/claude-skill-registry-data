---
name: learn-and-improve
version: "1.0.3"
user-invocable: true
description: "Structured retrospective and knowledge sediment for completed work (the Act phase of PDCA). Run a disciplined post-work review (Keep-Problem-Try / Stop-Start-Continue / After-Action Review by context), judge which lessons are worth solidifying, pick the right carrier, validate the sediment gets reused, and feed improvements back. Use whenever finished work needs reflection — as a PDCA host closeout/review stage via frontmatter dependencies, or standalone on any completed task. Triggers — 「回顾总结」「复盘」「经验沉淀」「总结经验教训」「改进闭环」「沉淀规则」「项目复盘」 / learn and improve, lessons learned, retrospective, post-mortem, debrief."
---

# Learn and Improve

> The **Act** phase of PDCA: turn finished work into reusable knowledge. This skill exists because most "lessons learned" stages are shallow — a vague "what went well / what didn't" list that captures lessons but never applies them. This skill makes retrospective and sediment a disciplined, depth-bearing practice.

## Why this skill exists

Across PDCA-style fix workflows, the review stage was often an afterthought — each host wrote a shallow inline version, nobody imported real methodology, and the same lessons got captured then forgotten. Compare `solution-review`, which is a deep independent skill for phase 3 (citing FMEA / SRE PRR / CBAM). This skill is the **equivalent for the Act stage**: deep, methodology-anchored, reusable.

The core disease it treats is **"captured but not applied"** — lessons written into a doc and never retrieved. PMI identifies this as the dominant failure of lessons-learned programs. So retrieval/effectiveness validation is a first-class step here, not an afterthought (the **Retrieve** step of the lessons-learned 5-step: Identify → Document → Analyze → Store → **Retrieve**).

## When to use

- **Standalone**: the user finished work and wants to reflect — "复盘一下这次", "做个回顾总结", "what did we learn from this".
- **Integrated**: a PDCA host reaches its review or closeout stage and loads this skill via frontmatter `dependencies`.

The trigger phrases in the description govern both paths.

## Relationship to other skills

- **Referenced by**: PDCA hosts via frontmatter `dependencies` (strong; missing → host aborts at prerequisite check). Hosts are the source of truth for that edge — this skill does not maintain an integrator name list.
- **Analogous to**: `solution-review` (the deep review skill for phase 3). This is the deep review skill for the Act phase. Same pattern, different stage.

## The framework — 4 steps

### Step 1 — Structured retrospective

Do **not** default to a vague "what went well / what went wrong" list — that is the disease this skill replaces. Pick a format by context (full guidance in [reference.md](reference.md) § Retrospective formats):

- **Stop-Start-Continue** — light, new teams, short cycles.
- **KPT (Keep / Problem / Try)** — problem-driven, surfaces issues and generates experiments.
- **After-Action Review (AAR)** — post-project or post-incident, significant events. Four questions: what was *intended* → what *actually* happened → why the *gap* → what to *change*.

Surface three kinds of finding: **effective practices** (keep), **failed lessons** (avoid), and **unexpected discoveries** (often the most valuable — the things nobody predicted).

Then go deeper on any non-trivial failure with **5Why**: chase the root cause, do not stop at the symptom. A symptom-level "lesson" reproduces the failure next time.

### Step 2 — Sediment value judgment (decide what is worth keeping)

Most "lessons" are one-off and should **not** be solidified into long-term rules. Judge each candidate against three gates (full decision tree in [reference.md](reference.md) § Sediment value):

1. **Will this recur?** — will future projects/tasks plausibly hit it? If no → summary doc only, not a rule.
2. **Is it verified?** — confirmed in ≥2 distinct scenarios, not a single coincidence. If no → hold, do not solidify yet (one coincidence over-generalized into a rule is pollution).
3. **Is it team/engineering-level, not personal preference?** — personal taste must not be imposed as a team rule.

Only candidates passing all three are candidates for long-term sediment. The rest go to a one-off summary doc.

> Essence: this is SECI **Externalization** (Nonaka & Takeuchi) — converting tacit experience into explicit rules. Not all tacit knowledge *should* become explicit — only the recurring, verified, shared kind.

### Step 3 — Carrier selection (where to write it)

Pick by **audience × longevity × change-frequency**, not by habit. Full decision tree in [reference.md](reference.md) § Carrier selection; summary:

| Carrier | Use when |
|---------|----------|
| `AGENTS.md` | Cross-tool, team-wide, long-term engineering conventions |
| `CLAUDE.md` | Claude Code-specific behavior or workflow preferences |
| `.cursor/rules/` | Cursor-specific rules |
| Project skill | Stable, reusable workflow/domain knowledge that future work can trigger on its own |
| `CONTEXT.md` (via `domain-language-discipline`) | Project ubiquitous language / glossary only — not implementation or OpenSpec specs |
| Summary doc | One-off retrospective, background record (not a rule) |

**Before writing any long-term carrier, wait for an explicit user request** ("write to rules" / "create a skill" / "update AGENTS.md"). The default is to *recommend*, not to write — writing to shared long-term rules is a one-way door that pollutes conventions if done carelessly.

### Step 4 — Effectiveness validation + improvement loop

This is the step most reviews skip, and the one that cures "captured but not applied".

- **Define a retrieval/reuse mechanism for each solidified item** — a trigger, a checklist, a guard, a CI rule. A rule nobody retrieves is dead weight; the value of sediment is realized only when it is retrieved and applied later, not when it is written.
- **Check learning depth**: are you only fixing surface actions (**single-loop learning** — "do X differently"), or also questioning the underlying assumptions and goals (**double-loop learning**, Argyris — "why did we assume X at all?")? Push for double-loop on stubborn or repeated issues.
- **Improvement loop**: if the review concludes the goals were not met, feed back to the relevant earlier stage instead of ending here. (In integration mode, the host workflow decides which stage to loop to.)

## Two modes

- **Integration mode** (called by a workflow's review stage): the host workflow owns stage orchestration (e.g. `solve-workflow` may loop back to analyze/plan; `opsx-solve-workflow` also archives OpenSpec changes and runs a coverage gate). **This skill owns *how to reflect and sediment*, not the stage sequence.** Run steps 1–4 on the completed work and return sediment recommendations + a next-step suggestion.
- **Standalone mode** (user triggers directly): run steps 1–4 in full. If the scope of the finished work is unclear, ask what work is being reviewed before starting.

## Output

```
【Learn & Improve — 回顾总结】
1. Retrospective (format: SSC / KPT / AAR)
   - Keep (effective practices): ...
   - Problem / Avoid (failed lessons): ...
   - Discoveries (unexpected): ...
   - Root cause (5Why, for any non-trivial failure): ...
2. Sediment candidates (judged)
   - ✅ Solidify: <item> → <carrier>   (recurs × verified × team-level)
   - ⏸ Hold (unverified): <item>
   - 📝 One-off only: <item> → summary doc
3. Effectiveness
   - Retrieval/reuse mechanism per solidified item: ...
   - Learning depth: single-loop / double-loop (did we question assumptions?)
4. Next step
   - Loop back to <stage> / conclude
```

## Anti-patterns

- ❌ Vague "what went well / what didn't" with no framework — the exact disease this skill replaces.
- ❌ Solidifying a one-off coincidence as a rule (over-generalization).
- ❌ Writing unverified guesses into `AGENTS.md` / `CLAUDE.md` — pollutes long-term rules; verify in ≥2 scenarios first.
- ❌ Sediment with no retrieval path — "captured but not applied".
- ❌ Only single-loop fixes (tweak the action) when the assumption itself was wrong — push double-loop.
- ❌ Defaulting to one retrospective format regardless of context (SSC for a major incident is as wrong as AAR for a trivial tweak).
- ❌ In integration mode, taking over the host workflow's stage orchestration — you own *how to reflect*, not the sequence.

## Reference

Deep material — full retrospective-format comparison, the complete sediment-value and carrier-selection decision trees, single/double-loop learning, SECI Externalization, and the expanded anti-pattern catalog — is in [reference.md](reference.md). Read the relevant section when a step's judgment is ambiguous.
