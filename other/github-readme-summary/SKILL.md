---
name: github-readme-summary
description: Summarize a GitHub repo's README using browser tools.
version: 1.0.0

---

## Description
Summarize the README.md of a given GitHub repository using browser tools. Useful for quickly grasping the purpose, usage, and key details of a project without reading the entire file.

## When to use
- You need a quick overview of a GitHub project.
- The repository URL is known (or can be inferred from owner/name).
- You want to avoid manually opening the repo in a browser.

## Steps
1. **Identify the repository** in the format `owner/repo`. If only a URL is given, extract the owner and repo name from the URL (e.g., `https://github.com/owner/repo`).
2. **Construct the raw README URL**: `https://raw.githubusercontent.com/owner/repo/master/README.md`. If the default branch is not `master`, try `main` as a fallback.
3. **Navigate** to the raw URL using the browser tool (`browser_navigate`).
4. **Extract the text content** from the snapshot (the `snapshot` field contains the plain text of the README).
5. **Summarize** the extracted content:
   - Identify the project title (usually the first heading).
   - Extract the description paragraph(s) after the title.
   - List key sections (e.g., Installation, Usage, Features, License) by looking for headings (`##`).
   - Condense each section into one or two sentences.
6. **Return** the summary in a clear, bullet‑point or short‑paragraph format.

## Pitfalls
- The default branch may not be `master`; if the raw URL returns a 404, try `main` or look at the repo’s `HEAD` ref via the GitHub API (outside scope of this skill).
- Some repositories place the README in a different location (e.g., `docs/README.md`). If the raw URL fails, consider checking the repo’s file tree via the GitHub API or the repository’s web page.
- Very large READMEs may exceed the browser snapshot limit; in that case, truncate after a reasonable number of lines and note that the summary is based on the preview.

## References
- See `references/deepseek-harness.md` for an example summary produced from the DeepSeek‑Harness repository.
- For more robust automation, consider using the GitHub REST API to fetch the default branch and README directly.

## Example
Given the repository `deepseek-ai/deepseek-harness`, the skill will produce a summary similar to the one found in `references/deepseek-harness.md`.