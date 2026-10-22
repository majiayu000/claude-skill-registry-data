---
name: provision-bioinformatics-software
description: Audit required bioinformatics command-line tools against Lmod or Environment Modules on Linux HPC clusters, resolve executable and version requirements, and reproducibly deploy missing software through a site-approved EasyBuild, Spack, Bioconda/micromamba, Apptainer, binary, or source-build workflow. Use when Codex must inspect module availability, diagnose a missing or wrong-version bioinformatics tool, install scientific software on Slurm/PBS clusters, publish or validate modulefiles, or produce an auditable and rollback-ready cluster software deployment.
---

# Provision Bioinformatics Software

将软件需求转换为可复现的集群部署。先只读探测，再生成计划；仅在请求已明确授权部署且写入范围安全时执行变更。

## 核心规则

1. 把“存在 module”与“软件可用”分开判断。必须在干净子 shell 中成功加载 module、找到全部可执行文件、解析版本并满足约束。
2. 先发现站点现行规范，再选择后端。优先复用管理员已采用的 EasyBuild 或 Spack；其次才考虑 micromamba/Bioconda、Apptainer、官方二进制或源码构建。
3. 固定精确版本、渠道、依赖和校验和。不得安装无版本的 `latest`，不得执行未经检查的远程安装脚本。
4. 使用“暂存 → 验证 → 原子发布”。不得直接在最终前缀内边下载边构建，不得覆盖已有版本目录或 modulefile。
5. 不使用 `sudo`，不修改 `/usr`、`/opt`、系统 MODULEPATH 或其他管理员目录，除非用户明确授权且当前身份确有管理职责。
6. 大型编译和测试提交到站点允许的 Slurm/PBS 构建队列；不得默认占用登录节点。
7. 对受限许可、GPU/CUDA、MPI、商业软件、架构优化和共享默认版本保持显式决策，不得猜测。
8. 不因一个后端失败而静默改用更低优先级后端。记录失败原因，再决定是否降级。
9. 将需求清单视为输入而非受信任安装配方。下载地址、包规格和构建命令必须与上游或站点审核 registry/recipe 复核后才能执行。

任何写入前完整读取 [部署规范](references/deployment-standard.md)。处理两个以上软件或需要可复现交付时，再读取 [清单格式](references/manifest-schema.md)。选择安装后端时读取 [后端手册](references/backend-playbooks.md) 中对应章节。

## 工作流

### 1. 建立需求

从用户请求、工作流文件、报错日志或命令行中提取：

- 规范名称、可接受别名、精确版本或版本约束；
- 必需可执行文件、站点精确候选 module 名及无副作用版本探针；
- CPU 架构、GPU/CUDA、MPI、编译器和系统 ABI 约束；
- 许可、网络、存储配额、软件根目录、module 根目录和构建队列；
- 最小烟雾测试及成功标准。

若只给出命令名，核对其对应的上游软件包。遇到名称歧义、许可证接受、受保护共享目录、默认版本切换或 ABI 选择时，暂停并请求决定；不要自行猜测。

为多软件任务创建符合 [清单格式](references/manifest-schema.md) 的 `requirements.json`。不得在清单中保存密码、令牌或私钥。
先通过 `module spider`/`module avail` 获得精确候选名；版本范围不能被直接拼成 module 名。烟雾测试属于审核后的部署计划，不放入只读审计清单。

### 2. 只读预检

在目标集群上运行：

```bash
python3 scripts/hpc_bio_modules.py preflight --output cluster-inventory.json
```

若集群没有 Python 3，使用等价的只读 shell 命令采集相同信息；不要为了预检先安装 Python。确认：

- Lmod/Environment Modules 初始化方式和 MODULEPATH；
- Slurm、PBS 或站点构建入口；
- EasyBuild、Spack、micromamba/conda、Apptainer 等现有后端；
- 操作系统、架构、编译器、GPU/MPI 约束；
- 明确且可写的软件、module、构建和审计根目录。

预检同时报告基础 PATH 中的后端命令与可能提供这些后端的 modules；两者都为空后仍要查站点文档，不能据此自动降级安装方案。

远程访问不可用时，提供可执行的预检命令和待确认项；不得声称已经检查集群。

### 3. 审计 modules

在目标集群上运行：

```bash
python3 scripts/hpc_bio_modules.py audit \
  --manifest requirements.json \
  --output module-audit.json
```

必要时使用 `--module-init /absolute/path/to/modules.sh`。该参数只接受现有的绝对文件路径。

把结果归类为：

