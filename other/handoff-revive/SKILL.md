---
name: handoff-revive
description: Save a compact handoff checkpoint and resume work in a fresh session without replaying the entire transcript via `--resume`. SAVE trigger — the slash command `/handoff-revive:save` (carries forward still-relevant goal/decisions/lessons from any existing handoff, then runs a content-quality check). AUTO-SAVE trigger — when the UserPromptSubmit hook injects "5-hour usage at N%" context (run SAVE flow without asking, prepend brief notice). RESUME trigger — the slash command `/handoff-revive:resume`. Also use when the SessionStart hook surfaces an existing handoff at `.claude/handoff/current.md` — read that file instead of recommending `claude --resume`. Configuration via `/handoff-revive:auto on|off|status` (per-session toggle). Do NOT trigger on natural-language phrases like "save handoff" / "ハンドオフ保存して" / "続きから" — only the slash commands and hook contexts above.
---

# handoff-revive

Save the minimum state needed to continue work later, so the next session can start fresh (NOT via `--resume` / `-c`) and reload only a small file.

## Why not `claude --resume`

`--resume` and `-c` replay the entire prior transcript into context. For a typical session this costs **tens of thousands of tokens** (often **100k+ for long sessions**) before the user even asks anything. A handoff file costs **1,000–3,000 tokens**. Always prefer the handoff file when one exists.

## Two modes

### Mode 1: SAVE (`/handoff-revive:save`)

Triggered ONLY by:
- User runs the slash command `/handoff-revive:save`
- The UserPromptSubmit hook injects auto-save context (see Mode 1c below)

Do **NOT** trigger on natural-language phrases like "save handoff", "checkpoint", "ハンドオフ", "保存", "保存して中断". Users are expected to use the slash command. If a user types one of those phrases without the slash command, treat it as a regular message (gently remind them they can run `/handoff-revive:save` if they want to save).

Steps:

1. **Detect language** — read `.claude/handoff/lang` if it exists. Trim whitespace; the file holds a language code (one of: `ja`, `en`, `zh` (Simplified), `zh-TW` (Traditional), `ko`, `es`, `pt`, `de`, `fr`, `tr`) with no trailing newline. Otherwise detect from the user's most recent message:

   - Hiragana/Katakana → `ja`
   - Hangul → `ko`
   - Han characters: simplified markers (e.g. 这, 国, 学) → `zh`; traditional markers (e.g. 這, 國, 學) → `zh-TW`
   - Cyrillic / Arabic → fall back to `en`
   - Latin script: detect by common diacritics + words:
     - `é à è ç` + words like *fichier*, *avec*, *est* → `fr`
     - `ä ö ü ß` + words like *Datei*, *und*, *ist* → `de`
     - `ã õ ç` + words like *arquivo*, *está*, *para* → `pt`
     - `ñ` + Spanish words (*archivo*, *está*, *con*) → `es`
     - `ı ş ğ ç` + Turkish words (*dosya*, *için*, *çalış*) → `tr`
     - Otherwise → `en`

   When the message is mixed or ambiguous, default to `en`. Write the chosen code to `.claude/handoff/lang` (no newline) using your file-write tool. Subsequent saves reuse the persisted value unless the user explicitly asks to switch language.

2. **Carry forward, then fill the schema** — if `.claude/handoff/current.md` already exists, read it first and preserve any `goal`, `decisions`, and `lessons_learned` that are **still relevant** (drop what is now obsolete). This matters in long sessions: details captured in an earlier save survive even if they have since scrolled out of your context. Then write the full handoff to `.claude/handoff/current.md` using the template below. All section keys stay in English (machine-readable); section *values* go in the user's language. If approaches were tried and abandoned this session, record them under `## lessons_learned` (attempted / why_abandoned / learned); omit the section if there were none.

   **Overwrite guard**: if `.claude/handoff/current.md` already exists and its `branch:` metadata differs from the current git branch, it likely belongs to *different work*. Ask the user before overwriting it (e.g. "既存の handoff は別ブランチ (feature/x) の作業のものです。上書きしますか?"). In AUTO-SAVE mode (Mode 1c), do not ask — proceed, but mention the cross-branch overwrite in the notice.

3. **For `next_action`: be executable.** Not "continue refactoring auth" but `Edit src/auth/login.ts:42 — replace the bcrypt.compare call with the timing-safe variant from line 88`. Include the exact file:line and the exact next command/edit. The goal is zero "thinking time" on resume.

