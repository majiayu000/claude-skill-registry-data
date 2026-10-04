---
name: cloud-gcp
description: 使用 gcloud CLI 操作 Google Cloud Platform。当用户提到 GCP、Google Cloud、gcloud、Google Cloud SDK、GCE、GKE、BigQuery、Cloud Storage、Cloud Run、Cloud Functions、VPC、计算实例、VM、存储桶、部署到 GCP、GCP 项目、GCP 账单、IAM 权限等时触发此技能。即使用户只说"我的云服务器"、"查看服务器状态"、"云存储"等模糊表述，如果上下文暗示 Google Cloud，也应使用此技能。
---

# Google Cloud Platform Operator Skill

## 核心理念

这是一个**操作型技能**，帮助你通过 gcloud CLI 管理 Google Cloud 资源。理解三个原则：

1. **直接执行** - 不需要 wrapper 脚本，直接运行 `gcloud` 命令
2. **安全确认** - 写操作必须先展示命令，用户确认后执行
3. **问题自愈** - 遇到错误时自动诊断并尝试修复

---

## 工作流程

```
┌─────────────────────────────────────────────────────────────┐
│                    GCP 操作工作流                            │
├─────────────────────────────────────────────────────────────┤
│  1. 检查环境                                                 │
│     └─ which gcloud → 未安装则执行安装流程                    │
│                                                             │
│  2. 检查认证                                                 │
│     └─ gcloud auth list → 未认证则提示 gcloud auth login     │
│                                                             │
│  3. 确定项目                                                 │
│     └─ gcloud config get-value project                      │
│                                                             │
│  4. 执行操作                                                 │
│     ├─ 只读操作 → 直接执行                                   │
│     └─ 写操作 → 展示命令 → 用户确认 → 执行                    │
│                                                             │
│  5. 处理结果                                                 │
│     ├─ 成功 → 表格/JSON 展示结果                             │
│     └─ 失败 → 诊断错误 → 提供解决方案                         │
└─────────────────────────────────────────────────────────────┘
```

---

## 环境准备

### 快速检查
```bash
which gcloud && gcloud --version
```

### 安装（推荐官方一键安装）
```bash
curl https://sdk.cloud.google.com > install.sh && bash install.sh --disable-prompts
```

### 安装后必须配置
```bash
# 添加到 PATH（永久）
echo 'source ~/google-cloud-sdk/path.zsh.inc' >> ~/.zshrc
source ~/google-cloud-sdk/path.zsh.inc

# 认证
gcloud auth login

# 设置默认项目（可选）
gcloud config set project PROJECT_ID
```

### 常见问题修复

| 问题 | 解决命令 |
|-----|---------|
| gcloud not found | `source ~/google-cloud-sdk/path.zsh.inc` |
| Python 版本错误 | `export CLOUDSDK_PYTHON=/opt/homebrew/bin/python3` |
| 网络超时 | 检测或设置代理（见下方） |
| 未认证 | `gcloud auth login` |

### 网络代理配置

如果遇到网络超时，询问用户代理端口后设置：
```bash
export ALL_PROXY=http://127.0.0.1:<端口>
```

常见代理端口：7890、7897、1087、8080

---

## 安全机制（强制遵守）

### 操作分类

| 类型 | 示例命令 | 执行方式 |
|-----|---------|---------|
| **只读** | list, describe, get, ls | 直接执行 |
| **写操作** | create, delete, update, deploy | 先确认后执行 |
| **销毁操作** | delete, remove, destroy | 确认 + 风险提示 |

### 写操作确认流程

**正确示例：**
```
用户: 创建一个叫 my-bucket 的存储桶

Agent: 即将执行以下命令：
gcloud storage buckets create gs://my-bucket --project=xxx --location=asia-east1

这将创建一个新存储桶，可能产生存储费用。确认执行？(yes/no)
```

