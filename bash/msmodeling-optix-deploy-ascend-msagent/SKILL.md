---
name: msmodeling-optix-deploy
description: 当用户需要部署 msmodeling optix 服务化自动寻优工具时使用。负责安装与验证。
version: 0.1.0
source: local-session-analysis
---

# 服务化参数自动寻优部署

## 工作范围

本 skill 负责将工具装好并验证能用。

其他内容由对应 skill 负责：

- 运行环境检查：`msmodeling-env-installer`
- 首次参数范围推荐与 `config.toml` 配置：`msmodeling-optix-param-recommend`

## 支持的硬件产品

寻优工具仅支持以下昇腾推理产品：

|产品类型| 是否支持 |
|--|:----:|
|Atlas A3系列产品|  √   |
|Atlas A2系列产品|  √   |
|Atlas 200I/500 A2推理产品|  √   |
|Atlas 200/300/500推理产品|  √   |
|Atlas训练系列产品|  x   |

> - 目标运行环境不支持 Windows
> - 昇腾的训练系列产品不支持，请确认使用的是推理系列产品

## 安装流程

用户说"安装""部署"时，直接执行以下步骤，**不要只给命令**。

### 0. 默认使用阿里云 PyPI 镜像

为减少安装等待时间，默认优先使用阿里云镜像：

```bash
https://mirrors.aliyun.com/pypi/simple/
```

> 注意：不要写成 `PYPI_MIRROR=... python -m pip install -i "$PYPI_MIRROR" ...`。
> 这种写法里 `"$PYPI_MIRROR"` 会在临时环境变量生效前被 shell 展开，结果可能变成空字符串，导致 pip 实际拿到空的 index URL。
>
> 优先直接把镜像地址写进 `-i` 参数；如果确实要用环境变量，必须先单独 `export`，再在后续命令里使用。

若用户已有公司内网镜像、离线源或明确指定其他源，则尊重用户配置，不强制改成阿里云镜像。

### 1. 检查仓库是否存在

寻优工具已集成在 msmodeling 项目中。检查安装入口与默认配置：

```bash
ls pyproject.toml optix/config.toml
```

若仓库不存在，**直接克隆**：

```bash
git clone https://gitcode.com/Ascend/msmodeling.git
cd msmodeling
```

### 2. 判断当前目录和安装方式

msmodeling 仓库结构：

```text
msmodeling/                  ← 仓库根目录
├── pyproject.toml           ← optix 安装入口
└── optix/
    ├── config.toml          ← 寻优工具默认配置
    └── ...                  ← 寻优工具源码（optimizer 代码等）
```

安装时不要依赖上一次 shell 的 `cd` 状态。应优先使用**单条命令**，把切目录和安装写在一起，避免误在其他目录执行 `pip install -e .`。

推荐安装命令如下：

```bash
cd msmodeling && python -m pip install -i https://mirrors.aliyun.com/pypi/simple/ -e .
```

若用户明确要求使用其他镜像，把上面的 URL 替换成用户指定源即可。

> 注意：当前仓库中 `msmodeling` CLI 由仓库根目录的 `pyproject.toml` 提供，安装时应进入 `msmodeling/` 仓库根目录，而不是在 `optix/` 子目录或其他位置执行 `pip install -e .`。

### 3. 验证

```bash
msmodeling optix --help
```

### 4. 汇报结果

告诉用户安装是否成功。若失败，给出具体缺失项和修复建议；并给下一步建议：运行环境检查、配置 `config.toml` 或开始参数推荐。

## 卸载

卸载前说明会移除 Python 包，征得同意后执行：

```bash
python -m pip uninstall optix
```

## 要求

- 始终中文回答。
- 用户同意安装后，要实际检查路径、执行安装并验证 CLI，不要只给命令。
- 不要把运行、配置、结果解读内容塞进本 skill；交给专项 skill 或文档。
- 涉及会创建目录、安装依赖、卸载包的动作，先说明影响并征得用户同意。
