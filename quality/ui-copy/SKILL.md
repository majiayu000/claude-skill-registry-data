---
name: ui-copy
description: Write interface copy that makes controls, state, consequences, errors, empty states, permissions, confirmation, and recovery understandable at the moment of action.
---
# UI Copy

Use when product interfaces need labels, helper text, validation, errors, status, empty states, confirmation, or other concise user-facing language.

## Procedure
1. Define the user goal, product state, action, consequence, and knowledge the interface can safely assume.
2. Name controls by the action or destination users expect, using established product terminology consistently.
3. Put instructions and prerequisites before the user needs them rather than explaining preventable errors afterward.
4. Write validation and errors to identify what happened, what can be corrected, and the next useful action without exposing internal implementation detail.
5. Make destructive, irreversible, permission-sensitive, paid, or externally visible actions explicit before confirmation.
6. Write empty and loading states around what the user can understand or do next, not decorative filler.
7. Check text expansion, localization, screen-reader context, control labels, and whether a message still makes sense when announced without surrounding visual layout.
8. Review copy in the working interface and shorten wherever context already carries the meaning.

## Decision rules
- Interface copy is part of product behavior, not decoration.
- Buttons should normally describe the action they perform.
- Error messages should support recovery.
- Concision is useful only after meaning is clear.

## Quality gate
UI copy is ready when users can identify actions and consequences, errors provide a recovery path, sensitive decisions are explicit, terminology is consistent, accessibility context remains meaningful, and the words fit the real interface without redundant explanation.