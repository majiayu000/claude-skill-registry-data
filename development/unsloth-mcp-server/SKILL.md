---
name: unsloth-mcp-server
description: Work with the Unsloth MCP Server codebase. Use when maintaining, extending, or debugging this specific MCP server implementation. Provides architecture knowledge, code patterns, and development workflows.
---

# Unsloth MCP Server Development

Project-specific guidance for the Unsloth MCP Server codebase.

## Project Overview

A production-ready MCP (Model Context Protocol) server that enables Claude to fine-tune LLMs using Unsloth.

**Location:** `/home/user/unsloth-mcp-server`

**Key Stats:**

- Version: 2.1.0
- 12 MCP tools
- 66 tests (100% passing)
- 7 test suites
- TypeScript with strict mode
- Full CI/CD pipeline

## Architecture

```
src/
├── index.ts           # Main MCP server (1414 lines)
├── cli.ts             # CLI tool (245 lines)
├── utils/            # Utility modules
│   ├── logger.ts     # Winston logging
│   ├── validation.ts # Input validation
│   ├── security.ts   # Security controls
│   ├── metrics.ts    # Performance tracking
│   ├── config.ts     # Configuration system
│   ├── cache.ts      # Dual-layer cache
│   └── progress.ts   # Progress tracking
└── __tests__/        # Test suites
    ├── validation.test.ts
    ├── security.test.ts
    ├── metrics.test.ts
    ├── cache.test.ts
    ├── config.test.ts
    ├── progress.test.ts
    └── integration.test.ts
```

## Available Tools

1. **check_installation** - Verify Unsloth is installed
2. **list_supported_models** - List available models (with caching)
3. **load_model** - Load model with optimizations
4. **finetune_model** - Fine-tune with LoRA
5. **generate_text** - Generate text from model
6. **export_model** - Export to GGUF/Ollama/vLLM/HF
7. **train_superbpe_tokenizer** - Train SuperBPE tokenizer
8. **get_model_info** - Get model architecture details
9. **compare_tokenizers** - Compare tokenization efficiency
10. **benchmark_model** - Benchmark performance
11. **list_datasets** - Search Hugging Face datasets
12. **prepare_dataset** - Prepare dataset for training

## Development Workflow

### Running Tests

```bash
npm test                  # All tests
npm test:watch           # Watch mode
npm test:coverage        # With coverage
npm test -- integration  # Just integration tests
```

### Building

```bash
npm run build            # Compile TypeScript
npm run lint             # Type check + ESLint
npm run lint:fix         # Auto-fix issues
npm run format           # Format with Prettier
```

### Benchmarking

```bash
npm run bench            # Run performance benchmarks
npm run bench:compare baseline.json results.json  # Compare
```

### CLI Testing

```bash
npm run cli help         # Show help
npm run cli check        # Check installation
npm run cli models       # List models
npm run cli config       # Show config
npm run cli metrics      # Show metrics
```

## Code Patterns

### Adding a New Tool

1. **Add validation in `src/utils/validation.ts`:**

```typescript
case 'your_new_tool':
  validators.requiredField(args, 'required_param');
  validators.optionalPositive(args, 'optional_param', 'Optional param');
  break;
```

2. **Add tool definition in `src/index.ts` (ListToolsRequestSchema):**

```typescript
{
  name: 'your_new_tool',
  description: 'Clear description of what it does',
  inputSchema: {
    type: 'object',
    properties: {
      required_param: {
        type: 'string',
        description: 'Parameter description'
      }
    },
    required: ['required_param']
  }
}
```

3. **Add handler in `src/index.ts` (CallToolRequestSchema):**

```typescript
case 'your_new_tool': {
  const { required_param } = args as { required_param: string };

  const script = `
import json
try:
    # Your Python code here
    result = {"success": True}
    print(json.dumps(result))
except Exception as e:
    print(json.dumps({"error": str(e)}))
`;

  const result = await this.executeUnslothScript(script);
  return this.createSuccessResponse(name, startTime, result);
}
```

4. **Add tests in `src/__tests__/validation.test.ts`:**

```typescript
describe('your_new_tool', () => {
  it('should validate required parameters', () => {
    expect(() =>
      validateToolInputs('your_new_tool', {
        required_param: 'value',
      })
    ).not.toThrow();
  });

  it('should reject missing parameters', () => {
    expect(() => validateToolInputs('your_new_tool', {})).toThrow('required_param is required');
  });
});
```

### Using Utilities

#### Logging

