---
name: activate-caveman-mode
description: Activate, change, or stop the manual Caveman response mode only when the user explicitly says $caveman, /caveman, Caveman plus a level, asks to open/activate/switch to Caveman or mağara mode, or gives an explicit Caveman off/normal-mode command. Preserve a named level and default to full. Never use for “kısa yaz”, “kısa cevap ver”, “basit anlat”, “öz konuş”, “az kelime”, “be concise”, “use fewer tokens”, token efficiency, or an ordinary preference for short answers.
---

# Activate Caveman Mode

Interpret an explicit natural-language Caveman command without turning ordinary
brevity requests into a mode change. This gate is implicitly available; the
five Caveman-family skills remain manual-only.

## Decision

1. First handle explicit deactivation—`$caveman off`,
   `/caveman off`, `stop caveman`, `normal mode`, “Caveman modunu kapat,” or
   “mağara modunu kapat”—return to normal prose for the conversation.
2. Otherwise require one of these positive activation forms: the exact
   `$caveman` or `/caveman` command; `Caveman` plus a supported level; or
   `Caveman`/`mağara modu` plus an unnegated open, activate, start, enter, or
   switch verb. Merely mentioning, asking about, inspecting, or negating
   Caveman is not activation. If the requirement is not met, stop and do not
   load or apply any Caveman-family instructions.
3. Treat a qualifying message as an explicit manual request for `caveman`.
   Apply its installed instructions and preserve the requested level:
   `lite`, `full`, `ultra`, `wenyan-lite`, `wenyan-full`, or `wenyan-ultra`.
   Default to `full` when no level is named.
4. Keep the chosen level only for the current conversation and honor the main
   Caveman skill's clarity, safety, technical-invariant, and stop rules.

## Hard negatives

Never activate or inspect a Caveman-family skill solely because the user asks
for:

- a short, simple, clear, direct, concise, brief, or token-efficient answer;
- fewer words, fewer tokens, less detail, a summary, or plain language;
- an ordinary commit message, code review, file compression, or help;
- an output that merely happens to be terse.
- a definition, explanation, comparison, audit, or inspection of Caveman;
- a negated command such as “Caveman modunu açma” or “do not start Caveman.”

These requests may influence the answer normally, but they are not mode
commands.

## Companion gate

Route `caveman-commit`, `caveman-review`, `caveman-compress`, or
`caveman-help` only when the user explicitly names that companion or
unambiguously asks for its **Caveman-specific** form. Ordinary commit, review,
compression, and help requests belong to their normal specialists.

Do not announce internal routing. Acknowledge an explicit mode change briefly
only when that acknowledgement helps the user know which level is active.
