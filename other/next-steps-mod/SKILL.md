---
name: next-steps-mod
description: >-
  Load, verify or troubleshoot the Claude Code mod that makes Claude name the next steps at the end
  of every answer (a Next:/Also: block), draws them as one-press buttons above the prompt, offers the
  top one as the Tab suggestion, and adds /next-steps. Use when the operator says "install the
  next-steps mod", "why is there no next step band", "turn the next-steps band back on", or asks for
  Claude to recommend next steps without being asked. Deployed through Skills Army HQ; the HQ link in
  ~/.claude/skills auto-loads it. Requires Claude Code 2.1.309 or newer. Never approves, blocks or
  rewrites a tool call or an operator prompt.
---

# next-steps-mod — never ask "what's next?" again (GH-1240)

A Claude Code **mod** is a plugin whose TypeScript hooks run inside Claude Code. This one makes
Claude think one step ahead and say so, every turn, and puts the recommendation one press away:

1. **Every answer ends with a `Next:` block.** A `prompt.compose` hook appends one session-scope
   section to the system prompt: end every main-loop answer with `Next: <the one recommended step,
   pasteable as a prompt>` and up to two `Also:` alternatives; name the most valuable follow-up even
   when nothing is pending; never close with "let me know" or a question back. This works under any
   output style and under the short system prompt.
2. **A band above the prompt** (terminal and Desktop). After each answer a `turn.complete` hook parses
   the `Next:`/`Also:` lines; the band shows them as buttons (`1`, `2`, `3` hotkeys when the band has
   focus). Pressing one submits that step as your own prompt. The top step is also the dim
   Tab-to-take prompt suggestion. If an answer has no `Next:` line, the band says so and offers one
   button, **Ask what's next**. **Hide** mutes the band for the session.
3. **`/next-steps`** submits "What are the next steps? Rank the three most valuable…" without typing it.

Nothing is auto-submitted: every prompt the mod sends is a button press or the slash command.

## Load it

The plugin manifest sits at this folder's root, so the folder **is** the mod. Deploy it like any
skill through Skills Army HQ (`intake.py add` + `sync.py --apply`); the resulting link
`~/.claude/skills/next-steps-mod` is a folder Claude Code auto-loads and watches, in Desktop, terminal
and VS Code sessions alike. New sessions pick it up on start; `/plugin` lists it as active. No
`--plugin-dir`, no marketplace. For a one-off session from a clone:

```bash
claude --plugin-dir "<clone>/skills/2-daily/next-steps-mod"
```

The engine writes `.claude-plugin/types/` beside a loaded mod; this folder's `.gitignore` keeps that
out of the repo and of the Pulse collection copy.

## Turn it off

Press **Hide** (this session), or withdraw the HQ link (`intake.py --apply remove next-steps-mod`,
then `sync.py --apply`) to stop loading it everywhere. Removing the folder is the full rollback.

## Boundary

Registers `session.start`, `command.run{next-steps}`, `prompt.compose`, `turn.complete` and
`ui.render{AbovePrompt}`; calls `$.command.register`, `$.prompt.submit` (only from a button press or
the command), `$.prompt.suggest`, `$.state.get/set`, `$.ui.resolve`. It registers no `tool.call`,
`tool.check`, `prompt.submit` or `session.append` hook, so it cannot approve, block or rewrite a
tool call or an operator prompt. `prompt.compose` only appends; it never drops or edits a section.
Mods are not sandboxed: a later change that adds any of the excluded hooks needs its own issue.

## Manual diagnostic

A written checklist, not a test suite (GH-831). Record each run under
`TESTS-RESULTS/<date>+GH-1240/` with a `provenance.jsonl`.

| Check | How | Pass when |
|---|---|---|
| D1 | `claude --version` (the binary the surface runs; the Desktop app bundles its own) | 2.1.309 or newer |
| D2 | `claude plugin validate <clone>/skills/2-daily/next-steps-mod` | passes; hooks and calls are exactly the Boundary list |
| D3 | `tsc -p` with the tsconfig from the types file header, including the engine's `claude-code.d.ts` and this folder's `hooks` and `types` | zero errors |
| D4 | `/plugin` in a session started after `sync.py --apply` | the mod is listed active with no `--plugin-dir` |
| D5 | Send any prompt in a Desktop or terminal session | the answer ends with a `Next:` line; the band shows it as the primary button; Tab takes it in the empty prompt box |
| D6 | Press the primary button | that text is submitted as your prompt and a turn starts |
| D7 | `/next-steps` | the ranked-next-steps prompt is submitted; no typing |
| R1 (red control) | Reply to a prompt whose answer cannot carry a `Next:` line (e.g. an interrupted turn), or temporarily set `LINE` in `hooks/register.tsx` to a pattern that never matches (local edit, not committed) | the band reads "No Next: line in the last answer" with **Ask what's next**; restore and re-run: D5 passes |
