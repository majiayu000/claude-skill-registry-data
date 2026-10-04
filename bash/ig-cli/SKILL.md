---
name: ig-cli
description: |
  Python CLI wrapper for Instagram interaction using instagrapi.
  Use when the user wants to: (1) post photos/reels with captions, (2) reply to comments,
  (3) view feed/posts, (4) like/unlike posts, (5) follow/unfollow users, (6) view profile info.
  On first use, guide the user through credential setup (username + password via hidden prompt).
  Store config in ~/.libragent/ig_config.json and session settings in ~/.libragent/ig_session.json.
  Subsequent requests use the stored session without re-authentication.
  Triggers on requests like: "인스타 올리줘", "인스타그램 포스트", "ig post", "instagram post", "댓글 달아줘".
---

# Instagram CLI Skill

Enables the agent to interact with Instagram on behalf of the user via the instagrapi library.

## Path conventions

Paths in this skill are relative to the directory containing this `SKILL.md`, not to the workspace root or the shell's current `./`.

- Scripts in this skill use paths like `scripts/...`
- When a command below says `python scripts/...`, resolve that script path against the skill's absolute Base Directory.
- In command examples below, replace `<skill-base-dir>` with the skill's actual absolute Base Directory.

## ⚠️ Security Rules (Mandatory)

- **NEVER** ask for password in plain chat.
- **NEVER** display or repeat the contents of `~/.libragent/ig_config.json` or `~/.libragent/ig_session.json`.
- **NEVER** write the password to disk (no `ig_password.tmp` or similar). Session refresh requires re-running setup.
- Collect password exclusively through interactive hidden shell prompts (`requireUserInput=true`, `inputType=password`).
- **ALWAYS** use `setup.py` to persist config and session. Files are created with `0o600` permissions.

---

## Overview

Instagram integration involves these steps:

1. **Detect config** — run `check_config.py` to check if account is configured.
2. **Setup (first time only)** — configure via credentials (username + password).
3. **Dispatch action** — call `ig_cli.py` with the right action.
4. **Present results** — format and summarize the output for the user.

---

## Prerequisites

Ensure instagrapi is installed:

```bash
python -m pip install -r "<skill-base-dir>/requirements.txt"
```

---

## Step 1: Detect Config

Always start by checking if the account is configured:

```bash
python "<skill-base-dir>/scripts/check_config.py"
```

- Exit code `0` → configured, proceed to Step 3.
- Exit code `1` or `2` → not configured/corrupt, proceed to Step 2.

---

## Step 2: Account Setup (First Time or Reset)

Execute `workspace__runInPersistentShell` (or `workspace__runInPersistentPowerShell`) with:

- `requireUserInput=true`
- `inputType=password`
- `inputPrompt=Instagram 비밀번호를 입력하세요:`
- Command (replace username with user-supplied one):
  ```bash
  python "<skill-base-dir>/scripts/setup.py" \
    --username "your_instagram_username" \
    --password-stdin
  ```

### Setup output contract

`setup.py` prints a JSON object to stdout on success; errors go to stderr as JSON:

- Exit code `0` — session settings and config were saved (`0o600`).
- Exit code `1` — authentication failed; partial files are removed.
- Exit code `3` — missing required input (password).

On success, `status` is always `"ok"`.

If Instagram requires 2FA, setup returns `error_type: two_factor_required`. Ask the user how they want to proceed (temporary 2FA disable, alternate auth), then re-run setup — do not store codes or passwords in files.

---

## Step 3: Dispatch Action

Call `ig_cli.py` to execute Instagram actions. Success JSON is on stdout; errors are JSON on stderr.

### Action: `post_photo` — Post a photo with caption

```bash
python "<skill-base-dir>/scripts/ig_cli.py" --action post_photo \
  --file "/path/to/image.jpg" \
  --caption "Caption text here" \
  [--tags "tag1,tag2,tag3"]
```

**Notes:**
- `--tags` appends hashtags to the caption automatically.
- Image format: JPG/PNG (max ~1080px width recommended).

