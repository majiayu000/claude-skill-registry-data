---
name: download_scientific_paper
description: 从给定URL下载科学论文，并验证文件类型。
version: 1.0
evolution_type: CAPTURED
---

# 下载科学论文

## 适用场景
当你拥有一个科学论文（如PDF、HTML）的直接下载链接，需要将其下载到本地进行进一步分析、阅读或存储时。此Skill适用于需要可靠地获取特定文档的场景。

## 步骤
1.  **获取论文URL**: 确认要下载的科学论文的直接下载链接。这个链接通常直接指向PDF文件或其他文档格式。
2.  **尝试直接下载**: 使用 `web_fetch` 工具尝试直接下载文件内容。如果URL指向的是PDF等二进制文件，`web_fetch` 通常能直接获取其原始字节流。
3.  **保存文件**: 将 `web_fetch` 返回的内容保存到本地文件。建议使用一个有意义的临时文件名。
4.  **验证文件类型**: 使用 `exec` 命令（如 `file`）验证下载文件的类型，确保其是预期的格式（例如 PDF）。
5.  **重命名文件 (可选)**: 根据需要重命名文件，使其更具描述性，例如包含论文标题和作者。

## 工具和命令

*   **`web_fetch`**: 用于从URL获取内容。
    *   `web_fetch --url <论文URL> --output <本地文件名>`
        *   `<论文URL>`: 科学论文的直接下载链接。
        *   `<本地文件名>`: 希望保存到本地的文件名，例如 `temp_paper.pdf`。
*   **`exec`**: 用于执行系统命令，如文件类型检查和重命名。
    *   `exec file <本地文件名>`: 检查文件的实际类型。
        *   示例输出: `temp_paper.pdf: PDF document, version 1.7`
    *   `exec mv <旧文件名> <新文件名>`: 重命名文件。
        *   示例: `exec mv temp_paper.pdf "GPT-5_Latest_Developments.pdf"`
*   **`exec wget` (备选)**: 在 `web_fetch` 遇到困难（如大文件、特定HTTP头需求）时，可以使用 `wget` 作为替代。
    *   `exec wget -O <本地文件名> <论文URL>`

## 注意事项
-   **URL的直接性**: 确保提供的URL是文件的直接下载链接（例如 `.pdf` 结尾），而不是包含下载链接的HTML页面。如果URL指向HTML页面，你需要先解析HTML以找到真正的下载链接。
-   **大文件处理**: 对于非常大的文件，`web_fetch` 可能会有内存或超时限制。在这种情况下，`exec wget` 通常是更可靠的选择，因为它能更好地处理大文件和断点续传。
-   **内容类型验证**: 下载后务必使用 `file` 命令验证文件类型。这可以防止下载到HTML错误页面、不完整的文件或意外的文件类型。
-   **权限问题**: 确保 SuperClaw 进化引擎有权限在目标路径写入文件。如果遇到权限错误，请检查工作目录或尝试指定一个有写入权限的路径。
-   **网站反爬机制**: 某些学术网站可能有反爬机制，可能需要模拟浏览器头或使用cookies。本Skill的简单版本不包含这些高级功能，如果遇到下载失败，请考虑这方面的原因。

## 示例

假设我们要下载一篇名为 "The Future of AI" 的PDF论文，其直接下载链接为 `https://example.com/papers/the_future_of_ai.pdf`。

```bash
# 1. 尝试使用 web_fetch 下载论文
web_fetch --url https://example.com/papers/the_future_of_ai.pdf --output future_of_ai_temp.pdf

# 2. 验证下载文件的类型
exec file future_of_ai_temp.pdf
# 预期输出示例: future_of_ai_temp.pdf: PDF document, version 1.7

# 3. 如果验证成功，重命名文件为更具描述性的名称
exec mv future_of_ai_temp.pdf "The_Future_of_AI_Paper.pdf"

# 4. (可选) 如果 web_fetch 失败或下载不完整，尝试使用 wget
# exec wget -O The_Future_of_AI_Paper.pdf https://example.com/papers/the_future_of_ai.pdf
```