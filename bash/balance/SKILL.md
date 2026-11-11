---
name: balance
description: Tune and verify Vỉa Hè Online's economy — product prices, wearable prices, the BALANCE constants, the levelling curve, the sidewalk fee, employee costs. Use this skill when the user says "game dễ quá", "khó quá", "lên cấp chậm", "nhiều tiền quá", "món này vô dụng", "cân bằng lại", or wants to change any number in server/src/data.ts. It bundles a script that prints the profit table, so measure instead of guessing — run it before touching a number and again afterwards.
---

# Balance the economy

Every number that decides difficulty lives in `server/src/data.ts`: `PRODUCTS`, `WEARABLES`,
`BALANCE`, and the three functions at the end of the file (`xpToLevelUp`,
`maxEmployeesForLevel`, `hireCost`). The client keeps no copy — it requests the catalog over
the `catalog` message — so one edit covers both sides.

The trap is that these numbers feed each other: lowering a product's `sellSeconds` raises both
money per second and XP per second, so it makes players richer *and* faster to level at once.
Hence: measure, change one group of numbers, measure again.

## Step 1 — Measure what you have

```bash
cd server && npx tsx ../.agents/skills/balance/scripts/profit-table.ts
```

The script imports `data.ts` directly, so it can never drift from the code. It prints:

- **The product table** sorted by profit per second, with XP per second and the capital a full
  stall needs (20 portions).
- **The levelling curve**: XP required per level and the minutes of nonstop selling it takes,
  using the best product unlocked at that level.
- Wardrobe totals, employee hiring costs, and the street constants.

Two things to look for in the output:

1. **Dead products** — a high `unlockLevel` with lower profit per second than something
   unlocked earlier. Players level up, unlock it, and keep selling the old thing; the reward
   for levelling evaporates.
2. **Level walls** — the minutes-per-level jumping sharply between adjacent levels while the
   best product stays the same. That level is pure waiting.

## Step 2 — Change numbers, with these principles

- **Profit per second must rise with `unlockLevel`.** It is the only thread pulling players
  up the levels.
- **Capital is the brake.** A high-profit product should need a large `cost × 20`, so players
  must save up before they can stock a full stall. Compare against
  `BALANCE.startingMoney` (200,000đ) to see what a newcomer can actually set up.
- **Short `sellSeconds` is stronger than it looks.** A stall serves one customer at a time, so
  `sellSeconds` *is* the stall's throughput. Going from 4 to 2 doubles everything.
- **Do not tune difficulty with `customerSpawnSeconds` or `maxCustomers`.** Those set the
  footfall of the whole street, currently matched to 8 slots. Loosen them and everyone gets
  rich; tighten them and players fight over customers, with latecomers selling nothing. Fix
  prices first and leave these two for last.
- **`sidewalkFeePct` is a social number, not an economic one.** It decides whether visiting
  someone else's street is worth it, and how being skimmed feels to the owner. Reason about
  both sides' feelings rather than the profit table.
- **Wearables stack.** `moneyPct` and `charm` from hat + shirt + pants + accessory add up; the
  script prints the totals so a full set holds no surprises.

## Step 3 — Measure again and play it

Re-run the script, then check against the real server:

```bash
cd server && npm start      # separate window
cd server && npm test
```

`test/simulation.ts` has two simulated players open stalls, sell, skim customers and pay the
sidewalk fee. Some of its assertions hard-code amounts (`remaining * 7000`, `binhSold * 3000`),
so **changing the price of trà đá or bánh mì means updating those numbers in the test** — or it
fails without the game being wrong. Read `test/simulation.ts` before touching level-1 prices.

Report a change worth keeping as a before/after with numbers:
"Hoa tươi: profit/s 7,000 → 5,200; reaching level 6 goes from 20 to 27 minutes."
Numbers the user can compare are what makes the call reviewable; "rebalanced" is not.

## Existing players' data

The numbers in `data.ts` are only the catalog; each player's money, level and wardrobe live in
`server/data/game.db` (SQLite, managed by the profile module). Cutting a product's price does
**not** claw back money players already earned — so after a heavy pass, ask the user whether
they want `game.db` deleted for a clean start. Do not delete it on your own.
