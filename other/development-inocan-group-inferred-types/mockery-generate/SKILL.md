---
name: mockery-generate
description: 统一使用 mockery + go:generate 为 Golang 接口生成 Mock，禁止手写 mock 结构体；在实现或编写单测时需要为接口创建 mock 时启用本 Skill。
---

# Golang Mockery 生成 Skill（mockery-generate）

## 何时使用

- 为新的或已有的接口（例如 `IPackAuthAccountRepo`）编写或更新单元测试，需要 Mock 其依赖。
- 重构服务实现导致依赖接口发生变化，需要同步更新 Mock。
- 希望在仓库内收敛 Mock 生成方式，避免手写 mock struct。

## 行为概要

1. 扫描目标接口定义（根据 speckit.implement 或调用方传入的接口名和包路径）。
2. 在接口定义上方补充或校验 `//go:generate mockery --name=<Interface> --with-expecter=true` 注释：
   ```go
   //go:generate mockery --name=IPackAuthAccountRepo --with-expecter=true
   type IPackAuthAccountRepo interface {
       // ...
   }
   ```
3. 在任务总结中提示开发者在本地终端执行：
   ```bash
   go generate ./...
   ```
   以生成或更新 Mock 文件。
4. 在测试代码中，统一使用 mockery 生成的 Mock 类型：
   - 从 `mocks` 包导入 Mock 类型（例如 `domain/dmservice/mocks`）。
   - 使用 `New<Interface>(t)` 创建 Mock 实例，并通过 `EXPECT()`/`AssertExpectations` 配置与校验调用。
   - 不再手写任何实现接口的临时 struct。

## 关键约束

- **禁止手写 Mock**：生产代码与测试代码中都不允许手写 Mock 结构体或临时 Stub，实现接口的替身必须来自 mockery 生成的代码。
- **统一命令格式**：`go:generate` 注释必须使用 `mockery --name=<Interface> --with-expecter=true` 这一形式，必要时由 Skill 自动补齐。
- **目录约定**：Mock 文件推荐放在接口所在包的 `mocks/` 子目录中，以避免循环依赖和命名混乱。
- **CI 友好**：生成或更新 Mock 后应保证静态检查（SatCheck 等）不新增 Error 级别问题。
- **更多细节**：完整流程、参数与示例见同目录下的 `reference.md`。