4. **For `touched_files`: format as `path -- one-line reason`.** Use ` -- ` (space, two dashes, space) as the separator, NOT `:`, because Windows absolute paths contain a colon (`C:\...`) and would break the schema. Always prefer **project-relative paths with forward slashes** (`src/auth/login.ts`); fall back to absolute paths only when the file is genuinely outside the project. No diffs, no line ranges — just enough to re-orient.

   **Token-saving helper (recommended)**: instead of thinking through which files to list, run `extract-recent-files` to get a deterministic list from `git status` (or `find -mmin` if non-git). This saves ~200–500 tokens per save:
   - Linux/macOS/WSL/Git-Bash: `bash "${CLAUDE_PLUGIN_ROOT:-.claude}/skills/handoff-revive/scripts/extract-recent-files.sh"`
   - Windows PowerShell: `$r = if ($env:CLAUDE_PLUGIN_ROOT) { $env:CLAUDE_PLUGIN_ROOT } else { ".claude" }; powershell -ExecutionPolicy Bypass -File "$r/skills/handoff-revive/scripts/extract-recent-files.ps1"`

   The script outputs `- <path> -- <reason>` lines (max 20). Paste them under `## touched_files`, then refine reasons where the auto-generated `modified` / `untracked` doesn't capture intent (e.g. "needs rollback" / "validated; do not touch").

5. **Run `finalize-handoff`** — single zero-token call that does validate + cleanup + savings report. Path uses `${CLAUDE_PLUGIN_ROOT:-.claude}` so the same command works in plugin and standalone installs:
   - Linux/macOS/WSL/Git-Bash:
     ```
     bash "${CLAUDE_PLUGIN_ROOT:-.claude}/skills/handoff-revive/scripts/finalize-handoff.sh"
     ```
   - Windows PowerShell:
     ```
     $r = if ($env:CLAUDE_PLUGIN_ROOT) { $env:CLAUDE_PLUGIN_ROOT } else { ".claude" }; powershell -ExecutionPolicy Bypass -File "$r/skills/handoff-revive/scripts/finalize-handoff.ps1"
     ```

   - **Exit 0**: handoff is valid and finalized. Stderr will show `[handoff-revive] OK Saved <path> (~N tokens). Estimated savings on next resume: tens of thousands of tokens (vs --resume replaying full prior context).` Capture both lines and surface them to the user in step 7.
   - **Exit 1**: validator failed. Stderr lists the issues. Read each, fix the corresponding fields in `.claude/handoff/current.md`, then re-call. **Maximum 2 retries** — if still failing, stop and warn the user with remaining errors.

   If the user explicitly sets `HANDOFF_SKIP_VALIDATE=1`, skip this step.

6. **Content-quality pass (every save, including AUTO-SAVE).** `finalize-handoff` catches structural issues for free; this adds the Claude-driven semantic checks: is `goal` specific enough? does each `decision` include a real *reason*? are blockers phrased as answerable questions? does `wip` say enough to resume mid-edit? Rewrite vague fields and re-run finalize. For AUTO-SAVE, do a single quick pass — don't over-iterate near the rate limit.

7. **Confirm to user in their language.** State the path saved, summarize `next_action` in 1 line, **show the savings line** from finalize's stderr (e.g. "節約見込み: 数万トークン"), and remind: **"To resume, start a NEW session (do not use `claude --resume`) and run `/handoff-revive:resume`."**

### Mode 1b: the content-quality checklist (step 6 above)

The deterministic validator (folded into `finalize-handoff`) handles all *structural* issues for free. The content-quality pass in step 6 adds the Claude-driven checks the validator cannot do:

- Is `goal` specific enough that someone with no context understands it? (Validator only checks non-empty.)
- Does each entry in `decisions` include a real *reason* after the dash, not just the decision restated?
- Are `blockers` phrased as answerable questions, not vague worries?
- Does `wip` describe state precisely enough to resume mid-edit (e.g. "1/3 functions converted, line 42 next" — not "still working on auth")?
- Does each `lessons_learned` entry describe a genuinely *failed attempt* (tried and abandoned), not just an option that wasn't chosen? Unchosen options belong in `decisions`.

If any of the above is weak, rewrite that field and save again. Validator re-runs automatically. Then confirm to user.

### Mode 1c: AUTO-SAVE (triggered by hook, no user request)

