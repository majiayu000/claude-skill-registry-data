---
name: feishu-card-ws
description: >
  飞书（Lark）交互式卡片在 WebSocket 长连接模式下的配置指南。涵盖卡片模板结构、
  EventDispatcher 注册、按钮回调处理、下拉选择值缓存、响应格式等完整流程。
  当需要在飞书 Bot 中添加交互式卡片（带按钮、下拉菜单等）并且使用 WS 长连接模式时，
  必须使用此 skill。即使只是添加一个简单的按钮或下拉菜单，也要先读此 skill。
  触发关键词：飞书卡片、interactive card、card callback、card.action.trigger、
  管理面板、select_static、button callback、200672、WS 卡片。
---

# 飞书卡片 WS 长连接配置指南

## 适用范围

本 skill 适用于使用 `@larksuiteoapi/node-sdk` 通过 WebSocket 长连接模式接收
飞书交互式卡片回调的场景。这套模式经过 2026-04-12 的实战验证，是目前唯一稳定可用的方案。

## 核心约束（先读这里）

Lark Node SDK v1.60.0 的 WSClient 有以下已确认的限制：

| 限制 | 影响 | 应对 |
|------|------|------|
| WSClient 不支持 CardActionHandler | `start()` 只接受 `eventDispatcher` 参数 | 用 EventDispatcher 注册 card.action.trigger |
| card 更新响应导致 200672 | `{ card: {...} }` 经 base64 编码后飞书无法解析 | 所有操作只返回 toast |
| form_submit 按钮事件不到达 | `action_type: "form_submit"` 走不同协议路径 | 使用普通 button，服务端缓存 select 值 |
| monkey-patch handleEventData 破坏消息投递 | 干扰 SDK 内部分片合并逻辑 | 不要 monkey-patch |

## 架构总览

```
用户发关键词 → im.message.receive_v1 → EventDispatcher → 发送卡片
用户选下拉   → card.action.trigger(select_static) → 缓存值 → return undefined
用户点按钮   → card.action.trigger(button) → 注入缓存值 → 业务处理 → return toast
```

三种交互全部通过同一个 EventDispatcher 路由，不需要任何 SDK 扩展或 monkey-patch。

---

## 第一步：卡片模板

### 下拉菜单 + 按钮组合

```typescript
// ✅ 正确：普通 button + select_static，不用 form 容器
{
  tag: "select_static",
  name: "my_select_key",                          // 用于服务端缓存的 key
  placeholder: { tag: "plain_text", content: "请选择" },
  value: { action: "my_select_key" },              // value.action 也用于识别
  options: [
    { text: { tag: "plain_text", content: "选项1" }, value: "1" },
    { text: { tag: "plain_text", content: "选项2" }, value: "2" },
  ],
}

{
  tag: "button",
  name: "my_action_name",                          // 按钮名称
  text: { tag: "plain_text", content: "🟢 执行操作" },
  type: "primary",
  value: { action: "my_action_name" },             // value.action 用于路由
}
```

### 独立按钮（无下拉）

```typescript
{
  tag: "button",
  name: "my_simple_action",
  text: { tag: "plain_text", content: "🔄 刷新" },
  type: "default",
  value: { action: "my_simple_action" },
}
```

### 反模式（不要这样做）

```typescript
// ❌ form_container — form_submit 事件不通过 WS 到达
{ tag: "form", name: "myForm", elements: [select, { tag: "button", action_type: "form_submit" }] }

// ❌ action_type: "form_submit" — 事件完全不到达服务端
{ tag: "button", action_type: "form_submit", ... }

// ❌ 只靠 name 不设 value — 按钮的 action routing 依赖 value.action
{ tag: "button", name: "my_action" }  // 缺少 value
```

---

## 第二步：EventDispatcher 注册

在 WSClient 启动时，将 `card.action.trigger` 和消息事件一起注册到 EventDispatcher：

