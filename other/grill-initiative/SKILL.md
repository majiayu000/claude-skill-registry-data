---
name: grill-initiative
description: A relentless interview that sharpens a Kairos initiative (or a strategy) and writes each settled answer into the item at once. Pass an initiative or strategy short code, or a title for a new initiative.
argument-hint: "<initiative or strategy short code> | \"<title of a new initiative>\""
disable-model-invocation: true
---

# Grill an initiative

The arguments are: `$ARGUMENTS`

Run the `grilling` skill against one Kairos initiative or strategy. Read `grilling` first: it gives the interview loop, one question at a time, and that loop does not change here. This skill says which item you sharpen, which questions to ask, and where each answer goes.

The item is the record of the interview. A compaction loses the conversation, but not the item.

## 1. Find or create the item

- **A short code** (`PREFIX-I-NNNN` or `PREFIX-S-NNNN`): call `get_item`. If it does not find the item, tell the user and stop. Then read:
  - each document that supports it (for example the PRD), with `get_item`;
  - the parent strategy of an initiative;
  - the ADRs that inform it.
- **A title**: confirm the title and the board with the user. The board is `initiative_board` in `.claude/kairos.local.md`, else find it with `my_boards`. Then call `create_item` (`item_type: initiative`). Send `parent` only when the user names a parent strategy. From then on, name the initiative only by the short code in the result.
- **No argument**: ask the user which item to grill. Do not guess.

Every answer must trace back to the parent strategy, when there is one. When an answer does not, say so.

## 2. The column sets the depth

Read the column from `get_item`. The default columns of an initiative board are Discovery, Design, Ready, Decompose, Active, Monitoring and Completed. A board can have different columns: use its own order. The entry column is the first one.

| Column | What to grill |
|---|---|
| The entry column (Discovery) | The context, the goals and the non-goals. Is the problem clear enough to design? |
| The design columns (Design) | The design, the alternatives, the plan and the tests. |
| After the design (Ready, Decompose) | Only what the user asks to open again. Tell the user that a changed answer can make the existing tasks wrong. |
| Active, Monitoring | Only what the user asks. The work has started. |
| A done column (Completed) | Do not grill. Ask no design question. Offer a new initiative. |

For a strategy, the default columns are Draft, Review, Active, Monitoring and Completed. Grill in Draft and Review. In a done column, offer a new strategy.

**Never call `transition_item`.** The user moves the item.

## 3. Seed the questions

Each branch below is a root of the design tree. Look up each fact before you ask: the code, the documents, the ADRs, other items (`search`, `get_repository`). Ask only for decisions. Expect new branches as answers come in.

**An initiative**

- **Context.** What is true today that makes this work necessary now? Check it against the code and the strategy. Who asks for it? Who does it change, without a request from them? What did people try before, and why did it stop?
- **Goals and non-goals.** What can a user do after this initiative that they cannot do now? How do you see that a goal is met? If nobody can tell, it is not a goal yet.
  What will people think is in scope that is not? Write each such thing as a non-goal. Which goal stays if the others go?
- **Design.** What are the parts, and where are they in the code now? What is the interface to what exists: the data, the API, the owner? Walk through the main scenario, then the failure scenario, then the concurrent one. Which term in the design has two meanings?
- **Alternatives.** What is the simplest thing that can work, and why is it not enough? For each rejected alternative: which fact or value rules it out?
- **Plan.** Which first vertical slice proves the approach? What must be true before decomposition starts? Which other initiatives, teams or repositories does it depend on?
- **Tests.** How does the user know that it works? How does the code know? What would be bad to ship broken? Which check needs a person, and who does it?

**A strategy**

- **Purpose.** Who is it for, and what changes for them?
- **Current state.** What exists now? What works and must not break?
- **Future state.** What is different when the strategy succeeds? What is not part of it?
- **Success criteria.** What do you measure or see? `get_item` shows the `hypothesis` of the strategy: start from it. The kairos MCP tools do not change that field after `create_item`. Write the settled criteria under the Decisions heading, and tell the user when the `hypothesis` no longer agrees with them.
- **Principles.** When two good options conflict, which value wins? Ask for a real tie-breaker, not a slogan.
- **Constraints.** What is fixed: people, time, platform, compatibility, regulation? Which constraints are real, and which are assumptions?

An answer that is a separate capability is a candidate initiative. Name it as a quoted title marked "not yet created" (the `kairos-vocabulary` skill). Do not give it a code or "phase 2". Write it on the item, and do not grow the item to hold it.

## 4. Write as you go

When a decision settles, write it into the item at once, before the next question. Do not keep edits for the end.

1. Call `get_item` to read the current version.
2. Call `edit_item` on the initiative. When the initiative has a PRD and the decision is about the product, edit the PRD.
3. Put the decision under a heading `## Decisions (<who>, <date>)`, for example `## Decisions (Dylan, 2026-10-02)`. Write one line for each decision. Use one heading for each session, and add to it during the session.

Rules for the text:

- When the user reverses a decision, change its line in place, so that the text says what is true now. The history of the item keeps the old text.
- A decision is prose. Do not number decisions (`D1`, `D2`).
- When a term settles, it has one meaning from then on. Use only that term in the item, and do not use a synonym for it.
- The decisions are reasoning, so write them in plain, short sentences, not in STE. An acceptance criterion or a goal that a test checks is procedural: write it in STE ([the STE reference](../../../references/simplified-technical-english.md)).

## 5. ADRs

Offer an ADR only when the three tests of `engineering/domain-modeling` hold. The decision is hard to reverse, surprising without context, and a real trade-off. Most decisions are lines under the Decisions heading. When the user agrees, record the ADR with `engineering/domain-modeling/ADR-FORMAT.md`:

- `link_items` with `informs` from the ADR to the initiative;
- `link_items` with `impacts` from the ADR to each repository that it is about.

Then write the short code of the ADR on its line under the Decisions heading.

## 6. Close

When no open question is left:

1. Call `get_item` and read the item in full.
2. Give a summary of the settled design in a few lines. Ask the user to confirm that you have the same understanding.
3. Tell the user the column of the item. Do not move it.
4. When the user confirms, offer `/kairos:decompose` to make the tasks, then `/kairos:grill-decomposition` to review the tasks as a set.
