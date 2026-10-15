---
name: win-05-implementation
description: Windows App Workflow 阶段 5 —— 迭代实现（Sprint 循环）。适用场景：地基就绪，进入功能开发，需要安全编码规范（IPC/进程边界）、每任务 Dev↔QA 循环、足迹预算执行与代码审查标准。提炼自 Desktop App Engineer、Code Reviewer、Test Automation Engineer、Sprint Prioritizer 与 NEXUS Phase 3 的 Dev↔QA 循环。
---

# 阶段 5：迭代实现（Sprint 循环）

> 核心机制：**Dev↔QA 循环**——每个任务"实现 → 自测 → 证据化 QA → 通过才合并"。首版实现默认不完整，预留 2–3 轮返工预算。

## 1. Sprint 节奏（每周）

1. **计划（周一）**：从 RICE 排序的 backlog 取任务；每个任务有验收标准；估时超出本周容量的直接砍，不加班补救
2. **执行**：每任务一个分支 `feat/xxx`；小步提交；当天写完当天过 QA
3. **评审（周末）**：演示可运行的增量；更新 CHANGELOG
4. **回顾**：一句话记录本周最痛的点，下周改掉一个

## 2. 桌面端安全编码规范（每个功能都要过，来自 Desktop App Engineer）

### Electron 加固窗口（照抄）

```typescript
// main.ts —— 唯一接触操作系统的进程
const win = new BrowserWindow({
  webPreferences: {
    contextIsolation: true,   // 渲染进程拿到的是桥，不是你的内脏
    nodeIntegration: false,   // web 内容里永远没有 require()
    sandbox: true,
    preload: path.join(__dirname, 'preload.js'),
  },
});

// IPC：窄动词 + 边界处校验（zod），绝不提供通用文件/Shell 通道
import { z } from 'zod';
const ExportRequest = z.object({
  format: z.enum(['csv', 'json']),
  projectId: z.string().uuid(),
});
ipcMain.handle('project:export', async (event, raw) => {
  const req = ExportRequest.parse(raw);                 // 垃圾在边界处被拒绝
  const dest = await dialog.showSaveDialog(win, {       // 路径由用户选，应用不接收任意路径
    defaultPath: `export.${req.format}`,
  });
  if (dest.canceled) return { ok: false };
  await exportProject(req.projectId, req.format, dest.filePath);
  return { ok: true };
});
```

```typescript
// preload.ts —— 渲染进程能见到的全部 API
import { contextBridge, ipcRenderer } from 'electron';
contextBridge.exposeInMainWorld('app', {
  exportProject: (req: unknown) => ipcRenderer.invoke('project:export', req),
  onUpdateReady: (cb: () => void) => ipcRenderer.on('update:ready', cb),
});
```

### Tauri 能力授权（默认拒绝）

```json
// src-tauri/capabilities/main.json —— 前端恰好拿到这些，多一分没有
{
  "identifier": "main-window",
  "windows": ["main"],
  "permissions": [
    "core:default",
    "dialog:allow-save",
    { "identifier": "fs:allow-write-file", "allow": [{ "path": "$APPDATA/exports/*" }] }
  ]
}
```

### 每个功能的硬性要求

- 新增跨 IPC 功能 = 新增一个窄动词 + 特权侧输入校验 + 更新 IPC 契约文档
- 远程内容一律沙箱化、无 IPC
- 涉及文件/注册表/开机自启的操作，写清最小权限与失败回退
- 本地优先：断网状态下核心流程必须可用（有显式同步状态即可）

## 3. 足迹预算（CI 强制执行，超标即失败）

| 指标 | 预算 | 测量方式 |
|---|---|---|
| 冷启动到可交互 | < 2s（低端参考机） | CI 启动 trace，10 次取 p95 |
| 空闲内存（全进程） | < 300MB Electron / < 150MB Tauri（原生应用自定，宜更低） | 启动后静置 5 分钟采样 |
| 安装包体积 | 每个版本增长 ≤5%，超出要解释 | 与上一版产物 diff |
| 空闲 CPU | ~0%（不允许定时器唤醒机器） | 浸泡测试采样 |

## 4. 代码审查标准（来自 Code Reviewer：审正确性/可维护性/安全/性能，不审风格癖好）

每个任务自审清单：
1. **正确性**：边界条件（空数据、超长输入、并发双击、磁盘满、路径含中文/空格）
2. **安全**：输入在信任边界校验了吗？有新的通用通道吗？依赖更新了吗？
3. **可维护性**：命名是否说明意图；一个函数一件事；重复 ≥3 次才抽象
4. **性能**：渲染循环里有没有昂贵计算；大列表有没有虚拟化；启动路径懒加载
5. **平台**：快捷键、托盘、文件对话框符合 Windows 约定吗？

## 5. 测试伴随开发（不是最后补，细则见阶段 6）

- 每个功能带单元测试（域逻辑，不依赖 UI）
- 每个核心旅程带 1 条 E2E 冒烟（能进 CI 的）
- 测试代码与功能代码同一个 PR

## 6. 单任务质量门（每个任务合并前）

| # | 判据 | 通过？ |
|---|------|--------|
| 1 | 验收标准逐条演示（截图/录屏） | ☐ |
| 2 | 新增/修改测试全绿 | ☐ |
| 3 | 自审清单 5 项过一遍 | ☐ |
| 4 | 足迹指标无回归 | ☐ |
| 5 | CHANGELOG 更新 | ☐ |

全部任务完成后 → 阶段 6（测试加固）。若时间线内做不完：砍 Later 功能，**不砍加固周**。
