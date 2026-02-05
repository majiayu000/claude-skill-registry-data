---
name: codexray
description: codeXray 功能开发模块。当需要实现项目分析、文档生成、代码注释、AI 工作流、Copilot API 集成时使用。涵盖文件遍历、分层分析、上下文管理、文档输出等核心功能。
---

# codeXray 功能开发

codeXray 是 AI Omni 的核心功能模块，实现 AI 驱动的项目分析和文档生成。

## 功能概述

基于 [prd/codeXray/brief.md](../../../../prd/codeXray/brief.md) 的需求：

1. **项目遍历**：递归扫描目录，构建文件树
2. **分层理解**：以目录为单位进行 AI 分析
3. **文档生成**：生成项目概述 Markdown
4. **代码注释**：为文件添加行级注释

## 目录结构 (规划)

```
extension/
├─ commands/
│   └─ analyzeProject.ts     # 分析项目命令
├─ services/
│   ├─ fileScanner.ts        # 文件扫描服务
│   ├─ projectAnalyzer.ts    # 项目分析服务
│   ├─ documentGenerator.ts  # 文档生成服务
│   └─ codeAnnotator.ts      # 代码注释服务
└─ utils/
    ├─ fileTree.ts           # 文件树工具
    └─ contextManager.ts     # 上下文管理
```

## Instructions

### 1. 实现文件扫描服务

```typescript
// extension/services/fileScanner.ts
import * as vscode from 'vscode';
import * as path from 'path';

export interface FileInfo {
  path: string;
  relativePath: string;
  type: 'file' | 'directory';
  name: string;
  extension?: string;
  children?: FileInfo[];
}

export interface ScanOptions {
  maxDepth?: number;
  excludePatterns?: string[];
}

const DEFAULT_EXCLUDES = [
  'node_modules',
  '.git',
  'dist',
  '.vscode',
  '*.log'
];

export async function scanDirectory(
  rootPath: string,
  options: ScanOptions = {}
): Promise<FileInfo> {
  const { maxDepth = 10, excludePatterns = DEFAULT_EXCLUDES } = options;
  
  async function scan(dirPath: string, depth: number): Promise<FileInfo> {
    const name = path.basename(dirPath);
    const relativePath = path.relative(rootPath, dirPath);
    
    const info: FileInfo = {
      path: dirPath,
      relativePath: relativePath || '.',
      type: 'directory',
      name,
      children: []
    };
    
    if (depth >= maxDepth) return info;
    
    const entries = await vscode.workspace.fs.readDirectory(
      vscode.Uri.file(dirPath)
    );
    
    for (const [entryName, entryType] of entries) {
      // 检查排除模式
      if (shouldExclude(entryName, excludePatterns)) continue;
      
      const entryPath = path.join(dirPath, entryName);
      
      if (entryType === vscode.FileType.Directory) {
        info.children!.push(await scan(entryPath, depth + 1));
      } else if (entryType === vscode.FileType.File) {
        info.children!.push({
          path: entryPath,
          relativePath: path.relative(rootPath, entryPath),
          type: 'file',
          name: entryName,
          extension: path.extname(entryName)
        });
      }
    }
    
    return info;
  }
  
  return scan(rootPath, 0);
}

function shouldExclude(name: string, patterns: string[]): boolean {
  return patterns.some(pattern => {
    if (pattern.startsWith('*')) {
      return name.endsWith(pattern.slice(1));
    }
    return name === pattern;
  });
}
```

### 2. 集成 Copilot API (计划)

```typescript
// extension/services/projectAnalyzer.ts
import * as vscode from 'vscode';

export async function analyzeWithCopilot(
  content: string,
  prompt: string
): Promise<string> {
  // 获取 Copilot Language Model
  const models = await vscode.lm.selectChatModels({
    vendor: 'copilot',
    family: 'gpt-4o'
  });
  
  if (models.length === 0) {
    throw new Error('Copilot model not available');
  }
  
  const model = models[0];
  
  // 构建消息
  const messages = [
    vscode.LanguageModelChatMessage.User(prompt + '\n\n' + content)
  ];
  
  // 发送请求
  const response = await model.sendRequest(messages, {});
  
  // 收集流式响应
  let result = '';
  for await (const chunk of response.text) {
    result += chunk;
  }
  
  return result;
}
```

