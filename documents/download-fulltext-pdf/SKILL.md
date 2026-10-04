---
name: download-fulltext-pdf
description: 当用户明确要求"下载文献全文"或"获取论文PDF"时使用。通过 DOI 号下载学术论文全文 PDF，支持 arXiv、Sci-Hub、Unpaywall、期刊官网等多源策略。⚠️ 不适用：用户只是想解析或处理已有的 PDF 文件（应使用 pdf skill）、只是想搜索论文信息而无需下载全文、没有提供 DOI/标题/BibTeX 任何标识符。
metadata:
  author: Bensz Conan
  keywords:
    - download-fulltext-pdf
---

# 下载文献全文 PDF

## 目标

当用户明确要求"下载文献全文"或"获取论文PDF"时使用。通过 DOI 号下载学术论文全文 PDF，支持 arXiv、Sci-Hub、Unpaywall、期刊官网等多源策略。⚠️ 不适用：用户只是想解析或处理已有的 PDF 文件（应使用 pdf skill）、只是想搜索论文信息而无需下载全文、没有提供 DOI/标题/BibTeX 任何标识符。

## 流程

### 输入

输入至少包含 DOI、标题或 BibTeX 之一，并指定输出目录/文件路径；可选输入包括来源开关、Unpaywall 邮箱、验证阈值和覆盖策略。输出路径必须存在或可创建且可写，触发边界以本 Skill 的 `## 目标` 为准。

### 执行步骤

#### 核心工作流

##### 1. 输入验证与规范化

**必需参数**：
- `doi`: DOI 号（如 `10.1038/nature09492`）
- `output_path`: 输出目录或完整 PDF 文件路径

**可选参数**：
- `title`: 论文标题（作为 DOI 的备选）
- `bibtex`: BibTeX 条目（包含 DOI 或标题信息）

**验证逻辑**：
```python
# 由 scripts/validate_input.py 处理
- DOI 格式规范化（移除多余空格、补全前缀）
- 输出路径检查（目录存在性、写入权限）
- 至少提供一种标识符（DOI/title/bibtex）
```

##### 2. 多源下载策略

**优先级顺序**（按成功率和速度排序）：

| 优先级 | 数据源 | 优势 | 局限 | 触发条件 |
|--------|--------|------|------|----------|
| **1** | arXiv | 稳定可靠 | 仅限预印本论文 | 检测到 arXiv ID（如 `10.48550/arXiv.*`） |
| **2** | Sci-Hub | 覆盖较广、速度快 | 可能有 CAPTCHA | 非 arXiv 或 arXiv 失败 |
| **3** | Unpaywall | 合法开放获取（OA） | 取决于论文是否 OA | Sci-Hub 失败时兜底 |
| **4** | 期刊官网 | 合法渠道 | 常需订阅/登录 | 最后兜底 |

**策略执行**：
```python
# 由 scripts/download_pdf.py 实现
1. 如 DOI 可解析出 arXiv ID → 优先 arXiv
2. 尝试 Sci-Hub（通过 scihub 库）
3. 尝试 Unpaywall（合法 OA 获取）
4. 尝试 DOI 落地页并猜测常见 PDF 路径（期刊官网兜底）
```

##### 3. 下载后验证

**必需检查**（由 `scripts/verify_pdf.py` 处理）：
- [ ] 文件大小 > 0 且非 HTML 页面
- [ ] PDF 文件头正确（`%PDF-`）
- [ ] 文件可被 PyPDF2 解析

**失败处理**：
- 验证失败 → 记录错误 → 尝试下一个数据源
- 所有源失败 → 返回详细错误报告

##### 4. 输出格式

**成功时**：
```markdown
✅ 成功下载论文全文

**来源**: Sci-Hub
**DOI**: 10.1038/nature09492
**文件**: /path/to/paper.pdf
**大小**: 2.3 MB
```

**失败时**：
```markdown
❌ 无法下载论文全文

**尝试过的源**:
- Sci-Hub: CAPTCHA 验证失败
- arXiv: 非 arXiv 论文
- Unpaywall: 无开放获取版本
- 期刊官网: 未找到直接 PDF 链接

**建议**:
1. 手动访问 Sci-Hub 并完成 CAPTCHA 验证
2. 检查 DOI 是否正确
3. 尝试通过期刊官网获取
```

