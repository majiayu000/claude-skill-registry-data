---
name: frontend-design
description: Frontend design system utilities with component libraries, theme management, responsive design tools, and accessibility features.
license: MIT
---

# Frontend Design System Utilities

## Overview

Comprehensive frontend design toolkit providing component libraries, theme management, responsive design utilities, accessibility features, and design system automation for modern web applications.

## Quick Start

### Installation
```bash
npm install -g @frontend-design/cli
# or
npx @frontend-design/cli init
```

### Initialize Design System
```bash
# Initialize in existing project
frontend-design init

# Create new design system project
frontend-design create my-design-system --template=enterprise

# Add to existing frontend project
frontend-design add --project=my-react-app --framework=react
```

## Design System Foundation

### Color System
```bash
# Generate color palette
frontend-design colors generate --base=#3b82f6 --scheme=triadic

# Create semantic colors
frontend-design colors semantic --primary=#3b82f6 --secondary=#64748b

# Export color tokens
frontend-design colors export --format=css,js,figma
```

**Color Configuration**
```javascript
// design-system/colors.config.js
module.exports = {
  base: {
    primary: '#3b82f6',
    secondary: '#64748b',
    accent: '#f59e0b',
    neutral: '#6b7280',
    success: '#10b981',
    warning: '#f59e0b',
    error: '#ef4444',
    info: '#3b82f6'
  },
  
  semantic: {
    background: {
      primary: '#ffffff',
      secondary: '#f9fafb',
      tertiary: '#f3f4f6'
    },
    text: {
      primary: '#111827',
      secondary: '#6b7280',
      tertiary: '#9ca3af',
      inverse: '#ffffff'
    },
    border: {
      primary: '#e5e7eb',
      secondary: '#d1d5db',
      focus: '#3b82f6'
    }
  },
  
  scales: {
    // Generate 50-950 scale for each base color
    generateScales: true,
    steps: [50, 100, 200, 300, 400, 500, 600, 700, 800, 900, 950],
    algorithm: 'perceptual' // or 'linear', 'geometric'
  },
  
  accessibility: {
    contrastRatio: {
      AA: 4.5,
      AAA: 7.0,
      largeTextAA: 3.0,
      largeTextAAA: 4.5
    },
    autoGenerate: true
  }
};
```

### Typography System
```bash
# Generate typography scale
frontend-design typography generate --base=16 --ratio=1.25

# Create font families
frontend-design typography fonts --add=Inter,JetBrains+Mono

# Generate responsive typography
frontend-design typography responsive --breakpoints=sm,md,lg,xl
```

**Typography Configuration**
```javascript
// design-system/typography.config.js
module.exports = {
  fonts: {
    primary: {
      family: 'Inter, system-ui, sans-serif',
      weights: [400, 500, 600, 700],
      styles: ['normal', 'italic']
    },
    secondary: {
      family: 'Georgia, serif',
      weights: [400, 700],
      styles: ['normal', 'italic']
    },
    mono: {
      family: 'JetBrains Mono, Consolas, monospace',
      weights: [400, 500],
      styles: ['normal']
    }
  },
  
  scale: {
    base: 16, // px
    ratio: 1.25, // major third
    scale: [12, 14, 16, 20, 24, 30, 36, 48, 60, 72],
    lineHeight: {
      tight: 1.25,
      normal: 1.5,
      relaxed: 1.75
    },
    letterSpacing: {
      tight: -0.025,
      normal: 0,
      wide: 0.025
    }
  },
  
  semantic: {
    h1: { fontSize: 48, fontWeight: 700, lineHeight: 'tight' },
    h2: { fontSize: 36, fontWeight: 600, lineHeight: 'tight' },
    h3: { fontSize: 30, fontWeight: 600, lineHeight: 'normal' },
    h4: { fontSize: 24, fontWeight: 600, lineHeight: 'normal' },
    h5: { fontSize: 20, fontWeight: 500, lineHeight: 'normal' },
    h6: { fontSize: 16, fontWeight: 500, lineHeight: 'normal' },
    body: { fontSize: 16, fontWeight: 400, lineHeight: 'normal' },
    small: { fontSize: 14, fontWeight: 400, lineHeight: 'normal' },
    caption: { fontSize: 12, fontWeight: 400, lineHeight: 'normal' }
  },
  
  responsive: {
    breakpoints: {
      sm: '640px',
      md: '768px',
      lg: '1024px',
      xl: '1280px',
      '2xl': '1536px'
    },
    fluid: true,
    minScale: 0.8,
    maxScale: 1.2
  }
};
```

