---
name: styled-components
description: Implements CSS-in-JS styling with styled-components using tagged template literals, theming, and dynamic props. Use when wanting component-scoped CSS-in-JS, dynamic styling based on props, or theming support.
---

# styled-components

CSS-in-JS library using tagged template literals to style React components.

## Quick Start

**Install:**
```bash
npm install styled-components
```

**Create styled components:**
```tsx
import styled from 'styled-components';

const Button = styled.button`
  padding: 12px 24px;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  cursor: pointer;
  background: #3b82f6;
  color: white;

  &:hover {
    background: #2563eb;
  }
`;

const Container = styled.div`
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 16px;
`;

function App() {
  return (
    <Container>
      <Button>Click me</Button>
    </Container>
  );
}
```

## Props-Based Styling

### Transient Props ($ prefix)

Props prefixed with `$` are filtered from DOM:

```tsx
interface ButtonProps {
  $variant?: 'primary' | 'secondary';
  $size?: 'sm' | 'md' | 'lg';
}

const Button = styled.button<ButtonProps>`
  padding: ${props => {
    switch (props.$size) {
      case 'sm': return '8px 16px';
      case 'lg': return '16px 32px';
      default: return '12px 24px';
    }
  }};

  background: ${props => props.$variant === 'secondary' ? '#e5e7eb' : '#3b82f6'};
  color: ${props => props.$variant === 'secondary' ? '#1f2937' : 'white'};
`;

// Usage
<Button $variant="secondary" $size="lg">
  Secondary Button
</Button>
```

### Conditional Styles

```tsx
const Card = styled.div<{ $elevated?: boolean; $selected?: boolean }>`
  padding: 16px;
  border-radius: 8px;
  background: white;

  ${props => props.$elevated && `
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  `}

  ${props => props.$selected && `
    border: 2px solid #3b82f6;
  `}
`;
```

## Extending Styles

```tsx
const Button = styled.button`
  padding: 12px 24px;
  border: 2px solid #3b82f6;
  border-radius: 8px;
  background: transparent;
  color: #3b82f6;
  cursor: pointer;
`;

// Extend with additional styles
const PrimaryButton = styled(Button)`
  background: #3b82f6;
  color: white;
`;

const DangerButton = styled(Button)`
  border-color: #ef4444;
  color: #ef4444;

  &:hover {
    background: #ef4444;
    color: white;
  }
`;
```

## Polymorphic Components

Change the rendered element with `as`:

```tsx
const Button = styled.button`
  padding: 12px 24px;
  text-decoration: none;
  display: inline-block;
`;

// Render as anchor
<Button as="a" href="/about">About</Button>

// Render as Link (React Router)
<Button as={Link} to="/about">About</Button>
```

## Styling Existing Components

```tsx
import { Link } from 'react-router-dom';

// Component must accept and pass className
const StyledLink = styled(Link)`
  color: #3b82f6;
  text-decoration: none;

  &:hover {
    text-decoration: underline;
  }
`;

// Custom component
function CustomCard({ className, children }: { className?: string; children: React.ReactNode }) {
  return <div className={className}>{children}</div>;
}

const StyledCard = styled(CustomCard)`
  padding: 16px;
  border-radius: 8px;
`;
```

## Attrs

Attach default or computed attributes:

```tsx
const Input = styled.input.attrs<{ $size?: string }>(props => ({
  type: 'text',
  placeholder: props.placeholder || 'Enter text...',
}))`
  padding: ${props => props.$size === 'large' ? '16px' : '12px'};
  border: 1px solid #e5e7eb;
  border-radius: 6px;
`;

// Password input with overridden type
const PasswordInput = styled(Input).attrs({
  type: 'password',
  placeholder: 'Enter password',
})``;
```

## Animations

```tsx
import styled, { keyframes } from 'styled-components';

const fadeIn = keyframes`
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
`;

const spin = keyframes`
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
`;

const FadeInDiv = styled.div`
  animation: ${fadeIn} 0.3s ease-out;
`;

const Spinner = styled.div`
  width: 24px;
  height: 24px;
  border: 2px solid #e5e7eb;
  border-top-color: #3b82f6;
  border-radius: 50%;
  animation: ${spin} 0.8s linear infinite;
`;
```

## Theming

### ThemeProvider

