---
name: add-quest
description: Add a neighbour or edit neighbour quests in Vỉa Hè Online — touches NEIGHBOURS in server/src/stories.ts, the mechanical reward in server/src/world.ts, the portrait in client/Tools/sprites.js, and tests. Use this skill whenever the user wants a new neighbour, says "thêm hàng xóm", "thêm nhiệm vụ", "câu chuyện hàng xóm", "nhiệm vụ mới", "bác tổ dân phố", "cô ve chai", or wants to change an existing neighbour's quests or friendship 5 reward.
---

# Add a neighbour or quest

Neighbours give Vỉa Hè Online its neighborhood soul. Five fictional characters live in `server/src/stories.ts`, each with five sequential quests and a friendship 5 perk.

Adding or editing a neighbour touches multiple files across server and client. Follow these steps in order so the server, client UI, sprite library, and unit tests stay in sync.

## Step 1 — Declare the neighbour in `server/src/stories.ts`

`NEIGHBOURS` array in `server/src/stories.ts` is the single source of truth. The server sends this array to the client inside the `catalog` message payload, so the client's Neighbour window (`GameExpansion.cs`) populates automatically.

```ts
export interface Neighbour {
  id: string;        // lowercase snake_case English identifier, e.g. 'guard', 'scrap_collector'
  name: string;      // Vietnamese player-facing name, e.g. 'Bác bảo vệ', 'Cô ve chai'
  portrait: string;  // Sprite key, conventionally 'npc_<id>', e.g. 'npc_guard'
  likes: string;     // Item id liked as daily gift (from PRODUCTS, CROPS, or RECIPES in data.ts)
  reward: string;    // Vietnamese player-facing description of the friendship 5 reward
  quests: Quest[];   // Array of 5 sequential quests
}
```

### Supported Quest Types

Every quest has a `text`, a `type`, an optional `item`, and a `target`:

| QuestType | Purpose | `item` needed? | Example |
|---|---|---|---|
| `give` | Player hands over items from store inventory | **Yes** (must match key in store) | `{ text: 'Cho chú 5 ổ chuối chiên lót dạ.', type: 'give', item: 'fried_banana', target: 5 }` |
| `harvest` | Harvest any crop, or a specific crop | Optional (if omitted, any crop counts) | `{ text: 'Cháu thu hoạch thử 2 luống xem đất tốt không.', type: 'harvest', target: 2 }` |
| `sell` | Sell items at sidewalk stalls | No | `{ text: 'Cháu bán 20 phần hàng cho phố xôm tụ.', type: 'sell', target: 20 }` |
| `cook` | Cook food at the Bếp nhà (kitchen) | Optional (if specified, only that dish counts) | `{ text: 'Thử nấu một mẻ chè chuối ở Bếp nhà xem nào.', type: 'cook', item: 'banana_soup', target: 1 }` |
| `visit` | Take the bus to visit another player's street | No | `{ text: 'Cháu sang thăm một phố khác cho biết hàng xóm.', type: 'visit', target: 1 }` |
| `help` | Water or fertilize crops on a friend's street | No | `{ text: 'Cháu tưới giúp vườn một nhà nhé.', type: 'help', target: 1 }` |
| `build` | Construct a new building on an empty lot | No | `{ text: 'Cháu dựng một công trình đầu tiên đi.', type: 'build', target: 1 }` |
| `deliver` | Send a delivery order (needs a vehicle) | Optional order kind: `near`, `far` or `bulk` (if omitted, any kind counts) | `{ text: 'Gửi một đơn xa, anh chỉ đường cho.', type: 'deliver', item: 'far', target: 1 }` |

### Dialogue & Tone Guidelines

- **Player-facing text is Vietnamese** (project rule in `AGENTS.md`).
- Keep lines concise, warm, and authentic to Vietnamese urban street life. Characters should speak naturally according to their age and role (e.g. bác, chú, cô, anh, em, cháu).
- Quests 1 to 5 should scale gently in target and depth.

## Step 2 — Wire the Friendship 5 Perk in `server/src/world.ts` (Optional)

If the neighbour unlocks a functional gameplay perk upon reaching Friendship level 5 (`friendship(profile, '<id>') >= 5`), connect it in `server/src/world.ts`:

- **Building discount**: check `friendship(profile, '<id>') >= 5` inside `buildCost()`.
- **Seed discount**: check inside `seedCost()`.
- **Vehicle unlock**: set `needsFriend: '<id>'` in `VEHICLES` (`data.ts`).
- **Recipe unlock**: set `needsFriend: '<id>'` in `RECIPES` (`data.ts`).
- **Delivery bonus**: check inside `fillOrder()` or `claimDelivery()`.

If the reward is cosmetic or narrative, you only need the description string in `reward`.

## Step 3 — Draw the portrait in `client/Tools/sprites.js`

Add the portrait drawing function in `client/Tools/sprites.js` using the standard `portrait(...)` helper:

```js
portrait('npc_<id>', '<skinColorHex>', '<hairSvgPath>', '<shirtColorHex>', (g) => {
  // Optional extra accessories (e.g. hat, glasses, badge) drawn onto canvas context `g`
});
```

Dimensions for NPC portraits are `200x200` px.

## Step 4 — Export Sprites

Follow the standard export procedure:
1. Run `node client/Tools/export-server.mjs`.
2. Open `http://localhost:5181/` in a browser.
3. Call `exportSprites()` in the DevTools console.
4. In Unity, select **Via He → Reimport Sprites**.

## Step 5 — Update Tests

In `server/test/world.ts`, check the assertion:
```ts
check(S.NEIGHBOURS.length >= 5 && S.NEIGHBOURS.every((n) => n.quests.length === 5), 'Neighbours have five quests');
```
If adding a 6th neighbour, ensure `S.NEIGHBOURS.length >= 5` allows the test to pass.

Run the test suite:
```bash
cd server && npm run test:world
```

## Step 6 — Sync Skills

Always sync skills across agent directories:
```bash
node tools/sync-skills.mjs
```
