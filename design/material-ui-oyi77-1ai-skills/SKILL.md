---
name: material-ui
description: Use when material UI (MUI) React components — theming, styled engine,
  data grid, date pickers, icons. Use when working with material ui.
domain: content
author: oyi77
license: Apache-2.0
subdomain: content-creation
tags:
- content-creation
- digital-content
- material
- media
version: 1.0.0
category: content
---




## Overview

Material UI (MUI) is a comprehensive React component library implementing Google's Material Design. Includes components, icons, date pickers, data grid, and a powerful theming system with styled-engine.

## Capabilities

- 100+ production-ready Material Design components
- Theming with createTheme (colors, typography, spacing, breakpoints)
- sx prop for inline styling with theme access
- MUI X: DataGrid, DatePicker, TreeView, Charts
- 2000+ Material Design icons
- CSS-in-JS with Emotion or styled-components

## When to Use
**Trigger phrases:**
- "material ui"
- "Material UI (MUI) React components — theming, styled engine, data grid, date pic"


- Building enterprise React applications with Material Design
- Need advanced data tables with sorting, filtering, pagination
- Want a mature, well-documented component ecosystem
- Building admin panels, dashboards, data-heavy apps

## When NOT to Use

- Task is about content strategy, not creation (use strategy skills)
- Task is about content distribution (use distribution skills)
- You need to analyze content performance (use analytics skills)
- Task is about content moderation (use moderation tools)
- You don't have content guidelines
- Task requires domain expertise (consult experts)


## Pseudo Code

The material-ui workflow follows a standard pipeline pattern.

Core flow:
```
# material-ui primary flow
input = prepare(raw_data)
result = process(input, config={components, data, date, engine, grid})
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
# material-ui primary flow
input = prepare(raw_data)
result = process(input, config={components, data, date, engine, grid})
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
npm install @mui/material @emotion/react @emotion/styled @mui/icons-material
# Optional: DataGrid, DatePicker
npm install @mui/x-data-grid @mui/x-date-pickers
```

### Theme Setup
```tsx
import { ThemeProvider, createTheme, CssBaseline } from "@mui/material"

const theme = createTheme({
  palette: {
    primary: { main: "#1976d2" },
    secondary: { main: "#9c27b0" },
    mode: "light",
  },
  typography: { fontFamily: "Inter, Roboto, sans-serif" },
  shape: { borderRadius: 8 },
})

function App() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <YourApp />
    </ThemeProvider>
  )
}
```

### sx Prop Styling
```tsx
import { Box, Typography, Button } from "@mui/material"

export function Dashboard() {
  return (
    <Box sx={{ p: 4, display: "flex", gap: 2, bgcolor: "background.paper" }}>
      <Typography variant="h4" sx={{ fontWeight: 600 }}>
        Dashboard
      </Typography>
      <Button variant="contained" sx={{ ml: "auto" }}>
        Export
      </Button>
    </Box>
  )
}
```

### DataGrid
```tsx
import { DataGrid } from "@mui/x-data-grid"

const columns = [
  { field: "id", headerName: "ID", width: 90 },
  { field: "name", headerName: "Name", flex: 1 },
  { field: "status", headerName: "Status", width: 120 },
]

export function DataTable({ rows }) {
  return (
    <DataGrid
      rows={rows}
      columns={columns}
      pageSize={25}
      checkboxSelection
      disableRowSelectionOnClick
    />
  )
}
```

## Common Patterns

- **Theme tokens**: `sx={{ color: "primary.main", bgcolor: "grey.100" }}`
- **Responsive**: `sx={{ display: { xs: "none", md: "flex" } }}`
- **Styled API**: `const StyledBox = styled(Box)(({ theme }) => ({ padding: theme.spacing(2) }))`
- **Breakpoints**: `theme.breakpoints.up("sm")` for responsive queries
- **Component override**: `components: { MuiButton: { styleOverrides: { root: { textTransform: "none" } } } }`

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