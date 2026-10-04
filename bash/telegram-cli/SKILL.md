---
name: telegram-cli
description: |
  Python CLI wrapper for Telegram interaction using Telethon (MTProto protocol).
  Use when the user wants to: (1) send messages, (2) read messages from chats/channels/groups,
  (3) list chats, (4) download files, or (5) search messages.
  On first use, guide the user through authentication (API ID/Hash → phone → code → 2FA password).
  Store session and config in ~/.libragent/telegram_config.json.
  Subsequent requests use the stored session without re-authentication.
  Triggers on requests like: "텔레그램 메시지 보내줘", "텔레그램 확인", "send telegram", "텔레그램 채널 확인", "텔레그램 파일 다운로드".
---

# Telegram CLI Skill

Enables the agent to interact with Telegram on behalf of the user via Telethon (MTProto protocol).

## Path Conventions & Aliased Locations

LibrAgent organizes skill resources using canonical `@` aliases across all platforms (Windows, Linux, macOS):
- **Skill files & documentation**: Use `@system-skills/telegram-cli/SKILL.md` or `@system-skills/telegram-cli/references/cli-reference.md` with workspace tools (`workspace__readFile`, `workspace__listDirectory`, etc.).
- **Shell execution (`workspace__runInPersistentShell`)**: When invoking python scripts, reference `<skill-base-dir>/scripts/...` using the skill's Base Directory (either the canonical alias `@system-skills/telegram-cli` or the concrete Base Directory injected in your system prompt reference block).
- On Linux/macOS, use `python3` if `python` is unavailable.
- Always quote paths to handle spaces properly: `"<skill-base-dir>/scripts/check_config.py"`.

## ⚠️ Security Rules (Mandatory)

- **NEVER** ask for 2FA passwords, verification codes, or other transient secrets in chat.
- **NEVER** display or repeat the contents of `~/.libragent/telegram_config.json`.
- **NEVER pass `--password-value` or `--code-value` as command-line arguments**. Command-line arguments leak into system process tables (`ps aux`, `Get-Process`), shell histories, and execution logs.
- Collect transient secrets (verification codes, 2FA passwords) **exclusively** through `requireUserInput=true` with `--code-stdin` / `--password-stdin` via `workspace__runInPersistentShell`.
- If the user accidentally sends a password or code in chat:
  1. Acknowledge receipt without echoing or repeating the secret text.
  2. Use `--password-env` with an environment variable or run the setup tool with stdin.
  3. NEVER echo the secret in output.
- **ALWAYS** use `setup.py` to persist credentials and session.

---

## Overview

Telegram integration involves these steps:

1. **Detect environment & config** — verify Python and run `check_config.py` to check if account is configured
2. **Setup (first time only)** — gather API ID/Hash, phone number, then run `setup.py` with hidden prompts for code/password
3. **Dispatch action** — classify the user's request and call `telegram_cli.py` with the right action
4. **Present results** — format and summarize the output for the user

---

## Dependencies & Environment Setup

### 1. Python Environment Check
Before running any script, ensure Python 3.9+ is available in the shell:
- **Check version**:
  ```bash
  python --version || python3 --version
  ```
- **If Python is not installed**:
  - **Windows**:
    ```powershell
    winget install Python.Python.3.12 --silent --accept-package-agreements --accept-source-agreements
    ```
    (Or via Miniconda: `winget install Anaconda.Miniconda3 --silent --accept-package-agreements --accept-source-agreements`)
  - **macOS**: `brew install python`
  - **Linux**: `sudo apt update && sudo apt install -y python3 python3-pip`
  - You may also recommend the **setup-wizard** skill to guide automated environment diagnostics.

### 2. Telethon Installation
Telethon MTProto client library is required:
```bash
# Windows
python -m pip install telethon

# Linux / macOS
python3 -m pip install telethon
```

## References

These reference files are located in the skill directory:
- [cli-reference.md](references/cli-reference.md) (or `@system-skills/telegram-cli/references/cli-reference.md`) — CLI commands, options, outputs, and errors reference

---

## Step 1: Detect Config

Always start by checking if the account is configured:

```bash
python "<skill-base-dir>/scripts/check_config.py"
```
*(On Linux/macOS, use `python3` if `python` is not aliased)*

- Exit code `0` with `"status": "ok"` → configured and authorized, proceed to Step 3
- Exit code `1` → missing config/session or not authorized (`missing`, `missing_session`, `unauthorized`, `auth_restart_needed`), go to Step 2
- Exit code `2` → config exists but is incomplete/corrupt, go to Step 2 to reconfigure/overwrite it
- `"status": "auth_restart_needed"` → delete `~/.libragent/telegram_session.session` and restart from Step A (`send_code`)

---

## Step 2: Account Setup (First Time or Reset)

Do **not** run `python "<skill-base-dir>/scripts/setup.py"` bare without arguments inside LibrAgent.

### 2.1: Guide API ID/Hash Acquisition