```typescript
import logger from './utils/logger.js';

logger.info('Operation started', { param: value });
logger.debug('Debug info', { details });
logger.error('Error occurred', { error: err.message });
```

#### Cache

```typescript
import { cache } from './utils/cache.js';

// Check cache first
const cached = cache.get<ModelList>('models');
if (cached) return cached;

// Compute and cache
const models = await loadModels();
cache.set('models', models, 3600); // 1 hour TTL
```

#### Metrics

```typescript
import { metricsCollector } from './utils/metrics.js';

const startTime = Date.now();
// ... operation ...
metricsCollector.endTool('tool_name', startTime, true);

const stats = metricsCollector.getStats('tool_name');
```

#### Configuration

```typescript
import { config } from './utils/config.js';

const serverConfig = config.get();
const cacheEnabled = serverConfig.cache.enabled;
```

## Configuration

Config files (priority order):

1. Environment variables (`UNSLOTH_*`)
2. `./config.json`
3. `~/.unsloth-mcp-config.json`
4. Default values

Example `config.json`:

```json
{
  "cache": {
    "enabled": true,
    "ttl": 3600,
    "maxSize": 1000
  },
  "logging": {
    "level": "info"
  }
}
```

## Testing Strategy

### Unit Tests (56 tests)

- Validation: 15 tests
- Security: 10 tests
- Metrics: 15 tests
- Cache: 5 tests
- Config: 5 tests
- Progress: 3 tests

### Integration Tests (10 tests)

- Utilities working together
- Full workflow simulation
- Error handling across modules
- Performance under load

## Common Tasks

### Update Version

1. Update `package.json` version
2. Update `src/index.ts` version (2 places)
3. Update `CHANGELOG.md`
4. Commit: `feat: bump version to X.Y.Z`

### Add New Utility

1. Create `src/utils/your-utility.ts`
2. Export class and singleton
3. Add tests in `src/__tests__/your-utility.test.ts`
4. Import in `src/index.ts`
5. Document in README

### Fix Performance Issue

1. Run benchmarks: `npm run bench`
2. Compare with baseline
3. Identify bottleneck
4. Optimize
5. Run benchmarks again
6. Update baseline if improved >10%

## CI/CD

GitHub Actions runs on every push/PR:

- Test on Node 18.x and 20.x
- TypeScript type checking
- ESLint validation
- Build verification
- Security audit

Pre-commit hooks (Husky):

- ESLint --fix on staged .ts files
- Prettier on staged files
- TypeScript type checking

## Performance Targets

| Operation  | Target   | Actual     |
| ---------- | -------- | ---------- |
| Validation | <0.01ms  | ✅ 0.005ms |
| Cache Get  | <0.01ms  | ✅ 0.010ms |
| Cache Set  | <0.02ms  | ✅ 0.015ms |
| Config Get | <0.005ms | ✅ 0.005ms |
| Metrics    | <0.01ms  | ✅ 0.010ms |

## Deployment

### Docker

```bash
docker-compose build
docker-compose up unsloth-mcp
```

### Native

```bash
npm install
npm run build
npm start
```

### MCP Settings

```json
{
  "mcpServers": {
    "unsloth-server": {
      "command": "node",
      "args": ["/path/to/build/index.js"],
      "env": {
        "HUGGINGFACE_TOKEN": "your_token"
      }
    }
  }
}
```

## Troubleshooting

### Tests Failing

- Check Node version (18 or 20)
- Run `npm install` again
- Clear cache: `rm -rf .cache/`

### Build Errors

- Run `npm run lint` to see TypeScript errors
- Check `tsconfig.json` is valid
- Verify all imports end with `.js`

### Pre-commit Hooks Not Running

- Run `npm run prepare`
- Check `.husky/pre-commit` exists
- Verify executable: `chmod +x .husky/pre-commit`

## Resources

- **README.md** - User documentation
- **PRODUCTION_GUIDE.md** - Deployment guide
- **CHANGELOG.md** - Version history
- **CONTRIBUTING.md** - Contribution guidelines
- **examples/** - Usage examples
- **benchmarks/** - Performance benchmarks

## Quick Commands Reference

```bash
# Development
npm run dev          # Run in dev mode
npm run cli check    # Test CLI

# Testing
npm test             # Run all tests
npm run lint         # Check types and lint

# Building
npm run build        # Build for production

# Benchmarking
npm run bench        # Run benchmarks

# Formatting
npm run format       # Format all files
```

## Contact & Support

- **Issues**: GitHub Issues
- **Docs**: See README.md and examples/
- **Tests**: Run `npm test` for examples