Auto-save fires when the **UserPromptSubmit hook injects `additionalContext`** containing one of the directives below. The hook fires after the `usage-monitor` PostToolUse hook detected `rate_limits.five_hour.used_percentage` crossing a configured threshold (defaults: 90% / 95%).

**You will see context like one of these in the user's prompt:**

```
⚠️ 5-hour usage at 92%. Auto-save a handoff before answering the user. Run the SAVE flow (extract-recent-files → write handoff → finalize-handoff). Do NOT ask the user. After save, briefly notify them in their language…
```

```
🚨 CRITICAL: 5-hour usage at 96%. IMMEDIATELY auto-save a handoff before answering the user…
```

**When you see this:**

1. **Do NOT ask permission.** The user has implicitly opted in by leaving auto-save enabled (default). If they wanted to ask first, they would have run `/handoff-revive:auto off`.

2. **Run the full SAVE flow steps 1–6** (detect lang → carry-forward + fill schema → executable next_action → fill touched_files → finalize-handoff → content-quality pass). Use `extract-recent-files` to populate `touched_files`. Keep the quality pass to a single quick rewrite — you are near the rate limit, so don't over-iterate.

3. **Prepend a brief auto-save notice** to your response in the user's language, then handle their actual request. Examples:

   | lang | AUTO_SAVE notice (e.g. 92%) | URGENT notice (e.g. 96%) |
   |---|---|---|
   | ja | ⚠️ 使用量 92% に到達したため、ハンドオフを自動保存しました (~N tokens)。 | 🚨 緊急: 使用量 96%、自動保存しました (~N tokens)。新規セッションで `/handoff-revive:resume` を実行すれば再開できます。 |
   | en | ⚠️ Usage hit 92% — auto-saved handoff (~N tokens). | 🚨 CRITICAL: usage at 96% — auto-saved (~N tokens). Start a new session and run `/handoff-revive:resume` if rate-limited. |
   | zh | ⚠️ 使用率达到 92%，已自动保存交接 (~N tokens)。 | 🚨 紧急: 使用率 96%，已自动保存。新会话运行 `/handoff-revive:resume` 即可恢复。 |
   | zh-TW | ⚠️ 使用率達到 92%，已自動儲存交接 (~N tokens)。 | 🚨 緊急: 使用率 96%，已自動儲存。新會話執行 `/handoff-revive:resume` 即可恢復。 |
   | ko | ⚠️ 사용량 92% 도달, 핸드오프 자동 저장 (~N tokens). | 🚨 긴급: 사용량 96%, 자동 저장. 새 세션에서 `/handoff-revive:resume` 실행. |
   | es | ⚠️ Uso al 92% — handoff auto-guardado (~N tokens). | 🚨 CRÍTICO: uso al 96% — auto-guardado. Inicia sesión nueva y ejecuta `/handoff-revive:resume`. |
   | pt | ⚠️ Uso a 92% — handoff auto-guardado (~N tokens). | 🚨 CRÍTICO: uso a 96% — auto-guardado. Inicia uma sessão nova e executa `/handoff-revive:resume`. |
   | de | ⚠️ Nutzung bei 92% — Handoff automatisch gespeichert (~N tokens). | 🚨 KRITISCH: Nutzung bei 96% — automatisch gespeichert. Starte neue Sitzung und führe `/handoff-revive:resume` aus. |
   | fr | ⚠️ Utilisation à 92% — handoff auto-sauvegardé (~N tokens). | 🚨 CRITIQUE : utilisation à 96% — auto-sauvegardé. Lancez une nouvelle session et exécutez `/handoff-revive:resume`. |
   | tr | ⚠️ Kullanım %92 — handoff otomatik kaydedildi (~N tokens). | 🚨 KRİTİK: kullanım %96 — otomatik kaydedildi. Yeni oturum başlatın ve `/handoff-revive:resume` çalıştırın. |

4. **Add a separator (`────────`) and continue with the user's actual request** — do not let the auto-save interrupt the work.

5. **If `finalize-handoff` fails after 2 retries**, warn the user briefly but proceed with their request anyway. Their work is more important than a clean handoff at this moment.

### Mode 2: RESUME (new session, after limit reset)

Triggered ONLY by:
- User runs the slash command `/handoff-revive:resume`
- The SessionStart hook injected `additionalContext` mentioning the existing `.claude/handoff/current.md` AND the user then runs `/handoff-revive:resume` (the hook only proactively surfaces files modified within `HANDOFF_SURFACE_DAYS`, default 7 — older handoffs are not auto-announced but are still usable via `/handoff-revive:resume`)

