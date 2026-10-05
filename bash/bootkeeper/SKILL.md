---
name: bootkeeper
description: BootKeeper Windows 启动项管理工具 — 架构约束、已知坑、CI/发布模式
trigger: bootkeeper|启动项|startup item|Windows 启动|注册表 Run|BootKeeper
tags: [windows, rust, tauri, startup, bootkeeper]
category: devops
---

# BootKeeper 开发规范

## 架构约束

- **写链路唯一入口**：`core::windows::launcher::run_helper()`。CLI/GUI/MCP 都走它，不各自实现 ShellExecuteW。
- **确认窗硬核验**：helper 收到请求后自己重枚举+验签+规则引擎，**不信调用方传入的文本**。这是安全边界，绝不能省。
- **快照目录**：`%ProgramData%\BootKeeper\snapshots`，不是 `%APPDATA%`。原因：helper 提权后跑在管理员 profile，`%APPDATA%` 指向不同目录 → GUI 写的快照 helper 看不到。`launcher::data_root()` 统一。

## 注册表 location 格式铁律（踩坑记录）

**location 存真实路径，永远别用显示缩写。**

```rust
// ❌ 会导致所有写操作失败
let key_path = format!("HKCU\\...\\Run");

// ✅ 正确
let key_path = format!("HKCU\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run");
```

原因：写操作 `parse_hive_and_key()` 用 location 决定打开哪个注册表键。`HKCU\...\Run` 被解析成 `HKCU\Run` → 值查找 NotFound → 静默失败。**v0.1.0 的"点禁用无效"就是这个 bug。**

教训：
- 枚举器存真实路径；展示层（GUI tab label）才用缩写
- 任何依赖 location 做实际操作的代码，都要怀疑它是否能正确解析
- 加集成测试在真注册表写/读/禁用来抓这类 bug

## CI 发布流程

release.yml三步：tag `vX.Y.Z` → build + 版本注入 → publish。

版本注入（自动同步 tauri.conf.json + Cargo.toml）：
```yaml
- name: Set version from git tag
  shell: bash
  working-directory: .
  env:
    VER: ${{ github.ref_name }}
  run: |
    VER="${VER#v}"  # v0.1.1 -> 0.1.1
    export VER
    python3 -c "
    import os, re, json
    v = os.environ['VER']
    c = open('Cargo.toml').read()
    c = re.sub(r'(?m)^version\s*=\s*\"[^\"]+\"', f'version = \"{v}\"', c, count=1)
    open('Cargo.toml', 'w').write(c)
    d = json.load(open('gui/src-tauri/tauri.conf.json'))
    d['version'] = v
    open('gui/src-tauri/tauri.conf.json', 'w').write(json.dumps(d, indent=2, ensure_ascii=False) + '\n')
    "
```

产物上传用通配符 `*.exe` `*.msi`（不硬编码版本号）→ publish 用 `find installer -type f` 收集。

### 暗色模式 CSS 变量作用域（v0.2.1 真实 bug）

CSS 自定义属性必须挂在 `:root`（`document.documentElement`），不能挂在子 `<div>` 上。

❌ **错误**：Root.vue 的 wrapper `<div :style="cssVars">` 注入变量 → `html`/`body` 在外层，读不到
✅ **正确**：`watch(cssVars, (v) => { for (const [k,val] of Object.entries(v)) document.documentElement.style.setProperty(k, val) }, { immediate: true })`

- Naive UI 的 `NConfigProvider theme` 只控制组件面，不控制 raw CSS 全局色
- Vue 3 的 `watch` + `immediate: true` 是注入全局 CSS 变量的最简方式

### 禁用条目"消失"的调试方法论

当 CI 集成测试通过（真机注册表 disable→enable 往返 OK）但用户安装后报告条目消失时：

1. **加前端计数器**：标题栏显示 `{{ items.length }}` 实时条目数 → 看前后变化
2. **加 console.log 诊断**：`fetchItems` 打印 total + `.disabled` 后缀条目数
3. **让用户开 DevTools**（Ctrl+Shift+I → Console）看日志和 Tauri IPC 错误
4. **对比前后**：数字不变 → Rust 端正确，前端渲染问题；数字减少 → 枚举器丢失 renamed 条目

适用于任何"CI 绿但真机异常"的 GUI 交互类 bug。

### 启动文件夹：禁用后条目消失的扩展名筛选坑（v0.2.2 真实 bug）

**现象**：对启动文件夹条目点禁用，数字 24→23，条目消失。注册表禁用没问题。

