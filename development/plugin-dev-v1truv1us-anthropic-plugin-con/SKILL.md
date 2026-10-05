---
name: plugin-dev
description: Comprehensive plugin development toolkit for creating, testing, and managing plugins across multiple platforms with scaffolding, validation, and deployment utilities.
license: MIT
---

# Plugin Development Toolkit

## Overview

Complete development environment for creating plugins across different platforms including OpenCode, VS Code, Chrome, WordPress, and more. Provides scaffolding, testing, validation, and deployment utilities.

## Quick Start

### Installation
```bash
npm install -g @plugin-dev/cli
# or
npx @plugin-dev/cli create my-plugin
```

### Create New Plugin
```bash
# Interactive plugin creation
plugin-dev create

# Create specific type
plugin-dev create --type=opencode --name=my-awesome-plugin
plugin-dev create --type=vscode --name=my-extension
plugin-dev create --type=chrome --name=my-browser-extension
```

## Plugin Types

### OpenCode Plugins
```bash
# Create OpenCode plugin
plugin-dev create opencode my-plugin --template=skill

# Generated structure
my-plugin/
├── package.json
├── README.md
├── index.js
├── tests/
│   └── plugin.test.js
└── docs/
    └── api.md
```

**OpenCode Plugin Template**
```javascript
// index.js
module.exports = {
  name: 'my-plugin',
  version: '1.0.0',
  description: 'My awesome OpenCode plugin',
  type: 'skill',
  
  async initialize() {
    console.log('Plugin initialized');
  },
  
  async execute(input) {
    // Plugin logic here
    return {
      success: true,
      result: 'Plugin executed successfully'
    };
  }
};
```

### VS Code Extensions
```bash
# Create VS Code extension
plugin-dev create vscode my-extension --template=language-support

# Generated structure
my-extension/
├── package.json
├── extension.js
├── syntaxes/
├── snippets/
└── resources/
```

**VS Code Extension Template**
```javascript
// extension.js
const vscode = require('vscode');

function activate(context) {
  let disposable = vscode.commands.registerCommand(
    'extension.helloWorld', 
    function () {
      vscode.window.showInformationMessage('Hello World!');
    }
  );
  
  context.subscriptions.push(disposable);
}

function deactivate() {}

module.exports = { activate, deactivate };
```

### Chrome Extensions
```bash
# Create Chrome extension
plugin-dev create chrome my-extension --template=action

# Generated structure
my-extension/
├── manifest.json
├── popup.html
├── content.js
├── background.js
└── icons/
```

**Chrome Extension Template**
```javascript
// background.js
chrome.runtime.onInstalled.addListener(() => {
  chrome.contextMenus.create({
    id: 'myExtension',
    title: 'My Extension Action',
    contexts: ['selection']
  });
});

chrome.contextMenus.onClicked.addListener((info, tab) => {
  if (info.menuItemId === 'myExtension') {
    // Handle menu click
  }
});
```

## Development Tools

### Local Development Server
```bash
# Start development server with hot reload
plugin-dev dev --port=3000 --watch

# Platform-specific development
plugin-dev dev --platform=opencode
plugin-dev dev --platform=vscode --debug
```

### Testing Framework
```bash
# Run all tests
plugin-dev test

# Run specific test suite
plugin-dev test --unit
plugin-dev test --integration
plugin-dev test --e2e

# Test with coverage
plugin-dev test --coverage --threshold=80
```

**Test Examples**
```javascript
// tests/plugin.test.js
const { PluginTester } = require('@plugin-dev/testing');

describe('MyPlugin', () => {
  let tester;
  
  beforeEach(() => {
    tester = new PluginTester('./index.js');
  });

  test('should initialize correctly', async () => {
    const plugin = await tester.load();
    expect(plugin.name).toBe('my-plugin');
  });

  test('should execute successfully', async () => {
    const result = await tester.execute({ input: 'test' });
    expect(result.success).toBe(true);
  });
});
```

### Validation & Linting
```bash
# Validate plugin structure
plugin-dev validate

# Lint code
plugin-dev lint --fix

# Type checking
plugin-dev type-check

# Security audit
plugin-dev audit --security
```

## Plugin Configuration

### package.json Configuration
```json
{
  "name": "my-plugin",
  "version": "1.0.0",
  "description": "My awesome plugin",
  "main": "index.js",
  "type": "opencode-skill",
  "opencode": {
    "category": "utility",
    "tags": ["automation", "productivity"],
    "permissions": ["file-read", "network"],
    "dependencies": ["node-fetch", "lodash"]
  },
  "scripts": {
    "dev": "plugin-dev dev",
    "test": "plugin-dev test",
    "build": "plugin-dev build",
    "publish": "plugin-dev publish"
  },
  "devDependencies": {
    "@plugin-dev/testing": "^1.0.0",
    "@plugin-dev/linter": "^1.0.0"
  }
}
```

