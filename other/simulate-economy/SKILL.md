---
name: simulate-economy
description: Run headless bot simulations against the Colyseus game server to test economy balance, levelling progression, daily wages, sidewalk rent, and multi-player interactions. Use this skill whenever the user says "chạy giả lập", "test kinh tế", "mô phỏng người chơi", "kiểm tra bot", "kiểm tra lạm phát", "stress test", or wants to verify an economy change under real server conditions.
---

# Simulate the economy with headless bots

Vỉa Hè Online uses headless client bots powered by `@colyseus/sdk` to test real game server behavior without needing Unity. The primary test runner lives in `server/test/simulation.ts`.

## How the Simulation Works

1. **Server connection**: Connects to the Colyseus server over WebSocket (`ws://localhost:2567`).
2. **Virtual accounts**: Spawns multiple simulated players (e.g., `An`, `Bình`) via `/api/login`.
3. **Room join**: Each player joins a district room (`street`).
4. **Action simulation**: Bots send real client messages:
   - `createCharacter`: Sets gender and appearance layers.
   - `plant`: Sows crops on empty lots.
   - `water`: Waters crops to reduce grow time.
   - `harvest`: Collects ripe crops into store inventory.
   - `openStall`: Opens sidewalk stalls and stocks goods.
   - `inviteCustomer`: Pulls passing customers to test conversion and stamina cost.
   - `hire` / `fire`: Recruits employees and measures wage impact.
   - `buyVehicle` / `fillOrder`: Dispatches delivery vehicles.

## Running the Simulation

The simulation requires a running server:

```bash
# Terminal 1: Start the game server
cd server && npm start
```

```bash
# Terminal 2: Run the simulation suite
cd server && npm test
```

For isolated rule checks on a fake clock without starting the server, run:
```bash
cd server && npm run test:world
cd server && npm run test:garden
```

## Adding a Simulation Scenario

To test a new economic condition or edge case in `server/test/simulation.ts`:

```ts
// Example: Test hiring employee and passive sales
A.room.send('hire', { candidateId: 'emp_1' });
await wait(300);
check(A.profile.employees.length > 0, 'An hires an employee');

// Verify stall operation with employee
A.room.send('openStall', { slot: 2, productId: 'iced_tea', quantity: 10, employeeId: 'emp_1' });
await wait(300);
check(A.room.state.stalls.get(2)?.sellerId === 'emp_1', 'Employee mans the stall');
```

## Health Indicators to Check

1. **Starting Capital Safety**: New players starting with 500,000đ must never go bankrupt before their first banana harvest ripens.
2. **Sidewalk Fee Fairness**: When Player B sells on Player A's street, 10% fee transfers correctly to Player A without rounding errors or negative balances.
3. **Wage Deductions**: Daily employee wages (`BALANCE.employeeDailyWage`) must deduct once every 24h cycle and never push money below 0.
4. **Loot & XP Progression**: XP gains per sale must cleanly follow `PRODUCTS` table values without level skip glitches.

## Sync Skills

```bash
node tools/sync-skills.mjs
```