#### AI 动态判断

AI 需要动态处理的场景：

| 场景 | 处理方式 |
|------|----------|
| **CAPTCHA 检测** | 识别错误消息中的 "captcha" 关键词 → 切换数据源 |
| **网络超时** | 增加重试次数（最多 3 次）或切换源 |
| **404/未找到** | 直接切换下一个源，不重试 |
| **文件损坏** | 删除已下载文件，尝试下一个源 |
| **arXiv 检测** | DOI 中包含 arXiv ID → 优先使用 arXiv 源 |

#### 硬编码操作（scripts/）

##### scripts/validate_input.py

输入验证与规范化脚本：

```python
import sys
import re
from pathlib import Path

def normalize_doi(doi: str) -> str:
    """规范化 DOI 格式"""
    doi = doi.strip()
    if not doi.startswith("10."):
        doi = f"10.{doi}"  # 尝试补全
    return doi

def validate_output_path(path: str) -> Path:
    """验证输出路径"""
    path = Path(path).expanduser().resolve()
    if path.exists() and path.is_dir():
        # 目录：自动生成文件名
        return path / "paper.pdf"
    if path.parent.exists():
        # 完整路径：确保父目录可写
        return path
    raise ValueError(f"输出路径无效: {path}")

def main():
    if len(sys.argv) < 3:
        print("用法: python validate_input.py <doi> <output_path>", file=sys.stderr)
        sys.exit(1)

    doi = normalize_doi(sys.argv[1])
    output_path = validate_output_path(sys.argv[2])

    print(f"DOI:{doi}")
    print(f"OUTPUT:{output_path}")

if __name__ == "__main__":
    main()
```

##### scripts/download_pdf.py

核心下载逻辑（多源策略）：

```python
import sys
import requests
from pathlib import Path
from typing import Optional, Tuple

# 尝试导入 scihub 库（可选依赖）
try:
    from scihub import SciHub
    HAS_SCIHUB = True
except ImportError:
    HAS_SCIHUB = False

class PDFDownloader:
    """多源 PDF 下载器"""

    def __init__(self, doi: str, output_path: Path):
        self.doi = doi
        self.output_path = output_path
        self.sources_tried = []

    def download_from_scihub(self) -> Tuple[bool, str]:
        """从 Sci-Hub 下载"""
        if not HAS_SCIHUB:
            return False, "scihub 库未安装"

        try:
            sh = SciHub()
            result = sh.download(self.doi, path=str(self.output_path))
            if result and self.output_path.exists():
                return True, "Sci-Hub"
            return False, "下载失败"
        except Exception as e:
            error_msg = str(e).lower()
            if "captcha" in error_msg:
                return False, "CAPTCHA 验证失败"
            return False, str(e)

    def download_from_arxiv(self) -> Tuple[bool, str]:
        """从 arXiv 下载（检测 arXiv ID）"""
        # 简化实现：arXiv 直接下载 URL
        arxiv_id = self._extract_arxiv_id()
        if not arxiv_id:
            return False, "非 arXiv 论文"

        url = f"https://arxiv.org/pdf/{arxiv_id}.pdf"
        try:
            response = requests.get(url, timeout=30)
            if response.status_code == 200:
                self.output_path.write_bytes(response.content)
                return True, "arXiv"
            return False, f"HTTP {response.status_code}"
        except Exception as e:
            return False, str(e)

    def download_from_unpaywall(self) -> Tuple[bool, str]:
        """从 Unpaywall 下载（合法 OA）"""
        # Unpaywall API 端点
        # email 参数建议从 config.yaml 读取；可配置 emails 列表做负载均衡
        url = f"https://api.unpaywall.org/v2/{self.doi}"
        try:
            response = requests.get(url, timeout=30)
            if response.status_code == 200:
                data = response.json()
                if data.get("is_oa"):
                    pdf_url = data.get("best_oa_location", {}).get("url_for_pdf")
                    if pdf_url:
                        pdf_resp = requests.get(pdf_url, timeout=30)
                        if pdf_resp.status_code == 200:
                            self.output_path.write_bytes(pdf_resp.content)
                            return True, "Unpaywall"
            return False, "无开放获取版本"
        except Exception as e:
            return False, str(e)

    def _extract_arxiv_id(self) -> Optional[str]:
        """从 DOI 或上下文中提取 arXiv ID"""
        # 简化实现：检测 DOI 中是否包含 arXiv 信息
        # 实际应解析 BibTeX 或标题
        return None

    def download(self) -> Tuple[bool, str, str]:
        """执行多源下载策略"""
        # 策略 1: Sci-Hub
        self.sources_tried.append("Sci-Hub")
        success, source = self.download_from_scihub()
        if success:
            return True, source, "成功"

        # 策略 2: arXiv（如果是 arXiv 论文）
        self.sources_tried.append("arXiv")
        success, source = self.download_from_arxiv()
        if success:
            return True, source, "成功"

        # 策略 3: Unpaywall
        self.sources_tried.append("Unpaywall")
        success, source = self.download_from_unpaywall()
        if success:
            return True, source, "成功"

        # 所有源失败
        return False, "", f"尝试过的源: {', '.join(self.sources_tried)}"

def main():
    if len(sys.argv) != 3:
        print("用法: python download_pdf.py <doi> <output_path>", file=sys.stderr)
        sys.exit(1)

    doi = sys.argv[1]
    output_path = Path(sys.argv[2]).expanduser().resolve()

    downloader = PDFDownloader(doi, output_path)
    success, source, message = downloader.download()

    if success:
        print(f"SUCCESS:{source}")
        print(f"FILE:{output_path}")
        print(f"SIZE:{output_path.stat().st_size}")
    else:
        print(f"FAILURE:{message}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
```

