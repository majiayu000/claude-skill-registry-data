---
name: feishu-drive-backup
description: |
  飞书云盘备份工具 - 支持文件上传、压缩、分割、列表查询
  
  功能:
  - 上传本地文件到飞书云空间
  - 自动处理大文件(>20MB): 压缩、分割
  - 支持指定文件夹位置
  - 列出云空间文件
  
  依赖:
  - FEISHU_APP_ID: 飞书应用ID
  - FEISHU_APP_SECRET: 飞书应用密钥
  - 权限: drive:drive, drive:file, drive:file:upload
metadata:
  {
    "openclaw":
      {
        "emoji": "☁️",
        "requires": { 
          "env": ["FEISHU_APP_ID", "FEISHU_APP_SECRET"], 
          "bins": ["python3"] 
        },
        "install":
          [
            {
              "id": "env",
              "kind": "env",
              "vars": [
                { "name": "FEISHU_APP_ID", "label": "飞书应用ID" },
                { "name": "FEISHU_APP_SECRET", "label": "飞书应用密钥", "sensitive": true }
              ]
            }
          ],
      },
  }
---

# SKL-SKILL-v1.0-FIN-260325-Feishu-Drive-Backup.md

> **维度**: 云存储备份  
> **功能**: 飞书云盘文件上传、压缩、分割、列表  
> **状态**: FIN (7标准完整)  
> **版本**: V1.0  
> **创建时间**: 2026-03-25

---

## S1: 全局考虑（人/事/物/环境/外部/边界）

### 1.1 人的维度

| 利益相关方 | 需求 | 影响 |
|------------|------|------|
| **用户(Egbertie)** | 可靠备份工作文件，大文件支持 | 核心使用者 |
| **主控AI(满意妞)** | 简单API调用，明确错误反馈 | 调用方 |
| **飞书平台** | 遵守API限制，合理频率 | 依赖服务 |

### 1.2 事的维度

**输入**: 本地文件路径、目标文件夹Token（可选）
**处理**: 文件验证 → 大小判断 → 压缩/分割 → API上传
**输出**: 上传结果、文件Token、访问信息

**完整流程**:
```
用户请求上传
    ↓
验证文件存在性
    ↓
判断文件大小
    ├── ≤20MB → 直接上传
    ├── 20-40MB → ZIP压缩 → 上传
    └── >40MB → ZIP压缩 + 分片 → 多部分上传
    ↓
调用飞书Drive API
    ↓
返回结果（成功/失败详情）
```

### 1.3 物的维度

| 资源 | 类型 | 约束 |
|------|------|------|
| 本地文件 | 输入 | 必须存在且可读 |
| 飞书API | 外部服务 | QPS限制: 5/秒 |
| 云盘空间 | 外部存储 | 依赖企业配额 |
| Token | 认证信息 | 环境变量提供 |

### 1.4 环境维度

**网络环境**:
- 需要访问飞书API (`open.feishu.cn`)
- 国内网络优化

**运行时环境**:
- Python 3.8+
- 依赖: `requests`

**API限制**:
- 简单上传: ≤20MB
- 分片上传: ≤40MB/片
- 日调用上限: 10,000次

### 1.5 外部集成

| 集成方 | 方式 | 说明 |
|--------|------|------|
| 飞书Drive API | REST API | 核心依赖 |
| OpenClaw工具 | 命令行封装 | 间接调用 |
| 企微 | 可配合使用 | 飞书作Backup-1，企微作Backup-2 |

### 1.6 边界情况

| 场景 | 处理方式 |
|------|----------|
| 文件不存在 | 返回明确错误，提示检查路径 |
| 文件被占用 | 尝试读取，失败则报错 |
| 网络中断 | 重试3次，失败返回部分结果 |
| API限流 | 指数退避重试，最多5次 |
| 权限不足 | 返回错误码+申请链接 |
| 空间不足 | 返回错误，建议清理 |
| 文件名重复 | 自动重命名 (添加时间戳) |
| 超大文件(>100MB) | 建议用户手动上传 |

---

## S2: 系统闭环（输入→处理→输出→反馈）

### 2.1 输入规范

**必需参数**:
```python
{
  "file_path": "/path/to/file",  # 本地文件绝对路径
  "parent_node": "fldxxxxx"      # 可选，目标文件夹Token
}
```

