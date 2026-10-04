---
name: LaTeX Tectonic
description: Compile LaTeX and TeX documents with the bundled Tectonic executable.
---

# LaTeX Tectonic

Use this skill when the user asks to compile, preview, build, or troubleshoot a LaTeX or TeX document with Tectonic.

The plugin bundles Tectonic under the plugin root:

- macOS/Linux: `bin/tectonic`
- Windows: `bin/tectonic.exe`

Resolve the plugin root from this `SKILL.md` file by going two directories up from `skills/latex-tectonic/`.

Use `scripts/tectonic-path.mjs` when another script needs the executable path:

```bash
node scripts/tectonic-path.mjs
```

For normal compilation, run the bundled executable directly from the document directory:

```bash
<plugin-root>/bin/tectonic --outdir <output-directory> <tex-file>
```

Prefer writing generated PDFs and auxiliary files into an explicit output directory. Do not install a system TeX distribution unless the user asks for that fallback.

## When to Use

- When a task involves compile latex and tex documents with the bundled tectonic executable
- When an agent needs specialized guidance for latex tectonic workflows
- When the orchestrator identifies this domain in goal decomposition

## Protocol

1. **Assess** — Review the current context and requirements
2. **Plan** — Identify the specific latex tectonic approach needed
3. **Execute** — Follow the guidance above to complete the task
4. **Verify** — Confirm the output meets quality standards
5. **Report** — Summarize what was done and any follow-up needed

## Integration

Available via `invoke_skill("latex-tectonic")` in the agent kernel or `POST /api/skills/invoke`.
