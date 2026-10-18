---
name: qwen38-skill-style
description: "How to write a skill that Qwen3.8 (27B or Flash-Next) will actually follow. For the author, not the model. Nine rules with the run that produced each: enumerate the unnamed deliverables, a command and a pass condition per rule, a fixed done-report, scripts as files, no sentence that harms when followed literally, measured anchors, a stated boundary, one with/without pair before merge, and one shared report shape across the family."
target-model: Qwen3.8
triggers:
  - /qwen38-skill-style
  - write a skill for qwen
  - เขียน skill ให้ qwen
  - skill สำหรับ model เล็ก
---

# Writing a skill for Qwen3.8 (`qwen38-skill-style`)

**The premise (the developer's, 2026-09-05):** Qwen3.8-27B is strong for its size; what its parameter count cannot supply is the *thinking-of* — the unnamed deliverable, the pushback, the discipline — that a frontier model gets from scale. A skill in this family stands in for those missing parameters as a written guide. It is not a new capability, and it is not written for what the model already does unaided.

**The model:** capable, literal, and forgetful of what is not written. On 2026-09-05 the same brief went to it nine times without a skill and five times with one (`Qwen-3.8-27B-Tuning/docs/results/11-quality-bench-2026-09-05.md`, xeno-skills #353). Without a skill it omitted the same unnamed deliverables every time and got the named ones right. With a skill shaped as below it ran the checks itself and scored 8/8. With a skill shaped as prose it broke a rule the prose stated (#134: nine pages over the two-font cap with `design-rules` loaded). Each rule here names the run behind it.

## The nine rules (and one exception, at the end, for the harness)

1. **Enumerate; do not inspire.** List the deliverables the brief leaves implicit and make the model fill a table against them before it starts. *Evidence:* Open Graph 0 / 3 and dark mode 0 / 3 without the list; 3 / 3 and 3 / 3 with it. Isolated, three reps each (2026-09-05 afternoon): the gate alone 8/8 ×3; the design knowledge alone **4/8 ×3** — a third font every run and nothing counted; none 6/8 ×3.
2. **A command and a pass condition per rule.** "Two font families at most" transfers as a `grep … | sort -u` and "the list has ≤ 2 entries"; as a sentence it transferred 4 times out of 9, and the knowledge skills alone scored below no skill at all (4/8 ×3 vs 6/8 ×3). The model runs commands it is given — six of them, unprompted, in the 8/8 run.
3. **A fixed done-report.** Give the exact lines the model must end with (`GATE: n/8 (…)`, `brief table: k rows, all filled`) and say that the line without the pasted outputs is not a pass. It ended with exactly those lines.
4. **Scripts are files, never pasted one-liners.** Ship `gate-*.js` beside `SKILL.md` and run them by path. Three rounds of shell/Python escaping broke an inline regex on the author's side before it ever reached the model.
5. **No sentence that harms when followed literally.** Every sentence in context is an instruction to this model. A global rule "report skill feedback with `gh`" cost a run two turns hunting for `gh`; a rule "answer in the brief's language" plus a quant that cannot spell Thai cost another run six turns installing spellcheckers and a subagent. Write the escape explicitly: *if a tool is missing, say so in one line and continue*. Do not put anything in the model's context you would not want executed.
6. **Anchors are measured figures.** `5 / 9`, `390 px`, `-0.03em`, `.big span` — things a reader can check against a run, never a wording the author liked. The family's tests grep for these.
7. **State the boundary.** One section "What this does not touch", so the skill cannot be read as a second copy of a rule that lives elsewhere.
8. **One with/without pair before merge.** The same brief, the same model, the same effort, one run with the skill in an isolated `CLAUDE_CONFIG_DIR` and one without; record both scores in the issue. Not a rate — n = 1 is enough to show the model can follow it and not enough to say by how much it helps. (`quality-bench.py` in the tuning repo does this for web pages.)

9. **One report shape for the whole family, `THINK:` first.** When two skills are loaded, the model ends with the report of the one it invoked last, and whatever the earlier skill asked for has no line to land on. *Evidence:* 2026-09-05 17:38, `qwen38-think` + `qwen38-code-gate` on an impossible brief ended "Done. CODE GATE: 6/6" with no pushback; `qwen38-think` alone pushed back; after the report was unified (`THINK:` line, then the gate line, in every skill) the same pair pushed back and reported "RED before GREEN n/a — impossible brief" (18:00). A new skill in this family adds a line to the shared report; it does not define its own.

## Shape

```
skills/qwen38/<name>/SKILL.md      frontmatter: name, description, target-model: Qwen3.8, triggers (Thai included)
skills/qwen38/<name>/*.js|*.sh     the checks, run by path
tests/skills/test-<name>.sh        anchors from the runs, the no-skip sentences, the boundary
```

Length: the whole SKILL.md under ~6 KB. The model reads every skill in the router's table at session start; a long one is paid for on every task. **The budget is about what the model loads, so it does not bind this file** (an authoring standard, read by whoever writes a skill, never by the model) **nor `qwen38-claude-code`** (loaded on demand, 16 KB, exception below).

## Checklist before opening the PR

- [ ] a brief table or equivalent enumeration comes before the first instruction to build
- [ ] every rule has a command and a pass condition; none is prose alone
- [ ] the done-report is spelled out and says outputs must be pasted
- [ ] scripts are files; nothing to copy by hand longer than one line
- [ ] each sentence read literally leads somewhere safe; the missing-tool escape is written
- [ ] every figure is from a run, with the run named
- [ ] "What this does not touch" exists
- [ ] the with/without pair is in the issue
- [ ] the report is the family's shared shape (`THINK:` first, then this skill's line), not a new one

## The one exception: the harness itself

**A skill about Claude Code is written to cover everything, not only a measured gap** (#358, the developer 2026-09-06: *"เราอยากให้ qwen ใช้งาน claude code harness ได้แบบดีที่สุด … ไม่ให้ model ทำการหาเอง"*). Rule 1 still holds — enumerate — but the enumeration is the whole tool surface, and rule 6's "every figure from a run" applies only to the rows that have one; the rest are labelled harness facts.

**Why the usual rule inverts here.** Everywhere else, writing for something the model already does wastes the budget. The harness is the case where **not writing** is what costs: across the 44 bench streams Qwen touched 12 of the 31 tools Claude Code sends, and the reason is not that the other 19 were wrong for the work — it is that a JSON schema says what a tool *accepts* and never what it is *for*, so ignoring it was the safe move. Absence of use is not evidence of a decision. `qwen38-claude-code` therefore carries a verdict per tool and is capped at 24 KB rather than 6 (16 KB until #380 added the harness facts for Claude Code 2.1.281).

**This exception does not generalise.** It covers a fixed, externally-defined surface the model is handed whole and cannot discover by trying. A design rule, a code rule or a workflow is not that, and still gets written only where a run showed a gap.

## What this does not touch

The content of any task (design, code, prose): that is the pointed-at skill's. This file only says how to write one this model will follow.