**前置条件检查**:
- 文件存在性 ✓
- 文件可读性 ✓
- 文件大小 ≤100MB（软限制）

### 2.2 处理流程

```python
class FeishuUploader:
    def upload(self, file_path, parent_node=None):
        # 1. 验证输入
        if not os.path.exists(file_path):
            return {"success": False, "error": "文件不存在"}
        
        # 2. 获取文件信息
        file_size = os.path.getsize(file_path)
        
        # 3. 选择上传策略
        if file_size <= 20 * 1024 * 1024:  # 20MB
            return self._upload_direct(file_path, parent_node)
        elif file_size <= 40 * 1024 * 1024:  # 40MB
            return self._upload_compressed(file_path, parent_node)
        else:
            return self._upload_split(file_path, parent_node)
```

### 2.3 输出规范

**成功响应**:
```json
{
  "success": true,
  "total_parts": 1,
  "files": [
    {
      "file_token": "boxcnrHpsg1QDqXAAAyachabcef",
      "file_name": "report.pdf",
      "size": 1024000,
      "method": "direct"
    }
  ],
  "original": {
    "path": "/path/to/report.pdf",
    "name": "report.pdf",
    "size": 1024000
  }
}
```

**错误响应**:
```json
{
  "success": false,
  "error": "权限不足",
  "error_code": "99991672",
  "help": "https://open.feishu.cn/app/cli_a949c1e2f4f89cb3/auth"
}
```

### 2.4 反馈机制

**日志记录**:
- 每次上传记录到本地日志
- 格式: `[timestamp] [file] [size] [status] [token]`

**错误反馈**:
- 明确的错误信息
- 错误码对应表
- 解决建议链接

**状态查询**:
```bash
# 查询已上传文件列表
python3 feishu_drive_uploader.py list
```

---

## S3: 可观测输出（量化指标+报告）

### 3.1 量化指标

| 指标 | 目标 | 测量方式 |
|------|------|----------|
| 上传成功率 | >99% | 成功次数/总次数 |
| 压缩率 | >80% (文本文件) | (原大小-压缩后)/原大小 |
| 平均上传时间 | <30s (<10MB) | 从调用到返回 |
| API错误率 | <1% | 失败次数/总次数 |
| Token刷新成功率 | 100% | 自动获取Tenant Token |

### 3.2 使用报告

**单次上传报告**:
```
☁️ 飞书云盘上传完成
━━━━━━━━━━━━━━━━━━━━
文件名: report.pdf
原始大小: 25.0 MB
处理方式: ZIP压缩 (99.9%)
上传大小: 25.6 KB
文件Token: boxcnrHpsg1QDqXAAAyachabcef
耗时: 3.2秒
状态: ✅ 成功
━━━━━━━━━━━━━━━━━━━━
```

**批量上传报告**:
```
☁️ 批量上传完成
━━━━━━━━━━━━━━━━━━━━
总文件数: 5
成功: 5
失败: 0
总原始大小: 127.5 MB
总上传大小: 128.2 KB
压缩率: 99.9%
━━━━━━━━━━━━━━━━━━━━
```

---

## S4: 自动化集成（Cron+脚本+触发器）

### 4.1 定时备份任务

```yaml
# 每日自动备份
cron:
  name: daily-feishu-backup
  schedule: "0 3 * * *"
  command: |
    python3 /root/.openclaw/workspace/plugins/feishu_drive_uploader.py \
      upload /backup/daily_$(date +%Y%m%d).zip
```

### 4.2 事件触发备份

```python
# 重要文件变更时自动备份
def on_file_change(file_path):
    if is_important_file(file_path):
        uploader = FeishuUploader()
        result = uploader.upload(file_path, folder_token="fld_backup")
        log_backup_event(result)
```

### 4.3 一键备份脚本

```bash
#!/bin/bash
# feishu-backup.sh - 一键备份关键文件

FILES=(
  "/root/.openclaw/workspace/MEMORY.md"
  "/root/.openclaw/workspace/USER.md"
  "/root/.openclaw/workspace/SOUL.md"
)

for file in "${FILES[@]}"; do
  python3 /root/.openclaw/workspace/plugins/feishu_drive_uploader.py upload "$file"
done
```

---

## S5: 自我验证（质量检查+测试）

### 5.1 功能测试

