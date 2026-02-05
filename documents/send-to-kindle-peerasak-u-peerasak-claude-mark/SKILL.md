---
name: send-to-kindle
description: Sends EPUB and PDF files to Kindle device via email using Apple Mail.app on macOS. Use when the user wants to send documents to their Kindle, transfer reading materials, or email files to their Kindle address.
---

# Send to Kindle

Sends documents to Kindle via email using the `@peerasak-u/send-to-kindle` CLI.

## Quick Reference

### Run commands

```bash
bunx @peerasak-u/send-to-kindle [options]
```

| Option | Required | Description |
|--------|----------|-------------|
| `--to <email>` | Yes | Recipient Kindle email address |
| `--from <email>` | Yes | Sender email address (approved in Amazon) |
| `--file <path>` | Yes | Path to file to attach (EPUB, PDF, etc.) |
| `--subject <text>` | No | Email subject (default: "Daily News") |
| `--message <text>` | No | Email body message |
| `--help` | No | Show help message |

**Full command details**: See [references/COMMANDS.md](references/COMMANDS.md)

## Common Workflows

### Send an EPUB to Kindle

```bash
bunx @peerasak-u/send-to-kindle \
  --to=your-kindle@kindle.com \
  --from=your-email@gmail.com \
  --file=/path/to/book.epub
```

### Send with custom subject and message

```bash
bunx @peerasak-u/send-to-kindle \
  --to=your-kindle@kindle.com \
  --from=your-email@gmail.com \
  --file=/path/to/document.pdf \
  --subject="Monthly Report" \
  --message="Enjoy reading!"
```

## Requirements

- macOS (uses Apple Mail.app via JXA)
- Kindle email address (configured in Amazon account)
- Approved sender email in Amazon's "Approved Personal Document E-mail List"
- Apple Mail.app configured and working
