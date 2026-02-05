---
name: jomonsho-bootstrap
description: Jomonsho の前提資料を読み、変更前に制約を要約する。
metadata:
  short-description: 変更前にAGENTS/docsを読む前提を徹底する。
---

# Jomonsho Bootstrap（日本語）

このスキルが呼ばれたら、変更前に必ず以下を実施する。

1) 次のファイルを読み、要約する:
   - AGENTS.md
   - docs/GAME_LOGIC_OVERVIEW.md
   - docs/OPERATIONS.md
   - docs/DEBUG_METRICS.md
   - CLAUDE.md

2) 破ってはいけない制約を明示する:
   - Firestore/RTDB writes must go through lib/game/service.ts or server APIs.
   - Presence uses RTDB only (no Firestore lastSeen fallback).
   - FSM (XState) is always on; no legacy flags.
   - Pixi/GSAP cleanup and reduced-motion handling required.

3) 主要ライブラリ (Next.js/React/XState/Firebase/Stripe/Pixi/GSAP/Chakra) を触る場合は、
   変更前に Context7 のドキュメントを参照する。

4) 環境制約 (エミュレータ使用、workers=1、E2E 2回連続など) をユーザーと確認する。

出力:
- 制約と進め方の短い箇条書き。
