---
name: implementing-optimistic-updates
description: Teaches useOptimistic hook for immediate UI updates during async operations in React 19. Use when implementing optimistic UI patterns, instant feedback, or reducing perceived latency.
allowed-tools: Read, Write, Edit
version: 1.0.0
---

# Optimistic UI Updates with useOptimistic

<role>
This skill teaches you how to use React 19's `useOptimistic` hook for immediate UI feedback during async operations.
</role>

<when-to-activate>
- User mentions optimistic updates, instant feedback, or perceived performance
- Working with mutations that should feel instant (likes, comments, todos)
- Need to show pending states before server confirmation
</when-to-activate>

<overview>
`useOptimistic` enables immediate UI updates that revert if the operation fails:

1. Shows anticipated result immediately
2. Reverts to actual state when async completes
3. Provides better UX than waiting for server
4. Works with `startTransition` for async operations
</overview>

<workflow>
## Basic Pattern

```javascript
import { useOptimistic, startTransition } from 'react';

function MessageList({ messages, sendMessage }) {
  const [optimisticMessages, addOptimisticMessage] = useOptimistic(
    messages,
    (state, newMessage) => [...state, { ...newMessage, sending: true }]
  );

  const handleSend = async (text) => {
    addOptimisticMessage({ id: Date.now(), text });

    startTransition(async () => {
      await sendMessage(text);
    });
  };

  return (
    <ul>
      {optimisticMessages.map((msg) => (
        <li key={msg.id}>
          {msg.text} {msg.sending && <small>(Sending...)</small>}
        </li>
      ))}
    </ul>
  );
}
```
</workflow>

<examples>
## Like Button Example

```javascript
function LikeButton({ postId, initialLikes }) {
  const [optimisticLikes, addOptimisticLike] = useOptimistic(
    initialLikes,
    (state, amount) => state + amount
  );

  const handleLike = async () => {
    addOptimisticLike(1);

    startTransition(async () => {
      await fetch(`/api/posts/${postId}/like`, { method: 'POST' });
    });
  };

  return (
    <button onClick={handleLike}>
      ❤️ {optimisticLikes}
    </button>
  );
}
```

For comprehensive useOptimistic documentation, see: `research/react-19-comprehensive.md` lines 182-240.
</examples>

<constraints>
## MUST
- Keep update function pure (no side effects)
- Pair with `startTransition` for async operations
- Provide visual feedback for pending states

## NEVER
- Mutate state directly in update function
- Use for critical operations that must succeed
- Skip error handling for failed optimistic updates
</constraints>

<related-skills>
## Related Skills

If handling Prisma transaction errors in optimistic updates, use the handling-transaction-errors skill from prisma-6 for graceful P-code error handling.
</related-skills>
