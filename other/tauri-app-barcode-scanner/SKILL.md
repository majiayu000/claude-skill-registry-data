---
name: tauri-app-barcode-scanner
description: Guidance for Tauri v2 barcode scanner plugin with permissions and scan lifecycle.
license: Apache-2.0
---


## When to use this skill

**ALWAYS use this skill when the user mentions:**
- Barcode or QR code scanning / 条码或二维码扫描
- Camera permissions or scan callbacks / 相机权限或扫描回调
- Platforms with camera capabilities / 具备相机能力的平台

**Trigger phrases include:**
- "barcode", "QR code", "scanner", "camera permissions"
- "扫码", "二维码", "条码", "相机权限"

## How to use this skill

1. Identify supported platforms and camera permissions
2. Configure barcode scanner plugin capabilities
3. Implement scan trigger, result handling, and error flows
4. Validate fallback when camera is unavailable

## Outputs

- Scan flow and permission plan / 扫描流程与权限方案
- Fallback and error-handling checklist / 回退与错误处理清单

## Scope

- Boundary: Barcode scanner plugin usage only
- Key points: Permission handling and result callbacks

## References

- https://v2.tauri.app/llms.txt
- https://v2.tauri.app/plugin/barcode-scanner/
- https://v2.tauri.app/zh-cn/plugin/barcode-scanner/

## Keywords

tauri barcode scanner, qr code, camera, permissions

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
