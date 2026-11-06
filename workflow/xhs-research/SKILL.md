---
name: xhs-research
description: Use for read-only Xiaohongshu topic research, including keyword search, bounded post/detail collection, best-effort comments, time filtering, relevance screening, opinion synthesis, and evidence-backed reports.
---

# Xiaohongshu Research

Use the repository's controlled, read-only research pipeline. Never substitute an upstream
CLI command or direct browser action for the entrypoint named below.

## Required preparation

1. Read `references/installation.md`, `references/research-workflow.md`, and
   `references/output-contract.md` before collecting or analyzing evidence.
2. When this skill is installed, read `references/runtime.local.json` and resolve the
   repository from its `project_root` value. When the skill is loaded in place from a
   repository, locate that repository root by walking upward to `research_keyword.py`.
3. Use the installation reference if the runtime, extension, isolated Chrome profile, or
   login is unavailable.

## Execution boundary

Translate the user's request using the parameter rules in the workflow reference. Invoke
only `research_keyword.py`, from the resolved repository, with its locked Python
environment. Keep searches and detail collection serial and bounded. Do not expose or
route to any other upstream entrypoint.

Stop immediately when the page, browser, or runtime reports a QR prompt, CAPTCHA, security
verification, login challenge, or risk-control signal. Human intervention is required
before a later run may continue.

Analyze only successfully collected local records. Treat comments as best effort, apply
time filtering only to successfully detailed candidates, and never imply platform-wide
coverage. Build the final report exactly as required by the output contract, including
citations, coverage statistics, limitations, and `completeness_guaranteed: false`.
