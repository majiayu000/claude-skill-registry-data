---
name: ticket
description: Creating an Azure DevOps work item or posting a comment with the obvious `az boards` command silently stores HTML that cannot be fixed afterward. Use this instead. Also covers reading a work item and transitioning its state. Trigger on "create ticket", "new work item", "comment on #N", "show ticket", "set ticket cr", "/dev-azdo:ticket".
argument-hint: <show|create|comment|state> <id> …
---

# Ticket (Azure DevOps work item)

Multi-op skill. Pick the op from the intent of the request, read its reference, run the steps,
report the result.

Shared rules (org/project resolution, approval gate, writing, request bodies) live in
`${CLAUDE_PLUGIN_ROOT}/references/conventions.md`. Read it before the first op.

## Dispatch

| Op          | Input                                                                                           | Reference                                   |
| ----------- | ----------------------------------------------------------------------------------------------- | ------------------------------------------- |
| **show**    | work item id                                                                                    | `${CLAUDE_SKILL_DIR}/references/show.md`    |
| **create**  | what the item is about, optionally its type, parent, tags, and a description or a file with one | `${CLAUDE_SKILL_DIR}/references/create.md`  |
| **comment** | work item id and the comment text or a file with it, or which comment to update or delete       | `${CLAUDE_SKILL_DIR}/references/comment.md` |
| **state**   | work item id and the target state, or none to get the next state proposed                       | `${CLAUDE_SKILL_DIR}/references/state.md`   |

Ambiguous intent, or an op with no id where one is required: ask. An id plus a state name with
no other intent means `state`.

`create` and `comment` write to a shared board under the user's name. Both go through the
approval gate. Do not skip it.

## Notes

- Branch creation lives in `dev-azdo:feature-branch`, which offers `ticket state <id> active`
  after branching.
- `dev-azdo:pr` offers `state <id> cr` after creating a PR and the next state after completing one.
- Pull-request threads are a different API. Use `dev-azdo:pr` (`comments` op).
