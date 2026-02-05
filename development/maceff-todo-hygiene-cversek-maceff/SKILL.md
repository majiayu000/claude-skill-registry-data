---
name: maceff-todo-hygiene
description: Use BEFORE significant TODO modifications (adding subtrees, marking complete, reorganizing, collapsing). Ensures policy compliance through extractive questions. Run proactively when planning TODO changes.
allowed-tools: Read, Grep
---

## Policy Engagement Protocol

Navigate todo_hygiene policy using CLI tools:

1. **First access**: Get CEP navigation guide
   ```bash
   macf_tools policy navigate todo_hygiene
   ```

2. **Identify relevant sections**: Based on your planned action (adding, modifying, completing, removing)

3. **Selective read**: Read only sections relevant to your current action
   ```bash
   macf_tools policy read todo_hygiene --section N  # For specific section
   macf_tools policy read todo_hygiene --from-nav-boundary  # Skip CEP guide
   ```

**Why CLI tools**: Caching prevents redundant reads, line numbers enable precise citations.

## Questions to Extract from Policy (Action-Oriented)

**Before Adding Items:**
1. What structure requirements apply when adding new TODOs?
2. What format requirements apply to new TODO items?

**Before Modifying Items:**
3. What preservation requirements apply when editing existing TODOs?
4. What context must be maintained when reorganizing?

**Before Marking Complete:**
5. What verification is required before marking a TODO complete?
6. What must be added to completed items for traceability?
7. What minimum pending item requirement exists to prevent UI disappearance?

**Before Removing/Collapsing Items:**
8. What must happen before removing or collapsing completed work?
9. What are the requirements for reducing TODO hierarchy depth?
10. Is this cross-repo MISSION work? What determines archive location?
11. How should archive filenames identify the MISSION being archived?

**General:**
12. What documentation integration requirements exist for TODOs?
13. What backup requirements apply to significant TODO modifications?

## Execution

1. **Identify your action type**: Adding, modifying, completing, or removing
2. **Read relevant policy sections** using CEP navigation
3. **Extract requirements** for your specific action
4. **Apply requirements** to your planned TodoWrite operation

## Critical Meta-Pattern

**Policy as API**: This skill uses `macf_tools policy` CLI commands for reading policies. CLI tools handle framework path resolution, provide caching, and output line numbers for citations.

## Version History

- v1.0 (2025-11-25): Initial creation with timeless extractive questions
