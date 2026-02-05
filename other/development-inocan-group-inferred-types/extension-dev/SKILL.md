---
name: extension-dev
description: VS Code Extension 后端开发模块。当需要添加命令、修改插件入口、管理 Webview Panel、处理消息、使用 VS Code API 时使用。涵盖命令注册、Webview 管理、文件操作、配置管理等。
---

# Extension 后端开发

负责 VS Code Extension 后端的开发，包括命令注册、Webview 管理、VS Code API 调用等。

## 目录结构

```
extension/
├─ index.ts              # 插件入口 (activate/deactivate)
├─ commands/             # 命令处理器
│   └─ openWebview.ts    # 打开 Webview 命令
└─ webview/              # Webview 管理
    ├─ WebviewPanel.ts   # Panel 类
    └─ getHtml.ts        # HTML 生成
```

## Instructions

### 1. 添加新命令

**步骤 1**: 在 `package.json` 注册命令
```json
{
  "contributes": {
    "commands": [
      {
        "command": "my-extension.newCommand",
        "title": "My New Command"
      }
    ]
  }
}
```

**步骤 2**: 创建命令处理器 `extension/commands/newCommand.ts`
```typescript
import * as vscode from 'vscode';

export function newCommand(context: vscode.ExtensionContext) {
  vscode.window.showInformationMessage('New command executed!');
}
```

**步骤 3**: 在 `extension/index.ts` 注册
```typescript
import { newCommand } from './commands/newCommand';

export function activate(context: vscode.ExtensionContext) {
  context.subscriptions.push(
    vscode.commands.registerCommand('my-extension.newCommand', () =>
      newCommand(context)
    )
  );
}
```

### 2. 处理 Webview 消息

在 `WebviewPanel.ts` 的 `_handleMessage` 方法中添加：
```typescript
private _handleMessage(message: WebviewMessage) {
  switch (message.type) {
    case 'newAction':
      // 处理逻辑
      this._panel.webview.postMessage({
        type: 'newActionResponse',
        payload: result
      });
      break;
  }
}
```

### 3. 常用 VS Code API

```typescript
// 显示消息
vscode.window.showInformationMessage('Info');
vscode.window.showWarningMessage('Warning');
vscode.window.showErrorMessage('Error');

// 获取当前编辑器
const editor = vscode.window.activeTextEditor;

// 读取文件
const uri = vscode.Uri.file('/path/to/file');
const content = await vscode.workspace.fs.readFile(uri);

// 写入文件
await vscode.workspace.fs.writeFile(uri, Buffer.from('content'));

// 获取配置
const config = vscode.workspace.getConfiguration('my-extension');
const value = config.get<string>('settingName');

// 注册配置变化监听
vscode.workspace.onDidChangeConfiguration(e => {
  if (e.affectsConfiguration('my-extension')) {
    // 重新加载配置
  }
});
```

### 4. 添加配置项

在 `package.json` 添加：
```json
{
  "contributes": {
    "configuration": {
      "title": "My Extension",
      "properties": {
        "my-extension.setting1": {
          "type": "string",
          "default": "value",
          "description": "Setting description"
        }
      }
    }
  }
}
```

## Best Practices

- 所有命令都通过 `context.subscriptions.push()` 注册以确保清理
- 使用 `async/await` 处理异步操作
- 错误处理使用 `try/catch` 并显示用户友好消息
- Webview 消息类型在 `shared/types/message.ts` 定义

## 常见问题

**Q: 命令未出现在命令面板？**
A: 检查 `package.json` 中的命令 ID 是否与代码中一致

**Q: Webview 资源加载失败？**
A: 确保使用 `webview.asWebviewUri()` 转换路径，并检查 `localResourceRoots`