##### scripts/verify_pdf.py

PDF 验证脚本：

```python
import sys
from pathlib import Path

def verify_pdf(path: Path) -> Tuple[bool, str]:
    """验证 PDF 文件完整性"""
    if not path.exists():
        return False, "文件不存在"

    if path.stat().st_size == 0:
        return False, "文件大小为 0"

    # 检查 PDF 文件头
    with open(path, "rb") as f:
        header = f.read(5)
        if header != b"%PDF-":
            return False, "无效的 PDF 文件头"

    # 尝试用 PyPDF2 解析
    try:
        import PyPDF2
        with open(path, "rb") as f:
            PyPDF2.PdfReader(f)
        return True, "有效 PDF"
    except ImportError:
        # PyPDF2 未安装，跳过深度验证
        return True, "未安装 PyPDF2，跳过深度验证"
    except Exception as e:
        return False, f"PDF 解析失败: {str(e)}"

def main():
    if len(sys.argv) != 2:
        print("用法: python verify_pdf.py <pdf_path>", file=sys.stderr)
        sys.exit(1)

    path = Path(sys.argv[1]).expanduser().resolve()
    is_valid, message = verify_pdf(path)

    if is_valid:
        print(f"VALID:{message}")
        sys.exit(0)
    else:
        print(f"INVALID:{message}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
```

#### 配置参数（config.yaml）

```yaml
# 下载策略配置
download:
  # Sci-Hub 配置
  scihub:
    enabled: true
    timeout: 30  # 秒
    retries: 3

  # arXiv 配置
  arxiv:
    enabled: true
    timeout: 30

  # Unpaywall 配置
  unpaywall:
    enabled: true
    emails:
      - "hwb2012@qq.com"
      - "huangwb886@gmail.com"
    email_strategy: "round_robin"  # round_robin | hash_doi | random
    state_file: ".bensz-api/task-{yyyymmdd-hhmm}-{简短描述}/download-fulltext-pdf/state/unpaywall_email_state.json"
    email: ""  # 兼容旧字段（可选）

# 验证配置
verification:
  check_pdf_header: true
  require_pypdf2: false  # 是否强制要求 PyPDF2
  max_file_size: 100_000_000  # 100 MB

# 输出配置
output:
  default_filename: "paper.pdf"
  overwrite: false  # 是否覆盖已存在文件
```

#### 依赖说明

**必需依赖**：
- `requests`（网络请求）

**可选依赖（自动安装）**：
- `scihub`（Sci-Hub 支持，**首次使用时自动安装**）
- `PyPDF2`（PDF 验证，推荐安装）

##### 自动安装机制