### Spacing System
```bash
# Generate spacing scale
frontend-design spacing generate --base=4 --ratio=1.5

# Create semantic spacing
frontend-design spacing semantic --xs=4 --sm=8 --md=16 --lg=24 --xl=32

# Generate layout grid
frontend-design spacing grid --columns=12 --gutter=16
```

**Spacing Configuration**
```javascript
// design-system/spacing.config.js
module.exports = {
  scale: {
    base: 4, // px
    ratio: 1.5,
    values: [0, 1, 2, 3, 4, 5, 6, 8, 10, 12, 16, 20, 24, 32, 40, 48, 64, 80, 96],
    semantic: {
      xs: 4,
      sm: 8,
      md: 16,
      lg: 24,
      xl: 32,
      '2xl': 48,
      '3xl': 64
    }
  },
  
  layout: {
    container: {
      sm: '640px',
      md: '768px',
      lg: '1024px',
      xl: '1280px',
      '2xl': '1400px'
    },
    grid: {
      columns: 12,
      gutter: 16,
      maxWidth: '1400px'
    },
    sections: {
      paddingY: {
        sm: 32,
        md: 48,
        lg: 64,
        xl: 96
      }
    }
  },
  
  component: {
    padding: {
      button: { x: 16, y: 8 },
      card: { all: 24 },
      modal: { all: 32 }
    },
    margin: {
      between: 16,
      section: 48,
      container: 24
    }
  }
};
```

## Component Library

### Component Generation
```bash
# Generate component
frontend-design component create Button --variant=primary,secondary,ghost

# Generate with props
frontend-design component create Card --props=title,content,actions

# Generate with variants
frontend-design component create Input --type=text,email,password --size=sm,md,lg
```

**Component Template**
```javascript
// components/Button/Button.jsx
import React from 'react';
import { buttonVariants } from './Button.styles';
import { cn } from '../../utils/cn';

export const Button = React.forwardRef(({
  children,
  variant = 'primary',
  size = 'md',
  disabled = false,
  loading = false,
  className,
  ...props
}, ref) => {
  const classes = cn(
    buttonVariants.base,
    buttonVariants.variants[variant],
    buttonVariants.sizes[size],
    disabled && buttonVariants.disabled,
    loading && buttonVariants.loading,
    className
  );

  return (
    <button
      ref={ref}
      className={classes}
      disabled={disabled || loading}
      {...props}
    >
      {loading && <LoadingSpinner className="mr-2" />}
      {children}
    </button>
  );
});

Button.displayName = 'Button';
```

