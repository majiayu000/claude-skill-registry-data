---
name: maceff-todo-restoration
description: USE IMMEDIATELY when user reports TODO accessibility issues or session migration detected. Restores TODO context using policy-guided recovery.
allowed-tools: Read, Bash, Grep, TodoWrite
---

## User Trustworthiness Principle

**CRITICAL**: When user reports TODO accessibility issues, **TRUST THEM UNCONDITIONALLY**.

The user's UI is DISCONNECTED after session migration. You may see TODOs in system-reminders but the user cannot. Only TodoWrite reconnects their UI.

---

## Policy Engagement

```bash
macf_tools policy navigate todo_hygiene
```

Scan for sections about TODO backup and recovery mechanisms. Read those sections.

---

## Questions to Extract

1. What recovery mechanisms does the policy define?
2. How does the policy prioritize them?
3. What tools and formats enable direct restoration?
4. What minimum pending item requirement must restored lists satisfy?

---

## Execution

Apply the recovery workflow discovered from policy reading. Invoke TodoWrite with restored state.

---

## Version History

- v3.1 (2025-12-19): Radically minimal rewrite. Skill provides questions, policy provides answers.
- v3.0 (2025-12-19): Policy as API rewrite with extractive questions.
- v2.0 (2025-11-26): Three-tier recovery with event log intelligence.
- v1.0 (2025-11-18): Initial implementation.
