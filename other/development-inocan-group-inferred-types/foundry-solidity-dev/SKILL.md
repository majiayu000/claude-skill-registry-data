---
name: foundry-solidity-dev
description: 提供Foundry智能合约开发的专业指导,包括合约编写、测试、部署和安全最佳实践。当需要开发、测试或部署Solidity智能合约时使用此技能。
license: UNLICENSED
---

# Foundry Solidity开发技能

## 概述

此技能为AI代理提供使用Foundry工具链进行Solidity智能合约开发的完整指导。

**关键词**: Solidity, Foundry, 智能合约, 区块链, 以太坊, forge, cast, anvil, 测试, 部署

## 核心能力

### 1. 合约开发

#### 合约结构规范

- 使用SPDX许可证标识符
- 明确Solidity版本声明
- 遵循标准命名约定 (合约用帕斯卡命名,函数用驼峰命名)
- 状态变量应有明确的可见性修饰符
- 添加NatSpec注释说明函数用途

#### 示例合约模板

```solidity
// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.13;

contract MyContract {
    // 状态变量
    uint256 public value;
    
    // 事件
    event ValueChanged(uint256 newValue);
    
    // 构造函数
    constructor(uint256 _initialValue) {
        value = _initialValue;
    }
    
    // 公共函数
    function setValue(uint256 _newValue) public {
        value = _newValue;
        emit ValueChanged(_newValue);
    }
}
```

### 2. 测试开发

#### 测试合约规范

- 测试合约继承`forge-std/Test.sol`
- 测试合约命名: `<ContractName>Test`
- 必须包含`setUp()`函数
- 测试函数前缀: `test_` (标准) 或 `testFuzz_` (模糊测试)
- 使用forge-std断言函数

#### 测试模板

```solidity
// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.13;

import {Test} from "forge-std/Test.sol";
import {MyContract} from "../src/MyContract.sol";

contract MyContractTest is Test {
    MyContract public myContract;
    
    function setUp() public {
        myContract = new MyContract(0);
    }
    
    function test_SetValue() public {
        myContract.setValue(42);
        assertEq(myContract.value(), 42);
    }
    
    function testFuzz_SetValue(uint256 x) public {
        myContract.setValue(x);
        assertEq(myContract.value(), x);
    }
}
```

### 3. 常用命令

#### 构建和编译

```shell
# 编译合约
forge build

# 清理并重新编译
forge clean && forge build
```

#### 测试命令

```shell
# 运行所有测试
forge test

# 详细输出
forge test -vvv

# 运行特定测试
forge test --match-test test_SetValue

# 运行特定合约的测试
forge test --match-contract MyContractTest

# Gas报告
forge test --gas-report

# 测试覆盖率
forge coverage
```

#### 代码格式化

```shell
# 格式化所有Solidity文件
forge fmt

# 检查格式但不修改
forge fmt --check
```

#### 部署和交互

```shell
# 本地部署
forge script script/Deploy.s.sol:DeployScript --rpc-url http://localhost:8545 --broadcast

# 主网/测试网部署
forge script script/Deploy.s.sol:DeployScript --rpc-url <rpc_url> --private-key <key> --broadcast --verify

# 使用Cast调用合约
cast call <address> "functionName()(returnType)" --rpc-url <rpc_url>

# 发送交易
cast send <address> "functionName(paramType)" <value> --rpc-url <rpc_url> --private-key <key>
```

### 4. 安全最佳实践

#### 必须遵循的安全规则

1. **访问控制**: 使用适当的访问修饰符 (public, private, internal, external)
2. **重入保护**: 对于涉及外部调用的函数,考虑使用重入锁
3. **整数安全**: Solidity 0.8+有内置溢出保护,但仍需注意边界情况
4. **输入验证**: 始终验证函数参数
5. **事件记录**: 重要状态变更应发出事件
6. **Gas优化**: 注意循环和存储操作的Gas消耗

#### 安全检查清单

- [ ] 所有公共/外部函数都有适当的访问控制
- [ ] 外部调用后的状态变更已考虑重入风险
- [ ] 所有数学运算都经过边界测试
- [ ] 敏感操作都发出了事件
- [ ] 测试覆盖率达到90%以上
- [ ] 使用`forge coverage`验证覆盖率
- [ ] 运行`slither`等静态分析工具 (如果可用)

### 5. 调试技巧

#### 使用Console.log

```solidity
import {console} from "forge-std/console.sol";

function debugFunction() public {
    console.log("Value is:", value);
    console.log("Sender:", msg.sender);
}
```

#### 详细调试输出

```shell
# 显示调用栈
forge test -vvvv

# 交互式调试器
forge debug --match-test test_MyFunction
```

### 6. 项目结构

标准Foundry项目结构:

```
project/
├── src/              # 合约源代码
│   └── Contract.sol
├── test/             # 测试文件
│   └── Contract.t.sol
├── script/           # 部署脚本
│   └── Deploy.s.sol
├── lib/              # 依赖库
├── out/              # 编译输出
├── foundry.toml      # 配置文件
└── README.md
```

### 7. 配置文件

#### foundry.toml基础配置

```toml
[profile.default]
src = "src"
out = "out"
libs = ["lib"]
solc_version = "0.8.13"

# 优化设置
optimizer = true
optimizer_runs = 200

# 测试设置
fuzz_runs = 256
```

## 工作流程

### 开发新合约的标准流程

1. 在`src/`目录创建合约文件
2. 编写合约代码,遵循安全规范
3. 在`test/`目录创建对应测试文件
4. 编写全面的测试用例 (包括边界情况和模糊测试)
5. 运行`forge test`确保所有测试通过
6. 运行`forge coverage`检查覆盖率
7. 运行`forge fmt`格式化代码
8. 创建部署脚本 (如需要)
9. 在本地网络测试部署流程
10. 部署到测试网验证
11. 进行安全审计 (生产环境)
12. 部署到主网

## 常见问题解决

### 编译错误

- 检查Solidity版本是否匹配
- 确认所有依赖已正确安装 (`forge install`)
- 运行`forge clean`清理缓存

### 测试失败

- 使用`-vvv`或`-vvvv`查看详细输出
- 检查`setUp()`函数是否正确初始化
- 验证断言条件是否正确

### Gas优化

- 使用`forge snapshot`创建Gas基准
- 比较不同实现的Gas消耗
- 考虑使用`unchecked`块 (谨慎使用)
- 优化存储布局

## 参考资源

- Foundry Book: https://book.getfoundry.sh/
- Solidity文档: https://docs.soliditylang.org/
- Ethereum开发最佳实践: https://consensys.github.io/smart-contract-best-practices/

