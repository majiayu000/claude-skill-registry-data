---
name: scepticagent-publish
description: ScepticAgent packaging and Chrome Web Store publishing workflow. Use whenever the user wants to build the zip, package the extension, publish or submit to the Chrome Web Store, update the store listing, or deal with manifest/icon/permission requirements for publishing.
---

## Packaging

- Build zip: `zip -r scepticagent-extension.zip extension/ --exclude "*.DS_Store"`
- Never commit `*.zip` or `backend/venv/` — both are in `.gitignore`
- After any manifest change, always repackage before uploading to the Web Store

## Chrome Web Store checklist

- Permission justifications required for every entry in `permissions` and `host_permissions` — write them before submitting
- `manifest.description` max 132 chars — check with `echo -n "..." | wc -c`
- Privacy policy must be at a publicly reachable URL before submission — currently hosted at https://maros112358.github.io/scepticagent/privacy.html
- Icons required: 16px, 48px, 128px PNG in `extension/icons/`, referenced in both `icons` and `action.default_icon` in manifest
- `<all_urls>` host permission triggers an in-depth review warning — scope to specific API domains only (Anthropic, OpenAI, Gemini)
- Extension name must be unique in the Web Store — check before committing to a name
- At least one screenshot (1280×800 or 640×400) required before submission
- Contact email must be verified on the Account tab before submitting
