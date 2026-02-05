---
name: ink-cli
description: Build terminal CLI apps using Ink (React for CLIs). This skill should be used when the user wants to create command-line interfaces with React components, terminal UIs, interactive CLI tools, or needs help with Ink components, hooks, and patterns.
---

# Ink CLI Development

Ink is a React renderer for building command-line interfaces. It uses Yoga for Flexbox layouts and provides the same component-based experience as React in the browser.

## Quick Start

```bash
# Scaffold new project
npx create-ink-app my-cli

# With TypeScript (recommended)
npx create-ink-app --typescript my-cli
```

## Core Concepts

### Every Element is a Flexbox Container
Think of `<Box>` as `<div style="display: flex">`. All text must be wrapped in `<Text>`.

### Component Hierarchy
```tsx
import {render, Box, Text} from 'ink';

const App = () => (
  <Box flexDirection="column" padding={1}>
    <Text bold>Title</Text>
    <Box gap={2}>
      <Text color="green">Left</Text>
      <Text color="blue">Right</Text>
    </Box>
  </Box>
);

render(<App />);
```

## Essential Components

### `<Text>` - Styled Text
```tsx
<Text color="green">Green text</Text>
<Text color="#005cc5">Hex color</Text>
<Text bold italic underline>Styled</Text>
<Text dimColor>Dimmed</Text>
<Text inverse>Inverted</Text>
<Text wrap="truncate">Long text will be truncated...</Text>
```

### `<Box>` - Flexbox Container
```tsx
// Layout
<Box flexDirection="column" alignItems="center" justifyContent="space-between">

// Spacing
<Box padding={2} margin={1} gap={1}>

// Dimensions
<Box width={50} height={10} minWidth={20}>
<Box width="50%">  {/* Percentage of parent */}

// Borders
<Box borderStyle="round" borderColor="green">
<Box borderStyle="double" borderTop borderBottom>

// Background
<Box backgroundColor="blue">
```

**Border styles:** `single`, `double`, `round`, `bold`, `singleDouble`, `doubleSingle`, `classic`

### `<Static>` - Permanent Output
Renders above everything else, never re-renders. Use for logs, completed items.

```tsx
const App = () => {
  const [logs, setLogs] = useState<string[]>([]);

  return (
    <>
      <Static items={logs}>
        {(log, i) => <Text key={i}>{log}</Text>}
      </Static>
      <Box>
        <Text>Live UI here</Text>
      </Box>
    </>
  );
};
```

### `<Newline>` and `<Spacer>`
```tsx
<Text>Line 1<Newline />Line 2</Text>
<Newline count={3} />

<Box>
  <Text>Left</Text>
  <Spacer />  {/* Pushes Right to the edge */}
  <Text>Right</Text>
</Box>
```

### `<Transform>` - String Transformation
```tsx
<Transform transform={output => output.toUpperCase()}>
  <Text>hello</Text>  {/* Renders: HELLO */}
</Transform>
```

## Essential Hooks

### `useInput` - Keyboard Input
```tsx
import {useInput, useApp} from 'ink';

const App = () => {
  const {exit} = useApp();

  useInput((input, key) => {
    if (input === 'q') exit();
    if (key.leftArrow) { /* handle left */ }
    if (key.return) { /* handle enter */ }
    if (key.escape) { /* handle escape */ }
  });

  return <Text>Press q to quit</Text>;
};
```

**Key properties:** `leftArrow`, `rightArrow`, `upArrow`, `downArrow`, `return`, `escape`, `ctrl`, `shift`, `tab`, `backspace`, `delete`, `pageUp`, `pageDown`, `meta`

### `useApp` - App Control
```tsx
const {exit} = useApp();
exit();        // Clean exit
exit(error);   // Exit with error
```

### `useFocus` - Focus Management
```tsx
const Item = ({label}) => {
  const {isFocused} = useFocus();
  return (
    <Text color={isFocused ? 'green' : 'white'}>
      {isFocused ? '>' : ' '} {label}
    </Text>
  );
};
```

**Options:** `autoFocus`, `isActive`, `id`

### `useFocusManager` - Programmatic Focus
```tsx
const {focusNext, focusPrevious, focus} = useFocusManager();
focus('specific-id');
```

### `useStdout` / `useStderr` - Direct Output
```tsx
const {write} = useStdout();
write('Direct to stdout\n');  // Bypasses Ink rendering
```

## Common Patterns

### Loading Spinner
```tsx
import Spinner from 'ink-spinner';

const Loading = ({text}) => (
  <Text>
    <Text color="green"><Spinner type="dots" /></Text>
    {' '}{text}
  </Text>
);
```

### Progress Indicator
```tsx
const Progress = ({percent}) => {
  const width = 20;
  const filled = Math.round(width * percent / 100);
  return (
    <Box>
      <Text color="green">{'█'.repeat(filled)}</Text>
      <Text color="gray">{'░'.repeat(width - filled)}</Text>
      <Text> {percent}%</Text>
    </Box>
  );
};
```

### Selectable List
```tsx
const List = ({items}) => {
  const [selected, setSelected] = useState(0);

  useInput((input, key) => {
    if (key.upArrow) setSelected(s => Math.max(0, s - 1));
    if (key.downArrow) setSelected(s => Math.min(items.length - 1, s + 1));
  });

  return (
    <Box flexDirection="column">
      {items.map((item, i) => (
        <Text key={i} color={i === selected ? 'green' : 'white'}>
          {i === selected ? '>' : ' '} {item}
        </Text>
      ))}
    </Box>
  );
};
```

### Table Layout
```tsx
const Table = ({data}) => (
  <Box flexDirection="column">
    {data.map((row, i) => (
      <Box key={i} gap={2}>
        {row.map((cell, j) => (
          <Box key={j} width={15}>
            <Text>{cell}</Text>
          </Box>
        ))}
      </Box>
    ))}
  </Box>
);
```

## Testing

```tsx
import {render} from 'ink-testing-library';

const {lastFrame, rerender} = render(<MyComponent />);
expect(lastFrame()).toContain('expected text');
```

## API Reference

For complete API documentation, see `references/ink-api.md`.

For community components (spinners, inputs, tables, etc.), see `references/components.md`.

## Tips

1. **All text in `<Text>`**: Never put raw text directly in `<Box>`
2. **Use `<Static>` for logs**: Prevents re-rendering of completed output
3. **Disable input when needed**: `useInput(handler, {isActive: false})`
4. **Debug with React DevTools**: Run with `DEV=true my-cli`
5. **Handle Ctrl+C**: Enabled by default, disable with `exitOnCtrlC: false` in render options