### Action: `post_reel` — Post a Reel (short video)

```bash
python "<skill-base-dir>/scripts/ig_cli.py" --action post_reel \
  --file "/path/to/video.mp4" \
  --caption "Reel caption" \
  [--thumbnail "/path/to/thumb.jpg"] \
  [--tags "tag1,tag2"]
```

### Action: `reply_comment` — Reply to a comment on a post

```bash
python "<skill-base-dir>/scripts/ig_cli.py" --action reply_comment \
  --post-id "18234567890123456" \
  --parent-comment-id "17987654321098765" \
  --message "Reply message here"
```

Use `get_comments` to discover IDs.

### Action: `add_comment` — Add a comment to a post

```bash
python "<skill-base-dir>/scripts/ig_cli.py" --action add_comment \
  --post-id "18234567890123456" \
  --message "Comment text here"
```

### Action: `like_post` / `unlike_post`

```bash
python "<skill-base-dir>/scripts/ig_cli.py" --action like_post --post-id "18234567890123456"
python "<skill-base-dir>/scripts/ig_cli.py" --action unlike_post --post-id "18234567890123456"
```

### Action: `follow_user` / `unfollow_user`

```bash
python "<skill-base-dir>/scripts/ig_cli.py" --action follow_user --username "target_username"
python "<skill-base-dir>/scripts/ig_cli.py" --action unfollow_user --username "target_username"
```

### Action: `get_feed` — View home/timeline posts (falls back to your recent medias)

```bash
python "<skill-base-dir>/scripts/ig_cli.py" --action get_feed [--limit 10]
```

### Action: `get_user_posts` — View a user's posts

```bash
python "<skill-base-dir>/scripts/ig_cli.py" --action get_user_posts \
  --username "target_username" \
  [--limit 10]
```

### Action: `get_comments` — Get comments on a post

```bash
python "<skill-base-dir>/scripts/ig_cli.py" --action get_comments \
  --post-id "18234567890123456"
```

### Action: `get_profile` — View your own profile info

```bash
python "<skill-base-dir>/scripts/ig_cli.py" --action get_profile
```

### Action: `get_user_info` — View another user's profile

```bash
python "<skill-base-dir>/scripts/ig_cli.py" --action get_user_info \
  --username "target_username"
```

---

## Error Handling

- **Session expired / Login required**: Re-run `setup.py`. Password is never cached on disk.
- **Rate limited**: Wait 30–60 seconds and retry.
- **Media upload failed**: Check file path, format, and size.
- **Invalid post ID**: Prefer numeric media primary keys from `get_feed` / `get_user_posts` / `get_comments`.

---

## Common Patterns

### Posting an image

```bash
python "<skill-base-dir>/scripts/ig_cli.py" --action post_photo \
  --file "/path/to/image.png" \
  --caption "golden hour" \
  --tags "seoul,goldenhour"
```

### Replying to a comment

```bash
python "<skill-base-dir>/scripts/ig_cli.py" --action get_comments \
  --post-id "18234567890123456"

python "<skill-base-dir>/scripts/ig_cli.py" --action reply_comment \
  --post-id "18234567890123456" \
  --parent-comment-id "17987654321098765" \
  --message "Thanks!"
```

---

## Platform notes (Windows)

### Encoding

On Windows, prefer UTF-8 without BOM for any files written for captions. LibrAgent persistent shells already set encoding + `PYTHONUTF8=1`. `setup.py` strips a leading UTF-8 BOM from `--password-stdin` secrets.

Do not put the Instagram password in PowerShell command lines or history — always use `requireUserInput=true` + `--password-stdin`.

### Media paths

`--file` / `--thumbnail` must be real files outside `~/.libragent/` (config directory access is denied). Max media size is 100 MiB.

### Timeouts

Network actions time out after **60 seconds** (exit code `2`). On timeout or `LoginRequired`, re-run `setup.py` — passwords are never cached on disk.