**Component Styles**
```javascript
// components/Button/Button.styles.js
import { css } from '@emotion/react';
import { designTokens } from '../../design-tokens';

export const buttonVariants = {
  base: css`
    display: inline-flex;
    align-items: center;
    justify-content: center;
    border-radius: ${designTokens.borderRadius.md};
    font-weight: ${designTokens.fontWeight.medium};
    transition: all ${designTokens.transition.duration[150]} ${designTokens.transition.easing.default};
    cursor: pointer;
    border: 1px solid transparent;
    
    &:focus {
      outline: 2px solid ${designTokens.colors.primary[500]};
      outline-offset: 2px;
    }
    
    &:disabled {
      cursor: not-allowed;
      opacity: 0.6;
    }
  `,
  
  variants: {
    primary: css`
      background-color: ${designTokens.colors.primary[500]};
      color: ${designTokens.colors.white};
      
      &:hover:not(:disabled) {
        background-color: ${designTokens.colors.primary[600]};
      }
      
      &:active:not(:disabled) {
        background-color: ${designTokens.colors.primary[700]};
      }
    `,
    
    secondary: css`
      background-color: transparent;
      color: ${designTokens.colors.primary[500]};
      border-color: ${designTokens.colors.primary[500]};
      
      &:hover:not(:disabled) {
        background-color: ${designTokens.colors.primary[50]};
      }
    `,
    
    ghost: css`
      background-color: transparent;
      color: ${designTokens.colors.text.primary};
      
      &:hover:not(:disabled) {
        background-color: ${designTokens.colors.gray[100]};
      }
    `
  },
  
  sizes: {
    sm: css`
      padding: ${designTokens.spacing[2]} ${designTokens.spacing[3]};
      font-size: ${designTokens.fontSize.sm};
      min-height: ${designTokens.spacing[8]};
    `,
    
    md: css`
      padding: ${designTokens.spacing[3]} ${designTokens.spacing[4]};
      font-size: ${designTokens.fontSize.base};
      min-height: ${designTokens.spacing[10]};
    `,
    
    lg: css`
      padding: ${designTokens.spacing[4]} ${designTokens.spacing[6]};
      font-size: ${designTokens.fontSize.lg};
      min-height: ${designTokens.spacing[12]};
    `
  },
  
  disabled: css`
    cursor: not-allowed;
    opacity: 0.6;
  `,
  
  loading: css`
    position: relative;
    
    &::after {
      content: '';
      position: absolute;
      top: 50%;
      left: 50%;
      width: 16px;
      height: 16px;
      margin: -8px 0 0 -8px;
      border: 2px solid transparent;
      border-top-color: currentColor;
      border-radius: 50%;
      animation: spin 1s linear infinite;
    }
    
    @keyframes spin {
      to { transform: rotate(360deg); }
    }
  `
};
```

### Component Documentation
```bash
# Generate component docs
frontend-design docs generate Button

# Create storybook stories
frontend-design docs storybook Button

# Generate component tests
frontend-design docs test Button --framework=react-testing-library
```

**Component Documentation Template**
```markdown
# Button

Interactive button component with multiple variants and sizes.

## Usage

```jsx
import { Button } from './Button';

<Button variant="primary" size="md" onClick={handleClick}>
  Click me
</Button>
```

## Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| variant | `'primary' \| 'secondary' \| 'ghost'` | `'primary'` | Button style variant |
| size | `'sm' \| 'md' \| 'lg'` | `'md'` | Button size |
| disabled | `boolean` | `false` | Disable the button |
| loading | `boolean` | `false` | Show loading state |
| children | `ReactNode` | - | Button content |

## Variants

### Primary
Used for primary actions in the interface.

```jsx
<Button variant="primary">Primary Action</Button>
```

### Secondary
Used for secondary actions.

```jsx
<Button variant="secondary">Secondary Action</Button>
```

### Ghost
Used for minimal, tertiary actions.

```jsx
<Button variant="ghost">Ghost Action</Button>
```

## Accessibility

- Supports keyboard navigation
- Proper focus management
- Screen reader friendly
- High contrast mode support
```

## Theme Management

### Theme Generation
```bash
# Create theme
frontend-design theme create --name=light --base=light

# Create dark theme
frontend-design theme create --name=dark --base=dark

# Generate theme variants
frontend-design theme variants --themes=light,dark,high-contrast
```

