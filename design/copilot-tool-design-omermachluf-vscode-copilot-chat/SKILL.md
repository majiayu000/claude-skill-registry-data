---
name: copilot-tool-design
description: Guide to designing and implementing tools for the vscode-copilot-chat extension, including patterns, testing, and best practices
keywords: tools, copilot, vscode, language model, api, implementation
---

This skill provides comprehensive guidance on designing, implementing, and testing tools for the vscode-copilot-chat extension.

## What are Tools?

Tools are capabilities that Copilot agents can invoke to interact with the system. They enable agents to:
- Read and write files
- Execute commands
- Search the codebase
- Interact with VS Code APIs
- Call external services

## Tool Architecture

### Tool Interface

Every tool implements this interface:

```typescript
export interface IToolName {
  invoke(
    options: LanguageModelToolInvocationOptions,
    token: CancellationToken
  ): Promise<LanguageModelToolResult>;
}
```

**Key components**:
- `LanguageModelToolInvocationOptions` - Contains input parameters
- `CancellationToken` - For cancellable operations
- `LanguageModelToolResult` - Structured response

### Tool Registration

Tools are registered in `src/extension/tools/vscode-node/tools.ts`:

```typescript
tools.push({
  name: ToolName.MyTool,           // Enum value
  description: 'What the tool does',  // For LLM understanding
  inputSchema: { /* JSON schema */ }, // Expected input format
  invoke: async (options, token) => {
    const tool = instantiationService.createInstance(MyTool);
    return tool.invoke(options, token);
  }
});
```

## Tool Design Principles

### 1. Single Responsibility

Each tool should do ONE thing well:

```typescript
// ✅ GOOD - Single purpose
class ReadFileTool {
  async invoke(options, token) {
    const { filePath } = options.input;
    const content = await this.fs.readFile(filePath);
    return this.formatResponse(content);
  }
}

// ❌ BAD - Multiple responsibilities
class FileOperationsTool {
  async invoke(options, token) {
    const { operation, filePath, content } = options.input;
    switch (operation) {
      case 'read': return this.read(filePath);
      case 'write': return this.write(filePath, content);
      case 'delete': return this.delete(filePath);
      case 'search': return this.search(filePath);
    }
  }
}
```

**Why**: Single-purpose tools are easier to understand, test, and compose.

### 2. Clear Input Schema

Define precise, well-documented schemas:

```typescript
inputSchema: {
  type: 'object',
  properties: {
    filePath: {
      type: 'string',
      description: 'Absolute path to the file to read'
    },
    encoding: {
      type: 'string',
      description: 'File encoding (default: utf-8)',
      enum: ['utf-8', 'ascii', 'base64'],
      default: 'utf-8'
    },
    maxLines: {
      type: 'number',
      description: 'Maximum number of lines to read',
      minimum: 1
    }
  },
  required: ['filePath']
}
```

**Best practices**:
- Describe every property clearly
- Use `enum` for fixed choices
- Mark required fields
- Provide defaults when sensible
- Use specific types (not just 'string')

### 3. Structured Output

Return well-formatted, parseable results:

```typescript
// ✅ GOOD - Structured JSON
return new LanguageModelToolResult([
  new LanguageModelTextPart(JSON.stringify({
    success: true,
    filePath: path,
    content: fileContent,
    lines: lineCount,
    encoding: 'utf-8'
  }, null, 2))
]);

// ❌ BAD - Unstructured text
return new LanguageModelToolResult([
  new LanguageModelTextPart(
    `File: ${path}\nContent: ${fileContent}\nLines: ${lineCount}`
  )
]);
```

**Why**: Structured output is easier for the LLM to parse and use.

### 4. Error Handling

Handle errors gracefully with informative messages:

```typescript
async invoke(options, token) {
  try {
    const { filePath } = options.input;

    // Validate input
    if (!filePath) {
      return this.errorResponse('filePath is required');
    }

    if (!path.isAbsolute(filePath)) {
      return this.errorResponse('filePath must be absolute');
    }

    // Perform operation
    const content = await this.fs.readFile(filePath, 'utf-8');

    return this.successResponse({
      filePath,
      content,
      size: content.length
    });

  } catch (error) {
    // Specific error messages
    if (error.code === 'ENOENT') {
      return this.errorResponse(`File not found: ${filePath}`);
    }
    if (error.code === 'EACCES') {
      return this.errorResponse(`Permission denied: ${filePath}`);
    }
    return this.errorResponse(`Error reading file: ${error.message}`);
  }
}

private successResponse(data: any) {
  return new LanguageModelToolResult([
    new LanguageModelTextPart(JSON.stringify({
      success: true,
      ...data
    }, null, 2))
  ]);
}

private errorResponse(message: string) {
  return new LanguageModelToolResult([
    new LanguageModelTextPart(JSON.stringify({
      success: false,
      error: message
    }, null, 2))
  ]);
}
```

### 5. Cancellation Support

Respect the CancellationToken:

```typescript
async invoke(options, token: CancellationToken) {
  // Check cancellation before expensive operations
  if (token.isCancellationRequested) {
    return this.errorResponse('Operation cancelled');
  }

  const files = await this.findFiles(pattern);

  // Check again during long operations
  for (const file of files) {
    if (token.isCancellationRequested) {
      return this.errorResponse('Operation cancelled');
    }

    await this.processFile(file);
  }

  return this.successResponse({ processedCount: files.length });
}
```

## Tool Implementation Pattern

### Complete Example

```typescript
// 1. Define the interface
export interface IMyTool {
  invoke(
    options: LanguageModelToolInvocationOptions,
    token: CancellationToken
  ): Promise<LanguageModelToolResult>;
}

export const IMyTool = createDecorator<IMyTool>('myTool');

// 2. Implement the tool
export class MyTool implements IMyTool {
  static readonly TOOL_ID = 'myTool';

  constructor(
    @IFileSystemService private readonly fs: IFileSystemService,
    @ILogService private readonly log: ILogService
  ) {}

  async invoke(
    options: LanguageModelToolInvocationOptions,
    token: CancellationToken
  ): Promise<LanguageModelToolResult> {
    try {
      this.log.info(`MyTool invoked with: ${JSON.stringify(options.input)}`);

      // Validate input
      const input = this.validateInput(options.input);

      // Check cancellation
      if (token.isCancellationRequested) {
        return this.errorResponse('Cancelled');
      }

      // Perform operation
      const result = await this.performOperation(input, token);

      // Return success
      return this.successResponse(result);

    } catch (error) {
      this.log.error(`MyTool error:`, error);
      return this.errorResponse(error.message);
    }
  }

  private validateInput(input: any): ValidatedInput {
    // Validation logic
    if (!input.requiredParam) {
      throw new Error('requiredParam is required');
    }
    return input as ValidatedInput;
  }

  private async performOperation(
    input: ValidatedInput,
    token: CancellationToken
  ): Promise<OperationResult> {
    // Implementation
  }

  private successResponse(data: any) {
    return new LanguageModelToolResult([
      new LanguageModelTextPart(JSON.stringify({ success: true, ...data }, null, 2))
    ]);
  }

  private errorResponse(error: string) {
    return new LanguageModelToolResult([
      new LanguageModelTextPart(JSON.stringify({ success: false, error }, null, 2))
    ]);
  }
}

// 3. Register in tools.ts
tools.push({
  name: ToolName.MyTool,
  description: 'Does something useful',
  inputSchema: {
    type: 'object',
    properties: {
      requiredParam: {
        type: 'string',
        description: 'A required parameter'
      }
    },
    required: ['requiredParam']
  },
  invoke: async (options, token) => {
    const tool = instantiationService.createInstance(MyTool);
    return tool.invoke(options, token);
  }
});

// 4. Add to toolNames.ts
export enum ToolName {
  // ... existing tools
  MyTool = 'myTool',
}
```