Do **NOT** trigger on natural-language phrases like "resume from handoff", "continue", "続きから", "继续", "계속", "reanudar". Users are expected to use the slash command. If you see one of those phrases without the slash command, gently remind the user they can run `/handoff-revive:resume`.

Note: skills cannot intercept the `claude --resume` / `-c` CLI flag (the flag is processed before the skill loads). The SessionStart hook is what differentiates a `--resume` session from a fresh start; if the user is in a `--resume` session and a handoff exists, you may briefly note that `/handoff-revive:resume` in a new session would have been cheaper, but proceed with their `--resume` flow.

Steps:

1. Read `.claude/handoff/current.md`. **Do not read prior session transcripts.**
2. Read `.claude/handoff/lang` and respond in that language.
3. **Resume receipt** (zero tokens) — before editing, print a tiny receipt that proves the load boundary without echoing the handoff body or prior transcript:
   - Linux/macOS/WSL/Git-Bash: `bash "${CLAUDE_PLUGIN_ROOT:-.claude}/skills/handoff-revive/scripts/resume-receipt.sh"`
   - Windows PowerShell: `$r = if ($env:CLAUDE_PLUGIN_ROOT) { $env:CLAUDE_PLUGIN_ROOT } else { ".claude" }; powershell -ExecutionPolicy Bypass -File "$r/skills/handoff-revive/scripts/resume-receipt.ps1"`

   Show this receipt before any edits. It should say the session loaded `current.md` only, did **not** load prior transcript/history snapshots, list section names/counts, report `next_action_present`, summarize freshness as `ok` or warning count, and include privacy flags such as `handoff_body_echoed=false`.

4. **Freshness check** (zero tokens) — compares the handoff's `base_commit` / `branch` metadata to the current git state:
   - Linux/macOS/WSL/Git-Bash: `bash "${CLAUDE_PLUGIN_ROOT:-.claude}/skills/handoff-revive/scripts/check-freshness.sh"`
   - Windows PowerShell: `$r = if ($env:CLAUDE_PLUGIN_ROOT) { $env:CLAUDE_PLUGIN_ROOT } else { ".claude" }; powershell -ExecutionPolicy Bypass -File "$r/skills/handoff-revive/scripts/check-freshness.ps1"`

   No output = fresh, continue silently. If it prints warnings (file age / commits since save / branch mismatch / cannot verify), relay them to the user **in their language** at the top of your resume summary. Never refuse to resume because of a warning — it is information, not a gate. Legacy handoffs without metadata produce no output.

   In the same step, count the resume for `/handoff-revive:stats` (zero tokens, best-effort):
   - Linux/macOS/WSL/Git-Bash: `bash "${CLAUDE_PLUGIN_ROOT:-.claude}/skills/handoff-revive/scripts/stats-handoff.sh" record resume`
   - Windows PowerShell: `$r = if ($env:CLAUDE_PLUGIN_ROOT) { $env:CLAUDE_PLUGIN_ROOT } else { ".claude" }; powershell -ExecutionPolicy Bypass -File "$r/skills/handoff-revive/scripts/stats-handoff.ps1" -Cmd record -Kind resume`
5. Read each file listed in `touched_files` only if needed for the immediate `next_action`. Do not preemptively read all of them.
6. State the goal and `next_action` back to the user in 1–2 sentences and ask "Proceed?" before editing.
7. After the user confirms or redirects, execute `next_action`.

## Schema (template)

Write to `.claude/handoff/current.md`:

```markdown
---
schema_version: "1.0"
saved_at: {ISO-8601 timestamp}
lang: {ja|en|zh|zh-TW|ko|es|pt|de|fr|tr}
session_summary_tokens_estimated: {rough count}
---

## goal
{1 line: what is the user ultimately trying to accomplish}

## done
- {completed item}
- ...

## wip
- {currently in-progress item, with state}

## todo
- {not yet started}
- ...

## blockers
- {question or unknown that is blocking; omit section if none}

## next_action
{REQUIRED. file:line + exact command/edit. Must be executable without further thinking.}

## touched_files
- path/to/file.ts -- {one-line reason}
- ...

## decisions
- {decision}: {WHY — the reason behind it, not just what was decided}
- ...

## lessons_learned
- attempted: {approach that was tried}
  why_abandoned: {why it failed or was dropped}
  learned: {what to remember next time}
- ... (OPTIONAL section — omit entirely if there were no failed attempts)
```