### 3. 分层分析策略

```typescript
// 自底向上分析
async function analyzeProjectHierarchy(root: FileInfo): Promise<void> {
  // 1. 先分析所有叶子目录
  const leafDirs = findLeafDirectories(root);
  for (const dir of leafDirs) {
    dir.summary = await analyzeDirectory(dir);
  }
  
  // 2. 向上汇总到父目录
  await rollupToParent(root);
  
  // 3. 生成整体文档
  const overview = await generateOverview(root);
}

// 上下文控制：每次只发送当前层 + 子层摘要
function buildPromptForDirectory(dir: FileInfo): string {
  const childSummaries = dir.children
    ?.filter(c => c.type === 'directory')
    .map(c => `- ${c.name}: ${c.summary}`)
    .join('\n');
  
  const files = dir.children
    ?.filter(c => c.type === 'file')
    .map(c => `- ${c.name}`)
    .join('\n');
  
  return `
分析目录: ${dir.name}

子目录摘要:
${childSummaries || '无'}

包含文件:
${files || '无'}

请总结此目录的职责和主要功能。
  `.trim();
}
```

### 4. 注册命令

```typescript
// extension/commands/analyzeProject.ts
import * as vscode from 'vscode';
import { scanDirectory } from '../services/fileScanner';

export async function analyzeProject(context: vscode.ExtensionContext) {
  // 1. 让用户选择目录
  const folders = await vscode.window.showOpenDialog({
    canSelectFolders: true,
    canSelectFiles: false,
    canSelectMany: false,
    title: 'Select Project to Analyze'
  });
  
  if (!folders || folders.length === 0) return;
  
  const rootPath = folders[0].fsPath;
  
  // 2. 显示进度
  await vscode.window.withProgress({
    location: vscode.ProgressLocation.Notification,
    title: 'Analyzing project...',
    cancellable: true
  }, async (progress, token) => {
    // 3. 扫描目录
    progress.report({ message: 'Scanning files...' });
    const fileTree = await scanDirectory(rootPath);
    
    if (token.isCancellationRequested) return;
    
    // 4. AI 分析 (待实现)
    progress.report({ message: 'Analyzing with AI...' });
    // await analyzeProjectHierarchy(fileTree);
    
    // 5. 生成文档 (待实现)
    progress.report({ message: 'Generating documentation...' });
    // await generateDocumentation(fileTree, rootPath);
    
    vscode.window.showInformationMessage('Project analysis complete!');
  });
}
```

## 配置项

在 `package.json` 添加：

```json
{
  "contributes": {
    "configuration": {
      "title": "AI Omni - codeXray",
      "properties": {
        "aiOmni.codeXray.commentLanguage": {
          "type": "string",
          "default": "chinese",
          "enum": ["chinese", "english"],
          "description": "Language for generated comments"
        },
        "aiOmni.codeXray.maxDepth": {
          "type": "number",
          "default": 10,
          "description": "Maximum directory depth to scan"
        },
        "aiOmni.codeXray.outputPath": {
          "type": "string",
          "default": "",
          "description": "Path to save generated documentation"
        }
      }
    }
  }
}
```

## 实施阶段

| 阶段 | 任务 | 状态 |
|------|------|------|
| 1 | 文件遍历和文件树构建 | 🔲 待开发 |
| 2 | Copilot API 集成和分层分析 | 🔲 待开发 |
| 3 | 文档生成和 UI 预览 | 🔲 待开发 |
| 4 | 代码注释功能 | 🔲 待开发 |
| 5 | 测试和优化 | 🔲 待开发 |

## 参考资料

- [需求文档](../../../../prd/codeXray/brief.md)
- [VS Code Language Model API](https://code.visualstudio.com/api/extension-guides/language-model)
- [Copilot Extension Sample](https://github.com/microsoft/vscode-extension-samples/tree/main/chat-sample)
