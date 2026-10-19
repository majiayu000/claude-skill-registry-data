---
name: zt-persian-writing
description: نگارش فارسی assistant for Codex; apply when building Persian/RTL web products, localizing content or integrating the related Iranian workflow. Local independent adaptation inspired by publicly documented VibeFarsi topics.
---

# Perfect_AI — نگارش فارسی (persian-writing)

This **original local Codex skill** is not a verbatim copy of VibeFarsi's official skill. To use the upstream maintained original consult https://vibefarsi.ir/skills/persian-writing. The external `persian-writing` is installed from its own GitHub repository; all other listed items use `npx vibefarsi add <slug>`.

## Mandatory workflow

1. Read user request, project code, locale/RTL style, existing conventions, and relevant security assumptions.
2. Apply target constraints: زبان طبیعی و دقیق، نیم‌فاصله، تیتر کوتاه، پرهیز از تکرار، ارجاع درست و تنظیم لحن برای متن وب.
3. Use accessible semantic UI, role-specific design tokens and a responsive layout. Do not change unrelated files.
4. For this topic: Optimize for clarity/readability; fact check claims and maintain meaningful headings and correct punctuation.
5. Write or change working implementation with minimal dependencies and functional feedback. Prefer tested utilities over fresh unverified regex or guessed API signatures.
6. Verify in 320px portrait, 768px tablet, 1440px desktop, zoom 200%, and Persian/LTR mixed text where relevant.
7. Report exactly which automated/browser/security checks were run, what passed and what remains unverified.

## Example Codex task

یک توضیح محصول را به فارسی واضح و کوتاه در سه طول بازنویسی کن.

## Tests / failure cases

- Empty, incomplete, malformed, mixed-script, unexpected long input, network/offline/API errors; when not applicable explain why.
- Keyboard focus/semantics and reduced-motion parity for animated interfaces.
- Logical CSS positioning and typography on Persian screens.
- If this workflow touches payments, SMS, identity or file uploads, ensure server-side validation, no embedded secrets and appropriate error handling.

## Integration

Read `../perfect-ai-master/references/09-persian-localization.md` and `../perfect-ai-master/references/08-quality-tests.md` if installed. For upstream author's full detail and source code use https://vibefarsi.ir/skills/persian-writing.