If the user doesn't have API credentials, guide them to:

1. Visit https://my.telegram.org
2. Log in with their phone number
3. Click "API development tools"
4. Fill in App title and Short name (can be anything)
5. Copy the `api_id` and `api_hash`

### 2.2: Two-Step Authentication Flow

#### 1. Collect API credentials in chat

Ask the user for:
- `api_id` (integer)
- `api_hash` (string)
- `phone` (international format, e.g., `+821012345678`)

#### 2. Interactive setup commands

**Step A — Send verification code:**

```bash
# Windows (PowerShell)
python "<skill-base-dir>/scripts/setup.py" --api-id 12345678 --api-hash "abcdef0123456789..." --phone "+821012345678" --action send_code

# Linux / macOS (Bash)
python3 "<skill-base-dir>/scripts/setup.py" --api-id 12345678 --api-hash "abcdef0123456789..." --phone "+821012345678" --action send_code
```

This outputs a JSON confirmation that the code was sent. On `AuthRestartError`, the script clears the partial session and retries once. If it still fails, you get `"status": "auth_restart_needed"` — run `send_code` again.

**Step B — Sign in with verification code:**

Execute `workspace__runInPersistentShell` tool call with:
- `command`: `python "<skill-base-dir>/scripts/setup.py" --action sign_in --code-stdin`
- `requireUserInput`: `true`
- `inputType`: `"text"`
- `inputPrompt`: `"텔레그램 인증 코드를 입력하세요:"`

```json
{
  "command": "python \"<skill-base-dir>/scripts/setup.py\" --action sign_in --code-stdin",
  "requireUserInput": true,
  "inputType": "text",
  "inputPrompt": "텔레그램 인증 코드를 입력하세요:"
}
```

LibrAgent auto-detects `--code-stdin` and pipes the UI input into Python stdin (`stdinDelivery=child`).

> [!NOTE]
> Do not use `Read-Host` inside LibrAgent persistent PowerShell. Those sessions run `-NonInteractive`, so `Read-Host` raises `PSInvalidOperationException`. The `--code-stdin` / `--password-stdin` path is the supported contract across Windows, macOS, and Linux.

**Step C — Handle 2FA (if Step B returns `"password_needed"`):**

Execute `workspace__runInPersistentShell` tool call with:
- `command`: `python "<skill-base-dir>/scripts/setup.py" --action sign_in --password-stdin`
- `requireUserInput`: `true`
- `inputType`: `"password"`
- `inputPrompt`: `"텔레그램 2FA 비밀번호를 입력하세요:"`

```json
{
  "command": "python \"<skill-base-dir>/scripts/setup.py\" --action sign_in --password-stdin",
  "requireUserInput": true,
  "inputType": "password",
  "inputPrompt": "텔레그램 2FA 비밀번호를 입력하세요:"
}
```

After successful setup, re-run `check_config.py` to confirm `"status": "ok"`, then proceed to Step 3.

---

## Step 3: Dispatch Action

Classify the user's request into one of six actions and call `telegram_cli.py`.

### 📌 Saved Messages (나와의 채팅 / 내게 쓰기)

Telegram provides personal cloud storage via "Saved Messages".
To send or retrieve messages from your Saved Messages:
- Use `--chat me` (or `@me`, `saved`, `@saved`, `saved messages`, `saved_messages`, `저장한 메시지`, `나와의 채팅`, `내게 쓰기`).
- The CLI automatically resolves `me` directly to your own Telegram account.
- **Example — Send to Saved Messages:**
  ```bash
  python "<skill-base-dir>/scripts/telegram_cli.py" --action send_message --chat me --message "메모 내용"
  ```
- **Example — Read from Saved Messages:**
  ```bash
  python "<skill-base-dir>/scripts/telegram_cli.py" --action get_messages --chat me --limit 20
  ```

### 🔢 Numeric Chat / User IDs & Username Resolution
- **Numeric User ID** (e.g., `5097924805`): Pass directly as `--chat 5097924805`. The CLI automatically detects numeric strings and resolves them as integer entity IDs.
- **Numeric Channel / Supergroup ID** (e.g., `-1001234567890`): Pass directly as `--chat -1001234567890`.
- **Username**: Use `@channel_name` or `channel_name`.
- **Unknown Chat Name**: If the user only provides a human-readable title (e.g. "가족방" or "팀 채널"), run `list_chats` first to find the exact numeric ID or username.

### Output handling (recommended for message/search actions)

On Windows, large JSON payloads can break in PowerShell (`cp949`). Prefer saving results to a UTF-8 file:

```powershell
python "<skill-base-dir>/scripts/telegram_cli.py" --action get_messages `
  --chat "<chat_id_or_username>" `
  --limit 50 `
  --output "<workspace>/telegram_messages.json"