```typescript
import * as lark from "@larksuiteoapi/node-sdk";

// select 值缓存（放在模块顶层）
const selectCache = new Map<string, { value: string; expiresAt: number }>();

function cacheSelect(operatorId: string, key: string, value: string): void {
  selectCache.set(`${operatorId}:${key}`, { value, expiresAt: Date.now() + 600_000 });
}

function getCachedSelect(operatorId: string, key: string): string | null {
  const entry = selectCache.get(`${operatorId}:${key}`);
  if (!entry || Date.now() > entry.expiresAt) return null;
  return entry.value;
}

// EventDispatcher 注册
const handlers: Record<string, (data: unknown) => Promise<unknown>> = {
  "im.message.receive_v1": async (data) => {
    // 消息处理逻辑
  },

  "card.action.trigger": async (data) => {
    const d = data as any;
    const action = d?.action ?? {};
    const operator = d?.operator ?? {};
    const tag = action.tag ?? "";
    const operatorId = operator?.open_id ?? "";

    // 1. 下拉选择：缓存值，返回 undefined
    if (tag === "select_static") {
      const selectName = (action.value as any)?.action ?? action.name ?? "";
      const selectedOption = action.option ?? "";
      if (selectName && selectedOption) {
        cacheSelect(operatorId, selectName, selectedOption);
      }
      return undefined;  // 不要返回 {} — 会导致 WS 断连
    }

    // 2. 非按钮交互：静默忽略
    if (tag !== "button") {
      return undefined;
    }

    // 3. 按钮点击：注入缓存值 + 业务处理
    const actionValue = { ...(action.value ?? {}) };
    // 注入所有需要的缓存 select 值
    const cached = getCachedSelect(operatorId, "my_select_key");
    if (cached) actionValue["my_select_key"] = cached;

    // 路由到业务 handler...
    const actionName = (actionValue as any).action ?? action.name ?? "";
    // dispatch(actionName, actionValue, operatorId)

    // 4. 只返回 toast（不返回 card 更新）
    return { toast: { type: "success", content: "操作成功" } };
  },
};

const dispatcher = new lark.EventDispatcher({
  encryptKey: config.encryptKey
}).register(handlers as any);  // as any 因为 SDK 类型不包含 card.action.trigger

const wsClient = new lark.WSClient({
  appId: config.appId,
  appSecret: config.appSecret,
  loggerLevel: lark.LoggerLevel.info
});

// 不要传 cardActionHandler — SDK 会忽略它
wsClient.start({ eventDispatcher: dispatcher });
```

**关键点**：
- `as any` 是必须的，因为 SDK 的 TypeScript 类型定义不包含 `card.action.trigger` 作为合法事件类型
- `select_static` 必须返回 `undefined`（不是 `{}`），否则 SDK 会 base64 编码一个空对象发回去，导致 WS 断连
- button 处理只返回 `{ toast: {...} }`，不返回 `{ card: {...} }`

---

## 第三步：业务 Handler

Handler 只返回 toast，不返回卡片更新：

```typescript
// ✅ 正确：返回 toast
async function handleOpenPeriod(num: number): Promise<CardActionResult> {
  await lifecycle.openNewPeriod(num);
  return { toast: { type: "success", content: `✅ 第 ${num} 期已开启` } };
}

// ❌ 错误：返回卡片更新 — 导致 200672
async function handleOpenPeriod(num: number): Promise<CardActionResult> {
  await lifecycle.openNewPeriod(num);
  return { newCardJson: buildNewCard() };  // 这会导致 200672
}
```

如果需要更新卡片内容，让用户重新发送关键词拉起新卡片，或者用飞书 API 主动发送新卡片消息。

---

## 第四步：权限控制

每个 handler 开头检查操作者权限。卡片发送到群聊后所有人可见，但按钮回调中 `operatorOpenId` 是实际点击者：

```typescript
function requireAdmin(repo: Repo, openId: string): CardActionResult | null {
  const member = repo.findMemberByOpenId(openId);
  if (!member) {
    return { toast: { type: "error", content: "未找到对应成员" } };
  }
  if (member.roleType !== "operator" && member.roleType !== "trainer") {
    return { toast: { type: "error", content: "仅管理员可执行此操作" } };
  }
  return null; // null = 权限通过
}

// 在每个 handler 开头调用
const denied = requireAdmin(deps.repo, ctx.operatorOpenId);
if (denied) return denied;
```

---

## 部署检查清单

每次修改卡片相关代码后，按此顺序验证：

1. **编译检查**：`npm run build` 退出码必须为 0
   - 不要用 `npm run build | tail`（管道吞掉非零退出码）
   - 使用 `set -euo pipefail` 确保错误传播
   - 检查 unused import（TS6133 导致编译失败）