**Theme Configuration**
```javascript
// design-system/themes.config.js
module.exports = {
  default: 'light',
  
  themes: {
    light: {
      colors: {
        background: {
          primary: '#ffffff',
          secondary: '#f9fafb',
          tertiary: '#f3f4f6'
        },
        text: {
          primary: '#111827',
          secondary: '#6b7280',
          tertiary: '#9ca3af'
        },
        primary: {
          50: '#eff6ff',
          500: '#3b82f6',
          900: '#1e3a8a'
        }
      },
      shadows: {
        sm: '0 1px 2px 0 rgba(0, 0, 0, 0.05)',
        md: '0 4px 6px -1px rgba(0, 0, 0, 0.1)',
        lg: '0 10px 15px -3px rgba(0, 0, 0, 0.1)'
      }
    },
    
    dark: {
      colors: {
        background: {
          primary: '#111827',
          secondary: '#1f2937',
          tertiary: '#374151'
        },
        text: {
          primary: '#f9fafb',
          secondary: '#d1d5db',
          tertiary: '#9ca3af'
        },
        primary: {
          50: '#1e3a8a',
          500: '#60a5fa',
          900: '#dbeafe'
        }
      },
      shadows: {
        sm: '0 1px 2px 0 rgba(0, 0, 0, 0.3)',
        md: '0 4px 6px -1px rgba(0, 0, 0, 0.4)',
        lg: '0 10px 15px -3px rgba(0, 0, 0, 0.5)'
      }
    },
    
    highContrast: {
      colors: {
        background: {
          primary: '#000000',
          secondary: '#1a1a1a',
          tertiary: '#333333'
        },
        text: {
          primary: '#ffffff',
          secondary: '#cccccc',
          tertiary: '#999999'
        },
        primary: {
          50: '#0000ff',
          500: '#0066ff',
          900: '#ccccff'
        }
      }
    }
  },
  
  customProperties: true,
  cssVariables: true,
  runtime: true
};
```

### Theme Provider
```javascript
// providers/ThemeProvider.jsx
import React, { createContext, useContext, useState, useEffect } from 'react';
import { themes } from '../design-system/themes';

const ThemeContext = createContext();

export const ThemeProvider = ({ children }) => {
  const [theme, setTheme] = useState('light');
  const [systemTheme, setSystemTheme] = useState('light');

  useEffect(() => {
    const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
    setSystemTheme(mediaQuery.matches ? 'dark' : 'light');
    
    const handleChange = (e) => {
      setSystemTheme(e.matches ? 'dark' : 'light');
    };
    
    mediaQuery.addEventListener('change', handleChange);
    return () => mediaQuery.removeEventListener('change', handleChange);
  }, []);

  const currentTheme = theme === 'system' ? systemTheme : theme;
  const themeTokens = themes[currentTheme];

  useEffect(() => {
    // Apply CSS custom properties
    const root = document.documentElement;
    Object.entries(themeTokens.cssVariables).forEach(([key, value]) => {
      root.style.setProperty(key, value);
    });
  }, [themeTokens]);

  const value = {
    theme,
    setTheme,
    systemTheme,
    currentTheme,
    tokens: themeTokens
  };

  return (
    <ThemeContext.Provider value={value}>
      {children}
    </ThemeContext.Provider>
  );
};

export const useTheme = () => {
  const context = useContext(ThemeContext);
  if (!context) {
    throw new Error('useTheme must be used within a ThemeProvider');
  }
  return context;
};
```

## Responsive Design

### Breakpoint System
```bash
# Generate responsive utilities
frontend-design responsive generate --breakpoints=sm,md,lg,xl

# Create responsive mixins
frontend-design responsive mixins --framework=emotion

# Generate container queries
frontend-design responsive container-queries
```

**Responsive Configuration**
```javascript
// design-system/responsive.config.js
module.exports = {
  breakpoints: {
    xs: '0px',
    sm: '640px',
    md: '768px',
    lg: '1024px',
    xl: '1280px',
    '2xl': '1536px'
  },
  
  containers: {
    sm: '640px',
    md: '768px',
    lg: '1024px',
    xl: '1280px',
    '2xl': '1400px'
  },
  
  grid: {
    columns: 12,
    gutter: {
      xs: 16,
      sm: 16,
      md: 24,
      lg: 24,
      xl: 32
    }
  },
  
  utilities: {
    generate: true,
    prefix: 'responsive',
    include: ['padding', 'margin', 'display', 'flex', 'grid']
  }
};
```