**销毁操作额外提示：**
```
用户: 删除 vm-1 实例

Agent: ⚠️ 警告：此操作不可逆！
即将执行：gcloud compute instances delete vm-1 --zone=asia-east1-a

实例上的所有数据将被永久删除。确认执行？(yes/no)
```

---

## 常用命令速查

### 项目与配置
```bash
gcloud projects list                          # 列出所有项目
gcloud config get-value project               # 查看当前项目
gcloud config set project PROJECT_ID          # 切换项目
gcloud config list                            # 查看所有配置
```

### Compute Engine (VM)
```bash
gcloud compute instances list                 # 列出所有实例
gcloud compute instances describe NAME --zone=ZONE
gcloud compute instances create NAME --zone=ZONE --machine-type=e2-micro
gcloud compute instances start NAME --zone=ZONE
gcloud compute instances stop NAME --zone=ZONE
gcloud compute instances delete NAME --zone=ZONE
```

### Cloud Storage (GCS)
```bash
gcloud storage buckets list                   # 列出存储桶
gcloud storage buckets create gs://BUCKET_NAME --location=LOCATION
gcloud storage ls gs://BUCKET_NAME            # 列出文件
gcloud storage cp LOCAL_FILE gs://BUCKET_NAME/  # 上传
gcloud storage cp gs://BUCKET_NAME/FILE .     # 下载
```

### BigQuery
```bash
gcloud bigquery datasets list
gcloud bigquery queries --use_legacy_sql=false 'SELECT * FROM `project.dataset.table` LIMIT 10'
```

### Cloud Run
```bash
gcloud run services list
gcloud run deploy SERVICE --image=IMAGE --region=REGION --allow-unauthenticated
```

### GKE (Kubernetes)
```bash
gcloud container clusters list
gcloud container clusters get-credentials CLUSTER --region=REGION
```

### IAM 与权限
```bash
gcloud iam service-accounts list
gcloud projects get-iam-policy PROJECT_ID     # 查看项目权限
```

### 账单与配额
```bash
gcloud billing accounts list                  # 列出账单账户
gcloud billing projects describe PROJECT_ID   # 查看项目计费状态
gcloud compute regions describe REGION        # 查看区域配额
```

---

## 输出格式

**默认使用 table 格式（人类可读）：**
```bash
gcloud compute instances list --format=table
```

**需要程序处理时使用 json：**
```bash
gcloud compute instances list --format=json
```

**表格字段筛选：**
```bash
gcloud compute instances list --format="table(name,zone,status,machineType.basename())"
```

---

## 错误诊断

### 常见错误速查

| 错误信息 | 原因 | 解决方案 |
|---------|-----|---------|
| `command not found: gcloud` | 未安装或未添加 PATH | 安装或 source path.zsh.inc |
| `You do not currently have an active account` | 未认证 | `gcloud auth login` |
| `PERMISSION_DENIED` | 权限不足 | 检查 IAM 权限或换账户 |
| `Quota exceeded` | 配额用尽 | 申请提高配额或清理资源 |
| `Not found` | 资源不存在 | 检查名称/区域是否正确 |
| `Python version` | Python 版本不兼容 | `export CLOUDSDK_PYTHON=...` |

### 诊断命令
```bash
# 检查认证状态
gcloud auth list

# 检查当前配置
gcloud config list

# 检查项目权限
gcloud projects get-iam-policy $(gcloud config get-value project)
```

---

## 示例交互

**示例 1：查看 VM 实例**
```
用户: 我的 Google Cloud 有哪些服务器？

Agent: [执行 gcloud compute instances list]
```

**示例 2：创建存储桶**
```
用户: 在 GCP 创建一个存储桶 backup-2026

Agent: 即将执行：
gcloud storage buckets create gs://backup-2026 --project=xxx --location=asia-east1

确认执行？(yes/no)
```

**示例 3：查看账单**
```
用户: 帮我看看 GCP 账单情况

Agent: [执行 gcloud billing accounts list 和 gcloud billing projects describe]
```