```tsx
import styled, { ThemeProvider } from 'styled-components';

const theme = {
  colors: {
    primary: '#3b82f6',
    secondary: '#6b7280',
    success: '#10b981',
    error: '#ef4444',
    background: '#ffffff',
    text: '#1f2937',
  },
  spacing: {
    xs: '4px',
    sm: '8px',
    md: '16px',
    lg: '24px',
    xl: '32px',
  },
  borderRadius: {
    sm: '4px',
    md: '8px',
    lg: '16px',
    full: '9999px',
  },
};

type Theme = typeof theme;

declare module 'styled-components' {
  export interface DefaultTheme extends Theme {}
}

// Access theme in components
const Button = styled.button`
  background: ${props => props.theme.colors.primary};
  padding: ${props => props.theme.spacing.md};
  border-radius: ${props => props.theme.borderRadius.md};
`;

// Wrap app
function App() {
  return (
    <ThemeProvider theme={theme}>
      <Button>Themed Button</Button>
    </ThemeProvider>
  );
}
```

### useTheme Hook

```tsx
import { useTheme } from 'styled-components';

function Component() {
  const theme = useTheme();

  return (
    <div style={{ color: theme.colors.primary }}>
      Using theme in regular component
    </div>
  );
}
```

### Dark Mode

```tsx
const lightTheme = {
  colors: {
    background: '#ffffff',
    text: '#1f2937',
    primary: '#3b82f6',
  },
};

const darkTheme = {
  colors: {
    background: '#1f2937',
    text: '#f9fafb',
    primary: '#60a5fa',
  },
};

function App() {
  const [isDark, setIsDark] = useState(false);

  return (
    <ThemeProvider theme={isDark ? darkTheme : lightTheme}>
      <AppContainer>
        <button onClick={() => setIsDark(!isDark)}>Toggle Theme</button>
      </AppContainer>
    </ThemeProvider>
  );
}
```

## Global Styles

```tsx
import { createGlobalStyle } from 'styled-components';

const GlobalStyle = createGlobalStyle`
  *,
  *::before,
  *::after {
    box-sizing: border-box;
  }

  body {
    margin: 0;
    font-family: system-ui, -apple-system, sans-serif;
    background: ${props => props.theme.colors.background};
    color: ${props => props.theme.colors.text};
  }

  a {
    color: ${props => props.theme.colors.primary};
  }
`;

function App() {
  return (
    <ThemeProvider theme={theme}>
      <GlobalStyle />
      <MainContent />
    </ThemeProvider>
  );
}
```

## CSS Helper

Share style fragments:

```tsx
import styled, { css } from 'styled-components';

const flexCenter = css`
  display: flex;
  align-items: center;
  justify-content: center;
`;

const truncate = css`
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
`;

const Card = styled.div`
  ${flexCenter}
  padding: 16px;
`;

const Title = styled.h2`
  ${truncate}
  max-width: 200px;
`;
```

## Component Selectors

Reference other styled components:

```tsx
const Icon = styled.span`
  color: #6b7280;
  transition: color 0.2s;
`;

const Button = styled.button`
  display: flex;
  align-items: center;
  gap: 8px;

  &:hover ${Icon} {
    color: #3b82f6;
  }
`;

// Usage
<Button>
  <Icon>+</Icon>
  Add Item
</Button>
```

## Best Practices

1. **Define outside render** - Prevent recreation on each render
2. **Use transient props** - Prefix with `$` to avoid DOM warnings
3. **Extend over duplicate** - Use `styled(Component)` for variants
4. **Type your theme** - Extend `DefaultTheme` for autocomplete
5. **Colocate with components** - Keep styles near their component

## Common Patterns

### Responsive Styles

```tsx
const breakpoints = {
  sm: '640px',
  md: '768px',
  lg: '1024px',
  xl: '1280px',
};

const Container = styled.div`
  padding: 16px;

  @media (min-width: ${breakpoints.md}) {
    padding: 24px;
  }

  @media (min-width: ${breakpoints.lg}) {
    padding: 32px;
    max-width: 1200px;
    margin: 0 auto;
  }
`;
```

### Variants with Object Syntax

```tsx
const variants = {
  primary: css`
    background: #3b82f6;
    color: white;
  `,
  secondary: css`
    background: #e5e7eb;
    color: #1f2937;
  `,
  outline: css`
    background: transparent;
    border: 2px solid #3b82f6;
    color: #3b82f6;
  `,
};

const Button = styled.button<{ $variant?: keyof typeof variants }>`
  padding: 12px 24px;
  border: none;
  border-radius: 8px;
  cursor: pointer;

  ${props => variants[props.$variant || 'primary']}
`;
```

## Reference Files

- [references/ssr.md](references/ssr.md) - Server-side rendering
- [references/patterns.md](references/patterns.md) - Advanced patterns