**Responsive Mixins**
```javascript
// utils/responsive.js
import { css } from '@emotion/react';
import { breakpoints } from '../design-system/responsive';

export const responsive = (styles) => {
  let mediaQueries = '';
  
  Object.entries(styles).forEach(([breakpoint, style]) => {
    if (breakpoint === 'base') {
      mediaQueries += css(style).styles;
    } else {
      const breakpointValue = breakpoints[breakpoint];
      mediaQueries += `@media (min-width: ${breakpointValue}) { ${css(style).styles} }`;
    }
  });
  
  return css`${mediaQueries}`;
};

export const container = () => css`
  width: 100%;
  margin: 0 auto;
  padding: 0 ${designTokens.spacing[4]};
  
  ${responsive({
    sm: { maxWidth: '640px' },
    md: { maxWidth: '768px' },
    lg: { maxWidth: '1024px' },
    xl: { maxWidth: '1280px' },
    '2xl': { maxWidth: '1400px' }
  })}
`;
```

## Accessibility Features

### A11y Utilities
```bash
# Generate accessibility utilities
frontend-design a11y generate --focus-visible,sr-only,skip-links

# Check color contrast
frontend-design a11y contrast --colors=#ffffff,#3b82f6

# Generate accessibility tests
frontend-design a11y test --framework=jest-axe
```

**Accessibility Configuration**
```javascript
// design-system/accessibility.config.js
module.exports = {
  focus: {
    visible: true,
    offset: 2,
    color: '#3b82f6',
    borderRadius: '4px'
  },
  
  skipLinks: {
    enabled: true,
    position: 'top-left',
    text: 'Skip to main content'
  },
  
  screenReader: {
    only: true,
    labels: true,
    descriptions: true,
    live: true
  },
  
  motion: {
    respectPrefers: true,
    reduced: true,
    duration: {
      fast: '150ms',
      normal: '300ms',
      slow: '500ms'
    }
  },
  
  contrast: {
    minimum: 4.5,
    enhanced: 7.0,
    largeText: 3.0
  }
};
```

**Accessibility Components**
```javascript
// components/Accessibility/SkipLink.jsx
import React from 'react';
import { css } from '@emotion/react';

const skipLinkStyles = css`
  position: absolute;
  top: -40px;
  left: 6px;
  background: ${designTokens.colors.primary[500]};
  color: ${designTokens.colors.white};
  padding: 8px;
  text-decoration: none;
  border-radius: ${designTokens.borderRadius.md};
  z-index: 1000;
  transition: top ${designTokens.transition.duration[150]} ${designTokens.transition.easing.default};
  
  &:focus {
    top: 6px;
  }
`;

export const SkipLink = ({ href = '#main-content', children = 'Skip to main content' }) => (
  <a href={href} css={skipLinkStyles}>
    {children}
  </a>
);

// components/Accessibility/FocusOutline.jsx
export const FocusOutline = () => css`
  &:focus-visible {
    outline: 2px solid ${designTokens.colors.primary[500]};
    outline-offset: 2px;
    border-radius: ${designTokens.borderRadius.md};
  }
  
  &:focus:not(:focus-visible) {
    outline: none;
  }
`;
```

## Design Tokens

### Token Generation
```bash
# Generate design tokens
frontend-design tokens generate --format=css,js,scss

# Export to Figma
frontend-design tokens export --platform=figma

# Sync with design tools
frontend-design tokens sync --source=figma --target=code
```