**根因**：枚举器 `enumerate_startup_folders` 按扩展名筛选 `.lnk/.exe/.cmd/.bat`。禁用把 `xxx.lnk` rename 成 `xxx.lnk.disabled`，`Path::extension()` 返回的是 `"disabled"` 而不是 `"lnk"` → 筛选器踢掉 → 条目从列表中消失。

**修复**（一行核心逻辑）：

```rust
// 在扩展名检查前，先剥掉 .disabled 后缀
let base = if name.ends_with(".disabled") {
    &name[..name.len() - 9]
} else {
    &name
};
let ext = PathBuf::from(base).extension().unwrap_or_default();
```

**模式泛化**：任何对文件名加后缀后查 `Path::extension()` 的地方都会命中此坑——`extension()` 返回最后一个 `.` 之后的部分，不是"真正的扩展名"。在 Windows 文件操作中（尤其是 rename/add suffix 后重新枚举），必须先 strip 人工后缀再查扩展名。

**集成测试验证**：
- 在真机 user_startup 创建 `.bat` 测试文件
- disable → 重枚举确认找到 `.bat.disabled` → enable → 重枚举确认恢复 → 清理
- 直接测试"禁用后条目是否还出现在列表里"

### 任务管理器禁用检测：StartupApproved 键（v0.2.4）

BootKeeper 的 `enabled` 判断有**两个来源**，不是只看 `.disabled` 后缀：

1. **BootKeeper 自己的禁用**：rename → `.disabled` 后缀 → `!name.ends_with(".disabled")`
2. **Windows 任务管理器的禁用**：写 `StartupApproved` 注册表键 → 必须额外检测

任务管理器不在文件/注册表值名上加后缀，而是在这里标记：
```
HKCU/HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\StartupApproved\
├── Run\          ← 注册表 Run 条目，value name = 注册表值名
└── StartupFolder\  ← 启动文件夹条目，value name = 文件完整路径
```

每个值是二进制 blob（≥4 bytes），首 4 字节是 little-endian u32 状态码：
- `0x01` → 启用（bit 0 = 1）
- `0x02` / `0x03` → 用户禁用（bit 0 = 0）
- `0x06` / `0x07` → 系统禁用

检测逻辑（`startup_approved.rs::is_entry_approved_disabled`）：
```rust
let state = u32::from_le_bytes([bytes[0], bytes[1], bytes[2], bytes[3]]);
(state & 1) == 0  // bit 0 = 0 → disabled
```

**enrich() 里的最终 enabled 字段**：
```rust
enabled: !raw.name.ends_with(".disabled") && !is_entry_approved_disabled(raw)
```

两个条件都要满足才算"启用"。

**踩坑注意**：
- 注册表 Run 条目的 value name = 注册表值名（如 "WeChat"）
- 启动文件夹条目的 value name = 文件**完整路径**（不是文件名）→ 用 `raw.command` 而不是 `raw.name`
- `is_entry_approved_disabled` 在 `enrich()` 里调用（enrich 不受 cfg(windows) 限制），所以模块声明**不能**包在 `#[cfg(windows)]` 里——函数内部已处理非 Windows 返回 false
- 键不存在（从未被任务管理器动过）→ 返回 false，不是错误

### MSI 版本号约束（v0.2.2-pre 构建失败）

Tauri v2 的 MSI 目标不接受 semver 预发布标签：
- `0.2.2-pre` → ❌ `optional pre-release identifier must be numeric-only` 
- `0.2.2` → ✅ 直接用纯数字 patch bump

## Bundle resources

tauri.conf.json 的 `beforeBuildCommand` 构建 CLI+helper 到根 workspace target：
```json
"beforeBuildCommand": "pnpm build && cargo build --release --manifest-path ../Cargo.toml -p bootkeeper-cli -p bootkeeper-helper && node scripts/prepare-resources.mjs"
```
`prepare-resources.mjs` 从 `../../target/release` 复制 exe 到 `src-tauri/resources`。

CI gui job 跑 `cargo check` 前也必须先构建 CLI+helper + 跑 prepare-resources（否则 check 失败：resource doesn't exist）。

## MCP server (rmcp 3.1) 注意

- `serve(stdio()).await?` 返回 `RunningService`，必须 `running.waiting().await?` 才保活——否则 init 握手后就退出
- `#[tool(aggr)]` 语法无效，直接用 `Parameters<SchemaType>` 作为参数
- schemars 版本：rmcp 依赖 1.0，项目必须用相同的版本（不是 0.8）
- stdio 传输：裸 JSON 行（`json + '\n'`），不是 Content-Length 帧
