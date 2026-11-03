---
name: agent-self-repo
description: "Use when publishing your own skills, soul and config. Pushes them to your own repo."
version: 1.0.0
author: iCLONE / CLONE FRAME
license: MIT
platforms: [macos, linux]
metadata:
  hermes:
    tags: [Git, GitHub, Security, Sterilization, Self-Repo, iNFT]
    related_skills: [iclone-os]
---

# Your own repo — built clean, published safe

When the user asks for "a repo of the agent" (of YOU — your skills, soul,
docs, config *templates*), build it on THEIR machine and publish it with the
sterilization doctrine below. One mistake here leaks keys forever: history
is permanent even after deletion.

## 1. What goes IN (and what NEVER does)

IN: your skills (`~/.hermes/skills/...` that you authored/curated), soul/
persona docs, README (what you are, how to run), config **templates** with
placeholders (`DEEPSEEK_API_KEY=__SET_ME__`), install notes.
NEVER — not even in one commit that you later delete:
`.env` and any real key/token/secret · `auth.json` · OS keychain exports ·
`~/.hermes/config.yaml` AS-IS (it can hold keys — template it) ·
chat/session logs · wallet files/private keys · `it.json` · anything under
`~/.iclone-os/` state.

## 2. Build (on the user's machine)

    DEST="$HOME/Desktop/<name>-agent"   # or where the user asks
    mkdir -p "$DEST" && cd "$DEST"
    git init -b main
    # .gitignore FIRST, before any add:
    printf '%s\n' '.env' '.env.*' '*.key' '*.pem' 'auth.json' \
      'config.yaml' '*.sqlite' 'node_modules/' '.DS_Store' > .gitignore
    # copy content, then TEMPLATE the configs (strip values):
    #   sed 's/\(api_key:\).*/\1 "__SET_ME__"/' etc.

## 3. Sterilize BEFORE the first commit (mandatory gate)

    # secrets sweep — all must return NOTHING:
    grep -rInE '(sk-[A-Za-z0-9]{20,}|ghp_[A-Za-z0-9]{20,}|gho_[A-Za-z0-9]{20,}|AKIA[0-9A-Z]{16}|xox[bap]-|-----BEGIN (RSA|EC|OPENSSH) PRIVATE KEY)' .
    grep -rInE '(api[_-]?key|secret|token|password)[\"'\'' ]*[:=][\"'\'' ]*[A-Za-z0-9_\-]{16,}' . | grep -v __SET_ME__
    # 0x private keys (64 hex) and mnemonic-looking word lists:
    grep -rInE '\b[0-9a-fA-F]{64}\b' . | grep -vi hash
    # if gitleaks exists, run it too:  gitleaks detect --no-git -s . || true

If ANY hit: fix, re-run, only then `git add -A && git commit`.

## 4. Publish (private by default)

    gh auth status || { echo "ask the owner to authenticate gh"; exit 1; }
    gh repo create <owner>/<name>-agent --private --source . --push

- **Private by default.** Only make it public if the user says so EXPLICITLY
  — and then re-run the sweep in §3 plus `git log -p | grep -cE '(sk-|ghp_)'`
  over the FULL history (history travels with the repo).
- Never commit with `-m` containing backticks or `$` (shell expansion).
- Add a LICENSE only if the user chooses one; default none.

## 5. If a secret ever lands

Stop. Tell the user immediately: the key must be ROTATED (revoked at the
provider) — history rewriting (`git filter-repo`) comes second and does not
un-leak a pushed secret. Never quietly amend and move on.