**Token Structure**
```javascript
// design-system/tokens.js
export const designTokens = {
  colors: {
    primary: {
      50: '#eff6ff',
      100: '#dbeafe',
      200: '#bfdbfe',
      300: '#93c5fd',
      400: '#60a5fa',
      500: '#3b82f6',
      600: '#2563eb',
      700: '#1d4ed8',
      800: '#1e40af',
      900: '#1e3a8a'
    },
    // ... other colors
  },
  
  spacing: {
    0: '0px',
    1: '4px',
    2: '8px',
    3: '12px',
    4: '16px',
    5: '20px',
    6: '24px',
    8: '32px',
    10: '40px',
    12: '48px',
    16: '64px',
    20: '80px',
    24: '96px'
  },
  
  typography: {
    fontSize: {
      xs: '12px',
      sm: '14px',
      base: '16px',
      lg: '18px',
      xl: '20px',
      '2xl': '24px',
      '3xl': '30px',
      '4xl': '36px',
      '5xl': '48px'
    },
    fontWeight: {
      light: 300,
      normal: 400,
      medium: 500,
      semibold: 600,
      bold: 700
    },
    lineHeight: {
      tight: 1.25,
      normal: 1.5,
      relaxed: 1.75
    }
  },
  
  borderRadius: {
    none: '0px',
    sm: '2px',
    md: '6px',
    lg: '8px',
    xl: '12px',
    full: '9999px'
  },
  
  shadows: {
    sm: '0 1px 2px 0 rgba(0, 0, 0, 0.05)',
    md: '0 4px 6px -1px rgba(0, 0, 0, 0.1)',
    lg: '0 10px 15px -3px rgba(0, 0, 0, 0.1)',
    xl: '0 20px 25px -5px rgba(0, 0, 0, 0.1)'
  },
  
  transition: {
    duration: {
      75: '75ms',
      100: '100ms',
      150: '150ms',
      200: '200ms',
      300: '300ms',
      500: '500ms',
      700: '700ms',
      1000: '1000ms'
    },
    easing: {
      default: 'cubic-bezier(0.4, 0, 0.2, 1)',
      in: 'cubic-bezier(0.4, 0, 1, 1)',
      out: 'cubic-bezier(0, 0, 0.2, 1)',
      'in-out': 'cubic-bezier(0.4, 0, 0.2, 1)'
    }
  }
};
```

## Integration

### Framework Integration
```bash
# React integration
frontend-design integrate react --typescript=true

# Vue integration
frontend-design integrate vue --composition-api

# Angular integration
frontend-design integrate angular --standalone=true
```

**React Integration**
```javascript
// utils/design-system.js
import { designTokens } from '../design-system/tokens';

export const createDesignSystem = (customTokens = {}) => {
  const tokens = { ...designTokens, ...customTokens };
  
  return {
    tokens,
    
    // CSS-in-JS utilities
    css: (styles) => styles,
    
    // Utility functions
    spacing: (value) => tokens.spacing[value] || value,
    color: (color, shade = 500) => tokens.colors[color]?.[shade] || color,
    fontSize: (size) => tokens.typography.fontSize[size] || size,
    
    // Responsive utilities
    responsive: (styles) => styles,
    
    // Theme utilities
    theme: (themeName) => tokens.themes?.[themeName] || tokens
  };
};

export const designSystem = createDesignSystem();
```

### Build Integration
```bash
# Webpack integration
frontend-design build webpack --config=webpack.config.js

# Vite integration
frontend-design build vite --config=vite.config.js

# Rollup integration
frontend-design build rollup --config=rollup.config.js
```

**Webpack Configuration**
```javascript
// webpack.config.js
const { DesignSystemPlugin } = require('@frontend-design/webpack');

module.exports = {
  plugins: [
    new DesignSystemPlugin({
      tokens: './design-system/tokens.js',
      output: {
        css: './dist/design-tokens.css',
        js: './dist/design-tokens.js',
        scss: './dist/design-tokens.scss'
      },
      optimization: {
        purgeUnused: true,
        minify: true
      }
    })
  ]
};
```

## API Reference

### Core Classes

**DesignSystem**
```javascript
import { DesignSystem } from '@frontend-design/core';

const designSystem = new DesignSystem({
  tokens: './tokens.json',
  theme: 'light'
});

const buttonStyles = designSystem.createStyles('button', {
  variant: 'primary',
  size: 'md'
});
```

**ThemeProvider**
```javascript
import { ThemeProvider } from '@frontend-design/react';

<ThemeProvider theme="dark">
  <App />
</ThemeProvider>
```

**ResponsiveUtils**
```javascript
import { responsive } from '@frontend-design/utils';

const styles = responsive({
  base: { padding: 16 },
  md: { padding: 24 },
  lg: { padding: 32 }
});
```

## Contributing

1. Fork repository
2. Create feature branch
3. Follow design system guidelines
4. Add comprehensive tests
5. Submit pull request

## License

MIT License - see LICENSE file for details.