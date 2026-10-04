---
name: nvidia-air-ngc
description: NVIDIA Air (air-ngc.nvidia.com) API 操作 — 认证、端点、服务器实例创建。NVIDIA GPU 云仿真平台，支持 GPU 驱动的云端仿真环境。
triggers:
  - NVIDIA Air NGC API
  - air-ngc
  - nvapi-
  - NVIDIA GPU cloud simulation
  - 创建 GPU 云服务器
---

# NVIDIA Air NGC API

## 认证

```bash
export NVIDIA_AIR_API_BASE="https://api.air-ngc.nvidia.com/api/v3"
export NVIDIA_AIR_API_KEY="nvapi-xxxxxxxxxxxxxxxxxxxx"
```

所有 API 请求使用 **Bearer Token** 认证：

```bash
-H "Authorization: Bearer $NVIDIA_AIR_API_KEY"
-H "Content-Type: application/json"
```

## 关键端点

| 端点 | 用途 |
|------|------|
| `GET /api/v3/simulations/` | 列出仿真实例 |
| `POST /api/v3/simulations/` | 创建仿真实例 |
| `GET /api/v3/simulations/{id}` | 获取实例详情 |
| `DELETE /api/v3/simulations/{id}` | 删除实例 |

**注意**：路径必须带 trailing slash，否则返回 301 重定向。

## 常见错误

### 403: Business Email Required

```
{"detail":"A business email address is required to sign in to Air. Please use your company or organization email."}
```

**原因**：NVIDIA Air 要求账号必须验证**企业/公司邮箱**（不能用 gmail, hotmail, 个人域名邮箱）。

**解决方案**：
1. 登录 https://air-ngc.nvidia.com
2. 进入 **Account Settings → Email**
3. 添加并验证一个企业邮箱（如 `name@yourcompany.com`）
4. 验证后 API 才能正常使用

### 环境连通性

- `api.air-ngc.nvidia.com` — 可达（HTTP 301 跳转到 `/api/v3/simulations/`）
- `api.air.ngc.nvidia.com` — 不可达（DNS 解析失败）
- `auth.ngc.nvidia.com` — 不可达（DNS 解析失败）

## 浏览器限制

此环境（容器/无沙盒）无法运行 Chrome/Chromium 进行网页操作。如需网页端操作，需要用户自己在浏览器完成。

## 创建实例的典型请求体

```json
POST /api/v3/simulations/
{
  "name": "my-simulation",
  "instance_type": "4核-4GPU-100G",
  "gpu": "A100",
  "disk_gb": 100,
  "duration_hours": 24
}
```

> ⚠️ 实际字段名需要参考 NVIDIA Air UI 或 API 文档确认。上表中的字段是示意。