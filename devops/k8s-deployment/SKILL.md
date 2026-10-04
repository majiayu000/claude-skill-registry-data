---
name: 容器编排部署Skill
description: Kubernetes 部署清单规范:Deployment/Service/Ingress、探针、资源限额、滚动策略与安全约束。当需要编写或评审 K8s 部署清单时使用。
---
# 容器编排部署Skill

## 适用场景
编写/评审应用的 K8s 部署清单(Deployment/Service/Ingress 等),保障部署可观测、可回滚、可限流。

## 执行步骤
1. 明确部署对象:镜像与 tag(禁止 latest)、副本数、启动参数与所需环境变量。
2. 编写 Deployment:定义探针、资源限额、滚动更新策略、优雅停机时间。
3. 配置 Service 与 Ingress:端口映射、健康检查路径、域名与 TLS 终止方式。
4. 配置敏感信息:凭证走 Secret 或外部密钥服务引用,禁止明文写入清单。
5. 预发布校验:命名空间权限、资源配额、镜像拉取凭证、网络策略是否就绪。
6. 执行发布:先发布到 staging 验证,再按发布方案(Skill:发布方案设计)推进生产。

## 规范要点
- 三类探针必配:就绪探针(接流量前)、存活探针(故障自愈)、启动探针(慢启动保护);参数以官方文档为准。
- 资源限额必配:requests 保证调度,limits 防止失控,两者按实测数据设定。
- 滚动策略:maxUnavailable/maxSurge 按服务可用性要求设定,禁止一次性全量替换。
- 优雅停机:preStop + terminationGracePeriodSeconds 配合,保证存量请求处理完。
- 镜像 tag 必须唯一可追溯,回滚必须能精确回到上一版本。
- 安全红线:直接对生产集群执行 kubectl 删除/扩容/改配置等高危操作,需「总控 + 安全合规」双签名审批;所有生产操作留痕(执行人、命令、时间、结果)。

## 输出模板
```
## K8s 部署清单
镜像信息 / Deployment(探针+限额+滚动策略) / Service / Ingress / Secret 引用(脱敏) / 回滚版本记录
```

## 自检清单
- [ ] 三类探针齐全且路径/端口正确
- [ ] requests/limits 已设置
- [ ] 镜像 tag 可追溯,无 latest
- [ ] 无明文密钥,生产高危操作具备双签名审批
