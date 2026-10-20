---
name: write-research-note
description: >-
  Load this skill when a question needs an answer from outside sources, written down: a background
  agent writes one note with every claim cited, then the citations are spot-checked. Trigger on
  "research X", "look into how Y works", "what do the docs say about".
argument-hint: "<question>"
disable-model-invocation: false
user-invocable: true
compatibility: >-
  Needs network access through WebSearch and WebFetch. Without them, only local files can be
  cited and the note says so.
license: Apache-2.0
---

# Write research note

Answer one question from sources outside the session and leave the answer behind as a note in
which every claim points at where it came from. Done means the note is written, its citations are
spot-checked, and its path and short answer are reported.

## Procedure

1. **Pin the question.** One sentence, answerable, with the decision it feeds ("Does library X
   support streaming in v3, so we can drop our polling code?"). A topic ("research X") becomes a
   question first: state the question you chose in the brief and in the note.
2. **Dispatch one background agent** with the Agent tool (`general-purpose`) so the fetched pages
   stay out of this session. Name the model: the session's own model when the
   note settles a decision, a cheaper one for a plain fact-find. The brief carries everything,
   because the agent sees none of this conversation:
   - the question and the decision it feeds;
   - the source rules under Rules, verbatim;
   - the output path and the format under Output;
   - "Return only the note's path and its Answer section."
3. **Spot-check before reporting.** When the agent returns, open the note, pick the two or three
   claims the answer rests on, and fetch their sources yourself. A citation that does not say what
   the note claims is fixed in the note or the claim moves to Not found. Record the check in the
   note's Checked line.
4. **Report** the path, the answer, and anything under Not found.

## Rules

- **Primary sources first:** the project's own docs, specification, source code, changelog,
  release notes, the paper, the vendor's own page. A blog, forum answer, or AI summary is cited
  only to point at a primary source or when nothing primary exists, and is marked secondary.
- **Every claim carries its citation** in the same sentence: `[n]` pointing at the Sources list.
  A sentence with no citation is labelled as inference.
- **Quote what is contested.** Where sources disagree or the wording matters (a limit, a license
  term, a deprecation), quote the exact words and give both sides.
- **Dates matter.** Record each source's publication or last-updated date. For anything that
  changes fast (APIs, prices, versions), flag a source older than a year.
- **"Not found" is a finding.** Searching and finding nothing is reported with what was searched,
  never filled with what is probably true.

## Output

Save to `.agents_workspace/research/<YYYYMMDD>-<topic>.md` in the working directory, creating the
directory if needed.

```markdown
# <Question>

Feeds: <the decision>. Researched <YYYY-MM-DD>.
Checked: <claims n, m re-fetched by the session; result>.

## Answer

<Three to five sentences, each with its [n].>

## Findings

- <Claim> [n]
- <Claim, quoted where contested> [n] [m]
- Inference: <what follows from the cited findings, labelled as such>

## Not found

- <What was searched for and where, with no result>

## Sources

1. <Title>, <URL>, <published or updated date>, primary | secondary
```