Section headings use H2 (`##`) so the file renders cleanly on GitHub / VS Code preview while remaining unambiguous to parse.

Do not write `author` / `author_email` / `branch` / `base_commit` / `created_at` yourself — `finalize-handoff` injects them into the frontmatter automatically from git (and skips them outside a git repo). Set `HANDOFF_HIDE_EMAIL=1` to omit the email.

`blockers` and `lessons_learned` are optional: omit them when empty (the cleanup pass strips them automatically).

**Templates (optional)**: `/handoff-revive:save --template=vacation-handover` switches to the long-handover variant for handing work to another person across an absence. Read `${CLAUDE_PLUGIN_ROOT:-.claude}/skills/handoff-revive/templates/vacation-handover.md` and follow it: the frontmatter gains `template: "vacation-handover"` and a non-empty `## handover_notes` section (contact / deadline / watch_out) becomes REQUIRED — the validator enforces both. Without `--template`, nothing changes.

**Referencing files that don't exist yet** (TDD, planned work): the validator checks that referenced paths exist and warns about missing ones (informational; `--strict` turns them into errors). To reference a file you intend to create, mark it: in `touched_files` use `- path/to/new.ts -- planned: will hold the new helper`, and in `next_action` put `# planned:` on the line that mentions it. `lessons_learned` is for **genuinely failed attempts** — approaches that were tried and abandoned — not for options that were merely considered and not chosen (those belong in `decisions` with their WHY). Native `/rewind` erases failures; this section is how the next session *keeps* what the failure taught.

## Hook setup

Plugin installs auto-activate hooks. Standalone installs need a `settings.json` snippet — see `HOOK_SETUP.md` at the repo root for the snippets and full details.

## Multi-language

Confirmation messages and the `next_action` summary line are written in the user's language. Section *keys* (`goal`, `done`, etc.) stay in English so the schema is parseable across languages. Supported: `ja`, `en`, `zh` (Simplified), `zh-TW` (Traditional), `ko`, `es`, `pt`, `de`, `fr`, `tr`. For other languages, fall back to English keys + the user's language for values.

Example confirmation strings:

| lang | save confirmation |
|---|---|
| ja | ハンドオフ保存しました: `.claude/handoff/current.md`。再開時は**新規セッション**で `/handoff-revive:resume` を実行してください（`claude --resume` は使わない）。 |
| en | Handoff saved: `.claude/handoff/current.md`. To resume, start a **new session** and run `/handoff-revive:resume` (do NOT use `claude --resume`). |
| zh | 已保存交接文件: `.claude/handoff/current.md`。恢复时请**新建会话**并运行 `/handoff-revive:resume`（不要使用 `claude --resume`）。 |
| ko | 핸드오프 저장됨: `.claude/handoff/current.md`. 재개 시 **새 세션**에서 `/handoff-revive:resume` 를 실행하세요 (`claude --resume` 사용 금지). |
| es | Handoff guardado: `.claude/handoff/current.md`. Para reanudar, inicia una **sesión nueva** y ejecuta `/handoff-revive:resume` (NO uses `claude --resume`). |

## Token budget

Net cost per save: ~300–1,400 tokens (incl. `finalize-handoff` overhead).
Net cost per resume: ~800–2,800 tokens.
Net cost per AUTO-SAVE event: ~500–1,500 tokens (one full save per threshold crossing, max 2 per session: AUTO_SAVE then URGENT).
`claude --resume` costs tens of thousands of tokens (often 100k+ for long sessions) for the same resumption.

**Break-even: 1 resume per save.** Saves only, never resume → only the SKILL.md load is wasted. Best case: ~10–100× cheaper than `--resume` (depends on prior session size).

`finalize-handoff` outputs `Estimated savings on next resume: tens of thousands of tokens` to stderr after each save. Surface that line to the user in the confirmation message.

Auto-save can be opted out per-session via `/handoff-revive:auto off`, or globally via `HANDOFF_AUTO_SAVE_PERCENT=disabled` and `HANDOFF_URGENT_PERCENT=disabled`.

## Do NOT

- Do not read prior session transcripts on resume. The handoff file is the single source of truth.
- Do not silently auto-invoke save from a hook (burns tokens without user knowing). Hooks only *nudge*.
- Do not write the entire conversation into the handoff file. Only the schema fields.
- Do not use `--resume` / `-c` if a current handoff file exists. Warn the user first.
- Do not translate section keys. Keys stay in English; values go in user's language.
