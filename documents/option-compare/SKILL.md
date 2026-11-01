---
name: option-compare
description: "Builds a side-by-side comparison of design options in docs/design/options.md: the criteria you choose, one column per scheme, every cell filled from what you supply, and a tradeoff summary that stops short of picking the winner. Trigger on \"compare options\", \"option A or B\", \"scheme comparison\", \"comparison matrix\", \"which scheme\", \"options for the client\", \"option-compare\", or pasted facts about two or more schemes. Areas can be read from a space-program file where one exists, costs arrive from you or a cited benchmark, and empty cells stay visibly empty rather than estimated. Weighted scoring runs only if you supply the weights, arithmetic shown. The decision is the client's and yours; the skill structures it and does not make it. Renders to Word or PDF through aec-doc-gen when the meeting needs a handout."
license: MIT
metadata:
  title: "Option Compare"
  summary: "Build a side-by-side comparison of design options for a decision"
  discipline: "design-building-types"
  tags: "Design"
---

# Option Compare

Every early design phase ends the same way: two or three schemes, one
meeting, and a decision that will be relitigated forever if nobody wrote
down what was traded for what. The comparison matrix is how the decision
gets made on the table instead of in the hallway. This builds it, keeps
every cell honest about where it came from, and leaves the choosing to
the people whose choice it is.

## Scope and limits — read first

**What this does.** Collects the schemes, asks which criteria matter for
this decision, fills the matrix from what you supply or from project
files you point it at, marks every cell with its source, writes the
tradeoff summary each option's column implies, and records the eventual
decision with its date and its why.

**What this does not do.**

- **It does not fill cells on its own.** An area you did not supply, a
  cost nobody stated, a "feels more open": none of it enters the matrix.
  Empty cells print as `not provided`, and a column with three of them
  reads as the less-studied option it is.
- **It does not pick the winner.** The summary names what each option
  gives up and gains, in parallel wording. Ranking happens only under
  weights you supply, with the arithmetic shown, and even then it prints
  as "your weights rank B first", not as a recommendation.
- It does not design or improve the options, and it does not invent a
  compromise scheme D. `design-critic` critiques a scheme; this compares
  what exists.
- It does not benchmark. A cost cell wants your number or a cited
  benchmark you accepted (`lookup-cost` is the tool for finding one).
- Criteria are yours. It proposes the blanks a decision usually needs
  (program fit, area, cost basis, schedule, code posture) as questions,
  never as filled rows.

**What you need before starting.** Two or more schemes that actually
exist, the criteria the decision turns on, and values for the cells you
want compared, with sources.

## Workflow

### Step 1. Bootstrap if needed

Check whether `docs/design/options.md` exists; create it if not, one
section per comparison round, dated. If the project has no `docs/`
folder at all, confirm before creating one.

### Step 2. Frame the decision

Ask, in one message:

> 1. What is being decided, and by whom, at what meeting?
> 2. Which options are on the table? Names and a one-line description
>    each, as you would say them to the client.
> 3. Which criteria should the decision turn on? I can suggest common
>    blanks, but this list is yours.
> 4. Where do values come from: typed, a space-program file, a cost
>    source?

### Step 3. Fill the matrix

One row per criterion, one column per option. Every cell records its
source: you, a named file, a cited benchmark. Where a `space-program`
file exists, offer to pull each option's areas from it and cite the
file. Quantitative rows keep units as supplied; qualitative rows keep
your wording, quoted, not paraphrased upward.

```
| Criterion       | Option A         | Option B         | Source    |
|-----------------|------------------|------------------|-----------|
| <as chosen>     | <as supplied>    | <as supplied>    | <each>    |
| <...>           | not provided     | <as supplied>    |           |
```

### Step 4. Score, only if weighted

If you supply weights, normalize them in the open, multiply, sum, and
show every step. No weights, no scores; a matrix quietly ranked by an
unstated weighting is the most common way these documents lie.

### Step 5. Write the tradeoff summary

One short paragraph per option, parallel in structure: what choosing it
buys, what it costs, stated from the matrix rows and nothing else. Then
the open questions: every `not provided` cell, listed as what would have
to be known for the comparison to be complete.

### Step 6. Record the decision

When the decision lands, record it under the round: which option, who
decided, the date, and the why in their words. Offer to log it to
`project-tracker` as a decision entry too; that log is where "why is
the building L-shaped" gets answered in a year.

### Step 7. Export, if the meeting needs paper

Offer `aec-doc-gen` to render the round to Word or PDF for the handout.

## Rules

- **Every cell carries a source.** No source, the cell reads
  `not provided`, and the summary counts them.
- **Parallel wording across columns.** "Efficient core" for A and
  "awkward core" for B is a decision wearing a matrix costume; state
  the measurable difference or quote the stated judgment with its
  author.
- **No scores without supplied weights**, and no recommendation either
  way.
- **Rounds append.** A revised comparison is a new dated section; the
  matrix the client saw in March stays as it was.
- **Quote judgments, with their author.** "Client prefers the porch
  (meeting 3/14)" is data; "warmer entry experience" from nowhere is
  not.

## Anti-patterns

- Filling an obvious cell (the bigger scheme "probably costs more") to
  complete the picture.
- Wording one column warmly and its neighbor clinically.
- Inventing a criterion because comparisons usually have one.
- Averaging two stakeholders' conflicting judgments into one cell.
- Deleting a superseded round instead of dating a new one.

## Resources

None. This skill is one file. The matrix is written directly to
`docs/design/options.md`.
