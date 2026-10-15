---
name: tauri-app-process
description: Guidance for Tauri v2 process plugin with controlled process information exposure.
license: Apache-2.0
---


## When to use this skill

**ALWAYS use this skill when the user mentions:**
- Process info or lifecycle management / 进程信息或生命周期管理
- Process capabilities and risks / 进程能力与风险
- Controlled exposure of process data / 受控暴露进程数据

**Trigger phrases include:**
- "process", "lifecycle", "capabilities", "security"
- "进程", "生命周期", "能力", "安全"

## How to use this skill

1. Define required process data and constraints
2. Configure process plugin capabilities and scope
3. Expose a limited API for process interactions
4. Validate security boundaries and platform support

## Outputs

- Process access plan / 进程访问方案
- Capability gating checklist / 能力门控清单

## Scope

- Boundary: Process plugin usage only
- Key points: Controlled exposure and capability gating

## References

- https://v2.tauri.app/llms.txt
- https://v2.tauri.app/plugin/process/
- https://v2.tauri.app/zh-cn/plugin/process/

## Keywords

tauri process, system process, capabilities, security

## 常见陷阱 (Gotchas)

1. **版本兼容性**：注意框架版本与依赖库的兼容性，不同版本 API 可能有差异
2. **配置文件格式**：配置文件格式错误是最常见的问题，建议使用编辑器的语法检查
3. **环境变量**：确保所有必要的环境变量已正确设置，敏感信息不要硬编码
4. **依赖冲突**：多版本共存时注意依赖冲突，使用 lock 文件锁定版本
5. **性能陷阱**：大数据量场景下注意性能优化，避免 N+1 查询等常见问题

## 使用流程

### Step 1: 环境准备
确保开发环境已安装必要的依赖和工具。

### Step 2: 配置初始化
根据项目需求进行基础配置。

### Step 3: 核心功能使用
按照示例代码实现核心功能。

### Step 4: 测试验证
运行测试确保功能正常。

### Step 5: 部署上线
完成开发后进行部署和监控。
