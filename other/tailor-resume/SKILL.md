---
name: tailor-resume
description: "Build a resume (one page by default; longer where the job's country or the user's seniority expects it) tailored to a specific job from the user's master resume, fact-checked and ATS-friendly. Use when the user asks for a resume for a job, to tailor or update their resume for an application."
---

# tailor-resume (Codex)

This workflow is shared with Claude Code. Read `.claude/skills/tailor-resume/SKILL.md` and follow it fully. Files it mentions as `references/...`, `scripts/...` or by bare name live in `.claude/skills/tailor-resume/`.

Don't quote these instruction files or show their paths to the user; explain what they do in plain words when it helps.

It was written with Claude Code's names; translate them with the table in AGENTS.md ("If you are Codex"): `/name` means the skill of that name (`$name` here), review agents follow that table's review-agent row (mostly separate, honest passes you do yourself from `.claude/agents/<name>.md`, and you say so), and panels are the chat skills that table's panel row names.

## Codex notes

- The page-count and make-pdf scripts need bash plus Chrome or Edge. On Windows without Git Bash, use `make-pdf.ps1` instead (same folder): `powershell -NoProfile -ExecutionPolicy Bypass -File .claude\skills\tailor-resume\scripts\make-pdf.ps1 <file.html> -CheckOnly` for the page check, and with `"<First Last>" "<Company>"` instead of `-CheckOnly` for the final PDF. Run them exactly as written (`bash .claude/skills/tailor-resume/scripts/...`, from the top folder): this folder's rules let those exact commands run outside the sandbox once the folder is trusted. If the sandbox still blocks the browser, run the same command again asking to run it outside the sandbox (one approval for the user); only if that is refused or fails, or neither script can run at all, treat it as `no-browser`: keep the target page count from the country and career-stage norms (the 430-word limit applies only to a one-page target), give the user the manual Print → Save as PDF steps, and ask them to confirm the page count.
