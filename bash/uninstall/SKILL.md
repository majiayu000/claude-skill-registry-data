---
name: uninstall
description: "Uninstall the flagrare plugin and remove the marketplace. Use when the user says 'uninstall flagrare', 'remove flagrare', 'disable flagrare skills', or 'remove flagrare-skills'."
---

# Uninstall Flagrare

Remove the flagrare plugin and its marketplace registration.

## When to Use

- User says "uninstall flagrare", "remove flagrare", "remove flagrare-skills"
- User wants to disable all flagrare skills

## Procedure

Run the uninstall script:

```bash
bash "${CLAUDE_PLUGIN_ROOT}/../../uninstall.sh"
```

If the script is not found at that path (e.g. running from a remote install), run these commands directly:

```bash
claude plugin disable "flagrare@flagrare-skills"
claude plugin marketplace remove flagrare-skills
```

After running, tell the user:

> Flagrare skills removed. Run `/reload-plugins` or restart Claude Code to apply.
>
> To reinstall later:
> ```bash
> bash <(curl -sL https://raw.githubusercontent.com/Flagrare/flagrare-skills/main/install.sh)
> ```
