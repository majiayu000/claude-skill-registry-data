---
name: rust-review
description: 审查和解释 Rust 代码，并结合 cargo 实际验证。当用户让你解释一段 Rust 代码、指出潜在 bug、检查所有权/生命周期问题、或要求 review Rust 项目时使用。
---

# Rust 代码审查

结合 TERMINAL 工具用真实编译器反馈支撑结论，不要只凭静态阅读下判断。

## 流程

1. **通读代码**：确定 crate 结构（ edition、依赖）、涉及的类型与 trait 边界。
2. **静态检查**：优先关注——
   - 所有权与借用：不必要的 `clone()`、`RefCell` 滥用、可见的借用冲突
   - 生命周期：返回引用的函数是否有悬垂风险
   - 错误处理：被 `unwrap()`/`expect()` 吞掉的错误、应传播而未传播的 `Result`
   - 并发：`Arc<Mutex<>>` 持锁跨 `.await`、潜在死锁顺序
   - API 误用：过期方法、非幂等操作被重试
3. **编译验证**：对独立片段，写入临时文件用 `cargo` 或 `rustc --edition 2021` 实际编译；对整个项目，运行 `cargo check` 与 `cargo clippy`，把 warning 作为证据引用。
4. **输出结论**：按"问题 → 证据（编译器/clippy 输出或代码行） → 修复建议（给出代码）"组织，按严重程度排序。验证过和未验证的结论要分开陈述。