```bash
#!/bin/bash
# 测试套件

echo "测试1: 小文件上传"
python3 feishu_drive_uploader.py upload /tmp/test_small.txt
assert_success

echo "测试2: 中等文件压缩上传"
dd if=/dev/zero of=/tmp/test_25m.bin bs=1M count=25
python3 feishu_drive_uploader.py upload /tmp/test_25m.bin
assert_compressed

echo "测试3: 文件列表"
python3 feishu_drive_uploader.py list
assert_has_files

echo "测试4: 错误处理 - 不存在的文件"
python3 feishu_drive_uploader.py upload /tmp/not_exist.txt
assert_error "文件不存在"

echo "所有测试通过 ✅"
```

### 5.2 质量检查清单

| 检查项 | 通过标准 |
|--------|----------|
| 文件存在性验证 | 不存在时返回明确错误 |
| 大小限制检查 | >100MB时给出警告 |
| 压缩效果验证 | ZIP压缩后大小减小 |
| Token刷新机制 | 过期自动获取新Token |
| 错误码映射 | 飞书错误码转可读信息 |

---

## S6: 认知谦逊（局限标注）

### 6.1 已知局限

| 局限 | 说明 | 缓解措施 |
|------|------|----------|
| **单文件100MB软限制** | 飞书API对超大文件支持有限 | 建议用户手动上传超大文件 |
| **无增量同步** | 每次上传都是全量 | 文件名加时间戳区分版本 |
| **无版本管理** | 飞书云盘自动版本有限 | 本地保留备份历史 |
| **依赖网络稳定性** | 上传过程需要稳定网络 | 支持断点续传（待开发） |
| **权限申请延迟** | 新权限需要审核时间 | 提前申请，预留时间 |

### 6.2 不确定性声明

- API限制可能随飞书政策调整而变化
- 压缩率因文件类型差异较大（文本高，视频低）
- 上传速度受网络环境影响

---

## S7: 对抗测试（失效场景验证）

### 7.1 异常输入测试

| 场景 | 测试内容 | 预期结果 |
|------|----------|----------|
| 空文件 | 上传0字节文件 | 允许上传，成功 |
| 特殊字符文件名 | `test@#$%.txt` | 正常处理或安全重命名 |
| 超长文件名 | >255字符 | 截断并保留扩展名 |
| 无权限文件 | `/root/.ssh/id_rsa` | 读取失败，返回错误 |

### 7.2 网络异常测试

| 场景 | 测试内容 | 预期结果 |
|------|----------|----------|
| 上传中断 | 上传50%时断网 | 失败，返回部分结果 |
| API限流 | 快速连续上传 | 指数退避，最终成功 |
| Token过期 | 使用过期Token | 自动刷新，重新上传 |
| 服务不可用 | 飞书API 500错误 | 重试3次后返回错误 |

### 7.3 边界条件测试

| 场景 | 测试内容 | 预期结果 |
|------|----------|----------|
| 正好20MB | 边界值测试 | 直接上传（不压缩） |
| 正好40MB | 边界值测试 | 压缩上传（不分割） |
| 100MB+1字节 | 超过软限制 | 警告但尝试上传 |

---

## 使用指南

### 命令行用法

```bash
# 上传文件
python3 feishu_drive_uploader.py upload /path/to/file.pdf

# 上传到指定文件夹
python3 feishu_drive_uploader.py upload /path/to/file.pdf fldxxxxx

# 强制压缩（即使<20MB）
python3 feishu_drive_uploader.py upload /path/to/file.pdf --compress

# 列出文件
python3 feishu_drive_uploader.py list

# 列出指定文件夹
python3 feishu_drive_uploader.py list --folder fldxxxxx
```

### Python API用法

```python
from feishu_drive_uploader import FeishuUploader

uploader = FeishuUploader()
result = uploader.upload("/path/to/file.pdf", parent_node="fldxxxxx")

if result["success"]:
    print(f"上传成功: {result['files'][0]['file_token']}")
else:
    print(f"上传失败: {result['error']}")
```

---

## 关联文档

- `/docs/FEISHU_WECOM_INTEGRATION_PLAN.md` - 飞书企微整体规划
- `/docs/FEISHU_WECOM_QUICKSTART.md` - 快速开始指南
- `/plugins/feishu_drive_uploader.py` - 核心实现

---

*Feishu Drive Backup Skill V1.0 - 7标准完整版*
