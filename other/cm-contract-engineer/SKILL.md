---
name: cm-contract-engineer
description: 智能合约工程师 Skill，执行合约开发、测试、部署，自动适配 EVM/Solana/Move 等链和开发框架
---

# cm-contract-engineer — 智能合约工程师

执行智能合约开发任务。自动识别链类型和开发框架。

## 触发条件

由 `/cm-ai` 自动调用，当 task 涉及智能合约开发时触发。

## 工作流程

### 1. 识别技术栈

自动检测，不做硬编码假设：

- **链/VM**：EVM（Ethereum/Base/Arbitrum/BSC...）/ Solana / Aptos / Sui / TON / Cosmos
- **语言**：Solidity / Rust / Move / Vyper / FunC / Cairo
- **框架**：Foundry / Hardhat / Anchor / Truffle / Brownie / Ape
- **检测方式**：`foundry.toml` / `hardhat.config.*` / `Anchor.toml` / `truffle-config.js` / `Move.toml` / `contracts/` 目录

### 2. 读取上下文

- `.claude/rules/smart-contract.md`、`.claude/rules/security.md`（如存在）
- design.md 中的合约接口设计
- 现有合约代码和部署配置
- 已有的测试文件和部署脚本

### 3. 开发

**合约编写：**

- 遵循项目已有的合约组织方式（单文件/模块化/Diamond 模式等）
- 接口（interface）先行，实现后补
- 使用成熟的库（OpenZeppelin / Solmate / SPL 等）而非手写基础功能
- NatSpec / Rust doc 注释覆盖所有 public 函数

**安全优先（EVM/Solidity 重点）：**

- 重入防护：使用 ReentrancyGuard 或 checks-effects-interactions 模式
- 整数溢出：Solidity ≥0.8 内置检查，低版本用 SafeMath
- 权限控制：Ownable / AccessControl / 多签，避免单点控制
- 外部调用：不信任外部合约返回值，限制 gas 转发
- 闪电贷攻击：价格预言机用 TWAP 而非即时价格
- 前端运行（MEV）：commit-reveal 或时间锁机制

**安全优先（Solana/Anchor 重点）：**

- 账户验证：每个 instruction 都要验证 account owner 和 signer
- PDA 派生：种子要唯一，避免碰撞
- CPI 调用：验证目标 program_id
- 整数溢出：用 checked_add / checked_mul

**Gas/资源优化：**

- 存储变量打包（EVM slot packing）
- 减少 SSTORE/SLOAD 操作
- 批量操作代替循环中的单次调用
- Solana: 减少账户数量，合理使用 zero-copy

### 4. 测试

```bash
# Foundry
forge test -vvv
forge coverage

# Hardhat
npx hardhat test
npx hardhat coverage

# Anchor
anchor test

# Move
aptos move test
```

**测试要求：**

- 正常流程覆盖所有 public 函数
- 边界值测试（零值、最大值、空地址）
- 权限测试（非授权调用应 revert）
- 攻击测试（重入、闪电贷等关键场景）
- Fuzz 测试（Foundry `forge test --fuzz-runs 1000`）

### 5. 部署准备

- 部署脚本使用项目约定的方式（Foundry script / Hardhat deploy / Anchor deploy）
- 环境变量管理私钥和 RPC URL，绝不硬编码
- 区分 testnet / mainnet 配置
- 合约验证脚本（Etherscan / Sourcify）

**部署前检查清单：**

- [ ] 所有测试通过
- [ ] 覆盖率 > 90%
- [ ] 权限模型正确（owner/admin/multisig）
- [ ] 升级机制明确（如使用代理模式）
- [ ] 紧急暂停功能（如需要）
- [ ] 事件覆盖所有状态变更

## 常见坑

| 问题 | 处理 |
| ---- | ---- |
| Solidity 版本不一致导致编译失败 | 检查 foundry.toml / hardhat.config 中的 solc 版本，与 pragma 一致 |
| OpenZeppelin 版本升级 API 变化 | 锁定依赖版本，升级前检查 changelog |
| Anchor IDL 生成失败 | 确保 `#[program]` 和 account struct 上的宏正确 |
| 合约大小超过 24KB（EVM） | 拆分合约、使用 library、Diamond 模式 |
| Gas estimation 失败 | 检查是否有 require 条件未满足，mock 依赖合约 |
| Solana 交易大小超限 | 拆分 instruction，使用 lookup table |

## 审计准备

合约开发完成后，生成审计辅助文档：

```markdown
## 合约审计信息

- 合约列表: {合约名及用途}
- 依赖: {使用的库及版本}
- 权限模型: {谁能做什么}
- 资金流向: {token/ETH 的流入流出路径}
- 已知风险: {设计上的取舍及原因}
```

## 输出

- 合约代码和接口
- 测试结果和覆盖率
- 部署脚本
- 需要其他工种配合的事项（如前端需要的 ABI 和合约地址）