### Plugin Configuration File
```javascript
// plugin.config.js
module.exports = {
  name: 'my-plugin',
  type: 'opencode-skill',
  
  // Plugin metadata
  metadata: {
    author: 'Your Name',
    license: 'MIT',
    repository: 'https://github.com/username/my-plugin',
    keywords: ['plugin', 'automation', 'utility']
  },
  
  // Runtime configuration
  runtime: {
    timeout: 30000,
    memory: '512MB',
    permissions: ['file-read', 'network']
  },
  
  // Development settings
  development: {
    port: 3000,
    hotReload: true,
    debugMode: true
  },
  
  // Build configuration
  build: {
    target: 'node',
    minify: true,
    bundle: true,
    output: './dist'
  }
};
```

## Advanced Features

### Plugin Hooks
```javascript
// index.js
module.exports = {
  name: 'my-plugin',
  
  // Lifecycle hooks
  async beforeInitialize() {
    console.log('About to initialize...');
  },
  
  async initialize() {
    // Initialization logic
  },
  
  async beforeExecute(input) {
    console.log('About to execute with:', input);
    return input; // Can modify input
  },
  
  async execute(input) {
    // Main plugin logic
    return { success: true, result: 'done' };
  },
  
  async afterExecute(result) {
    console.log('Execution result:', result);
    return result; // Can modify result
  },
  
  async beforeDestroy() {
    console.log('About to destroy plugin...');
  },
  
  async destroy() {
    // Cleanup logic
  }
};
```

### Plugin Communication
```javascript
// Inter-plugin communication
const { PluginBus } = require('@plugin-dev/communication');

// Subscribe to events
PluginBus.on('user:login', (user) => {
  console.log('User logged in:', user.id);
});

// Emit events
PluginBus.emit('plugin:ready', {
  plugin: 'my-plugin',
  version: '1.0.0'
});

// Direct plugin messaging
const otherPlugin = PluginBus.getPlugin('other-plugin');
const response = await otherPlugin.sendMessage('process', { data: 'test' });
```

### Plugin Storage
```javascript
// Persistent storage
const { PluginStorage } = require('@plugin-dev/storage');

// Local storage
const localStore = new PluginStorage('local');
await localStore.set('config', { theme: 'dark' });
const config = await localStore.get('config');

// Cloud storage
const cloudStore = new PluginStorage('cloud', {
  provider: 'aws',
  bucket: 'my-plugin-storage'
});
await cloudStore.set('user-data', userData);
```

## Platform Integration

### OpenCode Integration
```javascript
// OpenCode-specific features
const { OpenCodeAPI } = require('@plugin-dev/platforms');

const opencode = new OpenCodeAPI();

// Register commands
opencode.registerCommand('my-plugin.action', () => {
  console.log('Action executed');
});

// Access OpenCode services
const fileSystem = opencode.getService('filesystem');
const editor = opencode.getService('editor');
const terminal = opencode.getService('terminal');
```

### VS Code Integration
```javascript
// VS Code API access
const vscode = require('vscode');

// Register commands
vscode.commands.registerCommand('my-plugin.hello', () => {
  vscode.window.showInformationMessage('Hello from my plugin!');
});

// Register language features
const provider = vscode.languages.registerCompletionItemProvider(
  'javascript',
  {
    provideCompletionItems(document, position) {
      // Return completion items
    }
  }
);
```

### Chrome Integration
```javascript
// Chrome API access
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === 'getData') {
    // Handle request
    sendResponse({ data: 'result' });
  }
});

// Storage API
chrome.storage.local.set({ key: 'value' });
chrome.storage.local.get(['key'], (result) => {
  console.log(result.key);
});
```

## Build & Deployment

### Build Process
```bash
# Build for production
plugin-dev build --target=production

# Build for specific platform
plugin-dev build --platform=opencode
plugin-dev build --platform=vscode --minify

# Build with custom configuration
plugin-dev build --config=custom.build.js
```

**Build Configuration**
```javascript
// build.config.js
module.exports = {
  entry: './index.js',
  output: {
    path: './dist',
    filename: 'bundle.js'
  },
  
  plugins: [
    new MinifyPlugin(),
    new BundleAnalyzerPlugin()
  ],
  
  optimization: {
    minimize: true,
    splitChunks: true
  },
  
  platform: {
    opencode: {
      target: 'node',
      externals: ['fs', 'path']
    },
    vscode: {
      target: 'node',
      includeVSCodeAPI: true
    },
    chrome: {
      target: 'browser',
      polyfills: ['Promise', 'Object.assign']
    }
  }
};
```

