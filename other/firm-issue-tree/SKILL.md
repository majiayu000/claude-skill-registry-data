---
name: firm-issue-tree
description: Builds a short issue tree that splits the client's root question by one stated cut into branches that do not overlap and together cover it, three levels at most, each branch marked tested or untested with its evidence, the client's AI answer placed on the tree with what it got right said first, and the untested branches that matter most. Use for "run firm-issue-tree", "build an issue tree", "break this problem down", "is this split MECE", "the client already asked AI for the answer", "where could their AI answer be wrong", "which branches have no evidence", part of the Claude for Consultants · Team in Claude Pack by Polar Bear.
---

# Issue Tree

## When To Use
The client typed the question into a model last week and got four confident paragraphs. Now they want to know what you add. A tree is the honest reply: it shows which parts of that answer stand on evidence and which nobody has checked. Run it once the problem statement is agreed, with or without an AI answer on the table.

## When Not To Use
With no agreed root question, write the Problem Statement first; a tree without a root spreads in every direction. For the spoken reply to "why can't AI just do this?", use AI Objection Answer; this is the written analysis.

## Inputs
- The root question from your problem statement
- Your call record, as the evidence so far
- The AI answer or plan the client shared, if there is one
If you have none of this, I start from your own wording of the problem, label each branch untested and call the tree a first draft.

## Approach
An issue tree splits a question into parts that are mutually exclusive and collectively exhaustive, the MECE test associated with Barbara Minto (barbaraminto.com) and set out in practitioner guides to hypothesis-led problem solving. The judgment is in the labels and the depth. A neat tree with unchecked branches looks rigorous and is not, so every branch says tested or untested. And three levels is the limit before signature; deeper than that is the engagement itself, handed over for nothing.

## Workflow
1. Ask, in one go: what is the root question? Has the client shared an AI answer or plan? Which cut feels natural here: by cause, by step in a process, or by group affected?
2. Write the root as a single question. Split it into two to four branches with one cut and name the cut. Test for overlap (could one fact sit under two branches?) and for cover (is there a cause that fits nowhere?). If either fails, change the cut, not the wording.
3. Go one level down only where it would change what you do next. Stop at three levels.
4. Label each branch tested, with the line of evidence, or untested. For untested branches name the evidence needed and how you would get it: data they hold, a conversation with a role, a document, a small trial.
5. If there is an AI answer, place each of its claims on a branch. Say first, and plainly, where it is right and supported. Then mark what it assumed without evidence and which branches it never touched. It is judged on evidence, never on where it came from.
6. Pick out the two or three untested branches that would change the answer most if they turned out false. You choose which to check first.

## Output Format
```markdown
# Issue Tree
Root question: [from the problem statement] · Cut: [by cause / by step / by group]
## Tree
| Branch | Level | Tested or untested | Evidence so far (source) | Evidence needed | How to get it |
|---|---|---|---|---|---|
| 1. [branch] | 1 | [tested / untested] | [line, or none] | [evidence] | [route] |
| 1.1 [sub-branch] | 2 | [tested / untested] | [source] | [evidence] | [route] |
| 2. [branch] | 1 | [tested / untested] | [source] | [evidence] | [route] |
## Where the client's AI answer sits on the tree
| Branch | What the answer says | Supported? | Note |
|---|---|---|---|
| [branch] | [claim] | [yes, source / assumed / not covered] | [what it got right, or what it skipped] |
## Untested branches that matter most
1. [Branch] · if false: [what changes] · check: [route]
## Decision
[You] choose the first checks by [date] and decide whether the tree goes to [client role] or stays in your working notes.
```

## Done When
- One named cut per level, with no overlap and nothing left outside
- Every branch reads tested or untested, with a source or the evidence it needs
- Any AI answer sits on the tree, with what it got right written first
- No more than three levels

## Quality Bar
- Branches are causes, steps or groups, never anyone's competence
- Where the evidence supports the AI answer, agree with it plainly; never sell against AI
- No figure appears beyond those in your call record
- Untested branches say untested; I invent no evidence, and you decide what to check and what to show the client.

## Next
Run firm-hypothesis-test-plan (Hypothesis Test Plan) to turn the branches that matter into hypotheses that can fail.

## About the makers

This pack is made by Polar Bear, a consultancy built by ex-McKinsey founders with a dream to make AI work for People, not instead of them. We help our clients build people systems and AI-first ways of working, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
