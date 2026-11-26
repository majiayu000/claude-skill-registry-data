---
name: oa-sim
description: Simulate a timed online assessment (OA / coding test) like the ones used in campus placements and off-campus hiring. It generates a full test with coding problems (and optional aptitude/MCQ sections) as real files, the candidate solves them in their editor, then the agent runs hidden test cases and reports a cutoff verdict. Use when the user wants an OA, online test, coding round practice, HackerRank/CodeSignal-style test, or a placement test simulation.
---

# OA simulator

A realistic online assessment, run from files on disk: the candidate solves in their own editor, and you grade with **hidden test cases you execute**, just like the real platforms.

## 0. Setup

1. Call the Skill tool with "cracked-profile" (you need language, level, target companies).
2. **Ask which company the OA is for**, in one line: "Which company is this OA for? Say 'none' for a generic test." If the request or profile already names one, confirm it instead of asking. This is the one skill where you always ask, because OAs differ most by company.
3. **Company given**: call the Skill tool with "company-intel". Use its brief for the OA shape (platform, number of questions, duration, sections), and pick problems from its reported questions with the script: `questions.py get "<Company>" --window 6m --format json --limit 60`. Favour high-frequency problems from the recent windows, then match the brief's difficulty mix. Skip problems already in `journal.md`. If the brief doesn't describe the OA, use its archetype's preset below.
4. **No company**: choose a **format**. Offer these presets and recommend one from the profile:

| Preset | Sections | Time |
|---|---|---|
| `service` | 20 aptitude/logical MCQ + 10 CS-fundamentals MCQ + 2 easy coding | 90 min |
| `product` | 2–3 coding (easy-medium, medium, medium-hard) | 90 min |
| `bigtech` | 2 coding (medium, hard) | 70 min |
| `startup` | 1 practical coding task (parsing, data transform, small API logic) + 1 medium | 60 min |
| `custom` | user specifies | user specifies |

These are generic archetypes, not any specific company's real test. Say so once.

## 1. Generate the test

Create two folders for session id `<YYYY-MM-DD-HHMM>`:

- the **candidate folder** `$CRACKED_DIR/oa/<id>/`, the only folder you tell them about
- the **grader folder** `$CRACKED_DIR/oa/.sessions/<id>/`, outside the candidate folder, which holds everything hidden

In the candidate folder, write:

- `README.md`: the rules, the time limit, the section list, and how to submit ("say **submit** in the chat when done").
- For each coding problem `qN`:
  - `qN.md`: the full statement, input/output format via **stdin/stdout**, constraints, and 2 sample cases. Write it in the style of a real OA: a short story wrapper, precise constraints. For problems taken from the company list, **write the statement in your own words** (don't copy LeetCode's text), and **don't reveal the title or link until the debrief**, so the solution can't be looked up mid-test.
  - `qN.<ext>`: a starter file in the profile language that reads stdin and writes stdout, with a `solve` function stub.
  - in the **grader folder** `qN/`: 10–15 hidden test cases as `NN.in` / `NN.out` pairs. Include the samples, edge cases, and at least 2 **large** cases that time out a brute force. Generate the large cases with a small script, and compute every expected output with **your own reference solution, executed**. Never hand-write expected outputs for non-trivial cases. Keep the reference solution in the grader folder as `qN/ref.<ext>`, and a brute force (`qN/brute.<ext>`) where feasible, cross-checked as in [RUNNER.md](RUNNER.md) § Differential testing.
- For MCQ sections: `mcq.md` with numbered questions and options A–D, plus an answer-sheet template `answers.txt` (`1: `, `2: `, …). Keep the key in the grader folder as `mcq-key.txt`. **Compute every numerical answer** (aptitude, probability, time and work, page faults, subnetting) with Python and store the working next to the key. **Drop any question whose answer you can't verify** by computation or a definition you're certain of.

Verify before starting: run each reference solution against its own sample cases and confirm they match `qN.md`. Fix any mismatch before the candidate sees the test.

Tell the candidate only the candidate folder. If they ask where the tests are: "They're stored separately so the test stays fair. Looking at them would only cheat yourself."

## 2. Run the test

1. Record the start time with `date +%s` (or the fallback in [RUNNER.md](RUNNER.md) § Clock).
2. Print the session folder path, the problem titles, and the deadline as a wall-clock time.
3. Stay quiet. If asked for help, reply: "This is a test, so no hints. You can ask me to clarify a statement." Clarify ambiguous statements only.
4. If the candidate asks for remaining time, compute it from the clock.

## 3. Grade on "submit" (or when time is up)

1. Record the end time and elapsed minutes. Code submitted after the limit is still graded, but marked late.
2. For each coding problem, compile if needed, then run the candidate file against every hidden case **from the grader folder** using [RUNNER.md](RUNNER.md): a 2-second base limit scaled by the language's multiplier, with the portable Python timeout. Tell the candidate the limit that applied. Classify each case as AC / WA / TLE / RE / CE.
3. Score MCQs against the key.
4. Show a results table:

```
Q1  Two-Pointer Inventory   12/12 AC        100
Q2  Grid Delivery Routes     8/12 (2 WA, 2 TLE)  67
Q3  Interval Scheduler       0/12 (CE)        0
MCQ                          24/30            80
```

5. **Cutoff verdict (heuristic).** As a rule of thumb, shortlists tend to need near-full marks on the easiest problem plus substantial partial credit on the next. Report `Likely shortlisted`, `Borderline` or `Unlikely`, with the one-line reason, and label it: *"heuristic, not this company's real cutoff"*.

## 4. Debrief

For each problem: its original title and LeetCode link (in company mode, noting that it's "frequently reported for <Company>"), what the failing hidden cases had in common (e.g. "all TLE cases have n = 10⁵: your O(n²) loop"), the intended approach, and the clean reference solution. Show failing inputs only if they're small.

Then produce the scorecard by calling the Skill tool with "cracked-profile". Dimensions: **Correctness, Efficiency, Edge Cases, Time Management**, plus **Aptitude** if the test had MCQs. Tag weak spots by pattern.

## Rules

- Hidden tests must be **executed against a reference solution**, never guessed. A wrong expected output wrecks trust in the whole tool.
- If you cannot run code, say so up front and switch to `mock-interview` style hand-tracing. Don't pretend to have run tests.
- Never edit the candidate's solution files.

---

*Skill calls:* if your agent has no Skill tool, open the named skill's `SKILL.md` in the cracked skills folder (`core/`, `interview/`, `profile/`, `strategy/`) and follow it instead.