### Deployment
```bash
# Deploy to registry
plugin-dev publish --registry=opencode
plugin-dev publish --registry=vscode-marketplace
plugin-dev publish --registry=chrome-webstore

# Deploy with custom configuration
plugin-dev deploy --config=deploy.config.js --env=production
```

**Deployment Configuration**
```javascript
// deploy.config.js
module.exports = {
  environments: {
    development: {
      registry: 'opencode-staging',
      version: '1.0.0-dev'
    },
    production: {
      registry: 'opencode',
      version: '1.0.0',
      changelog: './CHANGELOG.md'
    }
  },
  
  beforeDeploy: async () => {
    console.log('Running pre-deployment checks...');
    await runTests();
    await validatePlugin();
  },
  
  afterDeploy: async (result) => {
    console.log('Deployment completed:', result.url);
    await notifyTeam(result);
  }
};
```

## Testing

### Unit Testing
```javascript
// tests/unit/plugin.test.js
const { expect } = require('chai');
const plugin = require('../../index.js');

describe('Plugin Unit Tests', () => {
  test('should have correct name', () => {
    expect(plugin.name).toBe('my-plugin');
  });
  
  test('should initialize correctly', async () => {
    await plugin.initialize();
    expect(plugin.initialized).toBe(true);
  });
});
```

### Integration Testing
```javascript
// tests/integration/api.test.js
const { PluginTester } = require('@plugin-dev/testing');

describe('Plugin Integration Tests', () => {
  let tester;
  
  beforeEach(async () => {
    tester = new PluginTester();
    await tester.start();
  });
  
  afterEach(async () => {
    await tester.stop();
  });
  
  test('should handle API requests', async () => {
    const response = await tester.request('/api/process', {
      method: 'POST',
      body: { data: 'test' }
    });
    
    expect(response.status).toBe(200);
    expect(response.body.success).toBe(true);
  });
});
```

### E2E Testing
```javascript
// tests/e2e/workflow.test.js
const { E2ETester } = require('@plugin-dev/testing');

describe('Plugin E2E Tests', () => {
  let tester;
  
  beforeAll(async () => {
    tester = new E2ETester({
      browser: 'chrome',
      headless: true
    });
    await tester.setup();
  });
  
  afterAll(async () => {
    await tester.cleanup();
  });
  
  test('should complete full workflow', async () => {
    await tester.navigateTo('/plugin');
    await tester.click('#start-button');
    await tester.waitFor('#result');
    
    const result = await tester.getText('#result');
    expect(result).toContain('success');
  });
});
```

## Debugging

### Debug Mode
```bash
# Start with debugging
plugin-dev dev --debug --port=9229

# Debug with VS Code
plugin-dev dev --debugger=vscode

# Debug with Chrome DevTools
plugin-dev dev --debugger=chrome
```

### Logging
```javascript
// Configure logging
const { PluginLogger } = require('@plugin-dev/logger');

const logger = new PluginLogger({
  level: 'debug',
  format: 'json',
  outputs: ['console', 'file']
});

// Use in plugin
logger.debug('Debug message');
logger.info('Info message');
logger.warn('Warning message');
logger.error('Error message');
```

## Performance Monitoring

### Metrics Collection
```javascript
// Performance monitoring
const { PluginMonitor } = require('@plugin-dev/monitoring');

const monitor = new PluginMonitor({
  interval: 60000, // 1 minute
  metrics: ['cpu', 'memory', 'latency', 'throughput']
});

// Custom metrics
monitor.addMetric('custom-metric', () => {
  return calculateCustomMetric();
});
```

### Performance Optimization
```bash
# Analyze performance
plugin-dev analyze --performance

# Optimize bundle
plugin-dev optimize --bundle

# Memory profiling
plugin-dev profile --memory --duration=300000
```

## Security

### Security Scanning
```bash
# Security audit
plugin-dev audit --security

# Dependency vulnerability check
plugin-dev audit --dependencies

# Code security analysis
plugin-dev audit --code --rules=owasp-top-ten
```

### Secure Development Practices
```javascript
// Secure input handling
const { SecurityUtils } = require('@plugin-dev/security');

function sanitizeInput(input) {
  return SecurityUtils.sanitize(input, {
    allowedTags: ['b', 'i', 'em'],
    allowedAttributes: ['class'],
    maxLength: 1000
  });
}

// Secure API calls
const secureApi = SecurityUtils.createSecureApi({
  timeout: 30000,
  retries: 3,
  validateSSL: true
});
```

## Contributing

1. Fork the repository
2. Create feature branch
3. Add tests
4. Ensure all checks pass
5. Submit pull request

## License

MIT License - see LICENSE file for details.