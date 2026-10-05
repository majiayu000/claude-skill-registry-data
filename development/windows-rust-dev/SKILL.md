---
name: windows-rust-dev
description: Windows 系统编程 in Rust — windows crate COM/注册表/任务计划/签名校验。
---

# Windows Rust 系统编程

Windows 平台 Rust 开发（非 Tauri UI 部分）：`windows` crate、`winreg`、COM 接口、WinVerifyTrust。

## 平台隔离（首要规则）

- Windows-only 依赖必须放 `[target.'cfg(windows)'.dependencies]`，否则 Linux/macOS 编译直接报 `compile_error!`。
- Windows 代码用 `#[cfg(windows)]` 门控；非 Windows 下给同一函数提供返回空 Vec/Unknown 的 stub，保证 crate 在 Linux 上可编译、纯逻辑单元测试可跑。
- **WSL 交叉编译验证 API 用法**（不用真 Windows）：
  ```bash
  rustup target add x86_64-pc-windows-msvc
  cargo build --target x86_64-pc-windows-msvc
  ```
  编译通过 = API 签名/feature 对；运行时行为（COM 连接、路径解析）仍需真机验证。

## 验证阶梯：交叉编译 ≠ 能跑（真机 CI 是最后一道）

- 交叉编译只验证**编译期**（签名、feature、类型）。**运行期崩溃它抓不到**。
- 实测案例：WINTRUST_DATA union 初始化写成 `*data.Anonymous.pFile = file_info`（对 zeroed 指针解引用）——交叉编译、Linux 单测全绿，GitHub Actions 真 Windows runner 一跑就 `STATUS_STACK_BUFFER_OVERRUN (0xc0000409)`。
- **Windows 代码必须配真机 CI**，用 GitHub Actions `windows-latest` runner（就是真 Windows：真实注册表、Task Scheduler 服务、WinVerifyTrust）：
  ```yaml
  test-windows:
    runs-on: windows-latest
    steps:
      - uses: actions/checkout@v4
      - uses: dtolnay/rust-toolchain@stable
      - run: cargo test --workspace
      - run: cargo clippy --workspace --all-targets -- -D warnings
  ```
  配套写 `tests/windows_integration.rs`（`#![cfg(windows)]`）：真机枚举注册表/任务计划/启动文件夹，断言不 panic、结构合理（enrich 过真实 WinVerifyTrust）。CI 会替你抓住交叉编译看不见的运行时 bug——不要只在本地交叉编译就认为"Windows 侧没问题"。

## windows crate 0.62 关键坑

- **feature 门控严格**：未启用的模块在源码里存在但构建时不可见。常用：
  - `Win32_System_TaskScheduler` + `Win32_System_Com` + `Win32_System_Variant` + `Win32_System_Ole`（任务计划）
  - `Win32_Security_WinTrust` + **`Win32_Security_Cryptography`**（`WINTRUST_DATA` 结构体被后者 gate！）
  - `Win32_UI_Shell`（SHGetFolderPathW）、`Win32_Foundation`（HWND/INVALID_HANDLE_VALUE）
- **COM 接口是高级封装，不是 raw 绑定**：方法签名与经典 C 版不同，写前必读 registry 缓存里目标模块的 mod.rs 源码（`~/.cargo/registry/src/.../windows-0.62.x/src/Windows/Win32/.../mod.rs`），确认实际签名，别凭文档猜。
- `let...else` 配 unsafe block 必须加括号：`let Ok(x) = (unsafe { f() }) else { ... };`
- 超范围字面量：`0x800B0100`（TRUST_E_NOSIGNATURE）要写成 `0x800B0100u32 as i32`。

## 各 API 实测形态（0.62.2）

见 `references/windows-crate-0.62.md`——含 TaskScheduler COM、WinVerifyTrust、SHGetFolderPathW、winreg 的逐条签名和用法。

## 参考

- `taskschd` crate 已死（2023 停更）——任务计划用 windows crate 官方 COM 绑定。
- 参考项目：BootKeeper `crates/core/src/windows/`（registry/startup_folder/scheduled_task/signature）。
