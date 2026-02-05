---
name: workflow
description: Automation workflow with OpenSpec
---

# Automation Workflow with OpenSpec

Automated workflow that chains $openspec-proposal, $openspec-apply, and $openspec-archive with self-review and git commits at each stage.
Since this is an automation flow, you must run without human interaction as much as possible.

## Workflow

Execute these steps in order:

### 1. Generate Proposal

- Run the $openspec-proposal skill with the user's feature description
- Self-review the generated proposal for completeness and correctness
- If issues found, iterate on the proposal

### 2. Commit Proposal

Commit with `-m "openspec:proposal for <feature>"`
This creates a checkpoint.
User can revert here if implementation is not satisfactory.
So you can go to next step without confirmation.

### 3. Apply Implementation

- Run the $openspec-apply skill to implement the proposal
- Self-review the implementation

### 4. Run Lint & Test

Confirm both lint and test pass.

If they fail, fix issues and run lint and test again until they pass.

### 5. Commit Implementation

Commit with `-m "openspec:apply for <feature>"`

### 6. Archive Spec

- Run the $openspec-archive skill to archive the completed spec

### 7. Commit Archive

Commit with `-m "openspec:archive"`