2. **服务重启**：`systemctl restart ai-seed-project`

3. **等待 WS 就绪**：确认日志出现 `ws client ready`
   - 频繁重启后等 2-3 分钟让飞书路由事件到新连接

4. **回归测试**：用户发关键词确认卡片能弹出
   - 这是最重要的验证步骤，每次必做

5. **功能测试**：选择下拉 → 点按钮 → 确认 toast 显示

---

## 常见问题排查

| 现象 | 根因 | 解决 |
|------|------|------|
| 200672 错误 | 返回了 card 更新而非 toast | 改为返回 toast |
| 按钮点击后无反应 | 用了 form_submit | 改为普通 button |
| 下拉值未传递到按钮 | 无 form_container 支持 | 用服务端缓存 |
| "管理"拉不起卡片 | monkey-patch 破坏消息投递 | 移除 monkey-patch |
| WS 连接断开 | 返回 {} 给 card.action.trigger | 改为 return undefined |
| 编译后功能不变 | tsc 失败但管道吞掉退出码 | 用 pipefail 验证 |
| UNIQUE constraint | 重复创建已存在的记录 | 先查后插 |
| 重启后事件不到达 | 飞书路由延迟 | 等 2-3 分钟 |

---

## Toast 状态提示最佳实践

操作成功后的 toast 应包含当前系统状态，让管理员了解上下文：

```typescript
// ✅ 好：包含操作结果 + 当前状态
return {
  toast: { type: "success", content: `✅ 第 ${num} 期已开启 | 当前活跃：第${num}期 | 窗口:W2` },
};

// ✅ 好：已存在的操作返回 info 而非 success
return {
  toast: { type: "info", content: `第 ${num} 期已存在 | 当前活跃：第3期` },
};

// ❌ 差：只有操作结果，没有上下文
return {
  toast: { type: "success", content: "操作成功" },
};
```

操作后获取当前状态的方法：
```typescript
const state = await buildCurrentState(lifecycle, deps);
const periodInfo = state.activePeriod ? `第${state.activePeriod.number}期` : "无";
const windowInfo = state.activeWindow?.code ?? "无";
```

## 幂等性设计

开期/开窗操作必须幂等 — 重复执行同一操作不应产生副作用：

```typescript
// ✅ 先查后插，已存在则 early return（不执行窗口关联等后续逻辑）
const existing = repo.findPeriodByNumber(campId, number);
if (existing) {
  return { periodId: existing.id, assignedWindowId: null, shouldSettleWindowId: null };
}
// 真正的新建逻辑...

// ❌ 先查后插但继续执行后续逻辑 — 会导致窗口重复关联
const existing = repo.findPeriodByNumber(campId, number);
if (!existing) { repo.insertPeriod({...}); }
// 窗口关联逻辑仍然跑... ← BUG
```

## 部署注意事项

### 国内服务器 git pull 超时问题

国内服务器直连 GitHub 不稳定。当 git pull 超时时：
1. **小文件**（<10KB）：用 Base64 直写 `echo '<b64>' | base64 -d > file`
2. **大文件**（>10KB）：tsc build 后直接 patch dist JS（用 node -e 脚本）
3. **验证**：patch 后跑 `node -c dist/xxx.js` 确认语法正确

### dist JS 直接 patch 的模式

```bash
node -e "
const fs = require('fs');
const f = 'dist/my-file.js';
let c = fs.readFileSync(f, 'utf8');
const old = 'exact old code';
const rep = 'exact new code';
if (c.includes(old)) {
  c = c.replace(old, rep);
  fs.writeFileSync(f, c);
  console.log('PATCHED');
} else {
  console.log('MARKER_NOT_FOUND');
}
"
node -c dist/my-file.js  # 验证语法
```

## 新增卡片的完整流程

1. 设计卡片模板（用普通 button，不用 form_container）
2. 给每个 select 和 button 设置唯一的 `name` 和 `value.action`
3. 在 EventDispatcher 的 card.action.trigger handler 中添加 select 缓存 key
4. 编写业务 handler，只返回 toast（含当前状态）
5. 确保操作幂等（先查后插，已存在 early return）
6. 注册 handler 到 CardActionDispatcher
7. 编译、部署、回归测试（发关键词确认卡片弹出 + 测试按钮）
