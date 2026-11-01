---
name: playtest-game
description: Play CampusCove's /game in the built-in browser pane to prove a change works — throwaway test player, faking pointer lock, walking and turning by script, a second player for multiplayer, collision overlay, logs and the code gates. Use after any change to the game, socket, assets or game-facing API, before reporting it done.
---

# Playtest CampusCove

## 0. Stack up

```bash
docker ps --format '{{.Names}} {{.Status}}'      # campuscove-front / -backend / -socket / -db
make up                                          # if not running
```

Front http://localhost:5173 (Vite HMR), API http://localhost:8000/api, socket :3000 (`node --watch`, restarts on
save), Postgres :5432. New migration → `make migrate`. Seeds → `make seed`.

## 1. Throwaway player (local only)

Open the pane with `preview_start {url: "http://localhost:5173/"}` (the Docker front is already serving; do not
start a second Vite). Then run in the page with `javascript_tool`:

```js
const rnd = () => crypto.getRandomValues(new Uint32Array(2)).join('').slice(0, 12)
const u = 'pt_' + rnd().slice(0, 6), p = rnd() + 'Aa!'
const r = await fetch('http://localhost:8000/api/register', { method: 'POST',
  headers: { Accept: 'application/json', 'Content-Type': 'application/json' },
  body: JSON.stringify({ email: u + '@campuscove.test', username: u, password: p, password_confirmation: p, accepted_terms: true, age_confirmed: true }) })
const d = await r.json()
if (r.ok) localStorage.setItem('campus_cove_auth', JSON.stringify({ user: d.user, token: d.token }))
;({ status: r.status, account_id: d.user?.account_id })
```

The password is random and thrown away: a new player per session is cheaper than remembering one. Give it
what the test needs with `make set-money ACCOUNT=<id> CURRENCY=coins SUM=5000`, `make set-admin EMAIL=<u>@campuscove.test`,
`make fill-outfit ACCOUNT=<id>`. After `set-admin` the stored user is stale; refresh it in the page:

```js
const a = JSON.parse(localStorage.getItem('campus_cove_auth'))
const r = await fetch('http://localhost:8000/api/user', { headers: { Accept: 'application/json', Authorization: 'Bearer ' + a.token } })
a.user = (await r.json()).user
localStorage.setItem('campus_cove_auth', JSON.stringify(a))
```

Then `navigate` to `/game` and wait ~5 s for the town to load.

## 2. Drive the game

Real pointer lock never engages in the pane (the Play overlay stays). Fake it — movement, mouse look and
left-click interactions are gated on `document.pointerLockElement === canvas` (`useGameMovement.ts`):

```js
const c = document.querySelector('canvas')
Object.defineProperty(document, 'pointerLockElement', { configurable: true, get: () => c })
document.dispatchEvent(new Event('pointerlockchange'))
```

Input listeners are on `document`:
- Walk: `document.dispatchEvent(new KeyboardEvent('keydown', { code: 'KeyW' }))` … then `keyup`. Codes are in
  `config/keybindings.ts` (WASD/ZQSD, I interact, E inventory, K keys, F2 buy, R rotate, Digit1-9 hotbar,
  **C collision overlay**).
- Turn: `document.dispatchEvent(new MouseEvent('mousemove', { movementX: 600, movementY: 0 }))` (~90°).
- Click a door: `mousedown` on the canvas with `button: 0`, or the `I` key.
- Position: the HUD shows `XYZ x, y, z` — read it from the DOM instead of guessing from screenshots.

When the pane is **hidden** (`tabs_context` says so) `requestAnimationFrame` only advances on screenshots:
hold a key, take 2–3 small screenshots (`scale: 0.3`), then release. Timed `setTimeout` walks do not move.

## 3. Two players

Same origin = same localStorage = same account, and one session per account (the second kicks the first,
code 4001). Put player 2 on the other allowed origin: `tabs_create`, `navigate` to `http://127.0.0.1:5173/`,
run the register snippet there, then `/game`. Confirm the join with `read_network_requests`
(`urlPattern: "3000"` → `POST /matchmake/joinOrCreate/city 200`). Check that both see the change and a player in
another zone does not. Close the extra tab after.

## 4. What to look at

- `read_console_messages {onlyErrors: true}` in each tab; `docker logs --tail 50 campuscove-socket` and
  `docker logs --tail 50 campuscove-backend` for server errors.
- Screenshot proof of the feature (a door open, a prompt, the item in hand). Use the collision overlay (C) for
  any wall/door/collision change; compare against `docs/OPEN_WORLD.md` expectations.
- Edge cases the game has already broken on: background tab (dt clamp), relog after an admin change, a locked
  house with a key holder inside, a seized house (`make collect-taxes`).

## 5. Gates

```bash
cd front && npx vue-tsc -b && node --experimental-strip-types --test "src/**/*.test.ts" && npx knip
make test
```

(Host Node is 22.13: the flag is required; see skill `game-feature` §4 for the knip note.)

Report exactly what was played, what was only checked by gates, and what was not verified.