```

When `--output` is set, stdout prints a compact summary (`status`, `output` path, `count`). Read the file for full message bodies.

All CLI output uses UTF-8 (`ensure_ascii=False`). Errors go to stderr as UTF-8 JSON.

### Output handling (Windows 필수)
On Windows, always set these before invoking any CLI command. Use UTF-8 **without BOM** — `[System.Text.Encoding]::UTF8` prepends U+FEFF to native stdin and will corrupt `--code-stdin` / `--password-stdin` secrets:

```powershell
$utf8 = New-Object System.Text.UTF8Encoding $false
[Console]::InputEncoding = [Console]::OutputEncoding = $OutputEncoding = $utf8
$env:PYTHONUTF8 = "1"
```

LibrAgent persistent shells already apply this encoding and `PYTHONUTF8=1`. `setup.py` also strips any leading UTF-8 BOM from stdin secrets as defense in depth.

### Input encoding & PowerShell escaping (Windows / Unicode / Literal $ workaround)

On Windows, passing Unicode characters (like Korean) as command-line arguments can cause character corruption (mojibake) due to PowerShell's default encoding (`cp949`).

To bypass this bottleneck, it is highly **recommended** to write the message or query to a UTF-8 file and use `--message-file` or `--query-file` instead of `--message` or `--query`.

> [!WARNING]
> **PowerShell Here-String Interpolation Danger**:
> If you use double-quoted Here-Strings (`@" ... "@`) in PowerShell, characters starting with `$` are treated as variables. For example, `$3,000` will evaluate `$3` as an empty variable, resulting in `,000`, and `$1.5B` will evaluate `$1` as empty, resulting in `.5B`.
> 
> **How to avoid this:**
> 1. **(Best/Recommended)**: Use the agent's `writeFile` (or `workspace__writeFile`) tool to directly create and write the message content to a file (e.g., `<workspace>/tg_message.txt`) as UTF-8. This completely bypasses any PowerShell escaping or variable interpolation issues.
> 2. **(Alternative - Single Quotes)**: If you must write the file via PowerShell, use single-quoted Here-Strings (`@' ... '@`) which disable variable interpolation.

#### Send Message (Windows Recommended via writeFile)

1. Use the `writeFile` (or `workspace__writeFile`) tool to save your message (e.g. including `$3,000` or Korean text) directly to `<workspace>/tg_message.txt` in UTF-8 format.
2. Call the CLI pointing to the file:

```powershell
python "<skill-base-dir>/scripts/telegram_cli.py" --action send_message `
  --chat "<chat_id_or_username>" `
  --message-file "<workspace>/tg_message.txt"
```

3. Clean up the temporary file afterwards:
```powershell
Remove-Item -Path "<workspace>/tg_message.txt" -ErrorAction SilentlyContinue
```

#### Search Messages (Windows Recommended via writeFile)

1. Use the `writeFile` (or `workspace__writeFile`) tool to save your query directly to `<workspace>/tg_query.txt` in UTF-8 format.
2. Call the CLI pointing to the file:

```powershell
python "<skill-base-dir>/scripts/telegram_cli.py" --action search_messages `
  --query-file "<workspace>/tg_query.txt" `
  --output "<workspace>/telegram_search.json"
```

3. Clean up the temporary file afterwards:
```powershell
Remove-Item -Path "<workspace>/tg_query.txt" -ErrorAction SilentlyContinue
```

### Dispatch CLI Actions

Classify the user's request into one of the actions (`send_message`, `get_messages`, `list_chats`, `search_messages`, `download_file`, `get_chat_info`) and execute the CLI. For a detailed reference of CLI parameters, JSON output schemas, and pagination strategies, see the [cli-reference.md](references/cli-reference.md) guide.

---

## Step 4: Present Results

- **Message list**: Show as a numbered table — `#  From  Date  Content`
- **Send confirmation**: Confirm action completed with brief summary
- **Chat list**: Show as a table — `#  Name  Type  Members/ID  Last Activity`
- **Search results**: Same as message list, with match count
- **Errors**: See Error Handling in [cli-reference.md](references/cli-reference.md)

Always provide the next concrete step, never just report the error.

---

## Output Format Guidelines

For message listings, use this format:

```
📨 텔레그램 메시지 (chat: @example_channel)

#  날짜              내용
1  06/01 14:23      오늘 회의는 14시에 시작됩니다.
2  06/01 13:45      [이미지]
3  06/01 12:00      새로운 기능 배포 완료

더 보려면: "다음 20개 보여줘"
```

For send confirmation:

```
✅ 텔레그램 메시지 발송 완료
  받는 곳: @example_channel
  발송 시각: 2026-06-01 14:30
```

For chat listings:

```
💬 텔레그램 채팅 목록 (총 25개)

#  이름                    유형       마지막 활동
1  ● LibrAgent Dev         채널       10분 전
2    GitHub Notifications  채널       1시간 전
3  ● 프로젝트 A            그룹(42)   3시간 전
4    김철수                개인       어제

● = 읽지 않음
```
