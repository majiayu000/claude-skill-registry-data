---
name: opencode-mcp-figma-auth
description: Authenticate OpenCode with Figma MCP server to enable Figma design integration
triggers:
  - authenticate with figma mcp
  - log into figma for opencode
  - connect opencode to figma
  - set up figma mcp authentication
  - create figma mcp auth file
  - enable figma access for mcp
  - configure figma mcp connection
  - authenticate figma design server
---

# OpenCode MCP Figma Authentication

> Skill by [ara.so](https://ara.so) — Design Skills collection.

This skill enables authentication with Figma's MCP (Model Context Protocol) server for OpenCode and other AI agents. Figma MCP rejects non-whitelisted agents by default; this tool generates the required authentication file to bypass that restriction.

## What It Does

OpenCode MCP Figma is a minimal authentication tool that:
- Connects to Figma's MCP server at `https://mcp.figma.com/mcp`
- Handles the OAuth-style authentication flow
- Generates an `mcp-auth.json` file with valid credentials
- Enables OpenCode and other AI agents to access Figma design data via MCP

This is specifically needed because Figma's MCP server has agent whitelisting that blocks OpenCode by default.

## Installation

```bash
# Clone or navigate to the project directory
npm install
npm run build
```

## Key Commands

### Authenticate with Figma MCP

```bash
npm start https://mcp.figma.com/mcp
```

This command:
1. Initiates authentication with Figma's MCP server
2. Creates an `mcp-auth.json` file in the current directory
3. The file contains credentials needed for subsequent MCP connections

### Install Authentication File

After authentication, move the generated file to OpenCode's MCP auth location:

```bash
# Linux/macOS
mv mcp-auth.json ~/.local/share/opencode/mcp-auth.json

# Or merge with existing file if you have other MCP authentications
cat mcp-auth.json >> ~/.local/share/opencode/mcp-auth.json
```

```bash
# Windows
move mcp-auth.json %LOCALAPPDATA%\opencode\mcp-auth.json
```

## Configuration

### Project Structure

```
opencode-mcp-figma/
├── src/
│   └── index.ts          # Main authentication logic
├── package.json
├── tsconfig.json
└── mcp-auth.json         # Generated after authentication
```

### Generated Auth File Format

The `mcp-auth.json` file follows this structure:

```json
{
  "https://mcp.figma.com/mcp": {
    "token": "generated-token-here",
    "expires": 1234567890000
  }
}
```

### OpenCode MCP Configuration

After authentication, configure OpenCode to use Figma MCP by adding to your MCP settings:

```json
{
  "mcpServers": {
    "figma": {
      "url": "https://mcp.figma.com/mcp"
    }
  }
}
```

## Code Examples

### Basic Authentication Flow (TypeScript)

```typescript
import { authenticate } from './src/index';

// Authenticate with Figma MCP server
const mcpUrl = 'https://mcp.figma.com/mcp';

authenticate(mcpUrl)
  .then(() => {
    console.log('Authentication successful');
    console.log('mcp-auth.json created in current directory');
  })
  .catch((error) => {
    console.error('Authentication failed:', error);
  });
```

### Programmatic Auth File Management

```typescript
import * as fs from 'fs';
import * as path from 'path';
import * as os from 'os';

// Read generated auth file
const authFile = fs.readFileSync('mcp-auth.json', 'utf-8');
const authData = JSON.parse(authFile);

// Get OpenCode's MCP auth path
const openCodeAuthPath = path.join(
  os.homedir(),
  '.local',
  'share',
  'opencode',
  'mcp-auth.json'
);

// Merge with existing auth if present
let existingAuth = {};
if (fs.existsSync(openCodeAuthPath)) {
  existingAuth = JSON.parse(fs.readFileSync(openCodeAuthPath, 'utf-8'));
}

const mergedAuth = { ...existingAuth, ...authData };

// Write merged auth
fs.mkdirSync(path.dirname(openCodeAuthPath), { recursive: true });
fs.writeFileSync(openCodeAuthPath, JSON.stringify(mergedAuth, null, 2));

console.log(`Auth file installed to ${openCodeAuthPath}`);
```

### Verify Authentication

```typescript
import * as fs from 'fs';

function verifyAuth(mcpUrl: string): boolean {
  try {
    const authFile = fs.readFileSync('mcp-auth.json', 'utf-8');
    const authData = JSON.parse(authFile);
    
    if (!authData[mcpUrl]) {
      console.error(`No authentication found for ${mcpUrl}`);
      return false;
    }
    
    const { token, expires } = authData[mcpUrl];
    
    if (!token) {
      console.error('Token is missing');
      return false;
    }
    
    if (expires && Date.now() > expires) {
      console.error('Token has expired');
      return false;
    }
    
    console.log('Authentication is valid');
    return true;
  } catch (error) {
    console.error('Failed to verify authentication:', error);
    return false;
  }
}

verifyAuth('https://mcp.figma.com/mcp');
```

## Common Patterns

### One-Time Setup Script

```typescript
#!/usr/bin/env node
import { authenticate } from './src/index';
import { execSync } from 'child_process';
import * as path from 'path';
import * as os from 'os';

async function setup() {
  const mcpUrl = 'https://mcp.figma.com/mcp';
  
  console.log('Authenticating with Figma MCP...');
  await authenticate(mcpUrl);
  
  const destPath = path.join(
    os.homedir(),
    '.local',
    'share',
    'opencode',
    'mcp-auth.json'
  );
  
  console.log('Installing auth file...');
  execSync(`mkdir -p ${path.dirname(destPath)}`);
  execSync(`mv mcp-auth.json ${destPath}`);
  
  console.log('✓ Figma MCP authentication complete');
  console.log('You can now use Figma with OpenCode');
}

setup().catch(console.error);
```

### CI/CD Authentication

```typescript
// For automated environments where manual auth isn't possible
import * as fs from 'fs';

function setupAuthFromEnv() {
  const figmaToken = process.env.FIGMA_MCP_TOKEN;
  const figmaExpires = process.env.FIGMA_MCP_EXPIRES;
  
  if (!figmaToken) {
    throw new Error('FIGMA_MCP_TOKEN environment variable required');
  }
  
  const authData = {
    'https://mcp.figma.com/mcp': {
      token: figmaToken,
      expires: figmaExpires ? parseInt(figmaExpires) : undefined
    }
  };
  
  fs.writeFileSync('mcp-auth.json', JSON.stringify(authData, null, 2));
  console.log('Auth file created from environment variables');
}
```

## Troubleshooting

### Authentication Fails

**Problem**: Authentication command returns an error

**Solutions**:
- Ensure you have network connectivity to `https://mcp.figma.com/mcp`
- Check that you're using the correct MCP URL
- Verify npm dependencies are installed: `npm install`
- Rebuild the project: `npm run build`

### Auth File Not Found by OpenCode

**Problem**: OpenCode doesn't recognize the authentication

**Solutions**:
```bash
# Verify file location
ls -la ~/.local/share/opencode/mcp-auth.json

# Check file permissions
chmod 600 ~/.local/share/opencode/mcp-auth.json

# Verify file contents
cat ~/.local/share/opencode/mcp-auth.json
```

### Token Expired

**Problem**: Authentication worked initially but now fails

**Solution**: Re-run authentication to generate a new token:
```bash
npm start https://mcp.figma.com/mcp
mv mcp-auth.json ~/.local/share/opencode/mcp-auth.json
```

### Multiple MCP Servers

**Problem**: Need to authenticate with multiple MCP servers

**Solution**: Merge auth files instead of overwriting:
```typescript
import * as fs from 'fs';

const newAuth = JSON.parse(fs.readFileSync('mcp-auth.json', 'utf-8'));
const existingPath = '~/.local/share/opencode/mcp-auth.json';
const existing = JSON.parse(fs.readFileSync(existingPath, 'utf-8'));

const merged = { ...existing, ...newAuth };
fs.writeFileSync(existingPath, JSON.stringify(merged, null, 2));
```

## Related Context

This tool addresses the issue described in [OpenCode Issue #988](https://github.com/anomalyco/opencode/issues/988) where Figma's MCP server whitelisting blocks certain AI agents. While designed for Figma, the authentication approach may work with other MCP servers that implement similar authentication mechanisms.
