---
name: jomonsho-repo-map
description: Jomonsho の主要ファイル・層・入口の早見表。
metadata:
  short-description: リポジトリ地図とガードレール。
---

# Jomonsho Repo Map（日本語）

編集前の方針確認に使う:

主要アーキテクチャ:
- Domain logic: lib/game/domain.ts
- Service layer (writes): lib/game/service.ts
- Server-authoritative API: app/api/rooms/* and lib/server/roomCommands.ts
- State machine: lib/state/roomMachine.ts (always on)
- Presence: RTDB only (lib/firebase/presence.ts, lib/hooks/useParticipants.ts)

主要 UI:
- Room view: app/rooms/[roomId]/_components/RoomLayout.tsx
- Spectator UI: components/ui/SpectatorNotice.tsx, lib/hooks/useSpectatorGate.ts
- Pixi background: components/ui/PixiBackground.tsx, lib/pixi/*

ガードレール:
- No direct Firestore/RTDB writes from UI (use service/API).
- Presence is RTDB only.
- Keep Pixi/GSAP cleanup and reduced-motion support.
- Add traceAction/traceError for important changes.
