---
name: chakra-ui
description: Use when chakra UI React component library — theming, responsive styles,
  color mode, component composition. Use when working with chakra ui.
domain: content
author: oyi77
license: Apache-2.0
subdomain: content-creation
tags:
- chakra
- content-creation
- digital-content
- media
version: 1.0.0
category: content
---




## Overview

Chakra UI is a modular, accessible React component library with built-in dark mode, responsive styles, and a flexible theming system. Uses style props for inline styling with theme tokens.

## Capabilities

- Theme customization with color mode (light/dark)
- Responsive style props with array syntax
- Component composition with `as` prop and `chakra()` factory
- Form components with built-in validation
- Modal, Drawer, Toast, and other overlay components
- CSS-in-JS with Emotion under the hood

## When to Use
**Trigger phrases:**
- "chakra ui"
- "Chakra UI React component library — theming, responsive styles, color mode, comp"


- Building React apps with accessible components out of the box
- Need responsive design without writing media queries
- Want a consistent design system with theme tokens
- Building dashboards, forms, and complex layouts

## When NOT to Use

- Task is about content strategy, not creation (use strategy skills)
- Task is about content distribution (use distribution skills)
- You need to analyze content performance (use analytics skills)
- Task is about content moderation (use moderation tools)
- You don't have content guidelines
- Task requires domain expertise (consult experts)


## Pseudo Code

The chakra-ui workflow follows a standard pipeline pattern.

Core flow:
```
# chakra-ui primary flow
input = prepare(raw_data)
result = process(input, config={chakra, color, component, composition, library})
validate(result)
deliver(result)
```

Error handling:
```
on error:
  log(error_details)
  retry_with_backoff(max=3)
  if still_failing: alert_and_escalate()
```


### Core Workflow
```
# chakra-ui primary flow
input = prepare(raw_data)
result = process(input, config={chakra, color, component, composition, library})
validate(result)
deliver(result)
```

### Error Handling
```
on error:
  log(error_details)
  retry_with_backoff(max=3)
  if still_failing: alert_and_escalate()
```


### Installation
```bash
npm install @chakra-ui/react @emotion/react @emotion/styled framer-motion
```

### Theme Provider
```tsx
import { ChakraProvider, extendTheme } from "@chakra-ui/react"

const theme = extendTheme({
  colors: {
    brand: { 500: "#3182ce", 600: "#2b6cb0" },
  },
  fonts: { heading: "Inter, sans-serif", body: "Inter, sans-serif" },
})

function App() {
  return <ChakraProvider theme={theme}><YourApp /></ChakraProvider>
}
```

### Responsive Props
```tsx
import { Box, Stack, Text } from "@chakra-ui/react"

export function Hero() {
  return (
    <Stack direction={["column", "row"]} spacing={8} p={[4, 8, 16]}>
      <Box flex={1}>
        <Text fontSize={["2xl", "3xl", "4xl"]} fontWeight="bold">
          Welcome
        </Text>
      </Box>
    </Stack>
  )
}
```

### Component Composition
```tsx
import { Button, Icon, Flex } from "@chakra-ui/react"
import { FaRocket } from "react-icons/fa"

export function ActionButton() {
  return (
    <Button colorScheme="blue" size="lg" leftIcon={<Icon as={FaRocket} />}>
      Launch
    </Button>
  )
}
```

### Dark Mode
```tsx
import { useColorMode, Button, Box } from "@chakra-ui/react"

export function ThemedCard() {
  const { colorMode, toggleColorMode } = useColorMode()
  return (
    <Box bg={colorMode === "light" ? "white" : "gray.800"} p={6} rounded="lg">
      <Button onClick={toggleColorMode}>Toggle {colorMode}</Button>
    </Box>
  )
}
```

## Common Patterns

- **Style props**: `<Box bg="blue.500" p={4} rounded="md" />` — inline styling with theme tokens
- **Array responsive**: `fontSize={["sm", "md", "lg"]}` — mobile-first breakpoints
- **useColorModeValue**: `useColorModeValue("white", "gray.800")` — theme-aware values
- **Component factory**: `const CustomBox = chakra("div", { baseStyle: { p: 4 } })`
- **Portal overlays**: Modals and Drawers use Portal for proper z-index layering

## How to Use

1. Define content goal (traffic, engagement, conversion, brand awareness)
2. Research target audience pain points and search intent
3. Generate content using appropriate AI tools
4. Edit and humanize output for authenticity
5. Optimize for target platform (SEO, hashtags, format)
6. Schedule and distribute across channels
7. Measure performance and iterate

## Red Flags

- **AI-generated content sounds robotic**: Always run through humanizer before publishing
- **Engagement dropping week-over-week**: Content fatigue or algorithm change — vary formats
- **Duplicate content across platforms**: Adapt content per platform, don't just cross-post
- **No content calendar**: Sporadic posting kills audience retention
- **Ignoring analytics**: Content without measurement is just publishing, not marketing

## Verification

- [ ] Skill output matches expected behavior

## Process

1. Analyze the task requirements
2. Apply domain expertise
3. Verify output quality

## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "Good enough content works" | Quality content drives engagement. Mediocre content gets ignored. |
| "I will optimize later" | SEO and distribution need optimization from the start. |
| "Templates are good enough" | Templates are a starting point. Custom content outperforms generic. |