---
name: analiz-task-spec
category: pm
description: Use when opening an analiz task for the system-architect - the required fields, what the criteria may say, and what the description must hand over
---
# Analiz Task Spec

create_board_task fields for analiz:

- task_type: "analiz" — the exact tool argument is `task_type`, not `type`. Passing the wrong field name is silently dropped (the tool ignores unknown arguments) and the task is created as `task_type: "task"` instead, which breaks analiz filtering, routing and board semantics. Always pass `task_type: "analiz"` explicitly.
- column: todo
- assignee: **system-architect** (REQUIRED — pass `assignee: "system-architect"` to create_board_task). Without an assignee the architect is never dispatched and the task sits idle in todo. The architect is not subscribed to the todo column; it reaches an analiz task only via the assignee.
- title: "Analiz: [what is being investigated]"
- description: investigation goal, scope boundaries, available context (links, prior docs).
  - **Relevant projects/repositories (required):** name every project/repository you believe the work touches, so the system-architect knows what to clone and review. If you are unsure, say so — the architect will verify and pull anything you missed. Missing a repo here does not block the architect (it cross-checks the codebase indexes), but naming them speeds the analysis.
  - **Design brief, if the work touches UI:** carry the same block implementation-task-spec uses (audience/tone, content language, visual direction, references, states, primary action) so the architect's spec inherits real design direction instead of inventing it. Detect an existing design system first (see implementation-task-spec); if none exists and this is new web UI, say so — the architect sequences a foundation task first.
- acceptance_criteria — statements about the CONTENT of the spec and the plan, which is the only thing this task delivers. Write what must be true of the documents, e.g.:
  * "The spec names every repository the change touches and, per repository, the files and interfaces that change."
  * "Each unit of work in the plan states its inputs, its outputs and how it is verified."
  * "The plan orders the units so nothing depends on work scheduled after it."
  * "Every option considered is recorded with the reason it was or was not chosen."
  * "Any question only a stakeholder can answer is listed with the decision it blocks."

  Board actions are NEVER criteria. Not "moved to analiz_review", not "attached
  with add_task_document", not "presented for approval", and above all not
  "implementation tasks are created" — those are the workflow around the card
  (the architect's routine, the human's approval, what happens after it), and
  none of them says whether the analysis is any good. Worse, they cannot be
  ticked before the hand-off that ends the task, so the criteria gate holds the
  card and it never reaches done. The architect knows the workflow from its own
  role; the criteria are where you say what the documents must contain.

  Do NOT ask for the documents to be committed to the repository: an analysis
  produces a decision, not code, and a docs/ commit means a branch and a pull
  request for a task that ships nothing.

This analiz task is the permanent home of the spec and the plan. Every implementation task opened from it carries `derived_from: ["A-N"]` pointing back here, which is how the developer working that task is handed these documents; `list_task_documents` on this key returns them to anyone at any time. Nothing is ever copied into a repository, so if this card's documents are wrong or missing, so is every task built from it.

After creation: tell stakeholder "Opened an analiz task for the system-architect to investigate [topic]. It will come back to you in Analiz Review to approve the plan before any implementation task is created."