## Testing Tools

### Unit Test Pattern

```typescript
import { describe, it, expect, beforeEach, vi } from 'vitest';
import { MyTool } from '../../node/myTool.js';
import { MockFileSystemService } from '../mocks/mockFileSystem.js';

describe('MyTool', () => {
  let tool: MyTool;
  let mockFs: MockFileSystemService;
  let mockToken: CancellationToken;

  beforeEach(() => {
    mockFs = new MockFileSystemService();
    mockToken = { isCancellationRequested: false } as CancellationToken;
    tool = new MyTool(mockFs, mockLog);
  });

  it('should perform operation successfully', async () => {
    const options = {
      input: { requiredParam: 'value' }
    };

    const result = await tool.invoke(options, mockToken);
    const parsed = JSON.parse(result.content[0].value);

    expect(parsed.success).toBe(true);
    expect(parsed.data).toBeDefined();
  });

  it('should handle missing required parameter', async () => {
    const options = {
      input: {}  // Missing requiredParam
    };

    const result = await tool.invoke(options, mockToken);
    const parsed = JSON.parse(result.content[0].value);

    expect(parsed.success).toBe(false);
    expect(parsed.error).toContain('required');
  });

  it('should respect cancellation token', async () => {
    mockToken.isCancellationRequested = true;

    const options = {
      input: { requiredParam: 'value' }
    };

    const result = await tool.invoke(options, mockToken);
    const parsed = JSON.parse(result.content[0].value);

    expect(parsed.success).toBe(false);
    expect(parsed.error).toContain('cancel');
  });
});
```

## Common Tool Patterns

### File Operations

```typescript
// Read file
class ReadFileTool {
  async invoke(options, token) {
    const { filePath } = options.input;
    const content = await this.fs.readFile(filePath, 'utf-8');
    return this.successResponse({ filePath, content });
  }
}

// Write file
class WriteFileTool {
  async invoke(options, token) {
    const { filePath, content } = options.input;
    await this.fs.writeFile(filePath, content, 'utf-8');
    return this.successResponse({ filePath, written: true });
  }
}
```

### Search Operations

```typescript
class SearchFilesTool {
  async invoke(options, token) {
    const { pattern, includePattern, excludePattern } = options.input;

    const files = await this.workspace.findFiles(
      includePattern || '**/*',
      excludePattern || '**/node_modules/**'
    );

    const matches = [];
    for (const file of files) {
      if (token.isCancellationRequested) break;

      const content = await this.fs.readFile(file.fsPath, 'utf-8');
      if (content.includes(pattern)) {
        matches.push(file.fsPath);
      }
    }

    return this.successResponse({ matches, count: matches.length });
  }
}
```

### Command Execution

```typescript
class RunCommandTool {
  async invoke(options, token) {
    const { command, cwd } = options.input;

    const process = this.processService.spawn(command, {
      cwd,
      shell: true
    });

    const output = await new Promise<string>((resolve, reject) => {
      let stdout = '';
      process.stdout.on('data', (data) => stdout += data);
      process.on('close', (code) => {
        if (code === 0) resolve(stdout);
        else reject(new Error(`Command failed with code ${code}`));
      });

      token.onCancellationRequested(() => {
        process.kill();
        reject(new Error('Cancelled'));
      });
    });

    return this.successResponse({ output, exitCode: 0 });
  }
}
```

## Best Practices Summary

1. **Single Responsibility**: One tool, one purpose
2. **Clear Schemas**: Document every input parameter
3. **Structured Output**: Return JSON with success/error
4. **Error Handling**: Specific, helpful error messages
5. **Cancellation**: Check token during long operations
6. **Validation**: Validate inputs before processing
7. **Logging**: Log invocations and errors
8. **Testing**: Comprehensive unit tests
9. **Documentation**: Clear descriptions for LLM
10. **Security**: Validate file paths, sanitize inputs

Remember: Tools are how agents interact with the world. Well-designed tools enable powerful agent capabilities!
