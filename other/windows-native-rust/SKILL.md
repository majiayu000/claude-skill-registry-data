---
name: windows-native-rust
description: Windows 原生 Rust — windows crate/winreg/COM/签名/提权/交叉编译/真机 CI。
---

# Windows 原生 Rust 开发

## 核心依赖选型（调研结论，2026-08）

| 能力 | 用 | 不用 |
|---|---|---|
| 注册表 | `winreg` 0.56+ (196M 下载) | 手写 RegGetValue |
| 任务计划 | `windows` crate `Win32_System_TaskScheduler` COM | `taskschd` crate（**已死**，2023 停更） |
| 签名校验 | `windows` crate `Win32_Security_WinTrust` (WinVerifyTrust) | schtasks CLI 解析（输出本地化脆弱） |
| 启动文件夹 | `SHGetFolderPathW` (Win32_UI_Shell) | 硬编码路径 |

## 平台隔离铁律

- Windows-only 依赖放 `[target.'cfg(windows)'.dependencies]`，否则 Linux 编译直接挂（winreg 有 `compile_error!` 守卫）。
- 平台无关的**协议类型**（JSON 序列化的 struct/enum）放 core 顶层，执行函数才放 `#[cfg(windows)]` 模块。CLI/helper 在 Linux 也要能编译。
- 交叉编译：`rustup target add x86_64-pc-windows-msvc`。`cargo check --target` 能验证 API 用法（lib 不需要 link.exe）；**bin 需要 link.exe，WSL 里没有 → 靠 CI 的 windows-latest 验证链接**。clippy 交叉跑不需要 linker。
- 验证优先级：交叉编译只能证"编译对"，**真机行为必须靠 GitHub Actions windows-latest**（注册表/任务计划/签名全是真环境）。

## windows crate 0.62 陷阱（详见 references/windows-crate-062-api-notes.md）

1. **feature 门控**：模块未开 feature 时编译报"cannot find X"，需要逐个确认。TaskScheduler 全家需要 `Win32_System_Com` + `Win32_System_Variant` + `Win32_System_Ole`；`WINTRUST_DATA` 需要 `Win32_Security_Cryptography`（不是 WinTrust！）；ShellExecute 需要 `Win32_UI_Shell` + `Win32_UI_WindowsAndMessaging`；`CloseHandle` 在 Foundation。
2. **COM 接口是高级封装不是 raw 绑定**：参数形态与文档/C 示例不同——`Connect` 要 `&VARIANT`×4、`GetFolder` 要 `&BSTR`、集合用 `Count()` + `get_Item(&VARIANT)` 不是迭代器、`IActionCollection::Count` 是 `(&mut i32)` 指针形式、`IExecAction::Path(&mut BSTR)` 是 out-param。
3. **CLSID 名**：Task Scheduler 类叫 `CLSID_CTaskScheduler`，不是 `TaskSchedulerClass`。
4. **WinVerifyTrust**：`pwvtdata` 是 `*mut c_void`（`.cast()`）、action 是 `*mut GUID`、HWND 从 `INVALID_HANDLE_VALUE.0 as *mut _` 转。
5. **WINTRUST_DATA union 初始化 = 空指针雷区**（CI 真机抓到的 bug）：
   ```rust
   // 错 — 解引用 null union 指针再赋值 → STATUS_STACK_BUFFER_OVERRUN
   unsafe { *data.Anonymous.pFile = file_info; }
   // 对 — 把地址赋给 union 成员；file_info 必须 mut
   data.Anonymous.pFile = &mut file_info;
   ```
6. `let Ok(x) = (unsafe { ... }) else { ... }` — let-else 配 unsafe block 必须加括号。
7. `ShellExecuteW` 是 6 参数函数形式（返回 HINSTANCE，`hinst.0 as isize <= 32` = 错误），不是 SHELLEXECUTEINFOW 结构体版本。

## 真 Windows CI 模式

```
test-linux:   ubuntu → cargo test（纯逻辑，快速反馈）
test-windows: windows-latest → cargo test + cargo clippy -D warnings
```
- windows_integration.rs 顶部 `#![cfg(windows)]`，跑真实枚举/签名，断言"不 panic + 结构合理"而非具体数量（CI 空机可能 0 项）。
- clippy `-D warnings` 只在 Windows job 跑——Linux 上 cfg(not(windows)) 分支的 dead-code 警告无害，别为它加 allow。

## AI 可调用设计模式（CLI-first）

让"任何 AI agent 能调用"的通用底座是**稳定的 CLI**，不是 skill 也不是 MCP：
- skill（skills.sh / SKILL.md 标准）是说明书层，覆盖 19+ agent（含 nous-research/Hermes）
- MCP 是后置协议适配层，包 CLI 不动 core
- 先 CLI + SKILL.md，MCP 以后再说——最懒且正确

## SCManager 服务枚举

枚举所有自动启动（StartType=Automatic）的 Windows 服务：

```rust
// 需要 feature: "Win32_System_Services"
use windows::Win32::System::Services::{
    OpenSCManagerW, EnumServicesStatusW, OpenServiceW, QueryServiceConfigW,
    CloseServiceHandle, SC_MANAGER_ENUMERATE_SERVICE, SERVICE_AUTO_START,
    SERVICE_STATE_ALL, SERVICE_WIN32,
};

// 1. OpenSCManagerW(None, None, SC_MANAGER_ENUMERATE_SERVICE) — 值传递 SC_HANDLE，不加 &
// 2. 第一次 EnumServicesStatusW(None, 0, &mut bytes_needed, &mut count, None) 取 buf size
// 3. 第二次带 buf 取 ENUM_SERVICE_STATUSW 数组
// 4. 每个条目 OpenServiceW + QueryServiceConfigW 两次调用取配置块，检查 dwStartType == SERVICE_AUTO_START
// 5. EnumServicesStatusW 8 参数（比 MSDN 多 dwServiceType）；SC_HANDLE 传值不传引用
// 6. SERVICE_WIN32 = ENUM_SERVICE_TYPE(48)；SERVICE_STATE_ALL = ENUM_SERVICE_STATE(3)
```
详见 `references/scmanager-services-enum.rs`。

## 提权确认窗（helper 模式）

需要"提权执行 + 用户确认"时，用独立 helper 进程（ShellExecuteW runas 拉起）+ 原生 MessageBox：
- helper 是**唯一**能执行写操作的进程，且必须先弹窗——调用方无法绕过（硬确认）
- 弹窗内容由 helper 自己重新查证（枚举+验签+规则引擎），**不信调用方文本**（防注入）
- 写操作后自动落快照（7 天保留）供恢复
