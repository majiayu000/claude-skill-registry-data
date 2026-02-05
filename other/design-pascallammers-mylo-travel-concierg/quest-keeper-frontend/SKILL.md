---
name: quest-keeper-frontend
description: Frontend development skill for Quest Keeper AI Tauri application. Use when working on React components, Zustand stores, Three.js battlemaps, TailwindCSS styling, or Tauri shell integration. Triggers on mentions of frontend, React, Zustand, Three.js, battlemap, UI, viewport, or Tauri.
---

# Quest Keeper Frontend Development

## Location
```
C:\Users\mnehm\Desktop\Quest Keeper AI attempt 2
```

## Tech Stack
- **Framework**: Tauri 2.x (Rust shell + WebView)
- **UI**: React 19 + TypeScript + Vite
- **State**: Zustand stores
- **3D**: Three.js via @react-three/fiber
- **Styling**: TailwindCSS (terminal/CRT aesthetic)

## Directory Structure
```
src/
├── components/
│   ├── viewport/     # BattlemapCanvas, CharacterSheet, WorldMap
│   ├── adventure/    # Main layout (AdventureView.tsx)
│   ├── terminal/     # Chat interface
│   └── sidebar/      # Navigation
├── stores/           # Zustand state management
├── services/         # MCP client, LLM providers
├── hooks/            # Custom React hooks
└── utils/            # Helpers
```

## Key Commands
```powershell
npm run tauri dev     # Development with hot reload
npm run build         # Production build
```

## MCP Response Parsing
```typescript
import { parseMcpResponse } from '@/utils/mcpUtils';
const result = await mcpClient.callTool('get_character', { id });
const character = parseMcpResponse<Character>(result, null);
```

## Terminal/CRT Aesthetic
Key classes: `terminal-green`, `terminal-dim`, `terminal-dark`, `crt-glow`, `font-mono`