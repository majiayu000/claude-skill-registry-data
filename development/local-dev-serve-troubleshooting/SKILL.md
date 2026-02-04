---
name: local-dev-serve-troubleshooting
description: Use this to run and debug the UI + server locally (Vite dev server, `lotar serve`, ports, SSE).
---

## Common local dev setups

### UI fast loop (Vite dev server)

- Start UI:
  - `npm run dev`

- In another terminal, start the Rust server:
  - `cargo run -- serve --port 8080`

Notes:
- `lotar serve` port must be set with `--port` (the short `-p` is reserved for the global `--project` flag).
  - Correct: `lotar serve --port 9000`
  - Also accepted: `lotar serve 9000` (positional port; kept for backward compatibility)
  - Incorrect (sets project, not port): `lotar serve -p 9000`
  - See: `docs/help/serve.md`

### Production-like UI (embedded/static bundle)

- Build web assets:
  - `npm run build:web`
- Build the binary:
  - `cargo build --release`
- Run:
  - `./target/release/lotar serve --port 8080`

## Debugging tips

- If the UI isn’t updating, confirm SSE is connected (`GET /api/events`). See `docs/help/sse.md`.
- If you’re working on REST handlers, use `docs/help/api-quick-reference.md` and keep `docs/openapi.json` in sync for contract changes.
- When chasing server behavior, enable logs:
  - `RUST_LOG=debug cargo run -- serve --port 8080`

## Safety

- Treat `.env*` and local config as sensitive; don’t paste secrets/PII into logs/issues.