当 AI 执行下载任务时，`scripts/download_pdf.py` 会：
1. 检测缺失的可选依赖
2. **提醒用户**将要安装的包（如 `📦 检测到缺失依赖: scihub`）
3. **自动安装**（使用 `pip install`）
4. 安装失败时自动降级到其他数据源

用户无需手动安装，skill 会"开箱即用"。

##### 手动安装（可选）

如果自动安装失败，用户可以手动安装：

```bash
pip install requests scihub PyPDF2
```

#### 使用示例

**示例 1：使用 DOI 下载**
```bash
/skill download-fulltext-pdf "10.1038/nature09492" ./downloads/
```

**示例 2：使用标题下载**
```bash
/skill download-fulltext-pdf --title "Deep Learning" ./downloads/
```

**示例 3：批量下载（从 BibTeX 文件）**
```bash
/skill download-fulltext-pdf --bibtex references.bib ./downloads/
```

### 输出

成功时交付经 `%PDF-` 文件头和可选 PyPDF2 解析验证的 PDF，并报告来源、规范化 DOI、文件路径和大小；失败时列出尝试过的来源、具体原因和可操作建议。状态文件、日志和调试材料留在任务工作区。

### 输出管理

#### BenszAPI 任务工作区


### 校验

#### 质量检查清单

- [ ] DOI 格式正确（以 `10.` 开头）
- [ ] 输出路径可写
- [ ] 至少一种数据源可用
- [ ] 下载后 PDF 验证通过
- [ ] 错误消息清晰可操作

### 失败与恢复

#### 错误处理

| 错误类型 | 表现 | 处理方式 |
|---------|------|----------|
| **CAPTCHA** | Sci-Hub 返回验证码页面 | 切换到 Unpaywall 或期刊官网 |
| **未找到** | 404 或 "not found" | 切换下一个数据源 |
| **超时** | 请求超时 | 重试（最多 3 次） |
| **文件损坏** | PDF 头无效 | 删除并重新下载 |

#### 注意事项

1. **版权合规**：仅用于学术研究，遵守当地版权法律
2. **Sci-Hub 可用性**：Sci-Hub 域名可能变化，需要定期更新
3. **网络环境**：某些地区可能需要代理才能访问 Sci-Hub
4. **CAPTCHA 处理**：遇到 CAPTCHA 时，建议手动完成验证


## 约束

<!-- BEGIN COMMON CONSTRAINTS -->
<!-- Source-Hash: sha256:15120201e9e0c7569517261d57ecefb63ac279c26ed13876f8e95b6dc35854d3 -->
<!-- Template-ID: skill-common-constraints; Template-Version: 1; Sync-Policy: exact-block -->

### 公共硬约束

本块由 `docs/templates/skill-common-constraints.md` 统一维护；每个 `SKILL.md` 的 `## 约束` 必须逐字同步本块，不得在副本中改写公共规则。

- 任务需要落盘时，使用唯一的 `./.bensz-api/task-{yyyymmdd-hhmm}-{简短描述}/` 根目录；共享材料放入 `shared/`，Skill 专属材料放入该 Skill 的 `input/`、`output/`、`log/`。
- 正式交付物、源代码和正式计划按项目约定保存，不写入任务工作区；未经授权不覆盖、删除、迁移或远程写入。
- 项目维护变更检查 BAC 可用性并记录需求、AI 产出、工具结果、文件改动和验证摘要；BAC 只做过程审计，不替代署名、责任或合规判断。
- 不记录 API Key、访问令牌、密码、Cookie、环境/凭据文件、私有 Prompt、身份信息、本地用户名、主机名或不必要的大体积原始数据。
- 文件路径必须规范化并限制在授权项目范围内；外部 URL、子进程和网络访问遵循最小权限，防止路径遍历、SSRF 和命令注入。
- Skill 版本唯一记录在自身 `config.yaml:skill_info.version`；公开 API、协议、目录或配置变更同步文档与 `CHANGELOG.md`。
- `bensz-collect-bugs` 是一个 Agent Skill；仅将 Bensz Agent Skill 或 Bensz 基础设施本身的设计缺陷交给它。先脱敏写入 `~/.bensz-skills/bugs/`，当前任务不中断，只有用户明确要求才公开上报，禁止直接修改用户已安装的 Skill 源码。

<!-- End of canonical common constraints. -->
<!-- END COMMON CONSTRAINTS -->
