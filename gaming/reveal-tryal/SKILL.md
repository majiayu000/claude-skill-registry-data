---
name: reveal-tryal
description: Use when implementing any code path that causes a tryal card to be revealed — accusation reaching 7, night elimination, confession, or conspiracy step 1. Handles win condition checks, multiple-witch-card logic, synchronized animation across host and mirror screens, and correct state broadcast order.
---

# Reveal Tryal

## The Reveal Sequence (Always This Order)
1. Determine which tryal card is being revealed
2. Update game state (mark card as revealed)
3. Check win conditions
4. Broadcast phase_resolve timestamp to host + mirrors
5. Broadcast updated game_state_update to all clients

Win conditions are checked BEFORE the animation plays. Never let gameplay
proceed after a win condition is met.

## Step 1 — Determine Which Card

- **7th accusation** — accusing player chooses which tryal to reveal (async input)
- **Night elimination** — reveal all remaining tryals (player eliminated)
- **Confession** — confessing player selects their own tryal
- **Conspiracy step 1** — black cat owner's tryal; if they drew conspiracy, they choose

## Step 2 — Handle Multiple Witch Cards

```js
const remainingWitchCards = game.players[targetPlayerId].tryals.filter(
  t => t.type === 'witch' && !t.revealed
);

if (tryal.type === 'witch' && remainingWitchCards.length > 0) {
  game.pendingAnnouncement = {
    playerId: targetPlayerId,
    message: 'has_more_witch_cards'
  };
  // Do NOT eliminate the player
}
```

## Step 3 — Check Win Conditions

```js
function checkWinConditions(game) {
  const allWitchTryals = getAllWitchTryals(game);
  if (allWitchTryals.every(t => t.revealed)) {
    return { gameOver: true, winner: 'townspeople' };
  }
  const activePlayers = getActivePlayers(game);
  if (activePlayers.every(p => p.isWitch)) {
    return { gameOver: true, winner: 'witches',
             loser: game.lastPlayerToBecomeWitch };
  }
  return { gameOver: false };
}
```

Call after: every tryal reveal, every elimination, every conspiracy resolution.

## Step 4 — Synchronized Animation via phase_resolve

```js
const revealAt = Date.now() + 3000;

// Send to host + mirrors only
getDisplaySockets(roomCode).forEach(s => s.emit('phase_resolve', {
  type: 'tryal_reveal',
  revealAt,
  targetPlayerId,
  tryalIndex,
  tryalType: tryal.type
}));
```

**Unity:**
```csharp
float delay = (revealAt - DateTimeOffset.UtcNow.ToUnixTimeMilliseconds()) / 1000f;
StartCoroutine(PlayRevealAnimationAfter(delay, data));
```

**Mirror browser:**
```js
socket.on('phase_resolve', ({ revealAt, ...data }) => {
  const delay = revealAt - Date.now();
  setTimeout(() => playRevealAnimation(data), Math.max(0, delay));
});
```

Never trigger reveal animations on message receipt — always use the timestamp.

## Step 5 — Test

- [ ] Revealing a not-a-witch card: game continues, no announcement
- [ ] Revealing last witch card: player eliminated, win check runs
- [ ] Revealing non-last witch card: announcement fires, player NOT eliminated
- [ ] All witch cards revealed: townspeople win fires immediately
- [ ] phase_resolve timestamp used — animation does not fire on message receipt
- [ ] Mirror animates within 100ms of host in a two-device test