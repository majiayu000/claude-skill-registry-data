---
name: implement-secret-phase
description: Use when implementing any secret phase in Salem 1692 — dawn (black cat placement), night witch vote, or constable save. Encodes the full identity masking pattern using the acting flag. Every secret phase must follow this pattern exactly or players will be able to identify witches by observing phone behavior.
---

# Implement Secret Phase

A secret phase is any game moment where specific players act secretly while
all other players must appear to be doing the same thing.

**Current secret phases:**
- Dawn — witches place the black cat
- Night witch vote — witches select elimination target
- Night constable save — constable selects player to protect

## The Core Invariant

From the outside, every phone must look identical at every moment of a secret
phase. Same screen. Same buttons. Same confirmation animation. Same waiting state.

## Step 1 — Define the Acting Condition

State explicitly before writing any code:
- Who are the acting players?
- What is their action?
- What happens to their submission?
- What is the timeout? (30–45 seconds recommended)

## Step 2 — Define the Prompt Payload

```js
{
  promptType: 'night_vote',
  targets: ['Alice', 'Bob', 'Carlos'],
  timeoutMs: 45000,
  acting: true | false   // THE ONLY DIFFERENCE BETWEEN PLAYERS
}
```

## Step 3 — Server: Send Prompt to ALL Players

```js
playerSockets.forEach(socket => {
  const isActing = determineActing(game, socket.playerId, promptType);
  socket.emit('secret_phase_prompt', {
    promptType,
    targets: getValidTargets(game, promptType),
    timeoutMs,
    acting: isActing
  });
});
```

NEVER send the prompt only to acting players. Send it to everyone.

## Step 4 — Server: Filter Submissions

```js
socket.on('secret_phase_submit', ({ selection }) => {
  const isActing = determineActing(game, socket.playerId, game.currentPhase);
  if (!isActing) return; // Silently discard — no error, no different response
  game.recordPhaseSubmission(socket.playerId, selection);
  if (game.allActingPlayersSubmitted()) {
    clearTimeout(game.phaseTimeout);
    resolveSecretPhase(socket.roomCode, game.currentPhase);
  }
});
```

## Step 5 — Web Client: Render Identically

```jsx
function SecretPhasePrompt({ promptType, targets, timeoutMs, acting }) {
  const [submitted, setSubmitted] = useState(false);

  function handleSubmit() {
    setSubmitted(true); // Show confirmation for EVERYONE
    socket.emit('secret_phase_submit', { selection: selected });
    // Server silently discards if acting === false
  }

  if (submitted) return <WaitingState />; // IDENTICAL for all players

  return (
    <PromptScreen
      title={getPromptTitle(promptType)}
      targets={targets}
      onSubmit={handleSubmit}
      timeoutMs={timeoutMs}
    />
    // DO NOT conditionally render anything based on the acting flag
  );
}
```

## Step 6 — Parallel Phases (Night Only)

Witch vote and constable save run simultaneously:

```js
const [witchTarget, constableSave] = await Promise.all([
  waitForWitchVote(roomCode),
  waitForConstableSave(roomCode)
]);
openConfessWindow(roomCode);
```

## Step 7 — Test the Non-Acting Path Explicitly

- [ ] Non-witch receives prompt with `acting: false`
- [ ] Non-witch submission is silently discarded by server
- [ ] Non-witch sees same confirmation animation as witch
- [ ] Timing of waiting state is identical for both paths