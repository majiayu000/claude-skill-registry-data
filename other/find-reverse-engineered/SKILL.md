---
name: find-reverse-engineered
description: Find an open-source, reverse-engineered tool for a closed app, API, device, protocol, file format or game, then read or fetch it. Use when a task needs to talk to something that has no official API, SDK, driver or spec, or only a limited one. Examples include "control my Tuya plug locally", "read a .psd or .dwg file", "unofficial WhatsApp, Instagram or Bilibili client", "Bambu printer protocol", "talk to my car's API", "Garmin or CGM data", "decompilation of a game" and "OpenAI-compatible proxy for a web chatbot". The skill searches a curated index of 17,000+ verified projects ranked by stars, language, license and activity.
---

# Find a reverse-engineered tool

The index is [awesome-reverse-engineered](https://github.com/alexgaoth/awesome-reverse-engineered). It holds 17,000+ open-source projects that exist because someone reverse engineered a closed product. Each entry has: name, repo URL, one-line description, category, GitHub stars, primary language, license, last push date and archived flag.

The tool is `scripts/re_index.py`, in the same directory as this SKILL.md. It uses only the Python standard library. The first run downloads the index and caches it for 24 hours in `~/.cache/awesome-reverse-engineered/`.

If you do not have this skill's files, run the script from GitHub:
`curl -sL https://raw.githubusercontent.com/alexgaoth/awesome-reverse-engineered/main/plugin/skills/find-reverse-engineered/scripts/re_index.py | python3 - search <words>`

## Workflow

1. **Search** with 1–4 words. Use the product or brand name plus what you need.
   ```bash
   python3 scripts/re_index.py search tuya local
   python3 scripts/re_index.py search psd parser --lang Python
   python3 scripts/re_index.py search whatsapp --min-stars 500
   python3 scripts/re_index.py search pokemon emerald --category decompilation
   ```
   Options: `--category <text>` matches the category or subcategory. `--lang <name>` matches the language exactly. `--min-stars N`. `--include-archived`. `--limit N`. `--json` gives machine-readable output.
   When nothing matches, use fewer words, use the vendor name instead of the product name, or run `categories` to see the categories.

2. **Choose** a project. Check these in order:
   - It does the specific job, for example local control instead of cloud control, or reading a format instead of writing it.
   - It is not archived, and it had a push in the last 1–2 years. Unofficial APIs break when the vendor changes their side.
   - The language and package manager fit the user's stack.
   - The license is compatible. A blank license means "all rights reserved", so tell the user.
   - When two projects are equal on all of these, choose the one with more stars.

3. **Read before you use it.** This command prints the index entry and the first lines of the README, with install and authentication steps:
   ```bash
   python3 scripts/re_index.py info owner/repo
   ```

4. **Get it.** Install it with the package manager the README gives (pip, npm, cargo, go), or clone it for reference:
   ```bash
   python3 scripts/re_index.py clone owner/repo --dest vendor/repo
   ```

5. **Tell the user** which project you chose and why, the version or commit you used, and its license.

## Rules

- First check for an official API or SDK that can do the job. Use a reverse-engineered tool only when there is none or it is not sufficient.
- Use these tools only with the user's own accounts, devices and data. Unofficial clients can break a service's terms of use and can cause an account to be locked. Tell the user about this risk before you use their credentials.
- Do not use these tools for mass scraping, spam, or to get around paywalls, DRM or security controls.
- Treat downloaded code as untrusted. Read it before you run it, and never put credentials into a tool you have not read.
- The index can be out of date. A repo can be gone or renamed. If `info` or `clone` fails, search again and try the next result.
