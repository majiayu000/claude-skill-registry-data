---
name: mui
description: Material UI — accessible React + Material Design; official MCP.
---

## Detection Signals

- `@mui/material` in `package.json`
- `@emotion/react` and `@emotion/styled` dependencies
- `ThemeProvider`, `createTheme` imports in codebase
- `CssBaseline` component at app root
- `sx` prop usage on components

## MCP Setup

MUI has an official MCP server for component docs, prop references, examples, and theming.

**Add to `.claude/settings.json`**:

```json
{
  "mcpServers": {
    "mui": {
      "command": "npx",
      "args": ["-y", "@mui/mcp@latest"]
    }
  }
}
```

> If auto-configuration fails, ask the user to add the entry manually in their CLI's MCP settings (**Claude Code → Settings → MCP Servers**, the `mcp` block of `opencode.json`, or Codex CLI's MCP config). The MCP provides real-time component API access without leaving the editor.

## Core Concepts

| Concept | Detail |
|---------|--------|
| **ThemeProvider** | Wraps the app; all components read theme tokens from it |
| **`sx` prop** | Inline styling via theme tokens — preferred over `style` or CSS classes |
| **`createTheme()`** | Extends/overrides Material Design defaults |
| **Emotion** | CSS-in-JS engine used internally — don't mix with other CSS-in-JS libs |
| **Breakpoints** | `xs` (0px), `sm` (600px), `md` (900px), `lg` (1200px), `xl` (1536px) |
| **`useTheme()`** | Access theme tokens inside component logic |

## Component Patterns

```tsx
// sx prop — use theme tokens, not raw values
<Box sx={{ p: 2, bgcolor: 'background.paper', borderRadius: 1 }}>

// Responsive values via sx
<Typography sx={{ fontSize: { xs: '1rem', md: '1.25rem' } }} />

// Theme extension — brand decisions belong here, not in CSS files
const theme = createTheme({
  palette: { primary: { main: '#1976d2' } },
  typography: { fontFamily: '"Inter", sans-serif' },
})

// Grid2 (v5+) — the deprecated Grid has been replaced
import Grid from '@mui/material/Grid2'
<Grid container spacing={2}>
  <Grid size={6}><Item /></Grid>
</Grid>
```

## Critical Rules

- **ThemeProvider is mandatory** at app root — components without it fall back to defaults and look inconsistent
- **Use `sx` over `style`** — `sx` resolves theme tokens, breakpoints, and pseudo-selectors; `style` does not
- **Extend via `createTheme()`** — put all brand decisions there, not in global CSS overrides
- **Use `Grid2`** (not the legacy `Grid`) in MUI v5+
- **Check MUI version** before writing code — v5 and v6 have significant API differences; look at `package.json`
- **Never mix Emotion with other CSS-in-JS** — style conflicts are hard to debug and runtime cost doubles
