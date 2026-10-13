---
description: "Entry-point skill for Imperial perpetual routing on Solana. Use before answering or acting on Imperial router flows, Phoenix-routed perps, profile funding, market/portfolio intel, risk checks, TP/SL, TWAP, grid, or Telegram bot trading workflows."
---
# Imperial

Imperial is the router layer. In this project, Phoenix is the preferred default venue when the user asks to "go straight Phoenix", but execution still flows through Imperial's authenticated `mobile/*` endpoints when the bot is acting as the operator.

Use this skill first, then route to the focused Imperial skill that matches intent.

Core rules:

- Treat `IMPERIAL_API_KEY` / `IMPERIAL_JWT` as a trading credential. Never display or log it.
- Treat every profile as isolated. Always track `profileIndex`.
- Always inspect `success` in `POST /api/v1/mobile/orders` responses even on HTTP 200.
- Prefer Phoenix (`underwriter=2`) unless the user explicitly requests another venue or route data says otherwise.
- For Telegram/webhook flows, only promise durable strategy execution when a real runner exists. Do not present a stateless webhook as a TWAP/grid engine.

See also: `imperial-skills-index`.
