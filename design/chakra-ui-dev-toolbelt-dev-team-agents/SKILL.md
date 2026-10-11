---
name: chakra-ui
description: Chakra UI — accessible React components. v2/v3 APIs incompatible.
---

## Detection Signals

- `@chakra-ui/react` in `package.json`
- `ChakraProvider` (v2) or `Provider` (v3) at app root
- `@emotion/react` and `@emotion/styled` dependencies
- Style props on components (`p`, `m`, `color`, `bg`, `fontSize` as JSX props)
- `extendTheme` import (v2) or `createSystem` import (v3)

## MCP Setup

No official MCP server is available for Chakra UI.

> Reference the docs for the correct version:
> - v2: [v2.chakra-ui.com](https://v2.chakra-ui.com)
> - v3: [chakra-ui.com](https://www.chakra-ui.com)
>
> Configure a documentation search MCP if your CLI supports one.

## Version Detection — Do This First

```bash
# Check installed version before writing any code
cat package.json | grep "@chakra-ui/react"
```

| Signal | Version |
|--------|---------|
| `extendTheme`, `ChakraProvider` | v2 |
| `createSystem`, `Provider` | v3 |

**v2 and v3 APIs are incompatible.** Do not mix patterns. Confirm version before writing a single line.

## Core Concepts

| Concept | Detail |
|---------|--------|
| **ChakraProvider / Provider** | Wraps app — required; components without it render unstyled or throw |
| **Style props** | CSS properties as component props: `p={4}`, `color="gray.700"`, `bg="blue.50"` |
| **Color tokens** | Semantic scale: `blue.500`, `gray.100`, `red.600` — not raw hex |
| **Responsive values** | Array syntax (mobile-first): `<Box fontSize={['sm', 'md', 'lg']}>` |
| **`useColorMode()`** | Toggle dark/light; `useColorModeValue('light-val', 'dark-val')` for tokens |
| **`useTheme()`** | Access theme tokens in component logic |

## Component Patterns (v2)

```tsx
// Provider at root
import { ChakraProvider } from '@chakra-ui/react'
const theme = extendTheme({
  colors: { brand: { 500: '#3182CE' } },
  fonts: { heading: 'Inter, sans-serif' },
})
<ChakraProvider theme={theme}><App /></ChakraProvider>

// Style props — always use tokens, not hex
<Box p={4} bg="gray.50" borderRadius="md" shadow="sm">
  <Text color="gray.700" fontSize="sm" fontWeight="medium">Content</Text>
</Box>

// Responsive — array is mobile-first breakpoints
<Stack direction={['column', 'row']} spacing={4} />

// Dark mode
<Box bg={useColorModeValue('white', 'gray.800')}>
```

## Critical Rules

- **Check v2 vs v3 first** — APIs are incompatible; generating v2 code for a v3 project breaks the app
- **Provider must wrap everything** — components outside it silently use no theme
- **Use color tokens** (`gray.500`) not hex values — tokens adapt to dark/light mode automatically
- **`useColorModeValue()` for dark mode** — never hardcode separate color values for each mode
- **Prefer `Stack`/`HStack`/`VStack`** over manual `Flex` + `flexDirection` — clearer intent, less props
- **v2: don't import from sub-packages** — import from `@chakra-ui/react`, not `@chakra-ui/button`; tree-shaking handles the rest