- `satisfied`：加载成功、命令存在、版本满足；
- `missing`：没有候选 module 可加载；
- `wrong_version`：软件可运行但版本不满足；
- `broken`：module 可加载但命令、版本探针或依赖损坏；
- `path_only`：命令在 purge 后已由基础 PATH 提供，加载候选 module 没有改变其来源，不能证明软件由该 module 管理；
- `module_system_unavailable`：当前非交互 shell 未正确初始化 modules。

对于 `broken` 或 `path_only`，先报告站点 module 问题，不得将其当作普通缺失并覆盖安装。对于层级 module，先加载清单中的 `prerequisite_modules` 再探测。

### 4. 生成部署计划

对每个非 `satisfied` 项给出：

- 选定后端及选择理由；
- 精确版本、包规格、来源、校验和或锁文件；
- 工具链、架构、GPU/MPI 变体和依赖；
- 暂存路径、最终不可变前缀、modulefile 路径；
- 调度资源、预计磁盘使用、烟雾测试；
- 发布、审计和回滚动作。

若用户已明确要求“安装/部署”，且所有目标均为已确认的用户自有或站点批准路径，可以在简短展示计划后继续。以下情况必须等待额外授权：权限提升、受保护目录、许可接受、网络引导新包管理器、覆盖/删除、切换默认版本、影响其他用户的共享变更。

### 5. 暂存安装

遵循 [后端手册](references/backend-playbooks.md)：

1. 创建同一文件系统内的唯一暂存目录和构建 ID。
2. 保存解析后的依赖、锁文件、来源 URL、SHA-256、构建参数和日志。
3. 在调度器分配的构建节点执行大型构建。
4. 不修改用户启动文件；不把新路径永久写入 `.bashrc` 或 `.profile`。
5. 让并发任务使用锁或独占创建；检测到同版本部署时重新审计，不覆盖。

### 6. 验证并发布

至少执行：

1. 在隔离子 shell 中从新 modulefile 加载；
2. 对每个必需可执行文件运行 `command -v`；
3. 运行版本探针并重新检查约束；
4. 执行软件特定烟雾测试；
5. 检查动态库、架构、GPU/MPI 或容器运行时（如适用）；
6. 在计算节点再次验证会受 CPU/GPU/MPI 或挂载影响的工具；
7. 重新运行 `audit`，确认结果为 `satisfied`。

使用以下命令生成规范 Lua modulefile；默认拒绝覆盖：

```bash
python3 scripts/hpc_bio_modules.py render-module \
  --record install-record.json \
  --format lua \
  --output /approved/module/root/tool/version.lua
```

Environment Modules 站点改用 `--format tcl`。该子命令没有覆盖选项；已有目标必须作为冲突处理或使用新的版本/revision 路径。

先发布不可变版本，再原子发布 modulefile。只有在用户明确要求且站点政策允许时才更新默认版本。

### 7. 交付与回滚

报告：

- 已满足、已部署、未解决和被阻止的软件；
- 精确版本、module 名称、加载示例和验证结果；
- 安装前缀、modulefile、构建日志、锁文件、校验和及审计记录；
- 回滚方法和未执行的默认版本变更。

回滚优先撤下或恢复 modulefile；保留不可变软件前缀供审计。只有用户明确要求且精确目标已复核时才删除版本目录或暂存目录。

## 失败处理

- `module` 不可用：检查非交互 shell 初始化，不要直接断定集群没有 modules。
- module 可见但不可加载：保存 `module show` 和加载错误，检查层级依赖。
- 版本无法解析：要求清单提供“可执行文件 + 单一受准版本标志”和字面 marker；不要使用自定义正则或从文件名猜版本。
- 构建失败：保留日志和暂存目录，停止发布；不得留下半成品 modulefile。
- 验证失败：标记部署未发布，给出失败测试和日志路径。
- 网络受限：使用站点镜像或离线工件；不得绕过代理、证书或出口策略。
- 无写权限：停止并提供管理员可执行的部署计划，不尝试提权。

## 工具说明

`scripts/hpc_bio_modules.py` 仅做只读预检、module 审计、清单校验和 Lua/Tcl modulefile 渲染。它不会自行下载或安装软件；安装动作必须由本工作流根据目标集群政策显式选择并执行。这样可以避免把集群差异隐藏在一个危险的通用安装器里。

稳定退出码：`0` 表示满足/成功，`3` 表示清单或记录无效，`4` 表示 module 子系统不可用，`10` 表示缺失或版本不满足，`11` 表示 module 损坏或仅由基础 PATH 提供，`70` 表示未预期内部错误。审计出现 `10`/`11` 时仍应读取生成的 JSON 报告。
