---
name: implement
description: Implement all .plan files — applies each plan's described changes to its target file, following project standards exactly
disable-model-invocation: true
---

# Scalpel Implement

Apply every `.plan` file to its target source file. Follow the plan. Do not improvise. Do not skip.

## Steps

### 1. Load Project Standards

Read every standards file found, in this order:

1. `AGENTS.md`
2. `CLAUDE.md`
3. `docs/ARCHITECTURE.md`, `docs/architecture.md`, or any file matching `docs/arch*`

These define how code must be written in this project. If none exist, note that and proceed.

Do not invent standards. Only enforce what is explicitly documented.

### 2. Gather Plan Files

```bash
find . -name "*.plan" -not -path '*/.git/*' -not -path '*/node_modules/*' | sort
```

Read every plan file found. Before proceeding, resolve the target for each plan:

- If the `file` frontmatter field is present, that is the target.
- If `file` is absent, the target is the file in the same directory with the same base name and the `.plan` extension
  removed.
- If the file does not exist, treat it as a new file to be created.

### 3. Implement Each Plan

Process the plan files.

1. Read the plan's `## Change` and `type` field in full
2. Execute based on `type`:

| `type`   | Action                                                                                                                           |
|----------|----------------------------------------------------------------------------------------------------------------------------------|
| `add`    | Create the target file with the described content. If the file already exists, stop and ask the user before overwriting.         |
| `modify` | Read the current contents of the target file, then apply the change exactly as described.                                        |
| `move`   | Move the target file to the path described in `## Change`. Update any imports or references only if the plan explicitly says to. |
| `delete` | Delete the target file. Do not delete anything else.                                                                             |
| absent   | Treat as `modify`. Read the ## Change for more information on what to do.                                                        |

3. If the plan includes a code example, treat it as the intended implementation — match it precisely, do not rewrite it

**If the plan is ambiguous** — the description could reasonably be implemented more than one way — stop and ask:

```
AMBIGUOUS: <plan file>
The description can be read as:
  A) <interpretation one>
  B) <interpretation two>
Which should be implemented?
```

Wait for the user's answer before continuing.

**If the plan conflicts with a project standard** — stop and surface it:

```
CONFLICT: <plan file>
Plan says: <what the plan describes>
Standard says: <specific rule from AGENTS.md / CLAUDE.md>
How would you like to proceed?
```

**If the plan conflicts with another plan** — stop and surface it the same way.

In all cases: wait for the user's decision. Do not resolve anything silently. Do not move to the next plan until the
current one is fully resolved and implemented.

### 4. Clean Up

Once all plans are implemented:

1. Delete every `.plan` file that was processed
2. Delete `.scalpel/change.md` if it exists
3. If `.scalpel/` is now empty, delete the directory too

### 5. Report

Output a summary:

List each implemented plan with its target file and one line describing what changed.

## Rules

- Every plan gets implemented — there is no skip
- The plan file is the source of truth — implement what it says, nothing more
- Do not add improvements, refactors, or related fixes not described in the plan
- Do not delete `.plan` files or `.scalpel/change.md` until all plans are fully implemented
- Never resolve a conflict or ambiguity silently — always surface it and wait
